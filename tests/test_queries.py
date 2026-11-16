
"""Unit tests for bitcoindatalabs_mcp.queries against local datalabs datasets."""

from __future__ import annotations

from pathlib import Path

import pytest

from bitcoindatalabs_mcp import queries

LOCAL_ROOT = Path("/home/sorukumar/dev/github")
pytestmark = pytest.mark.skipif(
    not (LOCAL_ROOT / "ln-client-diversity").is_dir(),
    reason="Requires local datalabs dataset checkouts",
)


@pytest.fixture(autouse=True)
def _use_local_root(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BDL_GITHUB_ROOT", str(LOCAL_ROOT))


def test_list_datasets_and_papers() -> None:
    ds = queries.list_datasets()
    assert ds["dataset_count"] == 11
    assert ds["attribution"]["orcid"] == "0009-0004-7944-3492"

    papers = queries.get_research_papers()
    assert papers["count"] == 3
    assert {p["arxiv"] for p in papers["papers"]} == {"2610.20952", "2610.30350", "2611.16311"}


def test_lightning_research_queries() -> None:
    cd = queries.get_ln_client_diversity("summary")
    assert cd["paper"] == "arXiv:2610.20952"
    assert cd["data"]["closes"] == 132360

    ud = queries.get_ln_upgrade_dynamics("summary")
    assert ud["highlights"]["DataUsableDays"] == "814"

    fc = queries.get_ln_force_close_costs("summary")
    assert fc["counts"]["force_closes"] == 523815
    assert fc["cutoff_height"] == 974041


def test_live_network_core_bips_and_funding() -> None:
    snap = queries.get_ln_network_snapshot(top_nodes_limit=5)
    assert snap["metrics"]["active_nodes"] > 10000
    assert len(snap["top_nodes_by_pleb_rank"]) == 5

    core = queries.get_core_dev_health("latest")
    assert core["maintainer_count"] >= 10
    assert len(core["kpis"]) >= 4

    bips = queries.get_bip_status(status="Deployed", limit=10)
    assert bips["total_returned"] > 0

    funding = queries.get_ecosystem_funding(query="OpenSats", limit=10)
    assert funding["total_sponsors"] >= 20
    assert len(funding["sponsors"]) >= 1


def test_oss_ecosystem_coldcard_and_mining_concentration() -> None:
    oss = queries.get_oss_app_stats(project="Bitcoin Core")
    assert oss["matched_count"] == 1
    assert oss["project_detail"]["total_releases"] >= 60

    eco = queries.get_oss_ecosystem_health(query="bitcoin", limit=10)
    assert eco["summary"]["total_tracked_repos"] >= 1000
    assert eco["summary"]["total_curated_projects"] >= 100
    assert eco["summary"]["security_tier_counts"]["high"] > 0
    assert eco["matched_repo_count"] >= 1

    eco_layer = queries.get_oss_ecosystem_health(layer="Lightning Network", security_tier="high", limit=10)
    assert eco_layer["matched_project_count"] >= 5
    assert all(r["security_maturity_tier"] == "high" for r in eco_layer["repositories"])

    cc = queries.get_coldcard_forensics_summary()
    assert cc["summary"]["addresses_drained_verified"] == 4925

    mining = queries.get_mining_pool_concentration(year=2026, limit=10)
    assert mining["total_blocks_in_year"] > 40000
    assert mining["hhi_index"] > 0
    assert 0 < mining["top3_share_pct"] <= 100
