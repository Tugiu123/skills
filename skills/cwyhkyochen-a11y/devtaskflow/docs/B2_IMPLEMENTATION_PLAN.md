# DevTaskFlow B2 实施方案

## 目标

将旧版 dev-pipeline 重构为可共享、可分发、可适配的 DevTaskFlow。

## Phase 1（已开始）

- [x] 新名称定稿：DevTaskFlow
- [x] 新 skill 目录建立
- [x] CLI 入口建立：dtflow
- [x] .dtflow 配置目录设计
- [x] 环境变量模板
- [x] doctor 命令
- [x] status 命令
- [x] init-project 脚手架

## Phase 2（待做）

- [ ] LLM adapter 抽象
- [ ] analyze / confirm / revise
- [ ] 任务计划解析器
- [ ] 状态推进机制完善

## Phase 3（待做）

- [ ] write / review / fix
- [ ] 文件写入策略增强
- [ ] 审查报告解析

## Phase 4（待做）

- [ ] deploy adapter
- [ ] archive adapter
- [ ] OpenClaw orchestration adapter

## Phase 5（待做）

- [ ] README 完善
- [ ] 示例项目
- [ ] 安装方式文档
- [ ] 迁移指南（dev-pipeline -> DevTaskFlow）

## 当前设计决策

1. 项目配置目录采用 `.dtflow/`
2. 命令名采用 `dtflow`
3. 敏感配置全部走环境变量
4. OpenClaw 协作作为 adapter，而不是核心硬依赖
5. 旧版 dev-pipeline 不直接硬改，采用新目录重建
