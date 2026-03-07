---
name: destiny-fusion-pro
description: 专业命理融合咨询（紫微斗数 + 八字）。默认东八区北京口径（Asia/Shanghai, longitude=120.0），全离线运行（不联网、无 headless 浏览器依赖）；排盘图为可选项，失败不影响文本报告输出。
---

# Destiny Fusion Pro

一条命令生成完整报告（推荐）：

```bash
python scripts/fortune_fusion.py \
  --date 1990-10-21 \
  --time 15:30 \
  --gender female \
  --year 2026 \
  --from-year 2026 \
  --years 10 \
  --template pro \
  --format markdown
```

## 默认口径
- 时区：`Asia/Shanghai`
- 经度：`120.0`（北京基准）
- 紫微引擎：`--engine py`
- 报告默认：优先尝试输出 `JPG` 排盘图（依赖缺失会自动跳过，不影响文本报告）

## 常用参数
- `--engine py|js|dual`：主引擎 / 备用 / 双引擎对照
- `--template lite|pro|executive`：简版 / 标准咨询版 / 高管版
- `--chart none|svg|jpg`：是否输出排盘图
- `--chart-quality 1-100`：JPG 质量，默认 `92`
- `--chart-backend auto|cairosvg`：JPG 渲染后端
  - `auto`：使用 `cairosvg`（纯离线、无浏览器）
- `--format markdown|json`：报告格式

## 输出内容
1. 排盘口径（时区、经度、统一计算时间）
2. 紫微斗数全盘（命身宫、十二宫、年度四化）
3. 八字深度（四柱、十神、藏干、大运、流年）
4. 综合咨询（事业、关系、健康、财务、风险边界）

想了解报告背后的解读框架，可查看：`references/ziwei-methodology.md`

## 依赖
```bash
python -m venv .venv
.venv/bin/pip install -U iztro-py lunar-python
npm install iztro
```

若需 JPG 导出，再安装：
```bash
.venv/bin/pip install -U cairosvg pillow
```

如果未安装图片依赖或图片生成失败，skill 会自动跳过排盘图，不影响文本报告输出。
