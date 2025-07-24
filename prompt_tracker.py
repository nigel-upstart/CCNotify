#!/usr/bin/env python3
"""
Claude Code Prompt Tracker System
"""

import os
import sys
import json
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path


class ClaudePromptTracker:
    def __init__(self):
        """Initialize the prompt tracker with database setup"""
        self.db_path = Path.home() / ".claude" / "prompt_tracker.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Create tables and triggers if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            # Create main table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prompt (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    prompt TEXT,
                    dirname TEXT,
                    seq INTEGER,
                    stoped_at DATETIME,
                    lastWaitUserAt DATETIME
                )
            """)
            
            # Create trigger for auto-incrementing seq
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS auto_increment_seq
                AFTER INSERT ON prompt
                FOR EACH ROW
                BEGIN
                    UPDATE prompt 
                    SET seq = (
                        SELECT COALESCE(MAX(seq), 0) + 1 
                        FROM prompt 
                        WHERE session_id = NEW.session_id
                    )
                    WHERE id = NEW.id;
                END
            """)
            
            conn.commit()
    
    def handle_user_prompt_submit(self, data):
        """Handle UserPromptSubmit event - insert new prompt record"""
        session_id = data.get('session_id')
        prompt = data.get('prompt', '')
        cwd = data.get('cwd', '')
        dirname = os.path.basename(cwd) if cwd else 'unknown'
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO prompt (session_id, prompt, dirname)
                VALUES (?, ?, ?)
            """, (session_id, prompt, dirname))
            conn.commit()
        
        print(f"[PROMPT_TRACKER] Recorded prompt for session {session_id}", file=sys.stderr)
    
    def handle_stop(self, data):
        """Handle Stop event - update completion time and send notification"""
        session_id = data.get('session_id')
        
        with sqlite3.connect(self.db_path) as conn:
            # Find the latest unfinished record for this session
            cursor = conn.execute("""
                SELECT id, created_at, dirname
                FROM prompt 
                WHERE session_id = ? AND stoped_at IS NULL
                ORDER BY created_at DESC
                LIMIT 1
            """, (session_id,))
            
            row = cursor.fetchone()
            if row:
                record_id, created_at, dirname = row
                
                # Update completion time
                conn.execute("""
                    UPDATE prompt 
                    SET stoped_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (record_id,))
                conn.commit()
                
                # Calculate duration and send notification
                duration = self.calculate_duration_from_db(record_id)
                self.send_notification(
                    title=dirname or "Claude Task",
                    subtitle=f"��: {duration}"
                )
                
                print(f"[PROMPT_TRACKER] Task completed for session {session_id}, duration: {duration}", file=sys.stderr)
    
    def handle_notification(self, data):
        """Handle Notification event - check for waiting input and send notification"""
        session_id = data.get('session_id')
        message = data.get('message', '')
        
        if 'waiting for your input' in message.lower():
            cwd = data.get('cwd', '')
            dirname = os.path.basename(cwd) if cwd else 'Claude Task'
            
            with sqlite3.connect(self.db_path) as conn:
                # Update lastWaitUserAt for the latest record
                conn.execute("""
                    UPDATE prompt 
                    SET lastWaitUserAt = CURRENT_TIMESTAMP
                    WHERE session_id = ? AND stoped_at IS NULL
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (session_id,))
                conn.commit()
            
            self.send_notification(
                title=dirname,
                subtitle="I����e"
            )
            
            print(f"[PROMPT_TRACKER] Waiting notification sent for session {session_id}", file=sys.stderr)
    
    def calculate_duration_from_db(self, record_id):
        """Calculate duration for a completed record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT created_at, stoped_at
                FROM prompt
                WHERE id = ?
            """, (record_id,))
            
            row = cursor.fetchone()
            if row and row[1]:
                return self.calculate_duration(row[0], row[1])
        
        return "*�"
    
    def calculate_duration(self, start_time, end_time):
        """Calculate human-readable duration between two timestamps"""
        try:
            if isinstance(start_time, str):
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            else:
                start_dt = datetime.fromisoformat(start_time)
            
            if isinstance(end_time, str):
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            else:
                end_dt = datetime.fromisoformat(end_time)
            
            duration = end_dt - start_dt
            total_seconds = int(duration.total_seconds())
            
            if total_seconds < 60:
                return f"{total_seconds}�"
            elif total_seconds < 3600:
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                if seconds > 0:
                    return f"{minutes}{seconds}�"
                else:
                    return f"{minutes}�"
            else:
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                if minutes > 0:
                    return f"{hours}�{minutes}�"
                else:
                    return f"{hours}�"
        except Exception as e:
            print(f"[PROMPT_TRACKER] Error calculating duration: {e}", file=sys.stderr)
            return "*�"
    
    def send_notification(self, title, subtitle):
        """Send macOS notification using terminal-notifier"""
        try:
            subprocess.run([
                'terminal-notifier',
                '-sound', 'default',
                '-title', title,
                '-subtitle', subtitle
            ], check=False, capture_output=True)
            print(f"[PROMPT_TRACKER] Notification sent: {title} - {subtitle}", file=sys.stderr)
        except FileNotFoundError:
            print("[PROMPT_TRACKER] terminal-notifier not found, notification skipped", file=sys.stderr)
        except Exception as e:
            print(f"[PROMPT_TRACKER] Error sending notification: {e}", file=sys.stderr)


def main():
    """Main entry point - read JSON from stdin and process event"""
    try:
        # Read JSON data from stdin
        input_data = sys.stdin.read().strip()
        if not input_data:
            print("[PROMPT_TRACKER] No input data received", file=sys.stderr)
            return
        
        data = json.loads(input_data)
        event_name = data.get('hook_event_name')
        
        tracker = ClaudePromptTracker()
        
        if event_name == 'UserPromptSubmit':
            tracker.handle_user_prompt_submit(data)
        elif event_name == 'Stop':
            tracker.handle_stop(data)
        elif event_name == 'Notification':
            tracker.handle_notification(data)
        else:
            print(f"[PROMPT_TRACKER] Unknown event: {event_name}", file=sys.stderr)
    
    except json.JSONDecodeError as e:
        print(f"[PROMPT_TRACKER] JSON decode error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"[PROMPT_TRACKER] Unexpected error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()