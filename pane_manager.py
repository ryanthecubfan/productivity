#!/usr/bin/env python3
"""
Claude Code pane manager — receives commands from daemon.py and arranges
iTerm2 panes accordingly using the iTerm2 Python API.

Usage (called by daemon.py, not directly):
    python3 pane_manager.py tile    '<sessions-json>'
    python3 pane_manager.py collapse '<sessions-json>'
"""

import json
import logging
import os
import sys

import iterm2

LOG_FILE = os.path.expanduser("~/.claude-panes.log")
CONFIG_PATHS = [
    os.path.expanduser("~/.claude-panes.json"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "claude-panes.json"),
]

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def load_config():
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    return {
        "pane_profiles": {},
        "fallback_profile": "Default",
        "window": {"columns": 220, "rows": 50},
    }


def build_session_command(session):
    """
    Return the shell command string to connect to a Claude session.
    Prefers `claude --resume <id>` for real session IDs; falls back to
    `cd <cwd> && claude` for pid-based fallback entries.
    """
    if session.get("_fallback"):
        cwd = session.get("cwd", "")
        if cwd:
            return f"cd {json.dumps(cwd)} && claude"
        return "claude"
    sid = session.get("id", "")
    if sid:
        return f"claude --resume {sid}"
    return "claude"


async def set_pane_profile(session_obj, slot_index, config):
    """Apply the color profile for slot_index (1-based) to session_obj."""
    profiles = config.get("pane_profiles", {})
    profile_name = profiles.get(str(slot_index), config.get("fallback_profile", "Default"))
    try:
        profiles_list = await iterm2.Profile.async_get(
            connection=session_obj.connection, guids=None
        )
        target = next((p for p in profiles_list if p.name == profile_name), None)
        if target is None:
            logging.warning("Profile %r not found; skipping color assignment", profile_name)
            return
        await session_obj.async_set_profile(target)
        logging.info("Set profile %r on slot %d", profile_name, slot_index)
    except Exception as exc:
        logging.warning("Could not set profile on slot %d: %s", slot_index, exc)


async def send_command(session_obj, command):
    """Send a shell command + Enter to an iTerm2 session."""
    await session_obj.async_send_text(command + "\n")


# ---------------------------------------------------------------------------
# Layout builders
# ---------------------------------------------------------------------------

async def layout_1(window, sessions, config, existing_sessions):
    """Single pane."""
    tab = await _ensure_tab(window)
    panes = tab.sessions
    if len(panes) >= 1:
        s = panes[0]
        if s not in existing_sessions:
            await set_pane_profile(s, 1, config)
            await send_command(s, build_session_command(sessions[0]))
        return
    # Tab is empty (shouldn't happen but guard anyway)
    s = tab.current_session
    await set_pane_profile(s, 1, config)
    await send_command(s, build_session_command(sessions[0]))


async def layout_2(window, sessions, config, existing_sessions):
    """Two panes side by side (vertical split)."""
    tab = await _ensure_tab(window)
    panes = tab.sessions
    # Ensure we have at least 1 pane to start from
    if len(panes) < 1:
        return
    s1 = panes[0]
    if s1 not in existing_sessions:
        await set_pane_profile(s1, 1, config)
        await send_command(s1, build_session_command(sessions[0]))
    if len(panes) < 2:
        s2 = await s1.async_split_pane(vertical=True)
        await set_pane_profile(s2, 2, config)
        await send_command(s2, build_session_command(sessions[1]))
    else:
        s2 = panes[1]
        if s2 not in existing_sessions:
            await set_pane_profile(s2, 2, config)
            await send_command(s2, build_session_command(sessions[1]))


async def layout_3(window, sessions, config, existing_sessions):
    """Three columns."""
    tab = await _ensure_tab(window)
    panes = tab.sessions
    s1 = panes[0] if len(panes) > 0 else tab.current_session
    if s1 not in existing_sessions:
        await set_pane_profile(s1, 1, config)
        await send_command(s1, build_session_command(sessions[0]))
    if len(panes) < 2:
        s2 = await s1.async_split_pane(vertical=True)
        await set_pane_profile(s2, 2, config)
        await send_command(s2, build_session_command(sessions[1]))
    else:
        s2 = panes[1]
        if s2 not in existing_sessions:
            await set_pane_profile(s2, 2, config)
            await send_command(s2, build_session_command(sessions[1]))
    if len(panes) < 3:
        s3 = await s2.async_split_pane(vertical=True)
        await set_pane_profile(s3, 3, config)
        await send_command(s3, build_session_command(sessions[2]))
    else:
        s3 = panes[2]
        if s3 not in existing_sessions:
            await set_pane_profile(s3, 3, config)
            await send_command(s3, build_session_command(sessions[2]))


async def layout_4(window, sessions, config, existing_sessions):
    """2x2 grid."""
    tab = await _ensure_tab(window)
    panes = tab.sessions
    # Row 1
    s1 = panes[0] if len(panes) > 0 else tab.current_session
    if s1 not in existing_sessions:
        await set_pane_profile(s1, 1, config)
        await send_command(s1, build_session_command(sessions[0]))
    if len(panes) < 2:
        s2 = await s1.async_split_pane(vertical=True)
        await set_pane_profile(s2, 2, config)
        await send_command(s2, build_session_command(sessions[1]))
    else:
        s2 = panes[1]
        if s2 not in existing_sessions:
            await set_pane_profile(s2, 2, config)
            await send_command(s2, build_session_command(sessions[1]))
    # Row 2
    if len(panes) < 3:
        s3 = await s1.async_split_pane(vertical=False)
        await set_pane_profile(s3, 3, config)
        await send_command(s3, build_session_command(sessions[2]))
    else:
        s3 = panes[2]
        if s3 not in existing_sessions:
            await set_pane_profile(s3, 3, config)
            await send_command(s3, build_session_command(sessions[2]))
    if len(panes) < 4:
        s4 = await s2.async_split_pane(vertical=False)
        await set_pane_profile(s4, 4, config)
        await send_command(s4, build_session_command(sessions[3]))
    else:
        s4 = panes[3]
        if s4 not in existing_sessions:
            await set_pane_profile(s4, 4, config)
            await send_command(s4, build_session_command(sessions[3]))


async def layout_5(window, sessions, config, existing_sessions):
    """
    3 panes top row, 2 panes bottom row.
    Bottom panes: half width each. Top panes: third width each.
    Built as: full rebuild of tab if coming from 4-pane (different row structure).
    """
    tab = await _ensure_tab(window)
    panes = tab.sessions
    # Top row: 3 columns
    s1 = panes[0] if len(panes) > 0 else tab.current_session
    if s1 not in existing_sessions:
        await set_pane_profile(s1, 1, config)
        await send_command(s1, build_session_command(sessions[0]))
    if len(panes) < 2:
        s2 = await s1.async_split_pane(vertical=True)
        await set_pane_profile(s2, 2, config)
        await send_command(s2, build_session_command(sessions[1]))
    else:
        s2 = panes[1]
        if s2 not in existing_sessions:
            await set_pane_profile(s2, 2, config)
            await send_command(s2, build_session_command(sessions[1]))
    if len(panes) < 3:
        s3 = await s2.async_split_pane(vertical=True)
        await set_pane_profile(s3, 3, config)
        await send_command(s3, build_session_command(sessions[2]))
    else:
        s3 = panes[2]
        if s3 not in existing_sessions:
            await set_pane_profile(s3, 3, config)
            await send_command(s3, build_session_command(sessions[2]))
    # Bottom row: 2 panes under s1 and s3 respectively
    if len(panes) < 4:
        s4 = await s1.async_split_pane(vertical=False)
        await set_pane_profile(s4, 4, config)
        await send_command(s4, build_session_command(sessions[3]))
    else:
        s4 = panes[3]
        if s4 not in existing_sessions:
            await set_pane_profile(s4, 4, config)
            await send_command(s4, build_session_command(sessions[3]))
    if len(panes) < 5:
        s5 = await s3.async_split_pane(vertical=False)
        await set_pane_profile(s5, 5, config)
        await send_command(s5, build_session_command(sessions[4]))
    else:
        s5 = panes[4]
        if s5 not in existing_sessions:
            await set_pane_profile(s5, 5, config)
            await send_command(s5, build_session_command(sessions[4]))


async def layout_6(window, sessions, config, existing_sessions):
    """
    3x2 full grid. This is a full rebuild because 5→6 reflows the top row
    from 2-wide bottom panes to 3 evenly-spaced columns.
    """
    tab = await _ensure_tab(window)
    # Close extra panes first (full rebuild)
    for s in list(tab.sessions):
        try:
            await s.async_close(force=True)
        except Exception:
            pass
    # Open fresh tab
    tab = await window.async_create_tab()
    s1 = tab.current_session
    await set_pane_profile(s1, 1, config)
    await send_command(s1, build_session_command(sessions[0]))
    s2 = await s1.async_split_pane(vertical=True)
    await set_pane_profile(s2, 2, config)
    await send_command(s2, build_session_command(sessions[1]))
    s3 = await s2.async_split_pane(vertical=True)
    await set_pane_profile(s3, 3, config)
    await send_command(s3, build_session_command(sessions[2]))
    s4 = await s1.async_split_pane(vertical=False)
    await set_pane_profile(s4, 4, config)
    await send_command(s4, build_session_command(sessions[3]))
    s5 = await s2.async_split_pane(vertical=False)
    await set_pane_profile(s5, 5, config)
    await send_command(s5, build_session_command(sessions[4]))
    s6 = await s3.async_split_pane(vertical=False)
    await set_pane_profile(s6, 6, config)
    await send_command(s6, build_session_command(sessions[5]))


LAYOUT_FNS = {
    1: layout_1,
    2: layout_2,
    3: layout_3,
    4: layout_4,
    5: layout_5,
    6: layout_6,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _ensure_tab(window):
    """Return the first tab of window, creating one if needed."""
    tabs = window.tabs
    if tabs:
        return tabs[0]
    return await window.async_create_tab()


async def _get_or_create_window(app, config):
    """Return the frontmost window or create a new one at the configured size."""
    windows = app.windows
    if windows:
        return windows[0]
    cols = config.get("window", {}).get("columns", 220)
    rows = config.get("window", {}).get("rows", 50)
    return await iterm2.Window.async_create(app, columns=cols, rows=rows)


# ---------------------------------------------------------------------------
# Main entry points
# ---------------------------------------------------------------------------

async def cmd_tile(connection, sessions, config):
    app = await iterm2.async_get_app(connection)
    window = await _get_or_create_window(app, config)
    n = min(len(sessions), 6)
    if n == 0:
        logging.info("tile: no sessions, nothing to do")
        return
    existing_sessions = set(window.tabs[0].sessions) if window.tabs else set()
    fn = LAYOUT_FNS.get(n)
    if fn:
        logging.info("tile: applying layout for %d sessions", n)
        await fn(window, sessions[:n], config, existing_sessions)
    else:
        logging.warning("tile: no layout defined for %d sessions", n)


async def cmd_collapse(connection, sessions, config):
    """
    Remove panes for sessions that are no longer running.
    We identify 'dead' panes heuristically: any pane beyond the current
    session count is a candidate for closing.
    """
    app = await iterm2.async_get_app(connection)
    windows = app.windows
    if not windows:
        logging.info("collapse: no windows open")
        return
    window = windows[0]
    n_target = min(len(sessions), 6)
    tab = window.tabs[0] if window.tabs else None
    if tab is None:
        return
    current_panes = tab.sessions
    n_current = len(current_panes)
    to_remove = n_current - n_target
    if to_remove <= 0:
        logging.info("collapse: nothing to remove")
        return
    logging.info("collapse: closing %d pane(s)", to_remove)
    # Close panes from the end (most recently added)
    for s in list(reversed(current_panes))[:to_remove]:
        try:
            await s.async_close(force=True)
        except Exception as exc:
            logging.warning("Could not close pane: %s", exc)
    # Re-tile remaining sessions if any
    if sessions and n_target > 0:
        fn = LAYOUT_FNS.get(n_target)
        if fn:
            remaining_existing = set(tab.sessions)
            await fn(window, sessions[:n_target], config, remaining_existing)


async def main(connection):
    command = sys.argv[1] if len(sys.argv) > 1 else "tile"
    sessions_raw = sys.argv[2] if len(sys.argv) > 2 else "[]"
    try:
        sessions = json.loads(sessions_raw)
    except json.JSONDecodeError:
        logging.error("Invalid sessions JSON: %r", sessions_raw)
        sessions = []

    config = load_config()
    logging.info("pane_manager: command=%s sessions=%d", command, len(sessions))

    if command == "tile":
        await cmd_tile(connection, sessions, config)
    elif command == "collapse":
        await cmd_collapse(connection, sessions, config)
    else:
        logging.error("Unknown command: %r", command)


if __name__ == "__main__":
    iterm2.run_until_complete(main)
