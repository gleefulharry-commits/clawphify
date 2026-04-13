# OpenClaw Framework Knowledge Graph Report

**Version:** 2026.3.22  
**Generated:** 2026-04-13  
**Type:** Pre-built Framework Graph with Multi-Agent Support

---

## Overview

This is a pre-built knowledge graph of the OpenClaw framework. It contains the essential structure, components, multi-agent configuration, and sessions_spawn mechanisms of OpenClaw 2026.3.22+.

## God Nodes (Highest Connectivity)

| Node | Type | Description |
|------|------|-------------|
| openclaw | system | Main system - multi-channel gateway for AI agents |
| gateway | core_component | Single source of truth for sessions, routing, channels |
| channels | category | All channel integrations |
| **multi_agent** | feature | Multi-agent system with coordination |
| **sessions_spawn** | tool | Dynamic sub-agent spawning |
| src_agents | module | Agent system implementation |
| src_cli | module | CLI commands implementation |

## Communities

### 1. Core System
**Nodes:** openclaw, gateway, pi_agent, config_file

The central gateway and agent system. The gateway manages all sessions, routing, and channel connections. Pi agent is the built-in AI coding agent with tool use and multi-agent routing.

### 2. Channel Ecosystem
**Nodes:** channels, built_in_channels, plugin_channels, src_channels, docs_channels, mobile_nodes

All channel integrations and their documentation. Built-in channels include Discord, Telegram, WhatsApp, Signal, Slack, iMessage, Google Chat, WebChat. Plugin channels include Matrix, Zalo, Nostr, Twitch, IRC, Mattermost, BlueBubbles, Feishu, WeChat.

### 3. Multi-Agent System ⭐
**Nodes:** multi_agent, sessions_spawn, agent_to_agent, sessions_tools, orchestrator_pattern, nested_spawning, agent_model_assignment, cost_control

Multi-agent coordination, spawning, and communication. The system supports:
- **Static agents**: Pre-configured in `agents.list`
- **Dynamic spawning**: On-demand via `sessions_spawn`
- **Agent-to-agent communication**: Via sessions_list, sessions_history, sessions_send
- **Orchestrator pattern**: Main agent delegates to workers
- **Cost optimization**: Different models for main vs workers

### 4. Agent Runtime
**Nodes:** src_agents, agents_config, subagent_limits, session_visibility

Agent runtime, configuration, and limits. Controls spawning depth, concurrency, and session visibility.

### 5. CLI & Interface
**Nodes:** src_cli, src_commands, src_tui, onboard_command, dashboard_command, web_control_ui, src_wizard

Command-line interface, web dashboard, and onboarding wizard. Key commands: `openclaw onboard`, `openclaw dashboard`.

### 6. Plugin System
**Nodes:** src_plugin_sdk, src_plugins, plugin_channels, extensions

Plugin SDK for extending OpenClaw with custom channels. VSCode extensions and editor integrations.

### 7. Infrastructure
**Nodes:** src_infra, src_utils, src_config, src_security, src_secrets, src_sessions, tailscale_integration

Shared infrastructure and utilities. Security features include tokens, allowlists, sandboxing. Session management and persistence.

### 8. Media Processing
**Nodes:** src_media, src_media_understanding, canvas_a2ui, browser_control

Media handling for images, audio, documents. Media understanding and processing capabilities.

### 9. Security & Sandboxing
**Nodes:** sandbox_config, src_security, src_secrets

Security features and sandbox configuration. Docker/SSH sandbox for non-main sessions.

### 10. Documentation
**Nodes:** docs_channels, docs_gateway, docs_cli, docs_concepts, docs_tools, docs_providers, docs_automation

All documentation hubs. Channel setup guides, gateway configuration, CLI docs, concepts, tools, providers, automation.

### 11. Ecosystem
**Nodes:** skills, clawteam

Third-party tools and frameworks. ClawTeam provides multi-agent swarm coordination.

---

## Multi-Agent Configuration Guide

### Quick Start

Enable multi-agent with agent-to-agent communication:

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["*"]
    }
  },
  "sessions": {
    "visibility": "all"
  }
}
```

### Sub-Agent Limits

Control spawning behavior:

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "maxSpawnDepth": 2,
        "maxConcurrent": 8,
        "maxChildrenPerAgent": 5,
        "runTimeoutSeconds": 900
      }
    }
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| maxSpawnDepth | 1 | Allow main→sub→sub-sub (depth 2) |
| maxConcurrent | 8 | Total concurrent sub-agents |
| maxChildrenPerAgent | 5 | Per parent agent limit |
| runTimeoutSeconds | 900 | 15 minutes default timeout |

### Sessions Spawn Tool

Dynamic sub-agent creation:

```javascript
// Basic usage
sessions_spawn({
  label: 'coder',
  task: 'Implement OAuth2 flow'
})

// With attachments
sessions_spawn({
  label: 'reviewer',
  task: 'Review this code',
  attachments: [file1, file2]
})
```

**Features:**
- Runtime: `subagent` (default) or `acp`
- Attachments: Up to 50 files, 5MB total
- Auto-cleanup: Follows cleanup policy
- No pre-configuration needed

### Agent-to-Agent Tools

| Tool | Purpose |
|------|---------|
| `sessions_list` | Discover active sessions/agents |
| `sessions_history` | Fetch transcript logs |
| `sessions_send` | Message another session |
| `sessions_spawn` | Create sub-agent |

### Orchestrator Pattern

Main agent coordinates workers:

```
Main Agent (opus - planning)
    │
    ├─→ Spawn Worker 1 (sonnet - coding)
    ├─→ Spawn Worker 2 (sonnet - testing)
    └─→ Spawn Worker 3 (local model - docs)
    │
    ← Collect results
    ← Synthesize output
```

### Cost Control Pattern

Optimize costs with tiered models:

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": "anthropic/claude-sonnet-4-5",
        "thinking": "low"
      }
    },
    "list": [
      {
        "id": "main",
        "model": { "primary": "anthropic/claude-opus-4-6" }
      }
    ]
  }
}
```

**Priority chain:** CLI > agent model > agent tier > template strategy > template model > config default

### Nested Spawning

Allow sub-agents to spawn their own sub-agents:

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "maxSpawnDepth": 2
      }
    }
  }
}
```

**Use cases:**
- Research agent → fact-checker
- Tech lead → coder + reviewer
- Audit agent → specialized sub-audits

**Warning:** Keep depth ≤ 2 to prevent complexity explosion.

### Sandbox Security

Isolate non-main sessions:

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "backend": "docker",
        "scope": "agent"
      }
    }
  }
}
```

| Mode | Description |
|------|-------------|
| off | No sandboxing |
| non-main | Sandbox group/channel sessions (recommended) |
| all | Sandbox all sessions |

---

## Key Relationships

```
openclaw → has_component → gateway
openclaw → includes → pi_agent
openclaw → supports → channels
openclaw → supports → skills
openclaw → implements → multi_agent

multi_agent → uses → sessions_spawn
multi_agent → requires → agent_to_agent
multi_agent → uses → sessions_tools
multi_agent → implements → orchestrator_pattern

sessions_spawn → controlled_by → subagent_limits
sessions_spawn → supports → nested_spawning

channels → includes → built_in_channels
channels → includes → plugin_channels
channels → implemented_in → src_channels

gateway → uses → config_file
config_file → contains → agents_config
config_file → configures → multi_agent
```

---

## Quick Reference

### Getting Started
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
openclaw dashboard
```

### Key Directories

| Path | Purpose |
|------|---------|
| src/agents | Agent system implementation |
| src/gateway | Gateway core |
| src/channels | Channel implementations |
| src/cli | CLI commands |
| src/plugin-sdk | Plugin development SDK |
| docs/channels | Channel setup guides |
| docs/gateway | Gateway configuration |

### Configuration

**Location:** `~/.openclaw/openclaw.json`

**Key Settings:**
- `channels.*.allowFrom` - Allowed senders
- `channels.*.groups` - Group chat settings
- `messages.groupChat.mentionPatterns` - Mention patterns
- `tools.agentToAgent.enabled` - Agent communication
- `agents.defaults.subagents.*` - Spawn limits

### Multi-Agent Commands

```bash
# List sessions
openclaw sessions

# List agents
openclaw agents list

# Spawn sub-agent (CLI)
openclaw sessions spawn --agent-id worker --message "Task"
```

---

## Usage with clawphify

```bash
# Load this graph
clawphify init

# Query multi-agent topics
clawphify query "how do I configure multi-agent?"
clawphify query "what is sessions_spawn?"
clawphify query "how to control sub-agent limits?"
clawphify query "cost optimization for multi-agent"

# General queries
clawphify query "how does channel routing work?"
clawphify query "where is session config?"
clawphify query "what channels are built-in?"
```

---

## Node Count

- **Total Nodes:** 55
- **Total Edges:** 49
- **Communities:** 11
- **God Nodes:** 7

## Edge Types

- **EXTRACTED:** Directly found in source code
- **INFERRED:** Reasonable inference with confidence scores

---

*This graph is pre-built from OpenClaw 2026.3.22. For the latest version or custom modifications, run graphify on the OpenClaw source directly.*
