#!/bin/bash
# Helper script to focus the correct Terminal tab by TTY
# Usage: focus-terminal-tab.sh <tty> <cwd>

TARGET_TTY="$1"
TARGET_CWD="$2"

if [ -z "$TARGET_TTY" ]; then
    echo "Error: TTY not provided" >&2
    exit 1
fi

# Create AppleScript that uses TTY to find the exact tab
osascript << EOF
tell application "Terminal"
    activate
    set foundTab to false

    -- Search all windows and tabs for matching TTY
    repeat with w from 1 to count windows
        repeat with t from 1 to count tabs of window w
            try
                -- Get the tty property of this tab
                set tabTTY to tty of tab t of window w

                -- Match by TTY (most reliable!)
                if tabTTY contains "$TARGET_TTY" then
                    set frontmost of window w to true
                    set selected of tab t of window w to true
                    set foundTab to true
                    return "Found and selected tab with tty=$TARGET_TTY"
                end if
            end try
        end repeat

        if foundTab then exit repeat
    end repeat

    -- If we didn't find by TTY, try by working directory as fallback
    if not foundTab then
        repeat with w from 1 to count windows
            repeat with t from 1 to count tabs of window w
                try
                    -- Check if any process in this tab is running in target cwd
                    set procList to processes of tab t of window w
                    repeat with proc in procList
                        if proc contains "$TARGET_CWD" or proc contains "claude" then
                            set frontmost of window w to true
                            set selected of tab t of window w to true
                            return "Found tab by process match (fallback)"
                        end if
                    end repeat
                end try
            end repeat
        end repeat
    end if

    return "Could not find matching tab"
end tell
EOF

exit $?
