import os
import tempfile
from pathlib import Path

import hishel

# Resolve the cache directory to an absolute, writable path so the server works
# regardless of the current working directory (e.g. when launched by Claude
# Desktop, whose cwd is "/" and read-only). Allow an override via env var.
_cache_dir = os.getenv("TRADING212_CACHE_DIR")
if _cache_dir:
    _base_path = Path(_cache_dir).expanduser()
else:
    _base_path = Path(tempfile.gettempdir()) / "trading212-mcp" / "hishel"
_base_path.mkdir(parents=True, exist_ok=True)

storage = hishel.FileStorage(base_path=_base_path, ttl=300)

# The API exposes non-idempotent POST endpoints for orders, pies, and exports,
# so we only cache GET requests.
controller = hishel.Controller(
    # Cache only GET methods
    cacheable_methods=["GET"],

    # Cache only 200 status codes
    cacheable_status_codes=[200],

    # Use the stale response if there is a connection issue and the new response cannot be obtained.
    allow_stale=True,

    force_cache=True,
)
