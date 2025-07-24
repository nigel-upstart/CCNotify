# Claude Prompt 追踪系统 - 正常功能测试数据

## 测试场景说明

以下提供正常功能流程的测试数据，用于验证prompt追踪系统的核心功能。

## 1. 基础功能测试

### 场景1：单次完整prompt流程

#### 1.1 UserPromptSubmit事件
```json
{
  "session_id": "session_001",
  "transcript_path": "/Users/developer/.claude/projects/my-app/transcript_001.jsonl",
  "cwd": "/Users/developer/projects/my-app",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "创建一个Python脚本来处理CSV文件数据"
}
```

#### 1.2 Stop事件
```json
{
  "session_id": "session_001",
  "transcript_path": "/Users/developer/.claude/projects/my-app/transcript_001.jsonl",
  "cwd": "/Users/developer/projects/my-app",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

### 场景2：包含等待用户输入的完整流程

#### 2.1 UserPromptSubmit事件
```json
{
  "session_id": "session_002",
  "transcript_path": "/Users/developer/.claude/projects/web-app/transcript_002.jsonl",
  "cwd": "/Users/developer/projects/web-app",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "帮我设计一个用户登录系统，需要考虑安全性"
}
```

#### 2.2 Notification事件（等待用户输入）
```json
{
  "session_id": "session_002",
  "transcript_path": "/Users/developer/.claude/projects/web-app/transcript_002.jsonl",
  "cwd": "/Users/developer/projects/web-app",
  "hook_event_name": "Notification",
  "message": "Claude is waiting for your input"
}
```

#### 2.3 Stop事件
```json
{
  "session_id": "session_002",
  "transcript_path": "/Users/developer/.claude/projects/web-app/transcript_002.jsonl",
  "cwd": "/Users/developer/projects/web-app",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

## 2. 多prompt会话测试

### 场景3：同一会话的连续多个prompt（测试seq自增）

#### 3.1 第一个prompt
```json
{
  "session_id": "session_003",
  "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
  "cwd": "/Users/developer/projects/data-analysis",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "分析这个销售数据CSV文件"
}
```

#### 3.2 第一个prompt完成
```json
{
  "session_id": "session_003",
  "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
  "cwd": "/Users/developer/projects/data-analysis",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

#### 3.3 第二个prompt
```json
{
  "session_id": "session_003",
  "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
  "cwd": "/Users/developer/projects/data-analysis",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "基于刚才的分析结果，生成一个可视化图表"
}
```

#### 3.4 第二个prompt完成
```json
{
  "session_id": "session_003",
  "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
  "cwd": "/Users/developer/projects/data-analysis",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

#### 3.5 第三个prompt
```json
{
  "session_id": "session_003",
  "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
  "cwd": "/Users/developer/projects/data-analysis",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "导出分析报告为PDF格式"
}
```

#### 3.6 第三个prompt完成
```json
{
  "session_id": "session_003",
  "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
  "cwd": "/Users/developer/projects/data-analysis",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

## 3. 并发会话测试

### 场景4：多个不同会话同时进行

#### 4.1 会话A开始
```json
{
  "session_id": "session_004a",
  "transcript_path": "/Users/developer/.claude/projects/mobile-app/transcript_004a.jsonl",
  "cwd": "/Users/developer/projects/mobile-app",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "开发一个React Native移动应用"
}
```

#### 4.2 会话B开始
```json
{
  "session_id": "session_004b",
  "transcript_path": "/Users/developer/.claude/projects/api-server/transcript_004b.jsonl",
  "cwd": "/Users/developer/projects/api-server",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "创建一个RESTful API服务器"
}
```

#### 4.3 会话C开始
```json
{
  "session_id": "session_004c",
  "transcript_path": "/Users/developer/.claude/projects/frontend/transcript_004c.jsonl",
  "cwd": "/Users/developer/projects/frontend",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "构建一个Vue.js前端界面"
}
```

#### 4.4 会话A完成
```json
{
  "session_id": "session_004a",
  "transcript_path": "/Users/developer/.claude/projects/mobile-app/transcript_004a.jsonl",
  "cwd": "/Users/developer/projects/mobile-app",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

#### 4.5 会话B完成
```json
{
  "session_id": "session_004b",
  "transcript_path": "/Users/developer/.claude/projects/api-server/transcript_004b.jsonl",
  "cwd": "/Users/developer/projects/api-server",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

#### 4.6 会话C完成
```json
{
  "session_id": "session_004c",
  "transcript_path": "/Users/developer/.claude/projects/frontend/transcript_004c.jsonl",
  "cwd": "/Users/developer/projects/frontend",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

## 4. 复杂交互流程测试

### 场景5：包含多次等待和通知的会话

#### 5.1 用户提交prompt
```json
{
  "session_id": "session_005",
  "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
  "cwd": "/Users/developer/projects/complex-task",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "创建一个完整的电商网站，包括前端和后端"
}
```

#### 5.2 第一次等待用户输入
```json
{
  "session_id": "session_005",
  "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
  "cwd": "/Users/developer/projects/complex-task",
  "hook_event_name": "Notification",
  "message": "Claude is waiting for your input"
}
```

#### 5.3 权限请求通知
```json
{
  "session_id": "session_005",
  "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
  "cwd": "/Users/developer/projects/complex-task",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash"
}
```

#### 5.4 第二次等待用户输入
```json
{
  "session_id": "session_005",
  "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
  "cwd": "/Users/developer/projects/complex-task",
  "hook_event_name": "Notification",
  "message": "Claude is waiting for your input"
}
```

#### 5.5 任务完成
```json
{
  "session_id": "session_005",
  "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
  "cwd": "/Users/developer/projects/complex-task",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

## 5. 不同项目目录测试

### 场景6：不同工作目录的会话

#### 6.1 Python项目
```json
{
  "session_id": "session_006a",
  "transcript_path": "/Users/developer/.claude/projects/python-ml/transcript_006a.jsonl",
  "cwd": "/Users/developer/projects/python-ml",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "开发一个机器学习模型"
}
```

#### 6.2 Node.js项目
```json
{
  "session_id": "session_006b",
  "transcript_path": "/Users/developer/.claude/projects/nodejs-backend/transcript_006b.jsonl",
  "cwd": "/Users/developer/projects/nodejs-backend",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "构建Express.js后端服务"
}
```

#### 6.3 文档项目
```json
{
  "session_id": "session_006c",
  "transcript_path": "/Users/developer/.claude/projects/documentation/transcript_006c.jsonl",
  "cwd": "/Users/developer/projects/documentation",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "编写API文档"
}
```

## 测试执行顺序建议

1. **按场景顺序执行**：从场景1开始，按顺序执行每个测试用例
2. **验证数据库状态**：每执行几个用例后，检查数据库中的记录是否正确
3. **检查通知功能**：确认是否收到系统通知
4. **验证时间计算**：检查completed_at和created_at的时间差计算是否正确

## 预期结果验证

执行这些测试后，应该能看到：

1. **数据库记录正确**：每个UserPromptSubmit事件在数据库中有对应记录
2. **seq字段自增**：同一session_id下的记录seq值正确递增
3. **时间字段更新**：Stop事件正确更新stoped_at字段
4. **Notification记录**：等待输入的通知正确更新lastWaitUserAt字段
5. **系统通知发送**：收到格式正确的terminal-notifier通知