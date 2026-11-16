<!-- mcp-name: io.github.bitcoindatalabs/bitcoindatalabs-mcp -->

# bitcoindatalabs-mcp

[![PyPI](https://img.shields.io/pypi/v/bitcoindatalabs-mcp.svg)](https://pypi.org/project/bitcoindatalabs-mcp/)
[![bitcoindatalabs/bitcoindatalabs-mcp MCP server](https://glama.ai/mcp/servers/bitcoindatalabs/bitcoindatalabs-mcp/badges/score.svg)](https://glama.ai/mcp/servers/bitcoindatalabs/bitcoindatalabs-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](pyproject.toml)
[![Organization: Bitcoin Data Labs](https://img.shields.io/badge/Org-Bitcoin%20Data%20Labs-f7931a.svg)](https://bitcoindatalabs.org)

Zero-clone **Model Context Protocol (MCP)** server for [Bitcoin Data Labs](https://bitcoindatalabs.org) open telemetry, open-source ecosystem security metrics, and reproducible empirical research.

Query **1,009 ecosystem OSS repositories**, **Bitcoin Core governance & BIPs**, **developer funding**, **three peer-cited Lightning Network security studies (`arXiv:2610.20952`, `2610.30350`, `2611.16311`)**, **mining pool HHI concentration**, and **aggregate on-chain forensics** inside Claude, Cursor, Antigravity, or VS Code — without cloning any data repositories.

---

## Quick Start (Zero Clone)

`bitcoindatalabs-mcp` lazily fetches only the JSON and Parquet files your query needs from `github.com/bitcoindatalabs/*` and caches them in `~/.cache/bitcoindatalabs-mcp/` (DuckDB queries Parquet slices in memory).

### Claude Desktop / Cursor / Antigravity (`mcpServers`)

```json
{
  "mcpServers": {
    "bitcoindatalabs-mcp": {
      "command": "uvx",
      "args": ["bitcoindatalabs-mcp"]
    }
  }
}
```

### Local Python Install (also installs the `bdl-mcp` CLI alias)

```bash
pip install bitcoindatalabs-mcp
bitcoindatalabs-mcp   # or CLI alias: bdl-mcp
```

For local development against cloned `bitcoindatalabs/*` repositories, set `BDL_GITHUB_ROOT` to avoid HTTPS requests:

```bash
export BDL_GITHUB_ROOT=/path/to/github/checkouts
pip install -e ".[dev]"
pytest -v
```

---

## Datasets, Tools & Resources (`11` Repositories, `13` Tools, `7` Resources)

| Repository | MCP Tool | Empirical Coverage |
| :--- | :--- | :--- |
| Meta / Papers | `list_datasets`, `get_research_papers` | Full catalog + summaries, arXiv DOIs & BibTeX for the 3 Lightning security papers |
| [`ln-client-diversity`](https://github.com/bitcoindatalabs/ln-client-diversity) | `get_ln_client_diversity` | 857 gossip snapshots, 132,360 closes, 2026 CLN shutdown metrics (`arXiv:2610.20952`) |
| [`ln-upgrade-dynamics`](https://github.com/bitcoindatalabs/ln-upgrade-dynamics) | `get_ln_upgrade_dynamics` | 814 usable daily snapshots, 12 disclosures, release-line patch lag (`arXiv:2610.30350`) |
| [`ln-force-close-costs`](https://github.com/bitcoindatalabs/ln-force-close-costs) | `get_ln_force_close_costs` | 973,581 channel closes (523,815 force closes) through block 974,041 (`arXiv:2611.16311`) |
| [`lightning-data`](https://github.com/bitcoindatalabs/lightning-data) | `get_ln_network_snapshot` | Weekly network snapshot + DuckDB PlebRank top-node leaderboard (`node_rank.parquet`) |
| [`orange-dev-tracker`](https://github.com/bitcoindatalabs/orange-dev-tracker) | `get_core_dev_health` | Monthly *State of Bitcoin Core* engineering KPIs, review health & maintainer footprints |
| [`orange-dev-data`](https://github.com/bitcoindatalabs/orange-dev-data) | `get_core_dev_health`, `get_bip_status` | Maintainer footprints + DuckDB search over 218 BIPs (`Deployed`, `Draft`, `Closed`, `Complete`) |
| [`orange-funding-data`](https://github.com/bitcoindatalabs/orange-funding-data) | `get_ecosystem_funding` | 20 funding organizations & 277 sponsored open-source developers |
| [`oss-app-stats`](https://github.com/bitcoindatalabs/oss-app-stats) | `get_oss_app_stats` | Release cadence, GitHub stars & download counts across 29 core OSS projects |
| [`orange-eco-data`](https://github.com/bitcoindatalabs/orange-eco-data) | `get_oss_ecosystem_health` | 1,009 ecosystem repos & 109 curated projects across 14 layers: security maturity tiers, `SECURITY.md` coverage, and issue health |
| [`coldcard-rng-tracker`](https://github.com/bitcoindatalabs/coldcard-rng-tracker) | `get_coldcard_forensics_summary` | Aggregate Coldcard weak-RNG sweep metrics, 10 attack waves & timeline (aggregates only) |
| [`mining-pools-data`](https://github.com/bitcoindatalabs/mining-pools-data) | `get_mining_pool_concentration` | 167 mining pools tracked with per-year HHI and top-3 share across `2009`–`2026` |

### Read-Only MCP Resources & Prompts

- **Resources:** `bdl://attribution`, `bdl://overview`, `bdl://papers`, `bdl://lightning/snapshot`, `bdl://core-dev/latest`, `bdl://ecosystem`, `bdl://coldcard/summary`
- **Prompts:** `lightning_security_brief`, `core_governance_brief`, `regulatory_data_brief`

---

## Data Ethics & Attribution

- Security outputs are **aggregates only** (no per-node vulnerability rankings or victim PII).
- Server code is **MIT**-licensed; underlying Bitcoin Data Labs datasets are published under **CC BY 4.0**.
- Attribution: `Source: Bitcoin Data Labs (bitcoindatalabs.org)` — ORCID [`0009-0004-7944-3492`](https://orcid.org/0009-0004-7944-3492).
