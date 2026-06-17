import builtins
import importlib
import io
import json
import os
import runpy
import sys
import warnings
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from fastmcp import Client
from fastmcp.exceptions import ToolError

import mcp_pyphotomol
import mcp_pyphotomol.server as photomol_server
import mcp_pyphotomol.tools._photomol as photomol_tools
from mcp_pyphotomol.main import run_app

EXAMPLE_DATA_DIR = Path(__file__).resolve().parents[1] / "example_data"
MASS_EXAMPLE_FILES = {
    "masses_monomer_1nM.csv",
    "masses_monomer_2nM.csv",
    "masses_monomer_4nM.csv",
    "masses_monomer_8nM.csv",
    "masses_monomer_16nM.csv",
    "masses_monomer_32nM.csv",
    "masses_monomer_64nM.csv",
}
CONTRAST_EXAMPLE_FILE = "contrasts.csv"
NOTEBOOK_DEMO_FILE = "demo.h5"
EXPECTED_EXAMPLE_MODEL_NAMES = [
    "1.0 nM",
    "2.0 nM",
    "4.0 nM",
    "8.0 nM",
    "16.0 nM",
    "32.0 nM",
    "64.0 nM",
]


def test_package_has_version():
    """Testing package version exist."""
    assert mcp_pyphotomol.__version__ is not None


def test_example_data_files_are_present():
    """Testing example data fixtures exist."""
    files = {path.name for path in EXAMPLE_DATA_DIR.glob("*.csv")}
    assert MASS_EXAMPLE_FILES | {CONTRAST_EXAMPLE_FILE} <= files
    assert (EXAMPLE_DATA_DIR / NOTEBOOK_DEMO_FILE).is_file()


@pytest.mark.asyncio
async def test_mcp_server_tools_with_example_data(isolated_tool_log_dir):
    """Testing MCP server tools with the bundled example data."""
    log_dir = isolated_tool_log_dir

    async with Client(mcp_pyphotomol.mcp) as client:
        tools = await client.list_tools()
        tool_names = {tool.name for tool in tools}

        assert {
            "list_MP_files_in_folder",
            "reset_analyzer",
            "reset_calibrator",
            "get_model_names",
            "import_folder",
            "load_example_data",
            "create_histogram_automatic",
            "fit_multi_gaussian",
            "show_fitted_parameters",
            "load_example_data_for_calibration",
        } <= tool_names

        result = await client.call_tool("get_user_name", {})
        assert isinstance(result.data, str)
        assert result.data

        result = await client.call_tool(
            "list_MP_files_in_folder",
            {"folder_path": str(EXAMPLE_DATA_DIR)},
        )
        listed_files = {file_name.strip() for file_name in result.data.split(",")}
        assert MASS_EXAMPLE_FILES | {CONTRAST_EXAMPLE_FILE, NOTEBOOK_DEMO_FILE} <= listed_files

        result = await client.call_tool(
            "import_folder",
            {"folder_path": str(EXAMPLE_DATA_DIR), "pattern": "does-not-exist"},
        )
        assert result.data == f"No files found in {EXAMPLE_DATA_DIR}."

        await client.call_tool("reset_analyzer", {})
        result = await client.call_tool(
            "import_single_file",
            {"file_path": str(EXAMPLE_DATA_DIR / "masses_monomer_1nM.csv")},
        )
        assert result.data == f"Data imported successfully from {EXAMPLE_DATA_DIR / 'masses_monomer_1nM.csv'}."

        result = await client.call_tool("get_model_names", {})
        assert result.data == ["masses_monomer_1nM"]

        with pytest.raises(ToolError, match="Histogram for model masses_monomer_1nM has not been created"):
            await client.call_tool("fit_multi_gaussian", {})

        result = await client.call_tool(
            "create_histogram_manual",
            {"min_value": 0, "max_value": 300, "bin_width": 8},
        )
        assert "Histograms were created successfully" in result.data
        assert "Bin width: 8" in result.data

        result = await client.call_tool(
            "fit_multi_gaussian",
            {"peaks_guess": [80, 160], "mean_tolerance": 80, "std_tolerance": 80},
        )
        assert result.data == "Multi-gaussian fitting completed successfully."

        await client.call_tool("reset_analyzer", {})
        result = await client.call_tool(
            "import_folder",
            {"folder_path": str(EXAMPLE_DATA_DIR), "pattern": "masses_monomer"},
        )
        assert result.data == f"{len(MASS_EXAMPLE_FILES)} files were imported successfully from {EXAMPLE_DATA_DIR}."

        result = await client.call_tool("get_model_names", {})
        assert {f.removesuffix(".csv") for f in MASS_EXAMPLE_FILES} == set(result.data)

        await client.call_tool("reset_analyzer", {})
        result = await client.call_tool("load_example_data", {})
        assert result.data == "Example data loaded successfully."

        result = await client.call_tool("get_model_names", {})
        assert result.data == EXPECTED_EXAMPLE_MODEL_NAMES

        result = await client.call_tool("create_histogram_automatic", {})
        assert "Histograms were created successfully" in result.data
        assert "Using masses: True" in result.data

        result = await client.call_tool("fit_multi_gaussian", {"experiment": "not-present"})
        assert result.data == "Multi-gaussian fitting completed successfully."

        result = await client.call_tool("fit_multi_gaussian", {})
        assert result.data == "Multi-gaussian fitting completed successfully."

        result = await client.call_tool("show_fitted_parameters", {})
        fitted_parameters = json.loads(result.data)
        assert {row["name"] for row in fitted_parameters} == set(EXPECTED_EXAMPLE_MODEL_NAMES)
        assert all("Position / kDa" in row for row in fitted_parameters)

        result = await client.call_tool(
            "update_plot_config",
            {
                "plot_width": 640,
                "plot_height": 480,
                "plot_type": "browser",
                "x_range": [0, 300],
            },
        )
        assert result.data == "Plot configuration updated successfully."

        result = await client.call_tool(
            "update_legend_config",
            {"add_percentage_to_legend": True, "line_width": 2},
        )
        assert result.data == "Legend configuration updated successfully."

        result = await client.call_tool(
            "update_layout_config",
            {"stacked": False, "show_subplot_titles": True},
        )
        assert result.data == "Layout configuration updated successfully."

        result = await client.call_tool("update_axis_config", {"n_y_axis_ticks": 5})
        assert result.data == "Axis configuration updated successfully."

        result = await client.call_tool(
            "plot_histograms",
            {"colors_hist": "red", "save_as_html": True},
        )
        assert result.data == "Histogram plot created successfully, but no valid image format was specified for saving."

        result = await client.call_tool("get_legends_dataframe", {"repeat_colors": False})
        legends = json.loads(result.data)
        assert {column for row in legends for column in row} >= {"legends", "color", "select", "show_legend"}

        result = await client.call_tool(
            "plot_histograms_and_fits",
            {"legends_df": json.dumps(legends), "colors_hist": "blue", "save_as_html": True},
        )
        assert result.data == "Histograms and fits plot created successfully, but no valid image format was specified for saving."
        assert any(path.name.startswith("histogram_") for path in log_dir.glob("*.html"))
        assert any(path.name.startswith("histograms_and_fits_") for path in log_dir.glob("*.html"))

        await client.call_tool("reset_calibrator", {})
        result = await client.call_tool("load_example_data_for_calibration", {})
        assert result.data == "Example calibration data loaded successfully."

        result = await client.call_tool("get_model_names", {"calibrator": True})
        assert result.data == ["file1", "file2"]

        result = await client.call_tool(
            "create_histogram_automatic",
            {"use_masses": False, "calibrator": True},
        )
        assert "Using contrasts: True" in result.data

        result = await client.call_tool("fit_multi_gaussian", {"calibrator": True})
        assert result.data == "Multi-gaussian fitting completed successfully."

        result = await client.call_tool("show_fitted_parameters", {"calibrator": True})
        calibration_parameters = json.loads(result.data)
        assert {row["name"] for row in calibration_parameters} == {"file1", "file2"}
        assert all("Position / contrasts" in row for row in calibration_parameters)

        with pytest.raises(ToolError, match="Length of known_standards must match number of models"):
            await client.call_tool("calibrate", {"known_standards": [480]})

        photomol_tools.MP_CALIBRATOR.known_standards = [66, 148, 480]
        photomol_tools.MP_CALIBRATOR.calibration_dic = {
            "exp_points": [-0.0035, -0.0086, -0.0288],
            "fit_params": [-0.00005, 0.0],
            "fit_r2": 0.99,
        }
        result = await client.call_tool("plot_calibration", {"save_as_html": True})
        assert result.data == "Calibration plot created successfully, but no valid image format was specified for saving."
        assert any(path.name.startswith("calibration_") for path in log_dir.glob("*.html"))


@pytest.mark.asyncio
async def test_mcp_results_match_simple_example_notebook(isolated_tool_log_dir):
    """Testing MCP output matches the simple example notebook fit table."""
    async with Client(mcp_pyphotomol.mcp) as client:
        await client.call_tool("reset_analyzer", {})
        await client.call_tool(
            "import_single_file",
            {"file_path": str(EXAMPLE_DATA_DIR / NOTEBOOK_DEMO_FILE), "name": "demo1"},
        )
        await client.call_tool(
            "create_histogram_manual",
            {"min_value": 0, "max_value": 800, "bin_width": 10},
        )
        await client.call_tool(
            "fit_multi_gaussian",
            {"peaks_guess": [65, 145, 465], "threshold": 40, "fit_baseline": False},
        )

        result = await client.call_tool("show_fitted_parameters", {})
        fit_table = json.loads(result.data)

    expected_rows = [
        {
            "Position / kDa": 65.272253,
            "Sigma / kDa": 15.861073,
            "Counts": 870.825870,
            "Counts / %": 61.0,
            "Amplitudes": 232.080891,
        },
        {
            "Position / kDa": 145.751043,
            "Sigma / kDa": 20.221630,
            "Counts": 293.735298,
            "Counts / %": 21.0,
            "Amplitudes": 57.949551,
        },
        {
            "Position / kDa": 480.554337,
            "Sigma / kDa": 29.687422,
            "Counts": 171.772627,
            "Counts / %": 12.0,
            "Amplitudes": 23.082962,
        },
    ]

    assert len(fit_table) == len(expected_rows)
    for actual, expected in zip(fit_table, expected_rows, strict=True):
        assert actual["name"] == "demo1"
        for key, value in expected.items():
            assert actual[key] == pytest.approx(value, rel=1e-6)


@pytest.mark.asyncio
async def test_mcp_results_match_simple_calibration_notebook(isolated_tool_log_dir):
    """Testing MCP output matches the simple calibration notebook."""
    async with Client(mcp_pyphotomol.mcp) as client:
        await client.call_tool("reset_calibrator", {})
        await client.call_tool(
            "import_single_file",
            {
                "file_path": str(EXAMPLE_DATA_DIR / CONTRAST_EXAMPLE_FILE),
                "name": "notebook_contrasts",
                "calibrator": True,
            },
        )
        await client.call_tool(
            "create_histogram_manual",
            {
                "min_value": -0.04,
                "max_value": 0,
                "bin_width": 0.0004,
                "use_masses": False,
                "calibrator": True,
            },
        )
        await client.call_tool(
            "fit_multi_gaussian",
            {
                "calibrator": True,
                "peaks_guess": [-0.03, -0.01, -0.005],
                "mean_tolerance": 0.1,
                "std_tolerance": 0.1,
                "threshold": -0.0022,
                "baseline": 0,
            },
        )
        result = await client.call_tool("calibrate", {"known_standards": [480, 146, 66]})

    assert "Calibration results" in result.data
    assert photomol_tools.MP_CALIBRATOR.calibration_dic["fit_params"][0] == pytest.approx(
        -6.115911272669366e-05,
        rel=1e-8,
    )
    assert photomol_tools.MP_CALIBRATOR.calibration_dic["fit_params"][1] == pytest.approx(
        0.0004374498828378568,
        rel=1e-8,
    )
    assert photomol_tools.MP_CALIBRATOR.calibration_dic["fit_r2"] == pytest.approx(
        0.9999993694482743,
        rel=1e-8,
    )


@pytest.mark.asyncio
async def test_mcp_logbook_resource(resource_data_root):
    """Testing MCP logbook resource reads."""
    date_dir = resource_data_root / "2026-01-02"
    date_dir.mkdir()
    (date_dir / "mcp_logbook.json").write_text(json.dumps({"calls": [{"tool": "load_example_data"}]}))
    empty_date_dir = resource_data_root / "2026-01-03"
    empty_date_dir.mkdir()

    async with Client(mcp_pyphotomol.mcp) as client:
        result = await client.read_resource("data://02-01-2026/logbook")
        assert json.loads(result[0].text) == {"calls": [{"tool": "load_example_data"}]}

        result = await client.read_resource("data://2026-01-03/logbook")
        assert json.loads(result[0].text) == {"error": "No logbook found for the specified date."}

        result = await client.read_resource("data://not-a-date/logbook")
        assert json.loads(result[0].text) == {"error": "No logbook found for the specified date."}


def test_cli_version_and_transports():
    """Testing CLI version and transport dispatch."""
    runner = CliRunner()
    result = runner.invoke(run_app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip() == mcp_pyphotomol.__version__

    calls = []
    mcp_module = importlib.import_module("mcp_pyphotomol.mcp")

    with patch.object(mcp_module.mcp, "run", lambda **kwargs: calls.append(kwargs)):
        result = runner.invoke(run_app, [])
        assert result.exit_code == 0
        assert calls[-1] == {"transport": "stdio"}

        result = runner.invoke(run_app, ["--transport", "http", "--port", "9999", "--host", "127.0.0.1"])
        assert result.exit_code == 0
        assert calls[-1] == {"transport": "http", "port": 9999, "host": "127.0.0.1"}

        result = runner.invoke(run_app, ["--env", "production"])
        assert result.exit_code == 1
        assert isinstance(result.exception, NotImplementedError)


def test_module_entrypoints_print_version(capsys):
    """Testing direct module entrypoint guards."""
    with patch.object(sys, "argv", ["mcp_pyphotomol", "--version"]):
        with pytest.raises(SystemExit) as package_exit:
            runpy.run_path(Path(mcp_pyphotomol.__file__), run_name="__main__")
    assert package_exit.value.code == 0
    assert capsys.readouterr().out.strip() == mcp_pyphotomol.__version__

    with patch.object(sys, "argv", ["mcp_pyphotomol.main", "--version"]):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            with pytest.raises(SystemExit) as main_exit:
                runpy.run_module("mcp_pyphotomol.main", run_name="__main__")
    assert main_exit.value.code == 0
    assert capsys.readouterr().out.strip() == mcp_pyphotomol.__version__


def test_server_initializes_user_data_when_not_skipped():
    """Testing user data initialization branches without writing to disk."""
    created_dirs = []

    class NoCloseStringIO(io.StringIO):
        def close(self):
            pass

    written = NoCloseStringIO()
    original_exists = os.path.exists
    original_open = open

    def fake_exists(path):
        if "user_data" in str(path):
            return False
        return original_exists(path)

    def fake_makedirs(path):
        created_dirs.append(str(path))

    def fake_open(path, mode="r", *args, **kwargs):
        if str(path).endswith("mcp_logbook.txt") and "w" in mode:
            return written
        return original_open(path, mode, *args, **kwargs)

    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("MCP_PYPHOTOMOL_SKIP_USER_DATA_INIT", None)
        with (
            patch.object(os.path, "exists", fake_exists),
            patch.object(os, "makedirs", fake_makedirs),
            patch.object(builtins, "open", fake_open),
        ):
            namespace = runpy.run_path(Path(photomol_server.__file__))

    assert any(path.endswith("user_data") for path in created_dirs)
    assert any(path.endswith(namespace["today"]) for path in created_dirs)
    assert "MCP Logbook" in written.getvalue()
    assert f"Date: {namespace['today']}" in written.getvalue()


def test_tool_failure_and_error_branches(isolated_tool_log_dir, tmp_path):
    """Testing low-level tool failure and validation branches."""
    with (
        patch.object(photomol_tools.MP_ANALYZER, "models", {}),
        patch.object(photomol_tools.MP_ANALYZER, "import_files", lambda *args, **kwargs: None),
    ):
        assert (
            photomol_tools.import_single_file(EXAMPLE_DATA_DIR / "masses_monomer_1nM.csv")
            == f"Data import failed for {EXAMPLE_DATA_DIR / 'masses_monomer_1nM.csv'}."
        )

        import_dir = tmp_path / "import"
        import_dir.mkdir()
        (import_dir / "measurement.csv").write_text("masses_kDa\n80\n160\n")
        assert photomol_tools.import_folder(import_dir) == f"Data import failed for {import_dir}."

    with patch.object(
        photomol_tools.MP_ANALYZER,
        "models",
        {"missing_masses": SimpleNamespace(masses=None, contrasts=None)},
    ):
        with pytest.raises(ValueError, match="Mass data is missing for model missing_masses"):
            photomol_tools.create_histogram_automatic()

    with patch.object(
        photomol_tools.MP_ANALYZER,
        "models",
        {"missing_contrasts": SimpleNamespace(masses=None, contrasts=None)},
    ):
        with pytest.raises(ValueError, match="Contrast data is missing for model missing_contrasts"):
            photomol_tools.create_histogram_automatic(use_masses=False)


def test_auto_histogram_large_mass_bins(isolated_tool_log_dir):
    """Testing automatic bin-width branches for larger mass ranges."""
    class FakeAnalyzer:
        def __init__(self, masses):
            self.models = {"sample": SimpleNamespace(masses=masses, contrasts=None)}
            self.calls = []

        def apply_to_all(self, method_name, **kwargs):
            self.calls.append((method_name, kwargs))

    medium = FakeAnalyzer([0, 600])
    with patch.object(photomol_tools, "MP_ANALYZER", medium):
        result = photomol_tools.create_histogram_automatic()
        assert "Bin width: 10" in result
        assert medium.calls[-1][1]["bin_width"] == 10

    large = FakeAnalyzer([0, 1500])
    with patch.object(photomol_tools, "MP_ANALYZER", large):
        result = photomol_tools.create_histogram_automatic()
        assert "Bin width: 12" in result
        assert large.calls[-1][1]["bin_width"] == 12


def test_plot_image_export_branches(isolated_tool_log_dir):
    """Testing image-export branches without invoking Kaleido."""
    class FakeFigure:
        def __init__(self):
            self.html_paths = []
            self.image_paths = []

        def write_html(self, path):
            self.html_paths.append(path)
            Path(path).write_text("<html></html>")

        def write_image(self, path, **kwargs):
            self.image_paths.append((path, kwargs))
            Path(path).write_text("<svg></svg>")

    histogram_fig = FakeFigure()
    fits_fig = FakeFigure()
    calibration_fig = FakeFigure()

    with (
        patch.multiple(photomol_tools.PLOT_CONFIG, plot_type="svg", plot_width=640, plot_height=480),
        patch.object(photomol_tools.MP_ANALYZER, "models", {"sample": object()}),
        patch.multiple(
            photomol_tools,
            pm_plot_histogram=lambda *args, **kwargs: histogram_fig,
            pm_plot_histograms_and_fits=lambda *args, **kwargs: fits_fig,
            pm_plot_calibration=lambda *args, **kwargs: calibration_fig,
        ),
    ):
        result = photomol_tools.plot_histograms(colors_hist="red", save_as_html=True)
        assert result.startswith("Histogram plot saved as svg at ")
        assert histogram_fig.html_paths
        assert histogram_fig.image_paths

        result = photomol_tools.plot_histograms_and_fits(colors_hist="blue", save_as_html=True)
        assert result.startswith("Histograms and fits plot saved as svg at ")
        assert fits_fig.html_paths
        assert fits_fig.image_paths

        photomol_tools.MP_CALIBRATOR.known_standards = [66, 148, 480]
        photomol_tools.MP_CALIBRATOR.calibration_dic = {
            "exp_points": [-0.0035, -0.0086, -0.0288],
            "fit_params": [-0.00005, 0.0],
            "fit_r2": 0.99,
        }
        result = photomol_tools.plot_calibration(save_as_html=True)
        assert result.startswith("Calibration plot saved as svg at ")
        assert calibration_fig.html_paths
        assert calibration_fig.image_paths
