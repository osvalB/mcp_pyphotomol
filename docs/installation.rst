Installation
============

Requirements
------------

mcp_pyphotomol requires Python 3.11 or later. The MCP server depends on
PyPhotoMol and FastMCP, plus the scientific Python stack used for mass
photometry analysis.

Run with uvx
------------

After publication to PyPI, run the server directly with ``uvx``:

.. code-block:: bash

   uvx mcp_pyphotomol

To run from the Git repository:

.. code-block:: bash

   uvx git+https://github.com/osvalB/mcp_pyphotomol.git@main

Install from PyPI
-----------------

Install the package with pip:

.. code-block:: bash

   pip install mcp_pyphotomol

Install from Source
-------------------

Clone the repository and install the development environment with ``uv``:

.. code-block:: bash

   git clone https://github.com/osvalB/mcp_pyphotomol.git
   cd mcp_pyphotomol
   uv sync --extra dev --extra doc --extra test

Run Tests
---------

Verify the development installation by running the test suite:

.. code-block:: bash

   uv run pytest

Build Documentation
-------------------

Create the local documentation build with:

.. code-block:: bash

   uv run --extra doc make -C docs html

The generated HTML documentation is written to ``docs/_build/html/``.
