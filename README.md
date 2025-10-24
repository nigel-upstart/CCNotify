![Notification Screenshot](alert.jpg)

# CCNotify

CCNotify provides desktop notifications for Claude Code, alerting you when Claude needs your input or completes tasks.
## Important Notes
Starting from claude-code v1.0.95 (2025-08-31), any invalid settings in `~/.claude/settings.json` will disable hooks. See [Why not working](#why-not-working) for solutions.

## Features

- 🔔 **Get notified** when Claude requires your input or completes a task.
- 🔗 **Smart click-to-focus** - Intelligently detects your environment and focuses the right window:
  - **VS Code**: Activates VS Code window
  - **Terminal**: Focuses the exact terminal tab using TTY matching
- ⏱️ **Task Duration**: Displays started time, and how long the task took to complete

**Note**: Currently compatible with macOS only.


## Installation Guide

### 1. Install CCNotify
```bash
# Create the directory if it doesn't exist
mkdir -p ~/.claude/ccnotify

# Copy ccnotify.py and helper script to the directory
cp ccnotify.py ~/.claude/ccnotify/
cp focus-terminal-tab.sh ~/.claude/ccnotify/

# Make them executable
chmod a+x ~/.claude/ccnotify/ccnotify.py
chmod a+x ~/.claude/ccnotify/focus-terminal-tab.sh

# Test that ccnotify is working (should print: ok)
~/.claude/ccnotify/ccnotify.py

ok

```
### 2. Install terminal-notifier
ccnotify uses `terminal-notifier` for macOS notifications. Install it using Homebrew:

```bash
brew install terminal-notifier
```

For alternative installation methods and more information, visit: https://github.com/julienXX/terminal-notifier

### 3. Configure Claude Hooks
Add the following hooks to your Claude configuration to enable ccnotify:

 ~/.claude/settings.json 
 
```json

  "hooks": {
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/ccnotify/ccnotify.py UserPromptSubmit"
        }
      ]
    }
  ],
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/ccnotify/ccnotify.py Stop"
        }
      ]
    }
  ],
  "Notification": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/ccnotify/ccnotify.py Notification"
        }
      ]
    }
  ]
}

```

## Try It Out

To verify the notification system works, start a new Claude Code session and run:
```
after 1 second, echo 'hello'
```
You should see a macOS notification appear.

## Why not working
1. Ensure hooks configuration is active. Here's an example where other configurations prevent hooks from working:

`claude -p --model haiku -d hooks --verbose "hi"`

Expected output:

```
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: ~/.claude/ccnotify/ccnotify.py UserPromptSubmit with timeout 60000ms
[DEBUG] Hook command completed with status 0: ~/.claude/ccnotify/ccnotify.py UserPromptSubmit
```

Actual output:

```
[DEBUG] Invalid settings in userSettings source - key: permissions.allow.0, error:.....
[DEBUG] Found 0 hook commands to execute
```
Reason: In September 2025, claude-code strengthened validation rules for settings.json. Any invalid configuration will disable hooks.
You need to modify the relevant configurations in `~/.claude/settings.json` until the `Invalid settings` error stops appearing.



## How It Works

ccnotify tracks Claude sessions and provides notifications at key moments:

- **When you submit a prompt**: Records the start time and project context
- **When Claude completes**: Calculates duration and sends a completion notification
- **When Claude waits for input**: Immediately alerts you that input is needed

All activity is logged to `~/.claude/ccnotify/ccnotify.log` and session data is stored in `~/.claude/ccnotify/ccnotify.db` locally. No data is uploaded or shared externally.


## Uninstall

Edit `~/.claude/settings.json` and remove all hook commands related to `ccnotify`.

Remove all files with a single command:
```bash
rm -rf ~/.claude/ccnotify
```

