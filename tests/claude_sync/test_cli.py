from pathlib import Path

import pytest

from skills_md.claude_sync.cli import main

SKILLS = ["grill-me", "to-prd"]


@pytest.fixture
def source(tmp_path: Path) -> Path:
    source = tmp_path / "skills"
    source.mkdir()
    for name in SKILLS:
        (source / f"{name}.md").write_bytes(f"# {name}\n".encode())
    return source


@pytest.fixture(autouse=True)
def isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    return home


def installed_skills(target: Path) -> list[str]:
    return sorted(p.name for p in target.iterdir())


def test_target_flag_receives_skills_and_prints_one_line_each(
    tmp_path: Path, source: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    target = tmp_path / "target"

    exit_code = main(["--target", str(target)], source)

    assert exit_code == 0
    assert installed_skills(target) == SKILLS
    lines = capsys.readouterr().out.splitlines()
    assert [line.split() for line in lines] == [["created", name] for name in SKILLS]


def test_target_flag_wins_over_claude_config_dir(
    tmp_path: Path, source: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_dir, target = tmp_path / "config", tmp_path / "target"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config_dir))

    main(["--target", str(target)], source)

    assert installed_skills(target) == SKILLS
    assert not config_dir.exists()


def test_claude_config_dir_wins_over_home(
    tmp_path: Path,
    source: Path,
    monkeypatch: pytest.MonkeyPatch,
    isolated_home: Path,
) -> None:
    config_dir = tmp_path / "config"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config_dir))

    main([], source)

    assert installed_skills(config_dir / "skills") == SKILLS
    assert not isolated_home.exists()


def test_home_claude_skills_is_the_default(source: Path, isolated_home: Path) -> None:
    main([], source)

    assert installed_skills(isolated_home / ".claude" / "skills") == SKILLS
