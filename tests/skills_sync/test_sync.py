import os
from pathlib import Path

import pytest

from skills_md.skills_sync.sync import sync_skills


def write_skill(source: Path, name: str, content: bytes) -> None:
    source.mkdir(parents=True, exist_ok=True)
    (source / f"{name}.md").write_bytes(content)


def test_new_skill_is_created(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "grill-me", b"# Grill me\n")

    results = sync_skills(source, target)

    assert (target / "grill-me" / "SKILL.md").read_bytes() == b"# Grill me\n"
    assert [(r.name, r.status) for r in results] == [("grill-me", "created")]


def test_changed_skill_is_overwritten(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "grill-me", b"old\n")
    sync_skills(source, target)
    write_skill(source, "grill-me", b"new\n")

    results = sync_skills(source, target)

    assert (target / "grill-me" / "SKILL.md").read_bytes() == b"new\n"
    assert [(r.name, r.status) for r in results] == [("grill-me", "updated")]


def test_identical_skill_is_left_alone(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "grill-me", b"same\n")
    sync_skills(source, target)
    installed = target / "grill-me" / "SKILL.md"
    os.utime(installed, (0, 0))

    results = sync_skills(source, target)

    assert installed.stat().st_mtime == 0
    assert [(r.name, r.status) for r in results] == [("grill-me", "unchanged")]


def test_content_is_copied_byte_for_byte(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    content = "---\r\nname: café\r\n---\r\n\tno trailing newline ✓".encode()
    write_skill(source, "grill-me", content)

    sync_skills(source, target)

    assert (target / "grill-me" / "SKILL.md").read_bytes() == content


def test_missing_nested_target_is_created(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "a" / "b" / "skills"
    write_skill(source, "grill-me", b"x")

    sync_skills(source, target)

    assert (target / "grill-me" / "SKILL.md").is_file()


def test_other_target_content_is_untouched(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "grill-me", b"x")
    (target / "jira-ticket").mkdir(parents=True)
    (target / "jira-ticket" / "SKILL.md").write_bytes(b"jira")
    (target / "synced" / "nested").mkdir(parents=True)
    (target / "synced" / "nested" / "SKILL.md").write_bytes(b"synced")
    (target / "notes.txt").write_bytes(b"notes")

    sync_skills(source, target)

    assert (target / "jira-ticket" / "SKILL.md").read_bytes() == b"jira"
    assert (target / "synced" / "nested" / "SKILL.md").read_bytes() == b"synced"
    assert (target / "notes.txt").read_bytes() == b"notes"


def test_removed_repo_skill_stays_in_target(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "old-skill", b"old")
    sync_skills(source, target)
    (source / "old-skill.md").unlink()

    results = sync_skills(source, target)

    assert (target / "old-skill" / "SKILL.md").read_bytes() == b"old"
    assert results == []


def test_only_md_files_directly_in_source_are_copied(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "grill-me", b"x")
    (source / "notes.txt").write_bytes(b"txt")
    (source / "nested").mkdir()
    (source / "nested" / "deep.md").write_bytes(b"deep")

    results = sync_skills(source, target)

    assert [r.name for r in results] == ["grill-me"]
    assert sorted(p.name for p in target.iterdir()) == ["grill-me"]


MANUAL_ONLY = (
    b"---\nname: implement\ndisable-model-invocation: true\n---\n# Implement\n"
)
POLICY_FILE = b"policy:\n  allow_implicit_invocation: false\n"


def test_manual_only_skill_gets_codex_policy_file(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "implement", MANUAL_ONLY)

    results = sync_skills(source, target, codex_policy=True)

    skill_dir = target / "implement"
    assert (skill_dir / "SKILL.md").read_bytes() == MANUAL_ONLY
    assert (skill_dir / "agents" / "openai.yaml").read_bytes() == POLICY_FILE
    assert [(r.name, r.status) for r in results] == [("implement", "created")]


@pytest.mark.parametrize(
    ("content", "codex_policy"),
    [
        (MANUAL_ONLY, False),
        (b"---\nname: x\ndisable-model-invocation: false\n---\n", True),
        (b"---\nname: x\n---\n", True),
        (b"# no frontmatter\ndisable-model-invocation: true\n", True),
    ],
    ids=["claude", "key-false", "key-missing", "no-frontmatter"],
)
def test_no_policy_file_unless_codex_and_manual_only(
    tmp_path: Path, content: bytes, codex_policy: bool
) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "implement", content)

    sync_skills(source, target, codex_policy=codex_policy)

    assert sorted(p.name for p in (target / "implement").iterdir()) == ["SKILL.md"]


def test_dropping_manual_only_deletes_policy_file(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "implement", MANUAL_ONLY)
    sync_skills(source, target, codex_policy=True)
    write_skill(source, "implement", b"---\nname: implement\n---\n")

    results = sync_skills(source, target, codex_policy=True)

    assert not (target / "implement" / "agents" / "openai.yaml").exists()
    assert [(r.name, r.status) for r in results] == [("implement", "updated")]


def test_unchanged_skill_with_policy_file_is_unchanged(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "implement", MANUAL_ONLY)
    sync_skills(source, target, codex_policy=True)

    results = sync_skills(source, target, codex_policy=True)

    assert [(r.name, r.status) for r in results] == [("implement", "unchanged")]


def test_hand_edited_policy_file_is_rewritten(tmp_path: Path) -> None:
    source, target = tmp_path / "skills", tmp_path / "target"
    write_skill(source, "implement", MANUAL_ONLY)
    sync_skills(source, target, codex_policy=True)
    policy = target / "implement" / "agents" / "openai.yaml"
    policy.write_bytes(b"policy: {}\n")

    results = sync_skills(source, target, codex_policy=True)

    assert policy.read_bytes() == POLICY_FILE
    assert [(r.name, r.status) for r in results] == [("implement", "updated")]
