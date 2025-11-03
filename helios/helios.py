# Copyright (c) 2025 Alibaba Group and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Helios MCP Server for Code Security Analysis.

This module provides the main entry point for the Helios MCP server that analyzes code
for security vulnerabilities and provides remediation guidelines.
"""

from .server.mcp_server import MCPServer


def main():
    """Main entry point for the Helios MCP server."""
    parser = MCPServer.create_argument_parser()
    args = parser.parse_args()
    
    server = MCPServer()
    server.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()