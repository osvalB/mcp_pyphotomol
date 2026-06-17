Usage
=====

Video Demonstration
-------------------

A demonstration of the MCP server is available here:
`Video Demo <https://drive.google.com/drive/search?q=mcp>`__.

Common MCP Configuration
------------------------

MCP clients that support an ``mcp.json`` configuration can start
``mcp_pyphotomol`` with ``uvx`` after the package is published:

.. code-block:: json

   {
     "mcpServers": {
       "mcp_pyphotomol": {
         "command": "uvx",
         "args": ["mcp_pyphotomol"]
       }
     }
   }

To run the server directly from GitHub:

.. code-block:: json

   {
     "mcpServers": {
       "mcp_pyphotomol": {
         "command": "uvx",
         "args": ["git+https://github.com/osvalB/mcp_pyphotomol.git@main"]
       }
     }
   }

For local development, point the client at the repository checkout:

.. code-block:: json

   {
     "mcpServers": {
       "mcp_pyphotomol": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "/absolute/path/to/mcp_pyphotomol",
           "mcp_pyphotomol"
         ]
       }
     }
   }

Claude Desktop
--------------

1. Download the `Claude desktop app <https://claude.ai/download>`__.
2. Edit the Claude Desktop configuration file. On Linux this is commonly
   ``~/.config/Claude/claude_desktop_config.json``; on macOS it is commonly
   ``~/Library/Application Support/Claude/claude_desktop_config.json``.
3. Add ``mcp_pyphotomol`` to ``mcpServers`` using one of the configurations
   above. Replace the local repository path with the path on your computer.
4. Restart Claude Desktop and select the ``mcp_pyphotomol`` server from the
   available MCP servers.

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
3. Edit the VS Code MCP configuration, commonly named ``mcp.json``. Replace
   the path with the path to your local checkout:

.. code-block:: json

   {
     "servers": {
       "mcp_pyphotomol": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "/absolute/path/to/mcp_pyphotomol",
           "mcp_pyphotomol"
         ]
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
