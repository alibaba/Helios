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
AI analysis module for Helios MCP Server.

This module handles AI-powered code analysis for security vulnerability detection.
"""

import re
import os
from openai import OpenAI


class AIAnalyzer:
    """Handles AI-powered code analysis for security detection."""
    
    def __init__(self):
        """Initialize the AI analyzer."""
        self._client = None
        self._api_key = None
    
    def _get_client(self) -> OpenAI:
        """
        Get or create OpenAI client.
        
        Returns:
            OpenAI client instance.
            
        Raises:
            ValueError: If BAILIAN_API_KEY environment variable is not set.
        """
        if self._client is None:
            api_key = os.getenv("BAILIAN_API_KEY")
            if not api_key:
                raise ValueError("BAILIAN_API_KEY environment variable is not set")
            
            self._api_key = api_key
            self._client = OpenAI(
                api_key=api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
        
        return self._client
    
    def extract_tag(self, content: str) -> str:
        """
        Extract tag from AI analysis content.
        
        Args:
            content: AI analysis response content.
            
        Returns:
            Extracted tag string.
        """
        return re.search(r'<tag>(.*?)</tag>', content).group(1)
    
    def analyze_code_content(self, code_content: str, system_prompt: str) -> str:
        """
        Analyze code content using AI to identify security patterns.
        
        Args:
            code_content: Source code content to analyze.
            system_prompt: System prompt for AI analysis.
            
        Returns:
            AI analysis response containing security tag.
            
        Raises:
            ValueError: If BAILIAN_API_KEY environment variable is not set.
        """
        client = self._get_client()
        
        completion = client.chat.completions.create(
            model="qwen3-coder-plus",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": code_content},
            ]
        )
        content = completion.choices[0].message.content
        return content
