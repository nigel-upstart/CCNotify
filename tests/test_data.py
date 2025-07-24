#!/usr/bin/env python3
"""
Test data generator for Claude Prompt Tracker System
Contains all test scenarios from the test documentation
"""

import json
from pathlib import Path


class TestDataGenerator:
    """Generate test data for various scenarios"""
    
    @staticmethod
    def get_scenario_1_data():
        """场景1：单次完整prompt流程"""
        return [
            {
                "session_id": "session_001",
                "transcript_path": "/Users/developer/.claude/projects/my-app/transcript_001.jsonl",
                "cwd": "/Users/developer/projects/my-app",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "创建一个Python脚本来处理CSV文件数据"
            },
            {
                "session_id": "session_001",
                "transcript_path": "/Users/developer/.claude/projects/my-app/transcript_001.jsonl",
                "cwd": "/Users/developer/projects/my-app",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            }
        ]
    
    @staticmethod
    def get_scenario_2_data():
        """场景2：包含等待用户输入的完整流程"""
        return [
            {
                "session_id": "session_002",
                "transcript_path": "/Users/developer/.claude/projects/web-app/transcript_002.jsonl",
                "cwd": "/Users/developer/projects/web-app",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "帮我设计一个用户登录系统，需要考虑安全性"
            },
            {
                "session_id": "session_002",
                "transcript_path": "/Users/developer/.claude/projects/web-app/transcript_002.jsonl",
                "cwd": "/Users/developer/projects/web-app",
                "hook_event_name": "Notification",
                "message": "Claude is waiting for your input"
            },
            {
                "session_id": "session_002",
                "transcript_path": "/Users/developer/.claude/projects/web-app/transcript_002.jsonl",
                "cwd": "/Users/developer/projects/web-app",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            }
        ]
    
    @staticmethod
    def get_scenario_3_data():
        """场景3：同一会话的连续多个prompt（测试seq自增）"""
        return [
            {
                "session_id": "session_003",
                "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
                "cwd": "/Users/developer/projects/data-analysis",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "分析这个销售数据CSV文件"
            },
            {
                "session_id": "session_003",
                "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
                "cwd": "/Users/developer/projects/data-analysis",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            },
            {
                "session_id": "session_003",
                "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
                "cwd": "/Users/developer/projects/data-analysis",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "基于刚才的分析结果，生成一个可视化图表"
            },
            {
                "session_id": "session_003",
                "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
                "cwd": "/Users/developer/projects/data-analysis",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            },
            {
                "session_id": "session_003",
                "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
                "cwd": "/Users/developer/projects/data-analysis",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "导出分析报告为PDF格式"
            },
            {
                "session_id": "session_003",
                "transcript_path": "/Users/developer/.claude/projects/data-analysis/transcript_003.jsonl",
                "cwd": "/Users/developer/projects/data-analysis",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            }
        ]
    
    @staticmethod
    def get_scenario_4_data():
        """场景4：多个不同会话同时进行"""
        return [
            {
                "session_id": "session_004a",
                "transcript_path": "/Users/developer/.claude/projects/mobile-app/transcript_004a.jsonl",
                "cwd": "/Users/developer/projects/mobile-app",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "开发一个React Native移动应用"
            },
            {
                "session_id": "session_004b",
                "transcript_path": "/Users/developer/.claude/projects/api-server/transcript_004b.jsonl",
                "cwd": "/Users/developer/projects/api-server",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "创建一个RESTful API服务器"
            },
            {
                "session_id": "session_004c",
                "transcript_path": "/Users/developer/.claude/projects/frontend/transcript_004c.jsonl",
                "cwd": "/Users/developer/projects/frontend",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "构建一个Vue.js前端界面"
            },
            {
                "session_id": "session_004a",
                "transcript_path": "/Users/developer/.claude/projects/mobile-app/transcript_004a.jsonl",
                "cwd": "/Users/developer/projects/mobile-app",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            },
            {
                "session_id": "session_004b",
                "transcript_path": "/Users/developer/.claude/projects/api-server/transcript_004b.jsonl",
                "cwd": "/Users/developer/projects/api-server",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            },
            {
                "session_id": "session_004c",
                "transcript_path": "/Users/developer/.claude/projects/frontend/transcript_004c.jsonl",
                "cwd": "/Users/developer/projects/frontend",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            }
        ]
    
    @staticmethod
    def get_scenario_5_data():
        """场景5：包含多次等待和通知的会话"""
        return [
            {
                "session_id": "session_005",
                "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
                "cwd": "/Users/developer/projects/complex-task",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "创建一个完整的电商网站，包括前端和后端"
            },
            {
                "session_id": "session_005",
                "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
                "cwd": "/Users/developer/projects/complex-task",
                "hook_event_name": "Notification",
                "message": "Claude is waiting for your input"
            },
            {
                "session_id": "session_005",
                "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
                "cwd": "/Users/developer/projects/complex-task",
                "hook_event_name": "Notification",
                "message": "Claude needs your permission to use Bash"
            },
            {
                "session_id": "session_005",
                "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
                "cwd": "/Users/developer/projects/complex-task",
                "hook_event_name": "Notification",
                "message": "Claude is waiting for your input"
            },
            {
                "session_id": "session_005",
                "transcript_path": "/Users/developer/.claude/projects/complex-task/transcript_005.jsonl",
                "cwd": "/Users/developer/projects/complex-task",
                "hook_event_name": "Stop",
                "stop_hook_active": False
            }
        ]
    
    @staticmethod
    def get_scenario_6_data():
        """场景6：不同工作目录的会话"""
        return [
            {
                "session_id": "session_006a",
                "transcript_path": "/Users/developer/.claude/projects/python-ml/transcript_006a.jsonl",
                "cwd": "/Users/developer/projects/python-ml",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "开发一个机器学习模型"
            },
            {
                "session_id": "session_006b",
                "transcript_path": "/Users/developer/.claude/projects/nodejs-backend/transcript_006b.jsonl",
                "cwd": "/Users/developer/projects/nodejs-backend",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "构建Express.js后端服务"
            },
            {
                "session_id": "session_006c",
                "transcript_path": "/Users/developer/.claude/projects/documentation/transcript_006c.jsonl",
                "cwd": "/Users/developer/projects/documentation",
                "hook_event_name": "UserPromptSubmit",
                "prompt": "编写API文档"
            }
        ]
    
    @staticmethod
    def get_all_scenarios():
        """获取所有测试场景的数据"""
        return {
            "scenario_1": TestDataGenerator.get_scenario_1_data(),
            "scenario_2": TestDataGenerator.get_scenario_2_data(),
            "scenario_3": TestDataGenerator.get_scenario_3_data(),
            "scenario_4": TestDataGenerator.get_scenario_4_data(),
            "scenario_5": TestDataGenerator.get_scenario_5_data(),
            "scenario_6": TestDataGenerator.get_scenario_6_data()
        }
    
    @staticmethod
    def save_test_data_files(output_dir):
        """将测试数据保存为JSON文件"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        scenarios = TestDataGenerator.get_all_scenarios()
        
        for scenario_name, data in scenarios.items():
            file_path = output_path / f"{scenario_name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Saved {scenario_name} to {file_path}")
    
    @staticmethod
    def create_individual_event_files(output_dir):
        """为每个事件创建单独的JSON文件，便于手动测试"""
        output_path = Path(output_dir) / "individual_events"
        output_path.mkdir(exist_ok=True)
        
        scenarios = TestDataGenerator.get_all_scenarios()
        
        for scenario_name, events in scenarios.items():
            scenario_dir = output_path / scenario_name
            scenario_dir.mkdir(exist_ok=True)
            
            for i, event in enumerate(events, 1):
                event_name = event['hook_event_name']
                file_name = f"{i:02d}_{event_name.lower()}.json"
                file_path = scenario_dir / file_name
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(event, f, ensure_ascii=False, indent=2)
                
                print(f"Created {file_path}")


if __name__ == "__main__":
    # 生成测试数据文件
    test_dir = Path(__file__).parent / "test_data"
    
    print("生成测试数据文件...")
    TestDataGenerator.save_test_data_files(test_dir)
    
    print("\n生成单独事件文件...")
    TestDataGenerator.create_individual_event_files(test_dir)
    
    print("\n测试数据生成完成！")
    print(f"文件位置: {test_dir.absolute()}")