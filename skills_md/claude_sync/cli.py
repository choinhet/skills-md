import argparse
import os
from collections.abc import Sequence
from pathlib import Path

from skills_md.claude_sync.sync import sync_skills

REPO_SKILLS = Path(__file__).resolve().parents[2] / "skills"


def main(argv: Sequence[str] | None = None, source: Path = REPO_SKILLS) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m skills_md.claude_sync",
        description="Copy every repo skill into the global Claude Code skills folder.",
    )
    parser.add_argument("--target", type=Path)
    target: Path | None = parser.parse_args(argv).target

    for result in sync_skills(source, target or default_target()):
        print(f"{result.status:<9} {result.name}")
    return 0


def default_target() -> Path:
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
    if config_dir:
        return Path(config_dir) / "skills"
    return Path.home() / ".claude" / "skills"
