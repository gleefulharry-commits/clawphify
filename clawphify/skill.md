# clawphify Skill

**Trigger:** `/clawphify`

clawphify injects pre-built OpenClaw framework knowledge into your project. New OpenClaw projects immediately understand the framework structure—including multi-agent configuration and sessions_spawn—without RAG-ing source code.

## What clawphify Provides

**Built-in OpenClaw Framework Graph (v2026.3.22):**
- Core system: gateway, Pi agent, channels, web UI
- Source structure: src/agents, src/gateway, src/channels, src/cli, etc.
- CLI commands: onboard, dashboard, agent, nodes, sessions
- Channel ecosystem: 20+ built-in and plugin channels
- **Multi-agent system:** sessions_spawn, agent-to-agent, orchestration patterns
- Plugin SDK and extension points
- Configuration patterns

### Multi-Agent Topics Covered

| Topic | Description |
|-------|-------------|
| `sessions_spawn` | Dynamic sub-agent spawning tool |
| `agent_to_agent` | Enable agent communication |
| `subagent_limits` | Control spawn depth, concurrency, timeouts |
| `orchestrator_pattern` | Main agent delegates to workers |
| `cost_control` | Use different models for main vs workers |
| `nested_spawning` | Sub-agents spawning sub-agents (depth-limited) |
| `session_visibility` | Control which sessions agents can see |

## Commands

```bash
# Show framework info (includes multi-agent)
clawphify info

# Initialize project with built-in graph
clawphify init

# Query the framework graph
clawphify query "how to configure multi-agent?"
clawphify query "sessions_spawn examples"
clawphify query "subagent limits configuration"

# Install skill for your AI assistant
clawphify install
```

## Multi-Agent Quick Reference

### Enable Multi-Agent

```json
// ~/.openclaw/openclaw.json
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

### Sessions Spawn Usage

```javascript
// In agent conversation
sessions_spawn({
  label: 'coder',
  task: 'Implement OAuth2 flow'
})
```

### Cost-Optimized Setup

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

## Usage Patterns

### New OpenClaw Project

When starting a new OpenClaw-based project:

1. Run `clawphify init` to copy the built-in graph to `clawphify-out/`
2. The AI assistant now knows OpenClaw's structure—including multi-agent setup
3. Ask questions like:
   - "how do I add a new channel?"
   - "how to configure multi-agent with sessions_spawn?"
   - "what are the subagent limits?"
   - "cost optimization strategies for multi-agent?"

### Multi-Agent Development

Common questions clawphify can answer:

- "What's the difference between static agents.list and dynamic sessions_spawn?"
- "How do I enable agent-to-agent communication?"
- "What is the orchestrator pattern?"
- "How to configure nested spawning?"
- "How do I sandbox sub-agents?"
- "What models should I use for main vs workers?"

### Extending OpenClaw

If you're modifying OpenClaw itself, use graphify directly:

```bash
graphify . --update
```

This merges the framework graph with your specific changes.

## Graph Location

- Built-in graph: `clawphify/data/openclaw_graph.json`
- Project graph: `clawphify-out/openclaw_graph.json` (after `clawphify init`)
- Report: `clawphify/data/GRAPH_REPORT.md`

## Integration with graphify

clawphify uses graphify's graph format. You can use graphify tools on clawphify graphs:

```bash
graphify query "sessions_spawn" --graph clawphify-out/openclaw_graph.json
```
