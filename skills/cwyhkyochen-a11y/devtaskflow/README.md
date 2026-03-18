# DevTaskFlow

DevTaskFlow 是一个可共享、可分发的开发任务流水线工具，用于管理版本化开发流程：

- 初始化项目
- 环境检查
- 需求分析
- 方案确认
- 代码生成
- 代码审查
- 问题修复
- 部署
- 封版归档

## 目标

相比旧版 dev-pipeline，DevTaskFlow 重点解决：

- 硬编码密钥
- 依赖不透明
- 入口不统一
- 仅适配单机环境
- 对 OpenClaw 耦合过深

## CLI

推荐命令名：`dtflow`

## 当前阶段

第一阶段只实现基础骨架与配置体系，后续再逐步迁移 analyze/write/review/fix 等核心能力。

## 目录结构

```text
skills/devtaskflow/
├── SKILL.md
├── README.md
├── commands/
│   └── dtflow
├── lib/
│   ├── cli.py
│   ├── config.py
│   ├── doctor.py
│   ├── state.py
│   └── scaffold.py
├── templates/
│   ├── config.json
│   └── env.example
└── docs/
    └── ARCHITECTURE.md
```
