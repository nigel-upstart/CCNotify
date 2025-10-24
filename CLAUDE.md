# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CCNotify is a macOS-only desktop notification system for Claude Code that alerts users when Claude needs input or completes tasks. It integrates with Claude Code through hooks (UserPromptSubmit, Stop, Notification) and uses `terminal-notifier` for macOS notifications.

**Key characteristics:**
- Single-file Python script (`ccnotify.py`) with no external dependencies beyond standard library + `terminal-notifier`
- SQLite database (`ccnotify.db`) for session tracking
- Designed to be installed in `~/.claude/ccnotify/` and configured via `~/.claude/settings.json`

## Architecture

### Core Components

**ClaudePromptTracker** (ccnotify.py:17-298)
- Main class that handles all hook events
- Manages SQLite database operations
- Sends notifications via `terminal-notifier` subprocess calls
- Key methods:
  - `handle_user_prompt_submit()` - Records new prompts with session tracking
  - `handle_stop()` - Updates completion time and calculates duration
  - `handle_notification()` - Detects notification types and updates database
  - `send_notification()` - Sends macOS notifications with clickable actions

**Database Schema** (ccnotify.py:56-82)
```sql
CREATE TABLE prompt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    prompt TEXT,
    cwd TEXT,
    seq INTEGER,          -- Auto-increments per session via trigger
    stoped_at DATETIME,
    lastWaitUserAt DATETIME
)
```

The `seq` field auto-increments per `session_id` using a trigger (ccnotify.py:69-81), allowing Claude to track "job #1, job #2" within each session.

**Notification Types** (ccnotify.py:163-184)
- **Waiting for input**: Detected by "waiting for your input" or "waiting for input" in message
- **Permission required**: Detected by "permission" in message
- **Action required**: Detected by "approval" or "choose an option" in message
- **Generic**: All other notifications

### Event Flow

1. **UserPromptSubmit**: User submits prompt → Record in DB with timestamp and cwd
2. **Notification**: Claude sends notification → Update `lastWaitUserAt` if waiting for input
3. **Stop**: Claude completes → Update `stoped_at`, calculate duration, send completion notification

## Common Commands

### Running the script

```bash
# Test that ccnotify is working (should print "ok")
~/.claude/ccnotify/ccnotify.py

# Process events (called by Claude Code hooks)
~/.claude/ccnotify/ccnotify.py UserPromptSubmit < event.json
~/.claude/ccnotify/ccnotify.py Stop < event.json
~/.claude/ccnotify/ccnotify.py Notification < event.json
```

### Testing

```bash
# Run full unit test suite
cd tests
python -m unittest test_prompt_tracker.py -v

# Run manual tests interactively
python run_tests.py

# Run specific test scenario
python run_tests.py scenario_1

# Run all scenarios with delay
python run_tests.py all 2

# Verify database state after tests
python run_tests.py verify

# Test individual events
cat tests/test_data/individual_events/scenario_1/01_userpromptsubmit.json | python ccnotify.py UserPromptSubmit
```

### Database Operations

```bash
# Connect to database
sqlite3 ~/.claude/ccnotify/ccnotify.db

# View all records
SELECT session_id, seq, prompt, created_at, stoped_at, lastWaitUserAt
FROM prompt
ORDER BY created_at;

# Check session statistics
SELECT session_id, COUNT(*) as count, MAX(seq) as max_seq
FROM prompt
GROUP BY session_id;

# View completion status
SELECT
  COUNT(CASE WHEN stoped_at IS NOT NULL THEN 1 END) as completed,
  COUNT(CASE WHEN stoped_at IS NULL THEN 1 END) as incomplete
FROM prompt;
```

### Log Management

```bash
# View recent logs
tail -f ~/.claude/ccnotify/ccnotify.log

# Search logs for specific session
grep "session_abc123" ~/.claude/ccnotify/ccnotify.log

# View notification activity
grep "Notification sent" ~/.claude/ccnotify/ccnotify.log
```

## Installation Context

CCNotify is designed for user installation, not as a pip package. The installation flow is:

1. User clones/downloads repository
2. User symlinks `ccnotify.py` to `~/.claude/ccnotify/`
3. User installs `terminal-notifier` via Homebrew
4. User configures hooks in `~/.claude/settings.json`

**Important**: Starting from claude-code v1.0.95, invalid settings in `~/.claude/settings.json` will disable hooks. When debugging hook issues, run:
```bash
claude -p --model haiku -d hooks --verbose "hi"
```
Look for "[DEBUG] Found 1 hook commands to execute" vs "[DEBUG] Invalid settings" errors.

## Key Implementation Details

### Duration Calculation (ccnotify.py:237-271)
Formats durations as human-readable strings:
- Less than 60s: "30s"
- Less than 1h: "2m30s" or "5m"
- 1h or more: "1h30m" or "2h"

### Notification Detection (ccnotify.py:169-177)
Uses case-insensitive string matching on the notification message:
- Suppresses "waiting for input" notifications (Stop handler will send "job done" instead)
- All other notification types trigger immediate notifications

### VS Code Integration (ccnotify.py:290-291)
When `cwd` is provided, notifications include an execute command that opens the project in VS Code when clicked:
```python
cmd.extend(["-execute", f'/usr/local/bin/code "{cwd}"'])
```

### Logging Configuration (ccnotify.py:25-49)
Uses `TimedRotatingFileHandler` with:
- Daily rotation at midnight
- 1 day of backup logs
- UTF-8 encoding
- Format: `YYYY-MM-DD HH:MM:SS - LEVEL - message`

## Testing Architecture

The test suite includes:
- **Unit tests** (test_prompt_tracker.py): Tests individual methods with mocked database
- **Integration tests** (run_tests.py): Tests full event processing flow
- **Test data generator** (test_data.py): Creates 6 standardized test scenarios

**6 Test Scenarios:**
1. Single complete prompt flow (UserPromptSubmit → Stop)
2. Flow with waiting for input (UserPromptSubmit → Notification → Stop)
3. Multiple sequential prompts in same session (tests seq auto-increment)
4. Multiple concurrent sessions (tests session isolation)
5. Complex flow with multiple notifications
6. Different working directories (tests cwd handling)

## Debugging Common Issues

**Hooks not executing:**
- Check `~/.claude/settings.json` for invalid configuration
- Verify file permissions: `chmod a+x ~/.claude/ccnotify/ccnotify.py`
- Test manually: `echo '{"session_id":"test","prompt":"test","cwd":"/tmp","hook_event_name":"UserPromptSubmit"}' | ~/.claude/ccnotify/ccnotify.py UserPromptSubmit`

**Notifications not appearing:**
- Install terminal-notifier: `brew install terminal-notifier`
- Check logs for "terminal-notifier not found" warnings
- Test terminal-notifier directly: `terminal-notifier -message "test"`

**Database errors:**
- Ensure `~/.claude/ccnotify/` directory exists and is writable
- Check database file permissions
- Verify database schema: `sqlite3 ~/.claude/ccnotify/ccnotify.db ".schema"`

**SQL syntax errors with UPDATE:**
- Fixed in ccnotify.py:189-202 by using subquery instead of ORDER BY/LIMIT in UPDATE statement
- This was necessary for SQLite compatibility

## Project Files

- `ccnotify.py` - Main executable script (single file, ~380 lines)
- `tests/test_prompt_tracker.py` - Unit test suite
- `tests/run_tests.py` - Manual test runner
- `tests/test_data.py` - Test data generator
- `tests/test_data/` - Pre-generated test scenarios (JSON files)
- `README.md` - User installation and usage guide
- `alert.jpg` - Screenshot for README

## Data Storage

All data is stored locally:
- **Database**: `~/.claude/ccnotify/ccnotify.db` (SQLite)
- **Logs**: `~/.claude/ccnotify/ccnotify.log` (rotated daily)
- No external network calls or data uploads
