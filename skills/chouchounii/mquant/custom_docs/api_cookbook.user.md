# API 用法速查手册

## 常用 API 速查

### 订阅行情
```python
# 订阅 Tick 行情
subscribe('000001.SZ', MarketDataType.TICK)

# 订阅 1分钟K线
subscribe('000001.SZ', MarketDataType.KLINE_1M)
```

### 下单
```python
# 市价单（amount 为正买入，负卖出）
order('000001.SZ', 100)   # 买入100股
order('000001.SZ', -100)  # 卖出100股
```

### 查询持仓
```python
# 返回字典 dict<symbol, Position>
positions = get_positions()

# 获取特定标的持仓
pos = positions.get('000001.SZ')
if pos:
    amount = pos.amount
```

## 我的 API 使用笔记

（在这里记录你使用 API 的经验和注意事项）
