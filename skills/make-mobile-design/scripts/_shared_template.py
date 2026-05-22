"""Shared helpers for the make-mobile-design scaffold scripts.

Strategy: each user project keeps its own copy of the shared chrome/JS
assets in a gitignored `.design/` folder at the project root. Scaffold
scripts call `asset_link()` / `asset_script()` which:

1. Walk up from the output file to find the project root (a directory
   containing `.git/`), falling back to the output file's parent.
2. Ensure `<project_root>/.design/` exists, append `.design/` to the
   root `.gitignore` if a git repo was found, and copy the requested
   asset from the plugin install into `.design/` if missing.
3. Emit a relative href from the output file to its `.design/` copy.

When the output file lives INSIDE this plugin's own tree (the showcase
under `examples/`), the helper skips `.design/` entirely and references
the canonical assets under `skills/make-mobile-design/assets/` via a
repo-relative path — no point duplicating the source.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path


def plugin_root() -> Path:
    """Locate the plugin root directory.

    1. Honor $CLAUDE_PLUGIN_ROOT if set (Claude Code sets this when running
       a plugin's scripts).
    2. Walk up from this file looking for `.claude-plugin/plugin.json`.
    3. Raise if neither resolves — refuse to silently emit a broken URL.
    """
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env:
        return Path(env).expanduser().resolve()

    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        if (parent / ".claude-plugin" / "plugin.json").is_file():
            return parent

    raise RuntimeError(
        "Could not locate the plugin root. Set $CLAUDE_PLUGIN_ROOT or run "
        "this script from inside the mobile-design-kit checkout."
    )


def _find_project_root(output_path: Path) -> Path:
    """Walk up from `output_path` looking for a project root.

    Markers, checked in order at each ancestor (closest wins):
    1. An existing `.design/` directory — if the user already has one,
       use it (don't create a competing one further up).
    2. A `package.json` — a self-contained sub-project (e.g. the
       plugin's own `examples/`, or a frontend workspace inside a
       monorepo).
    3. A `.git/` directory — the outer repo root.

    Falls back to the output file's parent dir if none of those exist.
    """
    out_dir = output_path.resolve().parent
    for candidate in (out_dir, *out_dir.parents):
        if (candidate / ".design").is_dir():
            return candidate
        if (candidate / "package.json").is_file():
            return candidate
        if (candidate / ".git").exists():
            return candidate
    return out_dir


def _ensure_gitignored(project_root: Path, entry: str) -> None:
    """Append `entry` to `<project_root>/.gitignore` if absent.

    No-op when the project root has no `.git/` directory (the user is
    not in a git repo, so there's nothing to ignore from).
    """
    if not (project_root / ".git").exists():
        return
    gitignore = project_root / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    lines = {line.strip() for line in existing.splitlines()}
    if entry in lines or entry.rstrip("/") in lines:
        return
    sep = "" if not existing or existing.endswith("\n") else "\n"
    with gitignore.open("a", encoding="utf-8") as f:
        f.write(f"{sep}{entry}\n")


def ensure_design_asset(output_path: Path, asset_name: str) -> Path:
    """Make sure `<project_root>/.design/<asset_name>` exists; return its path.

    Creates `.design/` on first use, registers it in `.gitignore` when in
    a git project, and copies the asset from the plugin install if the
    local copy is missing. Existing copies are NOT overwritten — once
    a project has its own `.design/` snapshot it stays put until the
    user deletes it (intentional: a plugin update shouldn't silently
    change every mockup the user has rendered against the old chrome).
    """
    project_root = _find_project_root(output_path)
    design_dir = project_root / ".design"
    design_dir.mkdir(exist_ok=True)
    _ensure_gitignored(project_root, ".design/")

    target = design_dir / asset_name
    if not target.exists():
        source = (
            plugin_root() / "skills" / "make-mobile-design" / "assets" / asset_name
        ).resolve()
        if not source.is_file():
            raise FileNotFoundError(
                f"Plugin asset missing: {source}. Reinstall the "
                "mobile-design-kit plugin or restore the assets/ directory."
            )
        shutil.copy2(source, target)
    return target


def asset_href(asset_name: str, output_path: Path) -> str:
    """Return the href for a shared asset, as a path relative to the output.

    Materializes `<project_root>/.design/<asset_name>` and emits a path
    relative to the output file. `_find_project_root` decides where
    `.design/` lives (closest `.design/` > `package.json` > `.git/` >
    output's parent dir).
    """
    out_dir = output_path.resolve().parent
    asset_path = ensure_design_asset(output_path, asset_name)
    return os.path.relpath(asset_path, out_dir)


def asset_link(asset_name: str, output_path: Path) -> str:
    """Return a <link rel="stylesheet"> tag for the named CSS asset."""
    return f'<link rel="stylesheet" href="{asset_href(asset_name, output_path)}">'


def asset_script(asset_name: str, output_path: Path) -> str:
    """Return a <script src="..."> tag for the named JS asset."""
    return f'<script src="{asset_href(asset_name, output_path)}"></script>'
