from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Status = Literal["created", "updated", "unchanged"]


@dataclass(frozen=True)
class SyncResult:
    name: str
    status: Status


def sync_skills(source: Path, target: Path) -> list[SyncResult]:
    results = []
    for skill_file in sorted(source.glob("*.md")):
        content = skill_file.read_bytes()
        destination = target / skill_file.stem / "SKILL.md"
        status = _status(destination, content)
        if status != "unchanged":
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        results.append(SyncResult(skill_file.stem, status))
    return results


def _status(destination: Path, content: bytes) -> Status:
    if not destination.exists():
        return "created"
    if destination.read_bytes() == content:
        return "unchanged"
    return "updated"
