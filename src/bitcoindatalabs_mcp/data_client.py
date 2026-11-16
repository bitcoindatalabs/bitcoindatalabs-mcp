
"""Zero-clone data resolver and DuckDB Parquet reader for Bitcoin Data Labs repos."""

from __future__ import annotations

import json
import math
import os
import tempfile
import time
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb
import httpx

DEFAULT_GITHUB_ORG = "bitcoindatalabs"
DEFAULT_BRANCH = "main"
DEFAULT_CACHE_TTL_HOURS = 24.0

_JSON_MEM_CACHE: dict[tuple[str, float], Any] = {}


def get_github_org() -> str:
    return os.environ.get("BDL_GITHUB_ORG", DEFAULT_GITHUB_ORG).strip() or DEFAULT_GITHUB_ORG


def get_cache_dir() -> Path:
    env_dir = os.environ.get("BDL_MCP_CACHE_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()
    return Path.home() / ".cache" / "bitcoindatalabs-mcp"


def get_cache_ttl_seconds() -> float:
    raw = os.environ.get("BDL_MCP_CACHE_TTL_HOURS", str(DEFAULT_CACHE_TTL_HOURS))
    try:
        return max(0.0, float(raw) * 3600.0)
    except ValueError:
        return DEFAULT_CACHE_TTL_HOURS * 3600.0


def _normalize_rel_path(rel_path: str) -> str:
    clean = rel_path.lstrip("/")
    if ".." in Path(clean).parts:
        raise ValueError(f"Invalid relative data path: {rel_path!r}")
    return clean


def _find_local_file(repo: str, rel_path: str) -> Path | None:
    """Resolve against BDL_GITHUB_ROOT (or default local github checkout dir if present)."""
    if os.environ.get("BDL_FORCE_REMOTE", "").lower() in {"1", "true", "yes"}:
        return None
    root_env = os.environ.get("BDL_GITHUB_ROOT")
    candidates_roots: list[Path] = []
    if root_env:
        candidates_roots.append(Path(root_env).expanduser().resolve())
    else:
        default_root = Path("/home/sorukumar/dev/github")
        if default_root.is_dir():
            candidates_roots.append(default_root)
    for root in candidates_roots:
        candidate = root / repo / rel_path
        if candidate.is_file():
            return candidate
    return None


def _is_fresh(path: Path, ttl_seconds: float) -> bool:
    if not path.is_file() or path.stat().st_size == 0 or ttl_seconds <= 0:
        return False
    return (time.time() - path.stat().st_mtime) <= ttl_seconds


def resolve_file(repo: str, rel_path: str) -> Path:
    """
    Resolve a Bitcoin Data Labs dataset file locally or lazily cache it from GitHub Raw.

    Order:
      1. Local checkout under BDL_GITHUB_ROOT (or /home/sorukumar/dev/github).
      2. Fresh cached copy under ~/.cache/bitcoindatalabs-mcp/<repo>/<rel_path>.
      3. Atomic HTTPS download from raw.githubusercontent.com/<org>/<repo>/main/<rel_path>.
    """
    clean = _normalize_rel_path(rel_path)
    local_path = _find_local_file(repo, clean)
    if local_path is not None:
        return local_path

    cache_path = get_cache_dir() / repo / clean
    if _is_fresh(cache_path, get_cache_ttl_seconds()):
        return cache_path

    org = get_github_org()
    url = f"https://raw.githubusercontent.com/{org}/{repo}/{DEFAULT_BRANCH}/{clean}"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_name = tempfile.mkstemp(
        prefix=".tmp_", suffix=cache_path.suffix or ".tmp", dir=str(cache_path.parent)
    )
    tmp_path = Path(tmp_name)
    try:
        os.close(tmp_fd)
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            with client.stream("GET", url) as resp:
                resp.raise_for_status()
                with tmp_path.open("wb") as out:
                    for chunk in resp.iter_bytes(chunk_size=65536):
                        out.write(chunk)
        os.replace(tmp_path, cache_path)
        return cache_path
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        if cache_path.is_file() and cache_path.stat().st_size > 0:
            return cache_path
        raise


def load_json(repo: str, rel_path: str) -> Any:
    """Load and memoize a JSON dataset by resolved path + mtime."""
    resolved = resolve_file(repo, rel_path)
    key = (str(resolved), resolved.stat().st_mtime)
    if key in _JSON_MEM_CACHE:
        return _JSON_MEM_CACHE[key]
    data = json.loads(resolved.read_text(encoding="utf-8"))
    if len(_JSON_MEM_CACHE) > 64:
        _JSON_MEM_CACHE.clear()
    _JSON_MEM_CACHE[key] = data
    return data


def clean_value(val: Any) -> Any:
    """Normalize DuckDB/Decimal/datetime/NaN scalars into strict JSON values."""
    if val is None:
        return None
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if hasattr(val, "item") and callable(val.item):
        return clean_value(val.item())
    if isinstance(val, dict):
        return {str(k): clean_value(v) for k, v in val.items()}
    if isinstance(val, (list, tuple)):
        return [clean_value(v) for v in val]
    return val


def query_parquet(
    tables: dict[str, tuple[str, str]],
    sql: str,
    params: list[Any] | tuple[Any, ...] = (),
) -> list[dict[str, Any]]:
    """
    Execute parameterized SQL in an ephemeral in-memory DuckDB connection.

    `tables` maps SQL view name -> (repo_name, rel_path).
    """
    con = duckdb.connect(database=":memory:")
    try:
        for alias, (repo, rel_path) in tables.items():
            resolved = resolve_file(repo, rel_path)
            con.read_parquet(str(resolved)).create_view(alias)
        cursor = con.execute(sql, list(params))
        cols = [desc[0] for desc in (cursor.description or [])]
        return [
            {col: clean_value(val) for col, val in zip(cols, row)}
            for row in cursor.fetchall()
        ]
    finally:
        con.close()
