---
name: DevTaskFlow
description: 可共享、可分发的版本化开发任务流水线。支持项目初始化、环境体检、任务分析、代码生成、审查、修复、部署与封版，并可选接入 OpenClaw 子 agent 协作。
license: Proprietary
---

# DevTaskFlow

## 定位

DevTaskFlow 是 dev-pipeline 的下一代版本，目标不是服务单一机器上的私有流程，而是成为：

- 可共享
- 可配置
- 可分发
- 可适配 OpenClaw / 非 OpenClaw 环境

的开发任务流水线工具。

## 当前阶段

当前为 B2 重构版第一阶段骨架，优先完成：

1. 标准 CLI 入口
2. 安全配置（移除硬编码密钥）
3. 项目初始化脚手架
4. 环境体检 doctor
5. 配置校验与状态管理基础层

## 推荐命令

```bash
dtflow init-project
dtflow doctor
dtflow status
dtflow analyze
dtflow confirm
dtflow write
dtflow review
dtflow fix
dtflow deploy
dtflow seal
```

## 设计原则

1. 核心逻辑与 OpenClaw 编排解耦
2. 敏感信息全部走环境变量
3. deploy / archive / orchestration 通过 adapter 接入
4. 允许跨项目、跨机器复用
5. 文档、配置、CLI 三者保持一致
