![Notification Screenshot](alert.jpg)

# CCNotify

CCNotify provides desktop notifications for Claude Code, alerting you when Claude needs your input or completes tasks.

## Features

- 🔔 **Get notified** when Claude requires your input or completes a task.
- 🔗 **Click to jump back** when notifications are clicked, automatically taking you to the corresponding project in VS Code.
- ⏱️ **Task Duration**: Displays started time, and how long the task took to complete


## Installation Guide

### 1. Install CCNotify
```bash
# Create the scripts directory if it doesn't exist
mkdir -p ~/.claude/scripts

# Copy ccnotify.py to the scripts directory
cp ccnotify.py ~/.claude/scripts/

chmod a+x ~/.claude/scripts/ccnotify.py

# run this script, should print: ok
~/.claude/scripts/ccnotify.py

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
          "command": "~/.claude/scripts/ccnotify.py UserPromptSubmit"
        }
      ]
    }
  ],
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/scripts/ccnotify.py Stop"
        }
      ]
    }
  ],
  "Notification": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/scripts/ccnotify.py Notification"
        }
      ]
    }
  ]
}

```

## How It Works

ccnotify tracks Claude sessions and provides notifications at key moments:

- **When you submit a prompt**: Records the start time and project context
- **When Claude completes**: Calculates duration and sends a completion notification
- **When Claude waits for input**: Immediately alerts you that input is needed

All activity is logged to `~/.claude/ccnotify.log` and session data is stored in `~/.claude/ccnotify.db` for tracking and analytics.