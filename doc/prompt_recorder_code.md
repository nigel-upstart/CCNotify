# Claude Code Prompt 追踪系统 - 实现指导

## 问题描述

需要创建一个Claude Code hooks系统，用于追踪和记录用户的每次prompt交互，并在适当的时机发送系统通知。主要需求包括：

1. **记录prompt历史**：每次用户提交prompt时记录到SQLite数据库
2. **追踪会话状态**：监控Stop和Notification事件，更新记录状态
3. **智能通知**：在任务完成或等待用户输入时发送系统通知
4. **时间统计**：计算prompt处理耗时并在通知中显示

## 技术方案

### 数据库设计

创建SQLite数据库，包含以下表结构：

```sql
CREATE TABLE prompt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,           -- Claude会话ID
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    prompt TEXT,                        -- 用户输入的prompt内容
    dirname TEXT,                       -- 当前工作目录
    seq INTEGER,                        -- 同session_id下的自增序号
    stoped_at DATETIME,                 -- 任务完成时间
    lastWaitUserAt DATETIME             -- 最后等待用户输入时间
);
```

### 核心实现架构

1. **统一Hook脚本**：创建单一Python脚本处理三种事件
   - `UserPromptSubmit`：插入新记录
   - `Stop`：更新完成时间并发送完成通知
   - `Notification`：更新等待时间并发送等待通知

2. **自动序号管理**：使用SQLite触发器自动维护seq字段

3. **系统通知**：使用`terminal-notifier`发送macOS通知

## 实现要求

### 1. 创建数据库管理类

```python
class ClaudePromptTracker:
    def __init__(self):
        # 数据库路径：~/.claude/prompt_tracker.db
        # 初始化数据库和触发器
    
    def init_database(self):
        # 创建表和自增触发器
    
    def handle_user_prompt_submit(self, data):
        # 插入新prompt记录
    
    def handle_stop(self, data):
        # 更新stoped_at，发送完成通知
    
    def handle_notification(self, data):
        # 更新lastWaitUserAt，发送等待通知
```

### 2. 触发器实现

创建SQLite触发器自动处理seq自增：

```sql
CREATE TRIGGER auto_increment_seq
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
```

### 3. 事件处理逻辑

#### UserPromptSubmit事件
- 从stdin读取JSON数据
- 提取：session_id, prompt, cwd
- 插入新记录到数据库

#### Stop事件
- 查找同session_id下最新的未完成记录
- 更新stoped_at为当前时间
- 计算耗时：stoped_at - created_at
- 发送通知：title=目录名，subtitle="已完成,耗时: X分钟"

#### Notification事件
- 检查message内容是否包含"waiting for your input"
- 更新lastWaitUserAt为当前时间
- 发送等待通知

### 4. 通知系统

使用terminal-notifier发送macOS通知：

```python
def send_notification(self, title, subtitle):
    subprocess.run([
        'terminal-notifier',
        '-sound', 'default',
        '-title', title,
        '-subtitle', subtitle
    ])
```

### 5. 时间计算

```python
def calculate_duration(self, start_time, end_time):
    # 解析ISO时间格式
    # 计算时间差
    # 返回友好的时间描述（如"2分30秒"）
```

## 配置文件

在`.claude/settings.json`中添加hooks配置：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/prompt_tracker.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/prompt_tracker.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/prompt_tracker.py"
          }
        ]
      }
    ]
  }
}
```

## 实现细节要求

1. **错误处理**：妥善处理JSON解析错误、数据库连接错误
2. **日志记录**：在stderr输出调试信息
3. **权限检查**：确保脚本可执行权限

## 测试验证

1. 创建测试数据库验证表结构
2. 模拟各种事件输入测试事件处理
3. 验证通知系统是否正常工作
4. 测试序号自增是否正确
5. 验证时间计算准确性

## 预期效果

- 用户每次提交prompt时，数据库中自动记录
- 任务完成时收到通知："项目名 - 已完成，耗时: 3分20秒"
- 等待用户输入时收到提醒通知
- 可通过数据库查询历史prompt记录和统计信息