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
Security service module for Helios MCP Server.

This module handles security analysis and guideline querying functionality.
"""

import json
import os
from typing import Optional
from ..core.config_manager import ConfigManager
from ..core.template_manager import TemplateManager
from ..core.ai_analyzer import AIAnalyzer


class SecurityService:
    """Service for handling security analysis and guideline queries."""
    
    def __init__(self):
        """Initialize the security service."""
        self.config_manager = ConfigManager()
        self.template_manager = TemplateManager()
        self.ai_analyzer = AIAnalyzer()
        
        # Load configuration and templates
        self.guideline_mapping = self.config_manager.get_guideline_mapping()
        self.templates = self.template_manager.get_all_templates()
        self.system_prompt = self.template_manager.get_system_prompt(self.guideline_mapping)
    
    def query_guide_line(self, path: str, explanation: Optional[str] = None) -> str:
        """
        Query security guidelines for generated Java code files.
        
        This method analyzes a code file and returns appropriate security
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
        try:
            if not os.path.exists(path):
                return json.dumps({
                    "sec": False,
                    "fix_guide_line": f"File path does not exist: {path}"
                }, ensure_ascii=False, indent=2)

            # Read local file content
            with open(path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            # Call analyze_code_content to get tag type
            content = self.ai_analyzer.analyze_code_content(file_content, self.system_prompt)
            tag = self.ai_analyzer.extract_tag(content)

            # Return corresponding content based on tag type from templates
            fix_guide_line = ""

            if self.template_manager.has_template(tag):
                fix_guide_line += f"{self.template_manager.get_template(tag)}\n\n"
            else:
                fix_guide_line += f"No corresponding fix guidelines found.\n\n"

            return json.dumps({
                "fix_guide_line": fix_guide_line.strip()
            }, ensure_ascii=False, indent=2)

        except Exception as e:
            return json.dumps({
                "fix_guide_line": f"Error occurred while checking file: {str(e)}"
            }, ensure_ascii=False, indent=2)
