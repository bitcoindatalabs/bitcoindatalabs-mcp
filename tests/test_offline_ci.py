
"""Offline fixture tests so CI runs full MCP and query verification without dataset clones."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters, stdio_client

from bitcoindatalabs_mcp import queries


def _write_eco_fixtures(root: Path) -> None:
    eco_out = root / "orange-eco-data" / "output"
    eco_out.mkdir(parents=True, exist_ok=True)
    (eco_out / "master_ecosystem_repos.json").write_text(
        json.dumps(["bitcoin/bitcoin", "lightningnetwork/lnd"]), encoding="utf-8"
    )
    (eco_out / "project_profiles.json").write_text(
        json.dumps({
            "_meta": {"generated_at": "2026-11-01T00:00:00Z"},
            "projects": {
                "Bitcoin Core": {
                    "layer": "Core & Protocol",
                    "description": "Reference Bitcoin node.",
                    "website": "https://bitcoincore.org",
                    "github": "bitcoin",
                    "aliases": [],
                    "repositories": [{"repo_name": "bitcoin/bitcoin"}],
                    "aggregate_metrics": {"total_stars": 80000, "total_code_contributors": 900, "total_code_reviewers": 300, "primary_language": "C++"},
                }
            },
        }),
        encoding="utf-8",
    )
    (eco_out / "security_posture.json").write_text(
        json.dumps({
            "bitcoin/bitcoin": {
                "has_security_md": True,
                "has_contributing_md": True,
                "security_advisories_count": 12,
                "security_score": 95,
                "security_maturity_tier": "high",
            },
            "lightningnetwork/lnd": {
                "has_security_md": False,
                "has_contributing_md": True,
                "security_advisories_count": 5,
                "security_score": 55,
                "security_maturity_tier": "medium",
            },
        }),
        encoding="utf-8",
    )
    (eco_out / "issue_health.json").write_text(
        json.dumps({
            "bitcoin/bitcoin": {"total_issue_events": 100, "total_issue_comments": 500, "avg_commenters_per_month": 42.0}
        }),
        encoding="utf-8",
    )


def test_offline_catalog_papers_and_eco_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write_eco_fixtures(tmp_path)
    monkeypatch.setenv("BDL_GITHUB_ROOT", str(tmp_path))

    ds = queries.list_datasets()
    assert ds["dataset_count"] == 11
    assert any(item["id"] == "orange-eco-data" for item in ds["datasets"])

    eco = queries.get_oss_ecosystem_health(query="bitcoin", security_tier="high")
    assert eco["summary"]["total_tracked_repos"] == 2
    assert eco["summary"]["has_security_md_pct"] == 50.0
    assert eco["matched_repo_count"] == 1
    assert eco["repositories"][0]["total_issue_comments"] == 500


def test_offline_mcp_stdio_handshake(tmp_path: Path) -> None:
    async def _run() -> tuple[int, dict, dict]:
        env = dict(os.environ)
        env["BDL_GITHUB_ROOT"] = str(tmp_path)
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "bitcoindatalabs_mcp.server"],
            env=env,
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                ds_res = await session.call_tool("list_datasets", {})
                attr_res = await session.read_resource("bdl://attribution")
                return (
                    len(tools.tools),
                    json.loads(ds_res.content[0].text),
                    json.loads(attr_res.contents[0].text),
                )

    tool_count, ds_payload, attr_payload = asyncio.run(_run())
    assert tool_count == 13
    assert ds_payload["dataset_count"] == 11
    assert attr_payload["repository"] == "https://github.com/bitcoindatalabs/bitcoindatalabs-mcp"
