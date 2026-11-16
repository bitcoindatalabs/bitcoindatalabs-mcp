
"""End-to-end stdio MCP protocol test for bitcoindatalabs_mcp.server."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters, stdio_client

LOCAL_ROOT = Path("/home/sorukumar/dev/github")


async def _run_stdio_roundtrip() -> tuple[list[str], list[str], list[str], dict, dict]:
    env = dict(os.environ)
    env["BDL_GITHUB_ROOT"] = str(LOCAL_ROOT)

    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "bitcoindatalabs_mcp.server"],
        env=env,
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            resources = await session.list_resources()
            prompts = await session.list_prompts()

            tool_res = await session.call_tool("get_ln_force_close_costs", {"section": "summary"})
            attr_res = await session.read_resource("bdl://attribution")

            return (
                [t.name for t in tools.tools],
                [str(r.uri) for r in resources.resources],
                [p.name for p in prompts.prompts],
                json.loads(tool_res.content[0].text),
                json.loads(attr_res.contents[0].text),
            )


@pytest.mark.skipif(not (LOCAL_ROOT / "ln-force-close-costs").is_dir(), reason="Requires local datalabs repos")
def test_mcp_stdio_protocol_roundtrip() -> None:
    tool_names, resource_uris, prompt_names, fc_payload, attr_payload = asyncio.run(_run_stdio_roundtrip())
    assert len(tool_names) == 13
    assert "get_oss_ecosystem_health" in tool_names
    assert "get_coldcard_forensics_summary" in tool_names
    assert "get_mining_pool_concentration" in tool_names
    assert len(resource_uris) == 7
    assert "bdl://ecosystem" in resource_uris
    assert "bdl://papers" in resource_uris
    assert len(prompt_names) == 3
    assert fc_payload["counts"]["force_closes"] == 523815
    assert attr_payload["orcid"] == "0009-0004-7944-3492"
