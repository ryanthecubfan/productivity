# clode — Claude Code Pane Manager

Type `clode` in iTerm2 to tile all your active Claude Code sessions into panes and start a background watcher that notifies you when sessions change.

## Prerequisites

- macOS
- [iTerm2](https://iterm2.com) with the Python API enabled:
  **Preferences → General → Magic → Enable Python API**
- [Claude Code](https://claude.ai/code) installed and on your `PATH`
- Python 3.8+

## Install

```bash
pip3 install iterm2
```

Clone or copy this folder somewhere permanent, then put it on your `PATH`:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$PATH:$HOME/path/to/clode-folder"
```

Copy the default config and edit it to match your iTerm2 profile names:

```bash
cp claude-panes.json ~/.claude-panes.json
```

Open `~/.claude-panes.json` and replace each profile name (`"Ocean"`, `"Tango Dark"`, etc.) with the exact name of a profile in **iTerm2 → Preferences → Profiles**. The `"fallback_profile"` is used for any slot whose name doesn't match.

```json
{
  "pane_profiles": {
    "1": "Ocean",
    "2": "Tango Dark",
    "3": "Solarized Dark",
    "4": "Tomorrow Night",
    "5": "Dracula",
    "6": "Nord"
  },
  "fallback_profile": "Default",
  "window": {
    "columns": 220,
    "rows": 50
  }
}
```

## Usage

```
clode            Tile current sessions + start background watcher
clode status     Show active sessions without changing anything
clode tile       Tile only (don't start/restart the watcher)
clode stop       Stop the background watcher
```

## How it works

**`clode`** — what you type. It finds your active Claude Code sessions, tiles them into iTerm2 panes immediately, and starts `clode_daemon.py` in the background if it isn't already running.

**`clode_daemon.py`** — the background watcher. It polls every 5 seconds. When the session count changes it fires a macOS dialog:

- New session detected → "New Claude session detected (N total). Re-tile?"
- Session ended → "Claude session ended (N total). Collapse layout?"

Click **Yes** and the panes are updated. Click **No** and nothing happens. You can also resize panes freely — the manager never resets sizes you've set by hand.

Logs are written to `~/.claude-panes.log`.

## Layouts

| Sessions | Layout |
|----------|--------|
| 1 | Single full pane |
| 2 | Two columns side by side |
| 3 | Three columns |
| 4 | 2×2 grid |
| 5 | 3 panes top row, 2 panes bottom row |
| 6 | 3×2 full grid |

Transitions are additive where possible — existing panes are never closed or reopened. The one exception is 5→6 sessions, which requires a full reflow of the top row.

## Customizing colors

Edit `~/.claude-panes.json` and change the profile names. Changes take effect on the next pane creation; existing panes keep their current colors.

## Troubleshooting

- **"Enable Python API" not visible in iTerm2:** Update to iTerm2 3.3 or later.
- **`iterm2` module not found:** Run `pip3 install iterm2`.
- **`clode` not found:** Make sure the script directory is on your `PATH`.
- **Profiles not found:** Names in `~/.claude-panes.json` must match exactly (case-sensitive) the names in iTerm2 Preferences → Profiles.
- **Check the log:** `tail -f ~/.claude-panes.log`
