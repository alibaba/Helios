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
Template management module for Helios MCP Server.

This module handles loading and managing security rule templates from markdown files.
"""

from pathlib import Path
from typing import Dict


class TemplateManager:
    """Manages template loading and system prompt generation."""
    
    def __init__(self):
        """Initialize the template manager."""
        self._templates = self._load_template_files()
    
    def _load_template_files(self) -> Dict[str, str]:
        """
        Load all template files from rules directory.
        
        Returns:
            Dict mapping rule tags to their content strings.
        """
        templates = {}
        template_dir = Path(__file__).parent.parent.parent / "rules"
        
        if not template_dir.exists():
            print(f"Error: rules directory not found at {template_dir}")
            return templates

        for file_path in template_dir.glob("*.md"):
            tag_name = file_path.stem  # Remove .md extension
            # Remove _guideline suffix to match code patterns
            if tag_name.endswith('_guideline'):
                tag_name = tag_name[:-10]  # Remove '_guideline' suffix
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    templates[tag_name] = content
            except Exception as e:
                print(f"Error loading template {file_path}: {e}")
        
        return templates
    
    def get_system_prompt(self, guideline_mapping: Dict[str, str]) -> str:
        """
        Generate system prompt for AI analysis.
        
        Args:
            guideline_mapping: Dict mapping rule tags to descriptions.
            
        Returns:
            Formatted system prompt string with scenario descriptions.
        """
        prompt_path = Path(__file__).parent.parent / "config" / "sys_prompt.md"
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        scenario = ""
        for tag, description in guideline_mapping.items():
            scenario += f"tag: {tag}, description: {description}\n"
        system_prompt = system_prompt.format(scenario=scenario)
        return system_prompt
    
    def get_template(self, tag: str) -> str:
        """
        Get template content for a specific tag.
        
        Args:
            tag: Rule tag to get template for.
            
        Returns:
            Template content string, empty string if not found.
        """
        return self._templates.get(tag, "")
    
    def get_all_templates(self) -> Dict[str, str]:
        """
        Get all loaded templates.
        
        Returns:
            Dict mapping rule tags to their content strings.
        """
        return self._templates.copy()
    
    def has_template(self, tag: str) -> bool:
        """
        Check if template exists for a specific tag.
        
        Args:
            tag: Rule tag to check.
            
        Returns:
            True if template exists, False otherwise.
        """
        return tag in self._templates
