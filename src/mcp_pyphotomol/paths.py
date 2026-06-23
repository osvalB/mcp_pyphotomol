import os
from pathlib import Path


USER_DATA_DIR_NAME = "user_data_mcp_pyphotomol"
RESULTS_DIR_ENV_VAR = "RESULTS_DIR"


def get_user_data_root() -> Path:
    """Return the root folder for user-visible MCP output files."""
    results_dir = os.environ.get(RESULTS_DIR_ENV_VAR)
    if results_dir:
        return Path(results_dir).expanduser().resolve()
    return Path.home() / USER_DATA_DIR_NAME
