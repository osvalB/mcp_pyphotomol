import os

import pytest

os.environ.setdefault("MCP_PYPHOTOMOL_SKIP_USER_DATA_INIT", "1")

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def isolated_tool_log_dir(tmp_path):
    """Use a per-test log directory for tool calls that append to the MCP logbook."""
    import mcp_pyphotomol.tools._photomol as photomol_tools

    previous_data_dir = photomol_tools.DATA_DIR
    log_dir = tmp_path / "user_data"
    log_dir.mkdir()
    (log_dir / "mcp_logbook.txt").write_text("MCP Logbook\n")
    photomol_tools.DATA_DIR = str(log_dir)

    try:
        yield log_dir
    finally:
        photomol_tools.DATA_DIR = previous_data_dir


@pytest.fixture
def resource_data_root(tmp_path):
    """Use a per-test root for MCP logbook resource lookups."""
    import mcp_pyphotomol.resources._photomol as photomol_resources

    previous_data_dir = photomol_resources.DATA_DIR_NO_DATE
    photomol_resources.DATA_DIR_NO_DATE = str(tmp_path)

    try:
        yield tmp_path
    finally:
        photomol_resources.DATA_DIR_NO_DATE = previous_data_dir
