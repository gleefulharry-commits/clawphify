"""clawphify - OpenClaw framework knowledge graph injector for graphify.

clawphify comes with a pre-built OpenClaw framework knowledge graph that includes:
- Core system architecture (gateway, agent, channels)
- Directory structure (src/, docs/, skills/, extensions/)
- CLI commands and configuration
- Channel ecosystem (built-in and plugin channels)
- Plugin SDK and extension points

This allows new OpenClaw projects to immediately understand the framework structure
without needing to RAG the entire source code.

Usage:
    clawphify info          # Show built-in OpenClaw framework information
    clawphify init          # Initialize clawphify-out/ with built-in graph
    clawphify install       # Install skill for your AI assistant
    clawphify query "..."   # Query the OpenClaw framework graph

For full graphify features (building custom graphs), use `graphify` directly.
"""

from pathlib import Path

def get_builtin_graph_path() -> Path:
    """Get the path to the built-in OpenClaw framework graph."""
    return Path(__file__).parent / "data" / "openclaw_graph.json"

__all__ = ["get_builtin_graph_path"]
