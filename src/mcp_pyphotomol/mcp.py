from fastmcp import FastMCP

from .server import mcp as _mcp

# Import modules for their registration side effects.
from .resources import *  # noqa: F403
from .tools import *  # noqa: F403

mcp: FastMCP = _mcp
