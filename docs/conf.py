# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------
import os
import sys
from datetime import datetime
from importlib.metadata import metadata
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "src"))
os.environ.setdefault("MCP_PYPHOTOMOL_SKIP_USER_DATA_INIT", "1")


# -- Project information -----------------------------------------------------

info = metadata("mcp_pyphotomol")
project = info["Name"]
author = info["Author"]
copyright = f"{datetime.now():%Y}, {author}."
version = info["Version"]
urls = dict(pu.split(", ") for pu in info.get_all("Project-URL"))
repository_url = urls["Source"]

# The full version, including alpha/beta/rc tags
release = info["Version"]

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_design",
    "numpydoc",
    "nbsphinx",
]

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "show-inheritance": True,
    "exclude-members": "__weakref__",
}

autosummary_generate = True
autosummary_imported_members = True
autodoc_member_order = "groupwise"
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_rtype = True
napoleon_use_param = True
numpydoc_show_class_members = False
nbsphinx_execute = "never"
nbsphinx_allow_errors = False
nbsphinx_codecell_lexer = "python"

templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_title = f"{project} documentation"

pygments_style = "sphinx"


def setup(app):
    app.add_css_file("custom.css")
