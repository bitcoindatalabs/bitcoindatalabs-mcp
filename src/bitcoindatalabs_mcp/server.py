
"""Zero-clone MCP Server entrypoint for Bitcoin Data Labs."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from bitcoindatalabs_mcp import queries

READ_ONLY_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=True,
)

mcp = MCPServer(
    name="bitcoindatalabs-mcp",
    title="Bitcoin Data Labs MCP",
    description=(
        "Zero-clone open telemetry from Bitcoin Data Labs (501(c)(3)): 1,009-repo OSS ecosystem "
        "security posture, Bitcoin Core engineering health, BIPs, developer funding, Lightning "
        "security papers (arXiv:2610.20952, 2610.30350, 2611.16311), mining pool HHI, and forensic aggregates."
    ),
    instructions=(
        "Use list_datasets() to discover all available Bitcoin Data Labs repositories, "
        "get_research_papers() for Lightning security paper metrics and BibTeX, and domain tools "
        "(get_ln_client_diversity, get_ln_upgrade_dynamics, get_ln_force_close_costs, "
        "get_ln_network_snapshot, get_core_dev_health, get_bip_status, get_ecosystem_funding, "
        "get_oss_app_stats, get_oss_ecosystem_health, get_coldcard_forensics_summary, "
        "get_mining_pool_concentration) for live empirical queries."
    ),
    website_url="https://bitcoindatalabs.org",
)


def _json_str(payload: Any) -> str:
    return json.dumps(payload, indent=2, default=str)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def list_datasets() -> dict[str, Any]:
    """List all Bitcoin Data Labs datasets, coverage windows, attribution, and corresponding tools."""
    return queries.list_datasets()


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_research_papers(paper_id: str | None = None) -> dict[str, Any]:
    """Get summaries, DOIs, key metrics, and BibTeX for Bitcoin Data Labs Lightning security papers."""
    return queries.get_research_papers(paper_id=paper_id)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_ln_client_diversity(section: str = "summary") -> dict[str, Any]:
    """Query Lightning Network client diversity and 2026 Core Lightning shutdown metrics (arXiv:2610.20952). Section: summary | outage | hubs | census."""
    return queries.get_ln_client_diversity(section=section)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_ln_upgrade_dynamics(section: str = "summary") -> dict[str, Any]:
    """Query Lightning Network release-line inference and security patch-lag metrics (arXiv:2610.30350). Section: summary | advisories | panel | all."""
    return queries.get_ln_upgrade_dynamics(section=section)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_ln_force_close_costs(section: str = "summary") -> dict[str, Any]:
    """Query 973,581 Lightning channel closes, anchor outputs, and HTLC outcomes (arXiv:2611.16311). Section: summary | breach_wave | pre_anchor | all."""
    return queries.get_ln_force_close_costs(section=section)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_ln_network_snapshot(top_nodes_limit: int = 10) -> dict[str, Any]:
    """Get latest Lightning Network weekly snapshot and top public nodes ranked by PlebRank."""
    return queries.get_ln_network_snapshot(top_nodes_limit=top_nodes_limit)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_core_dev_health(month: str = "latest") -> dict[str, Any]:
    """Get State of Bitcoin Core monthly engineering KPIs, review health, and maintainer footprints."""
    return queries.get_core_dev_health(month=month)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_bip_status(
    query: str | None = None,
    status: str | None = None,
    limit: int = 25,
) -> dict[str, Any]:
    """Search Bitcoin Improvement Proposals (BIPs) by keyword/ID or status (e.g. Deployed, Complete, Draft, Closed)."""
    return queries.get_bip_status(query=query, status=status, limit=limit)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_ecosystem_funding(
    query: str | None = None,
    limit: int = 25,
) -> dict[str, Any]:
    """Query Bitcoin open-source developer sponsors and funded contributors."""
    return queries.get_ecosystem_funding(query=query, limit=limit)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_oss_app_stats(
    project: str | None = None,
    category: str | None = None,
    limit: int = 30,
) -> dict[str, Any]:
    """Get release cadence, stars, and download stats for 29+ Bitcoin/Lightning open-source projects."""
    return queries.get_oss_app_stats(project=project, category=category, limit=limit)


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_oss_ecosystem_health(
    query: str | None = None,
    layer: str | None = None,
    security_tier: str | None = None,
    limit: int = 25,
) -> dict[str, Any]:
    """Query orange-eco-data across 1,009 OSS repos and 109 curated projects: security maturity tiers, SECURITY.md adoption, and issue health."""
    return queries.get_oss_ecosystem_health(
        query=query,
        layer=layer,
        security_tier=security_tier,
        limit=limit,
    )


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_coldcard_forensics_summary() -> dict[str, Any]:
    """Get aggregate Coldcard weak-RNG sweep metrics, timeline, and external cross-validation sources."""
    return queries.get_coldcard_forensics_summary()


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_mining_pool_concentration(year: int = 2026, limit: int = 15) -> dict[str, Any]:
    """Get Bitcoin mining pool block attribution, top-3 share %, and HHI concentration index for a year (2009-2026)."""
    return queries.get_mining_pool_concentration(year=year, limit=limit)


@mcp.resource("bdl://attribution", mime_type="application/json")
def attribution_resource() -> str:
    """Bitcoin Data Labs attribution, ORCID, and CC BY 4.0 / MIT licensing metadata."""
    return _json_str(queries.ATTRIBUTION)


@mcp.resource("bdl://overview", mime_type="application/json")
def overview_resource() -> str:
    """Catalog of all Bitcoin Data Labs open datasets and tools."""
    return _json_str(queries.list_datasets())


@mcp.resource("bdl://papers", mime_type="application/json")
def papers_resource() -> str:
    """Bitcoin Data Labs Lightning security research papers with arXiv DOIs and BibTeX."""
    return _json_str(queries.get_research_papers())


@mcp.resource("bdl://lightning/snapshot", mime_type="application/json")
def lightning_snapshot_resource() -> str:
    """Latest weekly Lightning Network snapshot and top 10 PlebRank routing nodes."""
    return _json_str(queries.get_ln_network_snapshot(top_nodes_limit=10))


@mcp.resource("bdl://core-dev/latest", mime_type="application/json")
def core_dev_latest_resource() -> str:
    """Latest State of Bitcoin Core monthly report KPIs and maintainer footprints."""
    return _json_str(queries.get_core_dev_health(month="latest"))


@mcp.resource("bdl://ecosystem", mime_type="application/json")
def ecosystem_health_resource() -> str:
    """Aggregate OSS ecosystem security posture and project layers across 1,009 repositories."""
    return _json_str(queries.get_oss_ecosystem_health(limit=10))


@mcp.resource("bdl://coldcard/summary", mime_type="application/json")
def coldcard_summary_resource() -> str:
    """Aggregate Coldcard weak-RNG forensic metrics and timeline."""
    return _json_str(queries.get_coldcard_forensics_summary())


@mcp.prompt(description="Generate an empirical Lightning security & operational resilience brief from BDL's 3 arXiv papers.")
def lightning_security_brief() -> str:
    return (
        "Build a concise empirical brief on Lightning Network security using bitcoindatalabs-mcp:\n"
        "1. Call get_research_papers() for arXiv DOIs and canonical citations.\n"
        "2. Call get_ln_client_diversity(), get_ln_upgrade_dynamics(), and get_ln_force_close_costs().\n"
        "3. Synthesize hub concentration vs node count, downstream packager patch lag, and force-close fee/HTLC risk."
    )


@mcp.prompt(description="Audit Bitcoin & OSS software supply-chain security posture, maintainer governance, and funding.")
def core_governance_brief() -> str:
    return (
        "Build an open-source software governance, security posture, and funding brief using bitcoindatalabs-mcp:\n"
        "1. Call get_core_dev_health(month='latest') for merge throughput, reviewers, and backlog.\n"
        "2. Call get_oss_ecosystem_health() and get_ecosystem_funding() for SECURITY.md adoption and grant coverage.\n"
        "3. Call get_oss_app_stats(category='Core Infrastructure') for release cadence and download telemetry."
    )


@mcp.prompt(description="Assemble verified BDL empirical figures for a regulatory or policy technical brief.")
def regulatory_data_brief(topic: str = "custody, OSS supply-chain security, and settlement resilience") -> str:
    return (
        f"Prepare a non-partisan technical policy brief on {topic} using bitcoindatalabs-mcp:\n"
        "1. Call get_coldcard_forensics_summary() for cryptographic RNG failure evidence.\n"
        "2. Call get_oss_ecosystem_health() and get_ln_upgrade_dynamics() for OSS security posture & patch-lag telemetry.\n"
        "3. Call get_ln_force_close_costs() for settlement resilience and cite exact arXiv DOIs and Bitcoin Data Labs attribution."
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
