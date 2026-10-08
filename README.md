# skills-md

My Claude Code skills and plugins.

## Layout

- `skills/` — one Markdown file per skill.
- `plugins/` — Claude Code plugins. See [plugins/README.md](plugins/README.md).
- `skills_md/` — Python code that syncs the skills into Claude Code.

## Sync skills

Copy every skill in `skills/` to `~/.claude/skills/<name>/SKILL.md`
(or `$CLAUDE_CONFIG_DIR/skills/` when set):

```
PS D:\Users\rafael.choinhet\github-projects\skills-md> task sync-skills
task: [sync-skills] uv run python -m skills_md.claude_sync
unchanged grill-me
updated   implement
updated   to-issues
unchanged to-prd
```

Pass `-- --target <dir>` to sync somewhere else.

## Dev

```sh
task test    # pytest
task check   # ruff + ty
```
