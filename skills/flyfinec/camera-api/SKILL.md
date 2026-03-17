---
name: camera-api
description:
  通过本地 CLI 查询 TIVS 设备相关信息。包括设备列表，设备截图等能力。用户提出摄像头等设备查询查看需求时使用。
---

# My Camera API Skill

## 作用

当用户需要查询 TIVS 设备相关信息时，使用这个技能。

## 通用约定

- [必须按此操作] 先进入当前 skill 目录，例如 `cd xxx/skills/camera-api`，再执行 `tivs-cli.js`
- 默认自动加载当前技能目录下的 `.env` 环境变量
- 优先使用 JSON 输出
- 先解析结构化结果，再向用户总结
- 所需环境变量：`TIVS_APP_ID`、`TIVS_AUTHORIZATION`、可选 `TIVS_PROVIDER`

## 能力清单

### 登录

- 命令：`node ./tivs-cli.js login skill --app icam365`
- 用途：通过终端交互式登录tivs账号，保存登录凭证
- 详细说明：交互登录并获取 `access_token`，自动写入当前文件夹的`.env`文件，保存`TIVS_AUTHORIZATION`和`TIVS_APP_ID`环境变量

### 设备列表

- 命令：`node ./tivs-cli.js devices list --json`
- 用途：获取当前账号下的设备列表

### 设备截图

- 命令：`node ./tivs-cli.js devices screenshot <deviceId> --json`
- 用途：查询指定设备的截图记录，返回截图时间和图片地址
- 附加说明：优先取 `items[0]` 作为最新一条截图记录
- 附加说明：使用该记录的 `imagePath` 下载截图，并优先用发送图片能力把截图发给用户，不要只返回链接让用户点开

## 通用流程

1. 判断用户要查询的是设备列表、设备事件还是设备截图
2. 选择对应命令并优先使用 JSON 输出
3. 解析结果并提炼关键信息
4. 向用户返回简洁结论

## 异常处理

- 缺少认证变量时，提示补充 `TIVS_APP_ID` 和 `TIVS_AUTHORIZATION`
- CLI 或 API 报错时，直接返回错误信息
- 无结果时，明确说明未查询到数据
- 截图列表为空时，明确说明该设备暂无截图记录
- 截图下载失败时，返回最近一条截图的时间和链接，并说明下载失败

