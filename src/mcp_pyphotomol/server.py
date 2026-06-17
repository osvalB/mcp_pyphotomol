import os
from pathlib import Path

from fastmcp import FastMCP
import pyphotomol

SKIP_USER_DATA_INIT = os.environ.get("MCP_PYPHOTOMOL_SKIP_USER_DATA_INIT") == "1"

# Instance to handle the mass photometry count data
MP_ANALYZER = pyphotomol.MPAnalyzer()

# Instance to handle the mass photometry calibration data
MP_CALIBRATOR = pyphotomol.MPAnalyzer()

# Options for plotting
PLOT_CONFIG = pyphotomol.PlotConfig(plot_height=800)
LEGEND_CONFIG = pyphotomol.LegendConfig()
LAYOUT_CONFIG = pyphotomol.LayoutConfig()
LAYOUT_CONFIG.stacked = True # Set default to stacked subplots
AXIS_CONFIG = pyphotomol.AxisConfig()


# Define the paths to the project data directories.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = str(PROJECT_ROOT / 'user_data')
EXAMPLE_DATA_DIR = str(PROJECT_ROOT / 'example_data')

# Create the data directory if it doesn't exist.
if not SKIP_USER_DATA_INIT and not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DATA_DIR_NO_DATE = DATA_DIR

# Create a folder with the current date, inside data
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')
DATA_DIR = os.path.join(DATA_DIR, today)

if not SKIP_USER_DATA_INIT and not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Create an empty file to store the mcp logbook text file - if it doesn't exist
logbook_file = os.path.join(DATA_DIR, 'mcp_logbook.txt')
if not SKIP_USER_DATA_INIT and not os.path.exists(logbook_file):
    with open(logbook_file, 'w') as f:
        f.write("MCP Logbook\n")
        f.write(f"Date: {today}\n")
        f.write("MCP function calls will be added here.\n")


# This is the shared MCP server instance
mcp = FastMCP(
    name="mcp_server_photomol",
    instructions="This server provides tools for analysing mass photometry count data. \
You can import data, create and fit histograms with a multi-gaussian model, \
and plot the results.  \
There are two important instances: MP_ANALYZER for analysis and MP_CALIBRATOR for calibration.")
