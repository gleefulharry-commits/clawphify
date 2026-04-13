"""clawphify CLI - OpenClaw framework knowledge graph injector for graphify."""
from __future__ import annotations
import json
import platform
import re
import shutil
import sys
from pathlib import Path

try:
    from importlib.metadata import version as _pkg_version
    __version__ = _pkg_version("clawphify")
except Exception:
    __version__ = "unknown"


def _get_builtin_graph_path() -> Path:
    """Get the path to the built-in OpenClaw framework graph."""
    return Path(__file__).parent / "data" / "openclaw_graph.json"


def _load_builtin_graph() -> dict:
    """Load the built-in OpenClaw framework knowledge graph."""
    graph_path = _get_builtin_graph_path()
    if graph_path.exists():
        return json.loads(graph_path.read_text(encoding="utf-8"))
    return {}


def _check_skill_version(skill_dst: Path) -> None:
    """Warn if the installed skill is from an older clawphify version."""
    version_file = skill_dst.parent / ".clawphify_version"
    if not version_file.exists():
        return
    installed = version_file.read_text(encoding="utf-8").strip()
    if installed != __version__:
        print(f"  warning: skill is from clawphify {installed}, package is {__version__}. Run 'clawphify install' to update.")


_SETTINGS_HOOK = {
    "matcher": "Glob|Grep",
    "hooks": [
        {
            "type": "command",
            "command": (
                "[ -f clawphify-out/graph.json ] && "
                "echo 'clawphify: OpenClaw knowledge graph exists. Read clawphify-out/GRAPH_REPORT.md "
                "for framework structure before searching raw files.' || true"
            ),
        }
    ],
}

_SKILL_REGISTRATION = (
    "\n# clawphify\n"
    "- **clawphify** (`~/.claude/skills/clawphify/SKILL.md`) "
    "- OpenClaw framework knowledge graph. Trigger: `/clawphify`\n"
    "When the user types `/clawphify`, invoke the Skill tool "
    "with `skill: \"clawphify\"` before doing anything else.\n"
)


_PLATFORM_CONFIG: dict[str, dict] = {
    "claude": {
        "skill_file": "skill.md",
        "skill_dst": Path(".claude") / "skills" / "clawphify" / "SKILL.md",
        "claude_md": True,
    },
    "codex": {
        "skill_file": "skill-codex.md",
        "skill_dst": Path(".agents") / "skills" / "clawphify" / "SKILL.md",
        "claude_md": False,
    },
    "opencode": {
        "skill_file": "skill-opencode.md",
        "skill_dst": Path(".config") / "opencode" / "skills" / "clawphify" / "SKILL.md",
        "claude_md": False,
    },
    "claw": {
        "skill_file": "skill-claw.md",
        "skill_dst": Path(".claw") / "skills" / "clawphify" / "SKILL.md",
        "claude_md": False,
    },
    "droid": {
        "skill_file": "skill-droid.md",
        "skill_dst": Path(".factory") / "skills" / "clawphify" / "SKILL.md",
        "claude_md": False,
    },
    "windows": {
        "skill_file": "skill-windows.md",
        "skill_dst": Path(".claude") / "skills" / "clawphify" / "SKILL.md",
        "claude_md": True,
    },
}


def install(platform: str = "claude") -> None:
    if platform not in _PLATFORM_CONFIG:
        print(
            f"error: unknown platform '{platform}'. Choose from: {', '.join(_PLATFORM_CONFIG)}",
            file=sys.stderr,
        )
        sys.exit(1)

    cfg = _PLATFORM_CONFIG[platform]
    skill_src = Path(__file__).parent / cfg["skill_file"]
    if not skill_src.exists():
        print(f"error: {cfg['skill_file']} not found in package - reinstall clawphify", file=sys.stderr)
        sys.exit(1)

    skill_dst = Path.home() / cfg["skill_dst"]
    skill_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(skill_src, skill_dst)
    (skill_dst.parent / ".clawphify_version").write_text(__version__, encoding="utf-8")
    print(f"  skill installed  ->  {skill_dst}")

    if cfg["claude_md"]:
        # Register in ~/.claude/CLAUDE.md (Claude Code only)
        claude_md = Path.home() / ".claude" / "CLAUDE.md"
        if claude_md.exists():
            content = claude_md.read_text(encoding="utf-8")
            if "clawphify" in content:
                print(f"  CLAUDE.md        ->  already registered (no change)")
            else:
                claude_md.write_text(content.rstrip() + _SKILL_REGISTRATION, encoding="utf-8")
                print(f"  CLAUDE.md        ->  skill registered in {claude_md}")
        else:
            claude_md.parent.mkdir(parents=True, exist_ok=True)
            claude_md.write_text(_SKILL_REGISTRATION.lstrip(), encoding="utf-8")
            print(f"  CLAUDE.md        ->  created at {claude_md}")

    print()
    print("Done. Open your AI coding assistant and type:")
    print()
    print("  /clawphify")
    print()


_CLAUDE_MD_SECTION = """\
## clawphify

This project uses clawphify with a pre-built OpenClaw framework knowledge graph.

Rules:
- clawphify comes with a built-in OpenClaw framework graph at clawphify-out/
- The built-in graph includes: core system, channel ecosystem, agent system, CLI interface, plugin system
- Before answering OpenClaw architecture questions, read clawphify-out/GRAPH_REPORT.md
- For new OpenClaw projects, the framework structure is already known - no need to RAG the source
- For existing OpenClaw projects, run `clawphify .` to merge project-specific knowledge with framework graph
"""

_CLAUDE_MD_MARKER = "## clawphify"

# AGENTS.md section for Codex, OpenCode, and OpenClaw.
_AGENTS_MD_SECTION = """\
## clawphify

This project uses clawphify with a pre-built OpenClaw framework knowledge graph.

Rules:
- clawphify comes with a built-in OpenClaw framework graph at clawphify-out/
- The built-in graph includes: core system, channel ecosystem, agent system, CLI interface, plugin system
- Before answering OpenClaw architecture questions, read clawphify-out/GRAPH_REPORT.md
- For new OpenClaw projects, the framework structure is already known - no need to RAG the source
- For existing OpenClaw projects, run `clawphify .` to merge project-specific knowledge with framework graph
"""

_AGENTS_MD_MARKER = "## clawphify"


def _agents_install(project_dir: Path, platform: str) -> None:
    """Write the clawphify section to the local AGENTS.md (Codex/OpenCode/OpenClaw)."""
    target = (project_dir or Path(".")) / "AGENTS.md"

    if target.exists():
        content = target.read_text(encoding="utf-8")
        if _AGENTS_MD_MARKER in content:
            print(f"clawphify already configured in AGENTS.md")
            return
        new_content = content.rstrip() + "\n\n" + _AGENTS_MD_SECTION
    else:
        new_content = _AGENTS_MD_SECTION

    target.write_text(new_content, encoding="utf-8")
    print(f"clawphify section written to {target.resolve()}")
    print()
    print(f"{platform.capitalize()} will now check the OpenClaw knowledge graph before answering")
    print("framework questions.")
    print()
    print("Note: unlike Claude Code, there is no PreToolUse hook equivalent for")
    print(f"{platform.capitalize()} — the AGENTS.md rules are the always-on mechanism.")


def _agents_uninstall(project_dir: Path) -> None:
    """Remove the clawphify section from the local AGENTS.md."""
    target = (project_dir or Path(".")) / "AGENTS.md"

    if not target.exists():
        print("No AGENTS.md found in current directory - nothing to do")
        return

    content = target.read_text(encoding="utf-8")
    if _AGENTS_MD_MARKER not in content:
        print("clawphify section not found in AGENTS.md - nothing to do")
        return

    cleaned = re.sub(
        r"\n*## clawphify\n.*?(?=\n## |\Z)",
        "",
        content,
        flags=re.DOTALL,
    ).rstrip()
    if cleaned:
        target.write_text(cleaned + "\n", encoding="utf-8")
        print(f"clawphify section removed from {target.resolve()}")
    else:
        target.unlink()
        print(f"AGENTS.md was empty after removal - deleted {target.resolve()}")


def claude_install(project_dir: Path | None = None) -> None:
    """Write the clawphify section to the local CLAUDE.md."""
    target = (project_dir or Path(".")) / "CLAUDE.md"

    if target.exists():
        content = target.read_text(encoding="utf-8")
        if _CLAUDE_MD_MARKER in content:
            print("clawphify already configured in CLAUDE.md")
            return
        new_content = content.rstrip() + "\n\n" + _CLAUDE_MD_SECTION
    else:
        new_content = _CLAUDE_MD_SECTION

    target.write_text(new_content, encoding="utf-8")
    print(f"clawphify section written to {target.resolve()}")

    # Also write Claude Code PreToolUse hook to .claude/settings.json
    _install_claude_hook(project_dir or Path("."))

    print()
    print("Claude Code will now check the OpenClaw knowledge graph before answering")
    print("framework questions.")


def _install_claude_hook(project_dir: Path) -> None:
    """Add clawphify PreToolUse hook to .claude/settings.json."""
    settings_path = project_dir / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            settings = {}
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})
    pre_tool = hooks.setdefault("PreToolUse", [])

    # Check if already installed
    if any(h.get("matcher") == "Glob|Grep" and "clawphify" in str(h) for h in pre_tool):
        print(f"  .claude/settings.json  ->  hook already registered (no change)")
        return

    pre_tool.append(_SETTINGS_HOOK)
    settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    print(f"  .claude/settings.json  ->  PreToolUse hook registered")


def _uninstall_claude_hook(project_dir: Path) -> None:
    """Remove clawphify PreToolUse hook from .claude/settings.json."""
    settings_path = project_dir / ".claude" / "settings.json"
    if not settings_path.exists():
        return
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    pre_tool = settings.get("hooks", {}).get("PreToolUse", [])
    filtered = [h for h in pre_tool if not (h.get("matcher") == "Glob|Grep" and "clawphify" in str(h))]
    if len(filtered) == len(pre_tool):
        return
    settings["hooks"]["PreToolUse"] = filtered
    settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    print(f"  .claude/settings.json  ->  PreToolUse hook removed")


def claude_uninstall(project_dir: Path | None = None) -> None:
    """Remove the clawphify section from the local CLAUDE.md."""
    target = (project_dir or Path(".")) / "CLAUDE.md"

    if not target.exists():
        print("No CLAUDE.md found in current directory - nothing to do")
        return

    content = target.read_text(encoding="utf-8")
    if _CLAUDE_MD_MARKER not in content:
        print("clawphify section not found in CLAUDE.md - nothing to do")
        return

    # Remove the ## clawphify section: from the marker to the next ## heading or EOF
    cleaned = re.sub(
        r"\n*## clawphify\n.*?(?=\n## |\Z)",
        "",
        content,
        flags=re.DOTALL,
    ).rstrip()
    if cleaned:
        target.write_text(cleaned + "\n", encoding="utf-8")
        print(f"clawphify section removed from {target.resolve()}")
    else:
        target.unlink()
        print(f"CLAUDE.md was empty after removal - deleted {target.resolve()}")

    _uninstall_claude_hook(project_dir or Path("."))


def _print_framework_info() -> None:
    """Print information about the built-in OpenClaw framework graph."""
    graph = _load_builtin_graph()
    if not graph:
        print("Warning: Built-in OpenClaw graph not found.")
        return
    
    meta = graph.get("metadata", {})
    nodes = graph.get("nodes", {})
    communities = graph.get("communities", {})
    quick_ref = graph.get("quick_reference", {})
    
    print("=" * 60)
    print("OpenClaw Framework Knowledge Graph")
    print("=" * 60)
    print(f"Version: {meta.get('version', 'unknown')}")
    print(f"Nodes: {len(nodes)}")
    print(f"Communities: {len(communities)}")
    print()
    print("Framework Communities:")
    for comm_id, comm in communities.items():
        print(f"  • {comm.get('name', comm_id)}: {comm.get('description', '')}")
    print()
    print("Quick Start:")
    gs = quick_ref.get('getting_started', {})
    for key, cmd in gs.items():
        print(f"  {key}: {cmd}")
    print()
    print("Key Directories:")
    dirs = quick_ref.get('key_directories', {})
    for path, desc in list(dirs.items())[:6]:
        print(f"  {path:<20} - {desc}")
    print()


def main() -> None:
    # Check all known skill install locations for a stale version stamp
    for cfg in _PLATFORM_CONFIG.values():
        skill_dst = Path.home() / cfg["skill_dst"]
        _check_skill_version(skill_dst)

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: clawphify <command>")
        print()
        print("clawphify - OpenClaw framework knowledge graph injector for graphify")
        print()
        print("Commands:")
        print("  info                    show built-in OpenClaw framework information")
        print("  install [--platform P]  copy skill to platform config dir (claude|windows|codex|opencode|claw|droid)")
        print("  query "<question>"       query the OpenClaw framework graph")
        print("    --dfs                   use depth-first instead of breadth-first")
        print("    --budget N              cap output at N tokens (default 2000)")
        print("  init                    initialize clawphify-out/ with built-in OpenClaw graph")
        print("  hook install            install post-commit/post-checkout git hooks")
        print("  hook uninstall          remove git hooks")
        print("  hook status             check if git hooks are installed")
        print("  claude install          write clawphify section to CLAUDE.md + PreToolUse hook")
        print("  claude uninstall        remove clawphify section from CLAUDE.md")
        print("  codex install           write clawphify section to AGENTS.md")
        print("  codex uninstall         remove clawphify section from AGENTS.md")
        print("  opencode install        write clawphify section to AGENTS.md")
        print("  opencode uninstall      remove clawphify section from AGENTS.md")
        print("  claw install            write clawphify section to AGENTS.md")
        print("  claw uninstall          remove clawphify section from AGENTS.md")
        print()
        print("For full graphify features (build custom graphs), use `graphify` directly.")
        print()
        return

    cmd = sys.argv[1]
    if cmd == "info":
        _print_framework_info()
    elif cmd == "init":
        # Copy built-in graph to clawphify-out/
        out_dir = Path("clawphify-out")
        out_dir.mkdir(exist_ok=True)
        builtin = _get_builtin_graph_path()
        target = out_dir / "openclaw_graph.json"
        shutil.copy(builtin, target)
        print(f"Built-in OpenClaw graph copied to {target}")
        print("New Claw projects can now use this pre-built framework knowledge.")
    elif cmd == "install":
        # Default to windows platform on Windows, claude elsewhere
        default_platform = "windows" if platform.system() == "Windows" else "claude"
        chosen_platform = default_platform
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i].startswith("--platform="):
                chosen_platform = args[i].split("=", 1)[1]
                i += 1
            elif args[i] == "--platform" and i + 1 < len(args):
                chosen_platform = args[i + 1]
                i += 2
            else:
                i += 1
        install(platform=chosen_platform)
    elif cmd == "claude":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "install":
            claude_install()
        elif subcmd == "uninstall":
            claude_uninstall()
        else:
            print("Usage: clawphify claude [install|uninstall]", file=sys.stderr)
            sys.exit(1)
    elif cmd in ("codex", "opencode", "claw", "droid"):
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "install":
            _agents_install(Path("."), cmd)
        elif subcmd == "uninstall":
            _agents_uninstall(Path("."))
        else:
            print(f"Usage: clawphify {cmd} [install|uninstall]", file=sys.stderr)
            sys.exit(1)
    elif cmd == "hook":
        from clawphify.hooks import install as hook_install, uninstall as hook_uninstall, status as hook_status
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "install":
            print(hook_install(Path(".")))
        elif subcmd == "uninstall":
            print(hook_uninstall(Path(".")))
        elif subcmd == "status":
            print(hook_status(Path(".")))
        else:
            print("Usage: clawphify hook [install|uninstall|status]", file=sys.stderr)
            sys.exit(1)
    elif cmd == "query":
        if len(sys.argv) < 3:
            print("Usage: clawphify query \"<question>\" [--dfs] [--budget N]", file=sys.stderr)
            sys.exit(1)
        from clawphify.serve import _load_graph, _score_nodes, _bfs, _dfs, _subgraph_to_text
        question = sys.argv[2]
        use_dfs = "--dfs" in sys.argv
        budget = 2000
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--budget" and i + 1 < len(args):
                budget = int(args[i + 1]); i += 2
            elif args[i].startswith("--budget="):
                budget = int(args[i].split("=", 1)[1]); i += 1
            else:
                i += 1
        # Load built-in OpenClaw graph
        graph_path = _get_builtin_graph_path()
        G = _load_graph(str(graph_path))
        terms = [t.lower() for t in question.split() if len(t) > 2]
        scored = _score_nodes(G, terms)
        if not scored:
            print("No matching nodes found.")
            sys.exit(0)
        start = [nid for _, nid in scored[:5]]
        nodes, edges = (_dfs if use_dfs else _bfs)(G, start, depth=2)
        print(_subgraph_to_text(G, nodes, edges, token_budget=budget))
    else:
        print(f"error: unknown command '{cmd}'", file=sys.stderr)
        print("Run 'clawphify --help' for usage.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
