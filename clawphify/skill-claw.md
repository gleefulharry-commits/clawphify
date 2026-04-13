# clawphify Skill for OpenClaw

**Trigger:** `/clawphify`

clawphify injects pre-built OpenClaw framework knowledge into your project—including **multi-agent configuration** and **sessions_spawn** mechanisms. When you're working with OpenClaw, you don't need to RAG the entire source code.

## Quick Start

```bash
# Show what OpenClaw knowledge is built-in (includes multi-agent)
clawphify info

# Initialize your project with the framework graph
clawphify init
```

## What You Get

### Pre-built knowledge of:
- OpenClaw architecture (gateway, agents, channels, plugins)
- **Multi-agent system** (sessions_spawn, agent-to-agent, orchestration)
- Directory structure and module purposes
- CLI commands and their implementations
- Channel types (built-in vs plugin)
- Configuration patterns

### Multi-Agent Configuration

clawphify includes detailed knowledge of:

| Feature | Config Path | Purpose |
|---------|-------------|---------|
| Agent-to-Agent | `tools.agentToAgent` | Enable agent communication |
| Sub-Agent Limits | `agents.defaults.subagents` | Control spawn behavior |
| Session Visibility | `sessions.visibility` | Debug cross-agent sessions |
| Sandbox | `agents.defaults.sandbox` | Isolate non-main sessions |
| Model Assignment | `agents.list[].model` | Per-agent model selection |

### Sessions Spawn

Dynamic sub-agent creation without pre-configuration:

```javascript
sessions_spawn({
  label: 'coder',
  task: 'Implement feature X'
})
```

**No need to:**
- Pre-create agents with `openclaw agents add`
- Configure allowlists for spawning
- Worry about cleanup (automatic)

## Common Questions

### Multi-Agent Setup

**Q: How do I enable multi-agent?**
```json
{
  "tools": {
    "agentToAgent": { "enabled": true, "allow": ["*"] }
  },
  "sessions": { "visibility": "all" }
}
```

**Q: How to limit sub-agent spawning?**
```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "maxSpawnDepth": 2,
        "maxConcurrent": 8
      }
    }
  }
}
```

**Q: Cost optimization?**
- Main agent: `claude-opus-4-6` (planning)
- Workers: `claude-sonnet-4-5` or local models

**Q: Can sub-agents spawn sub-agents?**
Yes, with `maxSpawnDepth: 2` (opt-in, depth-limited)

## For New Claw Projects

If you're creating a new project based on OpenClaw:

1. `clawphify init` - copies the built-in graph
2. Your AI assistant understands:
   - Framework structure
   - Multi-agent configuration
   - sessions_spawn usage
   - Common patterns
3. No need to read through src/ directories

## For OpenClaw Development

If you're modifying OpenClaw itself:

```bash
graphify . --update
```

This merges framework knowledge + your changes.
