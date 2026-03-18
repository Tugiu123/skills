# DevTaskFlow Architecture

## 目标架构

```text
CLI (dtflow)
  ├── config layer
  ├── state layer
  ├── scaffold layer
  ├── doctor layer
  ├── pipeline core
  │    ├── analyze
  │    ├── write
  │    ├── review
  │    ├── fix
  │    ├── deploy
  │    └── seal
  └── adapters
       ├── llm adapter
       ├── deploy adapter
       ├── archive adapter
       └── openclaw adapter
```

## 设计原则

### 1. Core / Adapter 分离
- 核心流程不直接绑定 OpenClaw
- OpenClaw 子 agent 协作作为可选适配器存在

### 2. 安全优先
- API Key 禁止硬编码
- 所有敏感信息走环境变量或本地配置

### 3. 项目自描述
- 每个项目通过 `.dtflow/config.json` 描述自身
- 每个版本通过 `versions/<version>/.state.json` 维护状态

### 4. 可诊断
- doctor 命令统一检查环境、依赖、配置、目录结构

## 第一阶段范围

- init-project
- doctor
- status
- config 校验
- 状态管理基础能力

## 第二阶段范围

- analyze / confirm / revise
- write / review / fix

## 第三阶段范围

- deploy / seal
- adapter 抽象
- OpenClaw 集成
