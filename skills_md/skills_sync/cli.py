import argparse
import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from skills_md.skills_sync.sync import sync_skills

REPO_SKILLS = Path(__file__).resolve().parents[2] / "skills"


@dataclass(frozen=True)
class Tool:
    name: str
    env_var: str
    default_home: str
    codex_policy: bool

    def home(self) -> Path | None:
        """The tool's home folder, or None when the tool is not installed."""
        configured = os.environ.get(self.env_var)
        if configured:
            return Path(configured)
        default = Path.home() / self.default_home
        return default if default.is_dir() else None


TOOLS = [
    Tool("claude", "CLAUDE_CONFIG_DIR", ".claude", codex_policy=False),
    Tool("codex", "CODEX_HOME", ".codex", codex_policy=True),
]


def main(argv: Sequence[str] | None = None, source: Path = REPO_SKILLS) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m skills_md.skills_sync",
        description="Copy every repo skill into each installed tool's skills folder.",
    )
    parser.parse_args(argv)

    synced = 0
    for tool in TOOLS:
        home = tool.home()
        if home is None:
            print(
                f"{tool.name:<6} skipped   (set {tool.env_var} or create ~/{tool.default_home})"
            )
            continue
        for result in sync_skills(source, home / "skills", tool.codex_policy):
            print(f"{tool.name:<6} {result.status:<9} {result.name}")
        synced += 1

    if not synced:
        names = " or ".join(tool.env_var for tool in TOOLS)
        print(f"No tool found. Set {names}.", file=sys.stderr)
        return 1
    return 0
