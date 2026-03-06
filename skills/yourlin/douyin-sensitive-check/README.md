# douyin-sensitive-check

> 抖音/短视频违禁词检测 OpenClaw Skill — 开源词库版，无需 API Key

## 功能

- 🔴 **违禁词检测**：涵盖政治、暴恐、色情、涉枪涉爆等（3,000+ 词）
- 🟠 **平台限流词**：抖音已知限流词，如"推广"、"加微信"、"优惠券"等
- 🟡 **广告极限词**：广告法违禁极限词，如"最好"、"第一"、"史上最"等
- 🟡 **医疗违禁词**：如"包治"、"根治"、"无副作用"等
- 📍 **上下文标注**：精确定位词在文案中的位置
- 🔄 **每日自动更新**：每天首次使用自动从 GitHub 拉取最新词库

## 词库来源（开源）

- [konsheng/Sensitive-lexicon](https://github.com/konsheng/Sensitive-lexicon) — MIT License
- [bigdata-labs/sensitive-stop-words](https://github.com/bigdata-labs/sensitive-stop-words)
- [jkiss/sensitive-words](https://github.com/jkiss/sensitive-words)

## 安装

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/YOUR_USERNAME/douyin-sensitive-check ~/.agents/skills/douyin-sensitive-check
```

## 使用

安装后直接在 OpenClaw 对话中说：

> "帮我检测这段文案有没有违禁词：今天给大家推广一款产品..."

### 命令行直接使用

```bash
SKILL=~/.agents/skills/douyin-sensitive-check

# 检测文案
python3 $SKILL/scripts/check.py "你的文案内容"

# 检测文件
python3 $SKILL/scripts/check.py -f script.txt

# 强制更新词库
python3 $SKILL/scripts/check.py --update

# 查看词库状态
python3 $SKILL/scripts/check.py --status
```

## 示例输出

```
🚨 发现 3 个风险词，建议修改后再发布

🟠 平台限流词（建议替换，影响流量）:
   ▸ 推广
     上下文: 今天给大家【推广】一款产品…

🟡 广告极限词（广告法风险）:
   ▸ 史上最
     上下文: …【史上最】好用！

── 标注后文案 ──
今天给大家【推广】一款产品，【史上最】好用！

📊 检测字数: 20 字 | 风险词: 3 个
```

## License

MIT
