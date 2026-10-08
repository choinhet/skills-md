# skills-md

My agent skills and plugins.

## Layout

- `skills/` — one Markdown file per skill.
- `plugins/` — Claude Code plugins. See [plugins/README.md](plugins/README.md).
- `skills_md/` — Python code that syncs the skills into each installed tool.

## Sync skills

Copy every skill in `skills/` to `<target>/<name>/SKILL.md` for each installed
tool:

| Tool   | Synced when                                    | Target                                               |
| ------ | ---------------------------------------------- | ---------------------------------------------------- |
| Claude | `CLAUDE_CONFIG_DIR` set, or `~/.claude` exists | `$CLAUDE_CONFIG_DIR/skills`, else `~/.claude/skills` |
| Codex  | `CODEX_HOME` set, or `~/.codex` exists         | `$CODEX_HOME/skills`, else `~/.codex/skills`         |

```
PS D:\Users\rafael.choinhet\github-projects\skills-md> task sync-skills
task: [sync-skills] uv run python -m skills_md.skills_sync
claude unchanged grill-me
claude updated   implement
codex  created   grill-me
codex  created   implement
```

A skill with `disable-model-invocation: true` also gets
`agents/openai.yaml` in the Codex copy, so Codex never starts it on its own.
The sync exits with an error when no tool is found.

## Dev

```sh
task test    # pytest
task check   # ruff + ty
```
