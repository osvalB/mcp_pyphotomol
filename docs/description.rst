Overview
========

mcp_pyphotomol exposes PyPhotoMol analysis workflows through the Model Context
Protocol. It provides tools for importing mass photometry measurements, creating
histograms, fitting multi-gaussian models, calibrating measurements, plotting
results, and inspecting the MCP logbook.

Basic Workflow
--------------

The typical workflow for mass photometry analysis is:

1. Import one or more HDF5 or CSV files.
2. Create histograms from mass or contrast data.
3. Fit a multi-gaussian model to the detected peaks.
4. Review fitted parameters and summary tables.
5. Plot histograms, fitted curves, or calibration results.

MCP Tools
---------

The server keeps separate analyzer and calibrator instances. Analysis data is
handled by the analyzer instance, while calibration data is handled by the
calibrator instance. Tool calls are appended to a dated MCP logbook in the
results folder. By default this is
``~/user_data_mcp_pyphotomol/<YYYY-MM-DD>/``. Set ``RESULTS_DIR`` before
starting the server to choose a different folder for plots and log files.

Local Development
-----------------

For local MCP clients that support the ``mcp.json`` convention, point the
server command at the repository:

.. code-block:: json

   {
     "mcpServers": {
       "mcp_pyphotomol": {
         "command": "uv",
         "args": ["run", "--directory", "/absolute/path/to/mcp_pyphotomol", "mcp_pyphotomol"]
       }
     }
   }

Citation
--------

If you use ``mcp_pyphotomol``, please cite it as:

Burastero, O. (2026). ``mcp_pyphotomol`` (Version 1.0) [Computer software].
GitHub. https://github.com/osvalB/mcp_pyphotomol

.. code-block:: bibtex

   @software{burastero_2026_mcp_pyphotomol,
     author = {Burastero, Osvaldo},
     title = {mcp_pyphotomol},
     version = {1.0},
     year = {2026},
     url = {https://github.com/osvalB/mcp_pyphotomol}
   }
