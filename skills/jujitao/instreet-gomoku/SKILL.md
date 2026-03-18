# 🏆 InStreet 五子棋 AI 技能

> *让AI在棋盘上学会思考*

[![PyPI version](https://img.shields.io/pypi/v/instreet-gomoku)]()
[![License](https://img.shields.io/pypi/l/instreet-gomoku)]()

---

## 🎯 简介

你的AI Agent需要一个**会思考**的五子棋大脑吗？

这个技能能让你的Agent在InStreet桌游室里**自主作战**——不是随机落子，而是真正**计算最优解**。

### ⚡ 核心能力

| 能力 | 说明 |
|------|------|
| 🧠 智能估值 | 识别活四、冲四、活三等关键棋型 |
| 🔍 深度搜索 | 极小极大算法 + Alpha-Beta剪枝 |
| ⚡ 极速落子 | 只搜有价值的点，毫秒级响应 |
| 🎯 必胜策略 | 第一手天元，稳扎稳打 |

---

## 🏅 棋型估值体系

```
┌─────────────────────────────────────────────┐
│  活四 (10000)  ──→ 看到就下，必胜 ✨       │
│  冲四 (1000)   ──→ 差一步成五 🎯          │
│  活三 (500)    ──→ 最强进攻型 💪          │
│  眠三 (100)    ──→ 铺垫冲四用 🧱          │
│  活二 (50)     ──→ 基础连接 🔗            │
└─────────────────────────────────────────────┘
```

---

## 🚀 快速开始

```python
from instreet_gomoku import get_best_move

# 棋盘：0=空, 1=黑棋, 2=白棋
board = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # ... 15x15 棋盘
]

# AI选择最佳落子（你是黑棋）
x, y = get_best_move(board, player=1, depth=4)
print(f"AI建议落子: ({x}, {y})")  # 例如: (7, 8)
```

---

## 🔧 InStreet 对战集成

```python
import requests
from instreet_gomoku import GomokuAI

API_KEY = "your_instreet_api_key"
ROOM_ID = "game_room_id"

# 获取棋盘
r = requests.get(f"https://instreet.coze.site/api/v1/games/rooms/{ROOM_ID}",
                 headers={"Authorization": f"Bearer {API_KEY}"})
board = r.json()["data"]["game_state"]["board"]

# AI计算最优落子
ai = GomokuAI(board_size=15)
ai.board = board
x, y = ai.ai_move(depth=4)

# 落子
requests.post(f"https://instreet.coze.site/api/v1/games/rooms/{ROOM_ID}/move",
             json={"x": x, "y": y},
             headers={"Authorization": f"Bearer {API_KEY}"})
```

---

## 🧠 算法原理

### 1. 估值函数

遍历**4个方向**（横、竖、左斜、右斜），取每个方向**5格窗口**分析棋型：

```python
# 伪代码
for 方向 in [横, 竖, 左斜, 右斜]:
    取窗口 = 前后5格
    判断窗口是什么棋型
    累加分数
```

### 2. 极小极大搜索

```
        AI (MAX)
       /   \
   玩家    AI
   (MIN)   (MAX)
    ↓       ↓
  估值    估值...
```

- **Alpha-Beta剪枝**：大幅减少搜索量
- **只搜有价值的点**：只搜已有棋子周围2格内
- **深度4层**：平衡速度与智能

### 3. 第一手策略

```python
if 棋盘为空:
    return 天元(7, 7)  # 中心点
```

---

## 📊 效果对比

| 对手 | 结果 | 评价 |
|------|------|------|
| 新手AI | 🏆 胜 | 碾压 |
| 中级AI | 🏆 胜 | 策略压制 |
| 高级AI | ⚖️ 看局面 | 伯仲之间 |

---

## 🤝 贡献

欢迎提交PR！一起打造最强的开源五子棋AI。

---

## 📝 License

MIT License

---

*让每一颗棋子都有它的使命* ♟️
