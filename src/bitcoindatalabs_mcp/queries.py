
"""Read-only analytical query layer for Bitcoin Data Labs datasets."""

from __future__ import annotations

from collections import Counter
from typing import Any

from bitcoindatalabs_mcp import data_client

ATTRIBUTION = {
    "organization": "Bitcoin Data Labs (501(c)(3))",
    "author": "Saurabh Kumar",
    "orcid": "0009-0004-7944-3492",
    "website": "https://bitcoindatalabs.org",
    "repository": "https://github.com/bitcoindatalabs/bitcoindatalabs-mcp",
    "license_code": "MIT",
    "license_data": "CC BY 4.0",
    "credit": "Source: Bitcoin Data Labs (bitcoindatalabs.org)",
    "privacy_policy": "Security metrics are published as aggregates only; no individual node vulnerability ranking or victim PII is exposed.",
}

PAPERS: list[dict[str, Any]] = [
    {
        "id": "ln-client-diversity",
        "num": "01",
        "title": "Does Client Diversity Protect the Lightning Network? Evidence from the 2026 Core Lightning Shutdown",
        "authors": "Saurabh Kumar",
        "orcid": "0009-0004-7944-3492",
        "arxiv": "2610.20952",
        "version": "v2",
        "doi": "10.48550/arXiv.2610.20952",
        "category": "cs.CR, cs.NI",
        "date": "2026-10-21",
        "repo": "https://github.com/bitcoindatalabs/ln-client-diversity",
        "url": "https://arxiv.org/abs/2610.20952",
        "finding": "The damage from a software failure depends on whether it reaches the network's hubs, not on how many nodes run the failing software.",
        "key_metrics": {
            "lnd_node_share_pct": 80,
            "lnd_capacity_share_pct": 84,
            "cln_dark_rate_aug26_pct": 22,
            "reachability_drop_pp": 7.8,
        },
        "bibtex": (
            "@misc{kumar2026clientdiversity,\n"
            "  author       = {Kumar, Saurabh},\n"
            "  title        = {Does Client Diversity Protect the {L}ightning {N}etwork? {E}vidence from the 2026 {C}ore {L}ightning Shutdown},\n"
            "  year         = {2026},\n"
            "  month        = oct,\n"
            "  howpublished = {arXiv:2610.20952 [cs.CR]},\n"
            "  doi          = {10.48550/arXiv.2610.20952},\n"
            "  url          = {https://arxiv.org/abs/2610.20952}\n"
            "}"
        ),
    },
    {
        "id": "ln-upgrade-dynamics",
        "num": "02",
        "title": "Who Patches the Lightning Network? Evidence from Release Lines in Gossip, 2023-2026",
        "authors": "Saurabh Kumar",
        "orcid": "0009-0004-7944-3492",
        "arxiv": "2610.30350",
        "version": "v1",
        "doi": "10.48550/arXiv.2610.30350",
        "category": "cs.CR, cs.NI",
        "date": "2026-10-21",
        "repo": "https://github.com/bitcoindatalabs/ln-upgrade-dynamics",
        "url": "https://arxiv.org/abs/2610.30350",
        "finding": "Lightning nodes patch on release and downstream platform packaging schedules (such as Umbrel), not when an upstream security advisory is published.",
        "key_metrics": {
            "gossip_usable_days": 814,
            "lnd_median_upgrade_lag_days": 88,
            "disclosures_accelerating_upgrades": "1 of 12",
            "lnd_exposed_unpatched_after_2mo_pct": 71,
        },
        "bibtex": (
            "@misc{kumar2026upgradedynamics,\n"
            "  author       = {Kumar, Saurabh},\n"
            "  title        = {Who Patches the {L}ightning {N}etwork? {E}vidence from Release Lines in Gossip, 2023--2026},\n"
            "  year         = {2026},\n"
            "  month        = oct,\n"
            "  howpublished = {arXiv:2610.30350 [cs.CR]},\n"
            "  doi          = {10.48550/arXiv.2610.30350},\n"
            "  url          = {https://arxiv.org/abs/2610.30350}\n"
            "}"
        ),
    },
    {
        "id": "ln-force-close-costs",
        "num": "03",
        "title": "What Does It Cost to Force-Close a Lightning Channel? Evidence from 974,000 Channel Closes, 2018-2026",
        "authors": "Saurabh Kumar",
        "orcid": "0009-0004-7944-3492",
        "arxiv": "2611.16311",
        "version": "v1",
        "doi": "10.48550/arXiv.2611.16311",
        "category": "cs.CR, cs.NI",
        "date": "2026-11-12",
        "repo": "https://github.com/bitcoindatalabs/ln-force-close-costs",
        "url": "https://arxiv.org/abs/2611.16311",
        "finding": "Fee spikes do not trigger waves of Lightning force closes; a force close costs 2-6x a cooperative close in fees, and forwarding nodes lost only 38 HTLC payments since 2021.",
        "key_metrics": {
            "total_channel_closes": 973581,
            "force_closes": 523815,
            "fee_spike_force_close_ratio": 0.97,
            "ordinary_week_ratio": 1.02,
            "htlc_losses_since_2021": 38,
        },
        "bibtex": (
            "@misc{kumar2026forceclosecosts,\n"
            "  author       = {Kumar, Saurabh},\n"
            "  title        = {What Does It Cost to Force-Close a {L}ightning {C}hannel? {E}vidence from 974,000 Channel Closes, 2018--2026},\n"
            "  year         = {2026},\n"
            "  month        = nov,\n"
            "  howpublished = {arXiv:2611.16311 [cs.CR]},\n"
            "  doi          = {10.48550/arXiv.2611.16311},\n"
            "  url          = {https://arxiv.org/abs/2611.16311}\n"
            "}"
        ),
    },
]

DATASETS: list[dict[str, str]] = [
    {
        "id": "ln-client-diversity",
        "repo": "ln-client-diversity",
        "title": "Lightning Client Diversity & 2026 Core Lightning Shutdown Resilience",
        "coverage": "2023-05 to 2026-10 (857 gossip snapshots, 132,360 closes)",
        "tool": "get_ln_client_diversity",
    },
    {
        "id": "ln-upgrade-dynamics",
        "repo": "ln-upgrade-dynamics",
        "title": "Lightning Network Release-Line Inference & Security Patch Lag Panel",
        "coverage": "2023-05 to 2026-10 (814 usable daily snapshots, 12 disclosures)",
        "tool": "get_ln_upgrade_dynamics",
    },
    {
        "id": "ln-force-close-costs",
        "repo": "ln-force-close-costs",
        "title": "Lightning Channel Force-Close Economics, Anchor Outputs & HTLC Outcomes",
        "coverage": "2018-01 to 2026-10 (973,581 channel closes through block 974,041)",
        "tool": "get_ln_force_close_costs",
    },
    {
        "id": "lightning-data",
        "repo": "lightning-data",
        "title": "Live Lightning Network Topology, Weekly Snapshots & PlebRank Leaderboard",
        "coverage": "Rolling daily/weekly snapshots & node/channel Parquet tables",
        "tool": "get_ln_network_snapshot",
    },
    {
        "id": "orange-dev-tracker",
        "repo": "orange-dev-tracker",
        "title": "State of Bitcoin Core Monthly Engineering & Governance Scorecard",
        "coverage": "Monthly snapshots with 12-month historical distributions",
        "tool": "get_core_dev_health",
    },
    {
        "id": "orange-dev-data",
        "repo": "orange-dev-data",
        "title": "Bitcoin Improvement Proposals (BIPs) & Core Maintainer Footprints",
        "coverage": "218 BIPs & full Bitcoin Core contributor/maintainer history",
        "tool": "get_bip_status",
    },
    {
        "id": "orange-funding-data",
        "repo": "orange-funding-data",
        "title": "Bitcoin Open-Source Developer Funding & Grants Registry",
        "coverage": "20 funding organizations & 277 sponsored developers",
        "tool": "get_ecosystem_funding",
    },
    {
        "id": "oss-app-stats",
        "repo": "oss-app-stats",
        "title": "Bitcoin & Lightning Open-Source Project Release & Adoption Telemetry",
        "coverage": "29 core infrastructure, wallet, and protocol repositories",
        "tool": "get_oss_app_stats",
    },
    {
        "id": "orange-eco-data",
        "repo": "orange-eco-data",
        "title": "Open-Source Ecosystem Directory, Security Posture & Issue Health",
        "coverage": "1,009 OSS repositories & 109 curated projects across 14 stack layers",
        "tool": "get_oss_ecosystem_health",
    },
    {
        "id": "coldcard-rng-tracker",
        "repo": "coldcard-rng-tracker",
        "title": "Coldcard Weak-RNG On-Chain Forensic Sweep Reconstruction (Aggregates)",
        "coverage": "10 attack waves, 4,925 verified drained single-sig addresses",
        "tool": "get_coldcard_forensics_summary",
    },
    {
        "id": "mining-pools-data",
        "repo": "mining-pools-data",
        "title": "Bitcoin Genesis-to-Present Mining Pool Attribution & HHI Concentration",
        "coverage": "167 pools tracked through latest tip height",
        "tool": "get_mining_pool_concentration",
    },
]


def _clean_tex_value(val: Any) -> Any:
    if isinstance(val, str):
        return val.replace("\\textendash", "-").replace("\\textpercent", "%")
    if isinstance(val, dict):
        return {k: _clean_tex_value(v) for k, v in val.items()}
    if isinstance(val, list):
        return [_clean_tex_value(v) for v in val]
    return val


def list_datasets() -> dict[str, Any]:
    """Return catalog of all Bitcoin Data Labs datasets, coverage, and attribution."""
    return {
        "attribution": ATTRIBUTION,
        "dataset_count": len(DATASETS),
        "datasets": DATASETS,
    }


def get_research_papers(paper_id: str | None = None) -> dict[str, Any]:
    """Return metadata, findings, DOIs, and BibTeX for BDL Lightning security papers."""
    if paper_id:
        needle = paper_id.strip().lower()
        matches = [
            p for p in PAPERS
            if needle in p["id"].lower()
            or needle in p["arxiv"].lower()
            or needle in p["title"].lower()
        ]
    else:
        matches = PAPERS
    return {
        "attribution": ATTRIBUTION,
        "count": len(matches),
        "papers": matches,
    }


def get_ln_client_diversity(section: str = "summary") -> dict[str, Any]:
    """Query empirical metrics from ln-client-diversity (arXiv:2610.20952)."""
    sup = data_client.load_json("ln-client-diversity", "data/supporting_numbers.json")
    sec = section.strip().lower()
    if sec == "census":
        census = data_client.load_json("ln-client-diversity", "data/client_census_monthly.json")
        return {"paper": "arXiv:2610.20952", "section": "census", "census": census}
    if sec == "outage":
        return {"paper": "arXiv:2610.20952", "section": "outage", "data_cutoff": sup.get("data_cutoff"), "outage": sup.get("outage")}
    if sec == "hubs":
        return {"paper": "arXiv:2610.20952", "section": "hubs", "data_cutoff": sup.get("data_cutoff"), "hubs": sup.get("hubs")}
    return {
        "paper": "arXiv:2610.20952",
        "section": "summary",
        "data_cutoff": sup.get("data_cutoff"),
        "data": sup.get("data"),
        "outage_summary": {
            "dark_rate_CLN": sup.get("outage", {}).get("dark_rate_CLN"),
            "dark_rate_LND": sup.get("outage", {}).get("dark_rate_LND"),
            "recovery_back_within_3_7_days": sup.get("outage", {}).get("recovery_back_within_3_7_days"),
        },
        "hubs_keys": list((sup.get("hubs") or {}).keys()),
    }


def get_ln_upgrade_dynamics(section: str = "summary") -> dict[str, Any]:
    """Query empirical metrics from ln-upgrade-dynamics (arXiv:2610.30350)."""
    sup = _clean_tex_value(data_client.load_json("ln-upgrade-dynamics", "data/supporting_numbers.json"))
    sec = section.strip().lower()
    if sec == "advisories":
        adv = data_client.load_json("ln-upgrade-dynamics", "data/advisory_exposure.json")
        return {"paper": "arXiv:2610.30350", "section": "advisories", "advisory_exposure": adv}
    if sec == "panel":
        manifest = data_client.load_json("ln-upgrade-dynamics", "data/panel_manifest.json")
        return {"paper": "arXiv:2610.30350", "section": "panel", "panel_manifest": manifest}
    summary_keys = [
        "DataUsableDays", "DataFirstDay", "NLiveLndCutoff", "NAnchorClient",
        "PrecLND", "RecLND", "PrecCLN", "RecCLN",
        "CohortLLBatch", "CohortStillLLBatch", "PctCohortStillLLBatch",
        "CohortClnGossipd", "PctCohortStillClnGossipd",
    ]
    return {
        "paper": "arXiv:2610.30350",
        "section": "summary",
        "highlights": {k: sup[k] for k in summary_keys if k in sup},
        "total_number_keys": len(sup),
        "all_numbers": sup if sec == "all" else None,
    }


def get_ln_force_close_costs(section: str = "summary") -> dict[str, Any]:
    """Query empirical metrics from ln-force-close-costs (arXiv:2611.16311)."""
    manifest = data_client.load_json("ln-force-close-costs", "data/snapshot_manifest.json")
    sec = section.strip().lower()
    if sec == "breach_wave":
        bw = data_client.load_json("ln-force-close-costs", "data/breach_wave.json")
        return {"paper": "arXiv:2611.16311", "section": "breach_wave", "breach_wave": bw}
    if sec == "pre_anchor":
        pa = data_client.load_json("ln-force-close-costs", "data/pre_anchor_2026.json")
        return {"paper": "arXiv:2611.16311", "section": "pre_anchor", "pre_anchor_2026": pa}
    sup = _clean_tex_value(data_client.load_json("ln-force-close-costs", "data/supporting_numbers.json"))
    if sec == "all":
        return {"paper": "arXiv:2611.16311", "manifest": manifest, "supporting_numbers": sup}
    return {
        "paper": "arXiv:2611.16311",
        "cutoff_utc": manifest.get("cutoff_utc"),
        "cutoff_height": manifest.get("cutoff_height"),
        "counts": manifest.get("counts"),
        "sample_metrics": {
            k: sup[k]
            for k in sorted(sup.keys())
            if any(prefix in k for prefix in ("AllForce", "Anchors", "AnchorValue", "Htlc", "Spike", "Ratio"))
        },
        "total_number_keys": len(sup),
    }


def get_ln_network_snapshot(top_nodes_limit: int = 10) -> dict[str, Any]:
    """Get latest Lightning Network snapshot and top public routing hubs by PlebRank."""
    limit = max(1, min(int(top_nodes_limit), 50))
    latest = data_client.load_json("lightning-data", "data/weekly_snapshots/latest.json")
    top_nodes = data_client.query_parquet(
        {"node_rank": ("lightning-data", "data/node_rank.parquet")},
        """
        SELECT pleb_rank, alias, node_type, entity, role,
               total_capacity, total_channels_rank, betweenness_centrality_rank
        FROM node_rank
        ORDER BY pleb_rank ASC
        LIMIT ?
        """,
        [limit],
    )
    return {
        "as_of": latest.get("as_of"),
        "date_range": latest.get("date_range"),
        "metrics": latest.get("metrics"),
        "top_nodes_by_pleb_rank": top_nodes,
    }


def get_core_dev_health(month: str = "latest") -> dict[str, Any]:
    """Get State of Bitcoin Core monthly KPIs and maintainer merge/commit footprints."""
    clean_month = month.strip().lower()
    rel = (
        "data/monthly_snapshots/latest.json"
        if clean_month == "latest"
        else f"data/monthly_snapshots/monthly_{clean_month.replace('-', '')}.json"
    )
    snap = data_client.load_json("orange-dev-tracker", rel)
    maintainers = data_client.load_json("orange-dev-data", "data/enriched/maintainer_footprints.json")
    return {
        "target_month": snap.get("target_month"),
        "data_through": snap.get("data_through"),
        "headline": snap.get("headline"),
        "kpis": snap.get("kpis"),
        "scorecard": snap.get("scorecard"),
        "maintainer_count": len(maintainers),
        "maintainers": list(maintainers.keys()),
    }


def get_bip_status(
    query: str | None = None,
    status: str | None = None,
    limit: int = 25,
) -> dict[str, Any]:
    """Search Bitcoin Improvement Proposals (BIPs) by keyword, number, or status."""
    lim = max(1, min(int(limit), 100))
    clauses = ["1=1"]
    params: list[Any] = []
    if query:
        q = f"%{query.strip()}%"
        clauses.append("(bip_id ILIKE ? OR title ILIKE ? OR layer ILIKE ?)")
        params.extend([q, q, q])
    if status:
        clauses.append("status ILIKE ?")
        params.append(f"%{status.strip()}%")
    where_sql = " AND ".join(clauses)
    rows = data_client.query_parquet(
        {"bips": ("orange-dev-data", "data/enriched/bips_refined.parquet")},
        f"""
        SELECT bip_id, title, status, type, layer, created_date_header, author_names
        FROM bips
        WHERE {where_sql}
        ORDER BY bip_id ASC
        LIMIT ?
        """,
        params + [lim],
    )
    status_counts = data_client.query_parquet(
        {"bips": ("orange-dev-data", "data/enriched/bips_refined.parquet")},
        "SELECT status, COUNT(*) AS count FROM bips GROUP BY status ORDER BY count DESC",
    )
    return {
        "total_returned": len(rows),
        "status_breakdown": status_counts,
        "bips": rows,
    }


def get_ecosystem_funding(
    query: str | None = None,
    limit: int = 25,
) -> dict[str, Any]:
    """Query Bitcoin open-source developer sponsors and funded developers."""
    lim = max(1, min(int(limit), 100))
    raw = data_client.load_json("orange-funding-data", "data/enriched/sponsors_merged.json")
    sponsors = raw.get("sponsors", [])
    devs = raw.get("sponsored_developers", [])
    if query:
        needle = query.strip().lower()
        matched_sponsors = [
            s for s in sponsors
            if needle in str(s.get("name", "")).lower()
            or needle in str(s.get("id", "")).lower()
            or needle in str(s.get("type", "")).lower()
        ]
        matched_devs = [
            d for d in devs
            if needle in str(d.get("canonical_name", "")).lower()
            or needle in str(d.get("github", "")).lower()
            or needle in str(d.get("grants", "")).lower()
        ]
    else:
        matched_sponsors = sponsors
        matched_devs = devs

    return {
        "last_updated": raw.get("_last_updated"),
        "total_sponsors": len(sponsors),
        "total_sponsored_developers": len(devs),
        "sponsors": matched_sponsors[:lim],
        "sponsored_developers": [
            {
                "canonical_name": d.get("canonical_name"),
                "github": d.get("github"),
                "grants": d.get("grants"),
            }
            for d in matched_devs[:lim]
        ],
    }


def get_oss_app_stats(
    project: str | None = None,
    category: str | None = None,
    limit: int = 30,
) -> dict[str, Any]:
    """Query release cadence, stars, and download metrics for Bitcoin/Lightning OSS projects."""
    lim = max(1, min(int(limit), 50))
    idx = data_client.load_json("oss-app-stats", "docs/data/index.json")
    projects = idx.get("projects", [])
    if category:
        cat = category.strip().lower()
        projects = [p for p in projects if cat in str(p.get("category", "")).lower()]
    if project:
        needle = project.strip().lower()
        projects = [
            p for p in projects
            if needle in str(p.get("name", "")).lower()
            or needle in str(p.get("full_name", "")).lower()
        ]
    detail: dict[str, Any] | None = None
    if project and len(projects) == 1 and projects[0].get("file"):
        proj_data = data_client.load_json("oss-app-stats", f"docs/data/{projects[0]['file']}")
        summary = proj_data.get("summary") or {}
        releases = proj_data.get("releases") or []
        detail = {
            "full_name": projects[0].get("full_name"),
            "summary": summary,
            "total_releases": summary.get("total_releases", len(releases)),
            "total_downloads": summary.get("total_downloads", projects[0].get("total_downloads")),
            "recent_releases": [
                {
                    "tag": r.get("tag"),
                    "published_at": r.get("published_at"),
                    "total_downloads": r.get("total_downloads"),
                    "html_url": r.get("html_url"),
                }
                for r in releases[:5]
            ],
        }
    return {
        "generated_at": idx.get("generated_at"),
        "total_projects": idx.get("total_projects"),
        "matched_count": len(projects),
        "projects": projects[:lim],
        "project_detail": detail,
    }


def _summarize_ecosystem(
    master_repos: list[str],
    projects: dict[str, dict[str, Any]],
    security_posture: dict[str, dict[str, Any]],
    issue_health: dict[str, dict[str, Any]],
    meta: dict[str, Any],
) -> dict[str, Any]:
    tier_counts = Counter(
        str(v.get("security_maturity_tier") or "unknown")
        for v in security_posture.values()
    )
    sec_md_count = sum(1 for v in security_posture.values() if v.get("has_security_md"))
    contrib_md_count = sum(1 for v in security_posture.values() if v.get("has_contributing_md"))
    scores = [v["security_score"] for v in security_posture.values() if isinstance(v.get("security_score"), (int, float))]
    layer_counts = Counter(
        (v.get("layer") or "Uncategorized")
        for v in projects.values()
    )
    total_sp = len(security_posture) or 1
    return {
        "generated_at": meta.get("generated_at"),
        "total_tracked_repos": len(master_repos),
        "total_curated_projects": len(projects),
        "security_posture_repos": len(security_posture),
        "issue_health_repos": len(issue_health),
        "security_tier_counts": dict(sorted(tier_counts.items())),
        "has_security_md_count": sec_md_count,
        "has_security_md_pct": round(sec_md_count * 100.0 / total_sp, 1),
        "has_contributing_md_count": contrib_md_count,
        "has_contributing_md_pct": round(contrib_md_count * 100.0 / total_sp, 1),
        "mean_security_score": round(sum(scores) / len(scores), 1) if scores else None,
        "layers": dict(sorted(layer_counts.items(), key=lambda item: (-item[1], item[0]))),
    }


def get_oss_ecosystem_health(
    query: str | None = None,
    layer: str | None = None,
    security_tier: str | None = None,
    limit: int = 25,
) -> dict[str, Any]:
    """Query orange-eco-data across 1,009 OSS repositories: security maturity, SECURITY.md adoption, and issue health."""
    lim = max(1, min(int(limit), 50))
    master_repos = data_client.load_json("orange-eco-data", "output/master_ecosystem_repos.json")
    profiles_doc = data_client.load_json("orange-eco-data", "output/project_profiles.json")
    security_posture = data_client.load_json("orange-eco-data", "output/security_posture.json")
    issue_health = data_client.load_json("orange-eco-data", "output/issue_health.json")

    meta = profiles_doc.get("_meta") or {}
    projects_map = profiles_doc.get("projects") or {}

    needle = query.strip().lower() if query else None
    layer_needle = layer.strip().lower() if layer else None
    tier_needle = security_tier.strip().lower() if security_tier else None

    matched_projects: list[dict[str, Any]] = []
    layer_repo_names: set[str] = set()
    for proj_name, info in projects_map.items():
        proj_layer = str(info.get("layer") or "")
        if layer_needle and layer_needle not in proj_layer.lower():
            continue
        repos_list = info.get("repositories") or []
        repo_names = [str(r.get("repo_name")) for r in repos_list if r.get("repo_name")]
        if layer_needle:
            layer_repo_names.update(r.lower() for r in repo_names)
        if needle:
            haystack = " ".join([
                proj_name,
                str(info.get("description") or ""),
                str(info.get("github") or ""),
                " ".join(str(a) for a in (info.get("aliases") or [])),
                " ".join(repo_names),
            ]).lower()
            if needle not in haystack:
                continue
        agg = info.get("aggregate_metrics") or {}
        matched_projects.append({
            "project": proj_name,
            "layer": proj_layer or "Uncategorized",
            "github": info.get("github"),
            "website": info.get("website"),
            "description": info.get("description"),
            "repo_count": len(repos_list),
            "total_stars": agg.get("total_stars", 0) or 0,
            "total_code_contributors": agg.get("total_code_contributors"),
            "total_code_reviewers": agg.get("total_code_reviewers"),
            "primary_language": agg.get("primary_language"),
            "repositories": repo_names[:10],
        })

    matched_projects.sort(key=lambda item: (-item["total_stars"], item["project"].lower()))

    repo_rows: list[dict[str, Any]] = []
    for repo_name, sec in security_posture.items():
        tier_val = str(sec.get("security_maturity_tier") or "").lower()
        if tier_needle and tier_val != tier_needle:
            continue
        if needle and needle not in repo_name.lower():
            continue
        if layer_needle and not needle and repo_name.lower() not in layer_repo_names:
            continue
        ih = issue_health.get(repo_name) or {}
        repo_rows.append({
            "repo": repo_name,
            "security_score": sec.get("security_score"),
            "security_maturity_tier": sec.get("security_maturity_tier"),
            "has_security_md": sec.get("has_security_md"),
            "has_contributing_md": sec.get("has_contributing_md"),
            "security_advisories_count": sec.get("security_advisories_count"),
            "total_issue_events": ih.get("total_issue_events"),
            "total_issue_comments": ih.get("total_issue_comments"),
            "avg_commenters_per_month": ih.get("avg_commenters_per_month"),
        })

    repo_rows.sort(key=lambda r: (-(r.get("security_score") or 0), r["repo"].lower()))

    return {
        "summary": _summarize_ecosystem(master_repos, projects_map, security_posture, issue_health, meta),
        "matched_project_count": len(matched_projects),
        "projects": matched_projects[:lim],
        "matched_repo_count": len(repo_rows),
        "repositories": repo_rows[:lim],
    }


def get_coldcard_forensics_summary() -> dict[str, Any]:
    """Get Coldcard weak-RNG on-chain sweep reconstruction aggregates (no victim PII)."""
    summary = data_client.load_json("coldcard-rng-tracker", "docs/data/metrics_summary.json")
    timeline = data_client.load_json("coldcard-rng-tracker", "docs/data/timeline.json")
    sources = data_client.load_json("coldcard-rng-tracker", "docs/data/sources.json")
    return {
        "attribution": ATTRIBUTION,
        "summary": summary,
        "timeline": timeline,
        "external_sources": sources,
    }


def get_mining_pool_concentration(year: int = 2026, limit: int = 15) -> dict[str, Any]:
    """Get Bitcoin mining pool block attribution, top-3 share, and HHI for a given year (2009-2026)."""
    yr = int(year)
    if yr < 2009 or yr > 2026:
        raise ValueError(f"Year must be between 2009 and 2026, got {yr}")
    lim = max(1, min(int(limit), 50))
    facts = data_client.load_json("mining-pools-data", "metrics/pool_facts.json")
    rows = data_client.query_parquet(
        {"blocks": ("mining-pools-data", f"attribution/blocks_{yr}.parquet")},
        """
        SELECT COALESCE(pool, pool_slug, 'unknown') AS pool_name,
               pool_slug,
               COUNT(*) AS blocks
        FROM blocks
        GROUP BY 1, 2
        ORDER BY blocks DESC
        """,
    )
    total_blocks = sum(r["blocks"] for r in rows)
    hhi = 0.0
    enriched: list[dict[str, Any]] = []
    for r in rows:
        share = (r["blocks"] / total_blocks * 100.0) if total_blocks else 0.0
        hhi += share * share
        enriched.append({
            "pool_name": r["pool_name"],
            "pool_slug": r["pool_slug"],
            "blocks": r["blocks"],
            "share_pct": round(share, 2),
        })
    top3_share = round(sum(r["share_pct"] for r in enriched[:3]), 2)
    return {
        "year": yr,
        "tip_height": facts.get("tip_height"),
        "generated_at": facts.get("generated_at"),
        "total_pools_in_registry": len(facts.get("pools", {})),
        "total_blocks_in_year": total_blocks,
        "hhi_index": round(hhi, 1),
        "top3_share_pct": top3_share,
        "top_pools": enriched[:lim],
    }
