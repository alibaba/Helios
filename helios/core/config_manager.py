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
Configuration management module for Helios MCP Server.

This module handles loading and managing configuration files and settings.
"""

import json
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from config.json file.
        
        Returns:
            Dict containing configuration data, empty dict if file not found or error.
        """
        config_path = Path(__file__).parent.parent / "config" / "config.json"

        if not config_path.exists():
            print(f"Warning: Config file not found at {config_path}")
            return {}

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def get_guideline_mapping(self) -> Dict[str, str]:
        """
        Get guideline mapping from configuration.
        
        Returns:
            Dict mapping rule tags to their descriptions.
        """
        return self._config.get("guideline_mapping", {})
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the complete configuration.
        
        Returns:
            Dict containing all configuration data.
        """
        return self._config.copy()
