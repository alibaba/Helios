<p align="center">
    <img src="docs/logo-2.png" width="360" alt="logo"/>
</p>
<h1 align="center">Helios</h1>

<p align="center">
<img src="https://img.shields.io/github/languages/top/alibaba/Helios.svg?&color=blueviolet" alt="languages"/>
<img src="https://img.shields.io/github/license/alibaba/Helios" alt="license"/>
<img src="https://img.shields.io/github/stars/alibaba/Helios.svg" alt="stars"/>
</p>

<p align="center">
  <a href="README.zh-CH.md">中文</a> | <a href="README.md">English</a>
</p>

> 🌞 Divine Light, Guardian of AI Code Realm

## What is Helios

Helios is derived from the ancient Greek "Ἥλιος", the name of the sun god. In Greek mythology, the sun god drives a
golden chariot pulled by four fire horses across the sky, representing light, energy, and guidance.

Helios symbolizes providing light and direction like the sun during developers' AI editor programming process,
protecting program security, preventing potential security threats, and generating more secure code.

## Features

## Usage

### Environment Setup

- Python: 3.12 or higher

Install uv (if not already installed) for project management and dependency synchronization:

```bash
# Install
curl -LsSf https://astral.sh/uv/install.sh | sh

# Update
uv self update 

# Sync dependencies
uv sync
```

### Running

Start the MCP server:

```bash
uv run -m helios.helios  
```

First you need a BAILIAN_API_KEY from https://bailian.console.aliyun.com

```shell
export BAILIAN_API_KEY=xxxxxx
```

Then Configure the server in MCP-compatible clients:

```json
{
  "mcpServers": {
    "sec-server": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

To ensure MCP tools are called properly, please add `config/project_rules.md` to your editor's project rules.

Or add the following to your input prompts:

```markdown
After writing files or generating files, you must call the MCP tool query_guide_line to query the best file security writing guidelines, then check and correct files according to the guidelines.
```

## Supported Security Checks

- **SQL Injection Detection**: Identifies unsafe SQL query construction
- **Command Injection Detection**: Detects unsafe command execution
- **File Operation Security Detection**: Identifies path traversal and file permission issues
- **Network Request Security Detection**: Detects unsafe network communication
- **Hardcoded Credentials Detection**: Identifies hardcoded passwords and API keys
- **Weak Encryption Algorithm Detection**: Detects use of insecure encryption algorithms
- **Sensitive Data Leakage Detection**: Identifies sensitive information leakage in logs
- ...

## Demo

![demo](docs/demo.gif)