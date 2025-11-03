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
MCP Server module for Helios MCP Server.

This module handles MCP server setup, tool registration, and server management.
"""

import asyncio
import traceback
import argparse
from typing import Optional
from fastmcp import FastMCP
from ..services.security_service import SecurityService


class MCPServer:
    """MCP Server for Helios security analysis."""
    
    def __init__(self, name: str = "code-analysis-service"):
        """
        Initialize the MCP server.
        
        Args:
            name: Name of the MCP service.
        """
        self.app = FastMCP(name)
        self.security_service = SecurityService()
        self._register_tools()
    
    def _register_tools(self):
        """Register MCP tools with the server."""
        
        @self.app.tool()
        def query_guide_line(path: str, explanation: Optional[str] = None) -> str:
            """
            Query security guidelines for generated Java code files.
            
            This tool analyzes a code file and returns appropriate security
            remediation guidelines based on detected security patterns.
            
            Args:
                path: Absolute path to the generated file.
                explanation: Optional explanation parameter for compatibility.
                
            Returns:
                JSON string containing fix guidelines:
                {
                    "fix_guide_line": "Security remediation guidelines string"
                }
            """
            return self.security_service.query_guide_line(path, explanation)
    
    def run(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Run the MCP server.
        
        Args:
            host: Host address to bind to.
            port: Port number to bind to.
        """
        try:
            print(f"Starting MCP server on {host}:{port}")
            exit_code = asyncio.run(self.app.run_http_async(host=host, port=port))
            exit(exit_code)
        except Exception as e:
            print(f"Server failed to start: {e}")
            traceback.print_exc()
            exit(1)
    
    @staticmethod
    def create_argument_parser() -> argparse.ArgumentParser:
        """
        Create command line argument parser.
        
        Returns:
            Configured ArgumentParser instance.
        """
        parser = argparse.ArgumentParser(description='Security MCP Server')
        parser.add_argument('--host', default='127.0.0.1', 
                           help='MCP server host address (default: 127.0.0.1)')
        parser.add_argument('-p', '--port', type=int, default=8000,
                           help='MCP server port (default: 8000)')
        return parser
