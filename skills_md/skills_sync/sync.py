from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Status = Literal["created", "updated", "unchanged"]

CODEX_POLICY = b"policy:\n  allow_implicit_invocation: false\n"


@dataclass(frozen=True)
class SyncResult:
    name: str
    status: Status


def sync_skills(
    source: Path, target: Path, codex_policy: bool = False
) -> list[SyncResult]:
    results = []
    for skill_file in sorted(source.glob("*.md")):
        content = skill_file.read_bytes()
        skill_dir = target / skill_file.stem
        # None means the file must not exist.
        files: dict[Path, bytes | None] = {skill_dir / "SKILL.md": content}
        if codex_policy:
            files[skill_dir / "agents" / "openai.yaml"] = (
                CODEX_POLICY if _is_manual_only(content) else None
            )
        status = _status(skill_dir, files)
        for path, data in files.items():
            if not _matches(path, data):
                _write(path, data)
        results.append(SyncResult(skill_file.stem, status))
    return results


def _status(skill_dir: Path, files: dict[Path, bytes | None]) -> Status:
    if not (skill_dir / "SKILL.md").exists():
        return "created"
    if all(_matches(path, data) for path, data in files.items()):
        return "unchanged"
    return "updated"


def _matches(path: Path, data: bytes | None) -> bool:
    if data is None:
        return not path.exists()
    return path.is_file() and path.read_bytes() == data


def _write(path: Path, data: bytes | None) -> None:
    if data is None:
        path.unlink()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _is_manual_only(content: bytes) -> bool:
    lines = content.decode(errors="replace").splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        if line.strip() == "---":
            return False
        key, _, value = line.partition(":")
        if key.strip() == "disable-model-invocation":
            return value.strip() == "true"
    return False
