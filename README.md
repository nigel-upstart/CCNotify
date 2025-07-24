# CCNotify

CCNotify provides desktop notifications for Claude Code, alerting you when Claude needs your input or completes tasks.

## Features

### 1. Smart Notifications
- **User Input Alerts**: Get notified when Claude is waiting for your input
- **Task Completion Alerts**: Receive notifications when Claude finishes a task

### 2. Rich Notification Content
- **Project Name**: Shows the current project directory name in the notification title
- **Task Duration**: Displays started time, and how long the task took to complete

### 3. IDE Integration
- **VS Code Integration**: Click on notifications to jump directly to the corresponding project in VS Code

## Installation Guide

### 1. Install ccnotify
Copy the `ccnotify.py` script to your Claude configuration directory:

```bash
# Create the scripts directory if it doesn't exist
mkdir -p ~/.claude/scripts

# Copy ccnotify.py to the scripts directory
cp ccnotify.py ~/.claude/scripts/
```

### 2. Install Python Dependencies
The script uses only Python standard library modules, so no additional Python packages are required.

### 3. Install terminal-notifier
ccnotify uses `terminal-notifier` for macOS notifications. Install it using Homebrew:

```bash
brew install terminal-notifier
```

For alternative installation methods and more information, visit: https://github.com/julienXX/terminal-notifier

### 4. Configure Claude Hooks
Add the following hooks to your Claude configuration to enable ccnotify:

```json
{
  "hooks": {
    "user_prompt_submit": "python3 ~/.claude/scripts/ccnotify.py UserPromptSubmit",
    "stop": "python3 ~/.claude/scripts/ccnotify.py Stop",
    "notification": "python3 ~/.claude/scripts/ccnotify.py Notification"
  }
}
```

## How It Works

ccnotify tracks Claude sessions and provides notifications at key moments:

- **When you submit a prompt**: Records the start time and project context
- **When Claude completes**: Calculates duration and sends a completion notification
- **When Claude waits for input**: Immediately alerts you that input is needed

All activity is logged to `~/.claude/ccnotify.log` and session data is stored in `~/.claude/ccnotify.db` for tracking and analytics.