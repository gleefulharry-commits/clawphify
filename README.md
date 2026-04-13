# clawphify 🦞

**OpenClaw Framework Knowledge Graph Injector**

[![GitHub](https://img.shields.io/github/license/han/clawphify)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

> 🍴 **Fork Notice**: This is a specialized fork of [graphify](https://github.com/safishamsi/graphify) by [@safishamsi](https://github.com/safishamsi). 
> While graphify is a general-purpose knowledge graph builder, clawphify focuses specifically on **pre-built OpenClaw framework knowledge** for instant project understanding. New OpenClaw projects immediately understand the framework structure—no need to RAG the entire source code.

## Why clawphify?

When you start a new project based on OpenClaw:

**Without clawphify:**
1. AI reads OpenClaw source files to understand structure
2. Consumes thousands of tokens
3. May miss architectural patterns

**With clawphify:**
1. Pre-built knowledge graph loaded instantly
2. Zero token cost for framework understanding
3. Structured, accurate framework knowledge

## Quick Start

```bash
# Install
pip install clawphify

# Show built-in OpenClaw knowledge
clawphify info

# Initialize your project with framework graph
clawphify init

# Query the framework
clawphify query "how does channel routing work?"
```

## What You Get

### Pre-built Framework Knowledge

**Core System:**
- Gateway architecture and session management
- Pi agent and multi-agent routing
- Channel ecosystem (20+ channels)
- Web Control UI

**Source Structure:**
```
src/agents     → Agent system, tools, sandbox
src/gateway    → Gateway core, routing
src/channels   → Channel implementations  
src/cli        → CLI commands
src/plugin-sdk → Plugin development SDK
src/security   → Tokens, allowlists
src/tasks      → Task management
```

**CLI Commands:**
- `openclaw onboard --install-daemon`
- `openclaw dashboard`
- `openclaw agent`
- `openclaw nodes`

**Channels:**
- Built-in: Discord, Telegram, WhatsApp, Signal, Slack, iMessage, WebChat
- Plugin: Matrix, Zalo, Nostr, Twitch, IRC, Mattermost, Feishu

### Knowledge Communities

The framework is pre-clustered into 8 communities:

1. **Core System** - gateway, agent, config
2. **Channel Ecosystem** - all channel integrations
3. **Agent System** - runtime, routing, skills
4. **CLI & Interface** - commands, TUI, web UI
5. **Plugin System** - SDK, extensions
6. **Infrastructure** - utils, security, sessions
7. **Media Processing** - images, audio, docs
8. **Documentation** - all docs hubs

## Usage Patterns

### New OpenClaw Project

```bash
# In your new project directory
clawphify init

# Now ask framework questions:
# "What files should I modify to add a channel?"
# "How does authentication work?"
# "Where is the session config?"
```

### OpenClaw Development

If you're modifying OpenClaw itself, use [graphify](https://github.com/safishamsi/graphify) directly:

```bash
graphify . --update
```

This builds a project-specific graph including your changes.

## Installation

```bash
pip install clawphify

# Install skill for your AI assistant
clawphify install                    # Claude Code
clawphify install --platform claw    # OpenClaw
clawphify install --platform codex   # Codex
```

## Commands

| Command | Description |
|---------|-------------|
| `clawphify info` | Show built-in OpenClaw framework info |
| `clawphify init` | Copy built-in graph to `clawphify-out/` |
| `clawphify query "Q"` | Query the framework graph |
| `clawphify install` | Install skill for AI assistant |
| `clawphify claude install` | Configure for Claude Code |
| `clawphify claw install` | Configure for OpenClaw |

## Example Queries

```bash
# Architecture questions
clawphify query "how does gateway manage sessions?"
clawphify query "what is the relationship between channels and plugins?"

# Implementation guidance
clawphify query "where should I add authentication logic?"
clawphify query "how do I create a new channel?"

# Configuration help
clawphify query "what are the key config settings?"
clawphify query "how do I configure WhatsApp channel?"
```

## Integration with graphify

clawphify uses graphify's graph format. You can use graphify tools:

```bash
# Merge with project-specific knowledge
graphify . --update --graph clawphify-out/openclaw_graph.json

# Use graphify's query on clawphify graph
graphify query "channels" --graph clawphify-out/openclaw_graph.json
```

## How It Works

1. **Built-in Graph:** Contains OpenClaw v3.22.0 framework structure
2. **JSON Format:** Compatible with graphify's graph.json format
3. **Node Types:** system, module, feature, command, config, docs
4. **Edges:** EXTRACTED (from source) and INFERRED (relationships)
5. **Communities:** Pre-clustered using Leiden algorithm

## Graph Contents

- **50+ nodes:** Core components, modules, features, docs
- **30+ edges:** Relationships and dependencies
- **8 communities:** Logical groupings
- **Quick reference:** Getting started, key directories, config essentials

## Requirements

- Python 3.10+
- networkx
- tree-sitter

## License

MIT - Same as OpenClaw and graphify

## Credits

- Built on [graphify](https://github.com/safishamsi/graphify) by @safishamsi
- OpenClaw framework by the OpenClaw team
- Graph extraction from OpenClaw v3.22.0

---

**For new Claw: Know thy framework instantly.** 🦞
