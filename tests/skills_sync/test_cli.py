from pathlib import Path

import pytest

from skills_md.skills_sync.cli import main

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
    monkeypatch.delenv("CODEX_HOME", raising=False)
    return home


def installed_skills(target: Path) -> list[str]:
    return sorted(p.name for p in target.iterdir())


def test_both_tools_present_receive_every_skill(
    source: Path, isolated_home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (isolated_home / ".claude").mkdir(parents=True)
    (isolated_home / ".codex").mkdir()

    exit_code = main([], source)

    assert exit_code == 0
    assert installed_skills(isolated_home / ".claude" / "skills") == SKILLS
    assert installed_skills(isolated_home / ".codex" / "skills") == SKILLS
    lines = capsys.readouterr().out.splitlines()
    assert [line.split() for line in lines] == [
        [tool, "created", name] for tool in ["claude", "codex"] for name in SKILLS
    ]


def test_missing_tool_is_skipped_with_a_message(
    source: Path, isolated_home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (isolated_home / ".codex").mkdir(parents=True)

    exit_code = main([], source)

    assert exit_code == 0
    assert not (isolated_home / ".claude").exists()
    assert installed_skills(isolated_home / ".codex" / "skills") == SKILLS
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].split()[:2] == ["claude", "skipped"]
    assert [line.split() for line in lines[1:]] == [
        ["codex", "created", name] for name in SKILLS
    ]


def test_no_tool_found_is_an_error(
    source: Path, isolated_home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main([], source)

    assert exit_code != 0
    assert "No tool found" in capsys.readouterr().err
    assert not isolated_home.exists()


def test_env_var_to_missing_folder_is_created_and_synced(
    tmp_path: Path, source: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    codex_home = tmp_path / "missing" / "codex"
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    exit_code = main([], source)

    assert exit_code == 0
    assert installed_skills(codex_home / "skills") == SKILLS


def test_env_vars_win_over_default_folders(
    tmp_path: Path,
    source: Path,
    monkeypatch: pytest.MonkeyPatch,
    isolated_home: Path,
) -> None:
    (isolated_home / ".claude").mkdir(parents=True)
    (isolated_home / ".codex").mkdir()
    config_dir, codex_home = tmp_path / "config", tmp_path / "codex"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config_dir))
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    main([], source)

    assert installed_skills(config_dir / "skills") == SKILLS
    assert installed_skills(codex_home / "skills") == SKILLS
    assert installed_skills(isolated_home / ".claude") == []
    assert installed_skills(isolated_home / ".codex") == []


def test_manual_only_skill_gets_policy_file_in_codex_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "skills"
    source.mkdir()
    content = b"---\nname: implement\ndisable-model-invocation: true\n---\n"
    (source / "implement.md").write_bytes(content)
    config_dir, codex_home = tmp_path / "config", tmp_path / "codex"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config_dir))
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    main([], source)

    claude_skill = config_dir / "skills" / "implement"
    codex_skill = codex_home / "skills" / "implement"
    assert (claude_skill / "SKILL.md").read_bytes() == content
    assert (codex_skill / "SKILL.md").read_bytes() == content
    assert not (claude_skill / "agents").exists()
    assert (codex_skill / "agents" / "openai.yaml").is_file()


def test_target_flag_is_rejected(source: Path) -> None:
    with pytest.raises(SystemExit):
        main(["--target", "x"], source)


def test_second_run_reports_unchanged_for_every_tool(
    source: Path, isolated_home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (isolated_home / ".claude").mkdir(parents=True)
    (isolated_home / ".codex").mkdir()
    main([], source)
    capsys.readouterr()

    main([], source)

    lines = capsys.readouterr().out.splitlines()
    assert [line.split()[1] for line in lines] == ["unchanged"] * 4
