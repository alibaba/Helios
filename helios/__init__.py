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
Helios MCP Server Package.

A Model Context Protocol (MCP) server for code security analysis that provides
AI-powered vulnerability detection and remediation guidelines.
"""

from .server.mcp_server import MCPServer
from .services.security_service import SecurityService
from .core.config_manager import ConfigManager
from .core.template_manager import TemplateManager
from .core.ai_analyzer import AIAnalyzer

__version__ = "1.0.0"
__all__ = [
    'MCPServer',
    'SecurityService', 
    'ConfigManager',
    'TemplateManager',
    'AIAnalyzer'
]
