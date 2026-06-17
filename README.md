# This package is being developed and breaking changes may occur at any moment


# mcp_pyphotomol

<!--
[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https%3A%2F%2Fbiocontext.ai%2Fregistry)](https://biocontext.ai/registry)
-->

[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/osvalB/mcp_pyphotomol/test.yaml?branch=main
[badge-docs]: https://img.shields.io/badge/docs-Sphinx-0a507a

Analysis of mass photometry data

## Video demonstration

Watch a demonstration of the MCP server in action: [Video Demo](https://drive.google.com/file/d/1NQNWErh1wtd1XFVcd_Lsf-STHb5QfaaC/view?usp=share_link).

## Getting started

Please refer to the [documentation]

## Installation

You need to have Python 3.12 or newer installed on your system.
If you don't have Python installed, we recommend installing [uv][].

There are several alternative options to install mcp_pyphotomol:

### 1. Use `uvx` to run it immediately
After publication to PyPI:
```bash
uvx mcp_pyphotomol
```

Or from a Git repository:

```bash
uvx git+https://github.com/osvalB/mcp_pyphotomol.git@main
```

### 2. Include it in one of various clients that supports the `mcp.json` standard

If your MCP server is published to PyPI, use the following configuration:

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
In case the MCP server is not yet published to PyPI, use this configuration:

```json
{
  "mcpServers": {
    "mcp_pyphotomol": {
      "command": "uvx",
      "args": ["git+https://github.com/osvalB/mcp_pyphotomol.git@main"]
    }
  }
}
```

For purely local development (e.g., in Cursor or VS Code), use the following configuration:

```json
{
  "mcpServers": {
    "mcp_pyphotomol": {
      "command": "uvx",
      "args": [
        "--refresh",
        "--from",
        "path/to/repository",
        "mcp_pyphotomol"
      ]
    }
  }
}
```

If you want to reuse and existing environment for local development, use the following configuration:

```json
{
  "mcpServers": {
    "mcp_pyphotomol": {
      "command": "uv",
      "args": ["run", "--directory", "path/to/repository", "mcp_pyphotomol"]
    }
  }
}
```

### 3. Install it through `pip`:

```bash
pip install --user mcp_pyphotomol
```

### 4. Install the latest development version:

```bash
pip install git+https://github.com/osvalB/mcp_pyphotomol.git@main
```

## Contact

If you found a bug, please use the [issue tracker][].

## Citation

Osvaldo Burastero,

[uv]: https://github.com/astral-sh/uv
[issue tracker]: https://github.com/osvalB/mcp_pyphotomol/issues
[tests]: https://github.com/osvalB/mcp_pyphotomol/actions/workflows/test.yaml
[documentation]: https://osvalb.github.io/pyphotomol
[api documentation]: https://github.com/osvalB/mcp_pyphotomol/blob/main/docs/modules.rst
[pypi]: https://pypi.org/project/mcp_pyphotomol
