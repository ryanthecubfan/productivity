# Claude Code Pane Manager

Automatically tiles iTerm2 panes for active Claude Code sessions. A background daemon watches for session changes and fires a macOS dialog asking you to approve any layout change — nothing ever happens without your confirmation.

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

Clone or copy this folder somewhere permanent (e.g. `~/scripts/claude-panes/`).

## Configuration

Copy the default config to your home directory and edit it to match your iTerm2 profile names:

```bash
cp claude-panes.json ~/.claude-panes.json
```

Open `~/.claude-panes.json` and replace the profile names (`"Ocean"`, `"Tango Dark"`, etc.) with the exact names of profiles you have in **iTerm2 → Preferences → Profiles**. The `"fallback_profile"` is used for any slot whose name doesn't match an existing profile.

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

`window.columns` and `window.rows` control the size of new iTerm2 windows created by the manager; they have no effect on existing windows.

## Start the daemon

```bash
python3 daemon.py &
```

The daemon polls every 5 seconds. Logs are written to `~/.claude-panes.log`.

## Stop the daemon

```bash
pkill -f daemon.py
```

## How it works

1. `daemon.py` runs in the background and watches for new or ended Claude Code sessions (using `claude session list --json`, falling back to `pgrep` + `lsof`).
2. When the session count changes, a macOS dialog pops up:
   - **New session:** "New Claude session detected (N total). Re-tile?"
   - **Ended session:** "Claude session ended (N total). Collapse layout?"
3. If you click **Yes**, `pane_manager.py` is invoked via the iTerm2 Python API to add, resize, or remove panes.
4. If you click **No** (or dismiss the dialog), nothing changes.

You can always resize panes manually — the manager never resets sizes you've set by hand, and only acts when you explicitly approve a notification.

## Layouts

| Sessions | Layout |
|----------|--------|
| 1 | Single full pane |
| 2 | Two columns side by side |
| 3 | Three columns |
| 4 | 2×2 grid |
| 5 | 3 panes top row, 2 panes bottom row |
| 6 | 3×2 full grid |

Transitions are **additive** where possible — existing panes are never closed or reopened unless going from 5 to 6 sessions (which requires a full reflow of the top row).

## Customizing colors

Edit `~/.claude-panes.json` and change the profile names. Changes take effect the next time a pane is created (existing panes keep their current color).

## Troubleshooting

- **"Enable Python API" not visible in iTerm2:** Update to iTerm2 3.3 or later.
- **`iterm2` module not found:** Run `pip3 install iterm2` and make sure you're using the same Python that runs the scripts.
- **Dialogs don't appear:** Make sure you're running macOS 10.14+ and that your terminal/shell has Accessibility or Automation permissions in **System Preferences → Privacy & Security**.
- **Profiles not found:** Profile names in `~/.claude-panes.json` must match exactly (case-sensitive) the names in iTerm2 Preferences → Profiles.
- **Check the log:** `tail -f ~/.claude-panes.log`
