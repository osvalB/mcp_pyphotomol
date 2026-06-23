Usage
=====

Video Demonstration
-------------------

A demonstration of the MCP server is available here:
`Video Demo <https://drive.google.com/file/d/1NQNWErh1wtd1XFVcd_Lsf-STHb5QfaaC/view?usp=share_link>`__.

Common MCP Configuration
------------------------

MCP clients that support an ``mcp.json`` configuration can start
``mcp_pyphotomol`` with ``uvx``:

.. code-block:: json

   {
     "mcpServers": {
       "mcp_pyphotomol": {
         "command": "uvx",
         "args": ["mcp_pyphotomol"],
         "env": {
           "RESULTS_DIR": "/absolute/path/to/results-folder"
         }
       }
     }
   }

``RESULTS_DIR`` is the folder where plots and log files are stored. The server
creates a date-stamped subfolder inside it for each run.

Claude Desktop
--------------

In Claude Desktop, open **Settings**, go to **Developer**, and click
**Edit Config**. Add ``mcp_pyphotomol`` to ``claude_desktop_config.json``:

.. code-block:: json

   {
     "mcpServers": {
       "mcp_pyphotomol": {
         "command": "uvx",
         "args": ["mcp_pyphotomol"],
         "env": {
           "RESULTS_DIR": "/Users/your-name/Documents/user_data_mcp_pyphotomol"
         }
       }
     }
   }

Claude Desktop stores this file at:

- macOS: ``~/Library/Application Support/Claude/claude_desktop_config.json``
- Windows: ``%APPDATA%\Claude\claude_desktop_config.json``

Save the file, then fully quit and reopen Claude Desktop.

For local development, point the client at the repository checkout:

.. code-block:: json

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

If you want to reuse the checkout's existing environment, run it through
``uv``:

.. code-block:: json

   {
     "mcpServers": {
       "mcp_pyphotomol": {
         "command": "uv",
         "args": ["run", "--directory", "/absolute/path/to/mcp_pyphotomol", "mcp_pyphotomol"]
       }
     }
   }

ChatMCP Desktop
---------------

1. Download the `ChatMCP desktop app <https://github.com/daodao97/chatmcp>`__.
2. Open the app and configure a model provider, such as OpenAI or Ollama.
3. Verify that the chat is working by sending a message to the model.
4. Open the settings and add a new MCP server.
5. Set the server type to ``STDIO``.
6. For a local checkout, set the command to ``uv`` and the arguments to:

.. code-block:: text

   run --directory /absolute/path/to/mcp_pyphotomol mcp_pyphotomol

VS Code with GitHub Copilot
---------------------------

1. Download and install `Visual Studio Code <https://code.visualstudio.com/>`__.
2. `Set up GitHub Copilot in VS Code
   <https://code.visualstudio.com/docs/copilot/setup>`__.
3. Edit the VS Code MCP configuration, commonly named ``mcp.json``:

.. code-block:: json

   {
     "servers": {
       "mcp_pyphotomol": {
         "command": "uvx",
         "args": ["mcp_pyphotomol"],
         "env": {
           "RESULTS_DIR": "/absolute/path/to/results-folder"
         }
       }
     }
   }

4. Start the MCP server from VS Code and use Copilot's agent mode to interact
   with the tools.

Developer Debugging
-------------------

To run the MCP server directly from a local checkout:

.. code-block:: bash

   uv run mcp_pyphotomol

If your environment provides the FastMCP development CLI, you can also use it
for interactive MCP debugging.
