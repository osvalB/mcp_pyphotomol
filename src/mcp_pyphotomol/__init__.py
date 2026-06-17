from importlib.metadata import version

from mcp_pyphotomol.main import run_app
from mcp_pyphotomol.mcp import mcp

__version__ = version("mcp_pyphotomol")

__all__ = [
    "mcp",
    "run_app",
    "__version__"
]


if __name__ == "__main__":
    run_app()
