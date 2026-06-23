Installation
============

Requirements
------------

mcp_pyphotomol requires Python 3.12 or later. The MCP server depends on
PyPhotoMol and FastMCP, plus the scientific Python stack used for mass
photometry analysis.

Run with uvx
------------

Run the server directly with ``uvx``:

.. code-block:: bash

   uvx mcp_pyphotomol

By default, plots and log files are saved in
``~/user_data_mcp_pyphotomol/<YYYY-MM-DD>/``. To choose a different results
folder, set ``RESULTS_DIR`` before starting the server. This folder is where
results are stored; each server run writes into a date-stamped subfolder.

.. code-block:: bash

   RESULTS_DIR=~/Documents/user_data_mcp_pyphotomol uvx mcp_pyphotomol

Install from PyPI
-----------------

Install the package with pip:

.. code-block:: bash

   pip install --user mcp_pyphotomol

Then run the server with:

.. code-block:: bash

   mcp_pyphotomol

If your shell cannot find the command, make sure your user-level Python scripts
directory is on ``PATH``. You can use the same output-folder setting when
running the installed command:

.. code-block:: bash

   RESULTS_DIR=~/Documents/user_data_mcp_pyphotomol mcp_pyphotomol

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
