# Plugins

Claude Code plugins (mods). Each one lives in its own folder.

## context-band

A one-line band above the prompt:

```
claude-opus-5-5 | 84.2k / 200k | ████░░░░░░ 42%
```

It shows the model, context tokens used / total, and a bar.
The bar is green under 50%, yellow from 50%, and red from 80%.

### Setup

1. Clone this repo:

   ```sh
   git clone git@github.com:choinhet/skills-md.git
   ```

2. Add the plugin folder to `env` in `~/.claude/settings.json`:

   ```json
   {
     "env": {
       "CLAUDE_CODE_PLUGIN_DIRS": "<repo path>/plugins/context-band"
     }
   }
   ```

   Use forward slashes on Windows, e.g. `D:/code/skills-md/plugins/context-band`.
   To load more than one plugin folder, separate paths with `;` on Windows or `:` elsewhere.

3. Restart Claude Code. The band appears above the prompt.

To try it once without editing settings:

```sh
claude --plugin-dir <repo path>/plugins/context-band
```

### Check it

```sh
claude plugin validate plugins/context-band
claude plugin test plugins/context-band
```

On first load, Claude Code writes `.claude-plugin/types/`. That folder is git-ignored.
