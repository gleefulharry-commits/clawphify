"""Built-in OpenClaw framework knowledge graph data."""
from pathlib import Path

def get_graph_path() -> Path:
    """Return the path to the built-in OpenClaw framework graph."""
    return Path(__file__).parent / "openclaw_graph.json"
