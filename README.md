# This package is being developed and breaking changes may occur at any moment


# mcp_pyphotomol

<!--
[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https%3A%2F%2Fbiocontext.ai%2Fregistry)](https://biocontext.ai/registry)
-->

[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/osvalB/mcp_pyphotomol/test.yaml?branch=main
[badge-docs]: https://img.shields.io/badge/docs-Sphinx-0a507a

This repository contains an MCP server for the analysis of mass photometry data.
It is based on the Python package [pyphotomol](https://github.com/osvalB/pyphotomol).

## Video demonstration

Watch a demonstration of the MCP server in action: [Video Demo](https://drive.google.com/file/d/1NQNWErh1wtd1XFVcd_Lsf-STHb5QfaaC/view?usp=share_link).

## Getting started

Please refer to the [documentation]

## Installation

You need to have Python 3.11 or newer installed on your system.
If you don't have Python installed, we recommend installing [uv][].

### Run from the command line

```bash
uvx mcp_pyphotomol
```

### Configure an MCP client

Add the server to any MCP-compatible client that supports the `mcpServers`
configuration format:

```json
{
  "mcpServers": {
    "mcp_pyphotomol": {
      "command": "uvx",
      "args": ["mcp_pyphotomol"]
    }
  }
}
```

After updating the configuration, restart the MCP client so it can launch the
server.

### Local development

To run the server from a local checkout, use an absolute path to the repository:

```json
{
  "mcpServers": {
    "mcp_pyphotomol": {
      "command": "uvx",
      "args": [
        "--refresh",
        "--from",
        "/absolute/path/to/mcp_pyphotomol",
        "mcp_pyphotomol"
      ]
    }
  }
}
```

If you want to reuse the checkout's existing environment, run it through `uv`:

```json
{
  "mcpServers": {
    "mcp_pyphotomol": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/mcp_pyphotomol", "mcp_pyphotomol"]
    }
  }
}
```

### Install with pip

```bash
pip install --user mcp_pyphotomol
```

Then run the server with:

```bash
mcp_pyphotomol
```

If your shell cannot find the command, make sure your user-level Python scripts
directory is on `PATH`.

## Contact

If you found a bug, please use the [issue tracker][].

## Citation

If you use `mcp_pyphotomol`, please cite it as:

Burastero, O. (2026). `mcp_pyphotomol` (Version 0.1.0) [Computer software].
GitHub. https://github.com/osvalB/mcp_pyphotomol

```bibtex
@software{burastero_2026_mcp_pyphotomol,
  author = {Burastero, Osvaldo},
  title = {mcp_pyphotomol},
  version = {0.1.0},
  year = {2026},
  url = {https://github.com/osvalB/mcp_pyphotomol}
}
```

[uv]: https://github.com/astral-sh/uv
[issue tracker]: https://github.com/osvalB/mcp_pyphotomol/issues
[tests]: https://github.com/osvalB/mcp_pyphotomol/actions/workflows/test.yaml
[documentation]: https://osvalb.github.io/mcp_pyphotomol
[api documentation]: https://github.com/osvalB/mcp_pyphotomol/blob/main/docs/modules.rst
[pypi]: https://pypi.org/project/mcp_pyphotomol
