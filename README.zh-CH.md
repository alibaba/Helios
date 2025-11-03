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

> 🌞 神祇之光，守护 AI 代码之境

## 什么是 Helios

Helios 是从古希腊语 “Ἥλιος”，即太阳神的名字中派生出来的。在希腊神话中，太阳神驾驶着由四匹火马拖拽的金车穿越天空，这代表了光明、能量以及指引的方向。

Helios 寓意着在开发者使用 AI 编辑器编程过程中，能够像太阳一样提供光明和方向，保护程序的安全性，防止潜在安全威胁，生成出更加安全的代码。

## 功能特性

## 使用方法

### 环境配置

- Python: 3.12 或更高版本

安装 uv（如尚未安装），用于项目管理与依赖同步

```bash
# 安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 更新
uv self update 

# 同步依赖
uv sync
 ```

### 运行

启动 MCP 服务器：

```bash
uv run -m helios.helios  
```

首先你需要从 https://bailian.console.aliyun.com 申请一个 BAILIAN_API_KEY

```shell
export BAILIAN_API_KEY=xxxxxx
```

然后在支持 MCP 的客户端中配置服务器：

```json
{
  "mcpServers": {
    "sec-server": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

为保证 mcp 工具被正常调用，请将 config/project_rules.md 添加到编辑器的 project rules 中。

或是在输入提示词时增加：

```markdown
在编写文件或生成的文件之后，必须调用 mcp 工具 query_guide_line 查询一下最佳的文件安全编写指南，然后按照指南对文件进行检查和修正。
```

## 支持的安全检查

- **SQL注入检测**：识别不安全的SQL查询构建
- **命令注入检测**：检测不安全的命令执行
- **文件操作安全检测**：识别路径遍历和文件权限问题
- **网络请求安全检测**：检测不安全的网络通信
- **硬编码凭据检测**：识别硬编码的密码和API密钥
- **弱加密算法检测**：检测使用不安全的加密算法
- **敏感数据泄露检测**：识别日志中的敏感信息泄露
- ...

## 效果演示

![demo](docs/demo.gif)