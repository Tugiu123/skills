# 我的策略模板库

## 模板1：基础网格策略框架

```python
# 我的常用初始化设置
def initialize(context):
    # 日志设置
    global LOG_FILE
    LOG_FILE = os.path.splitext(__file__)[0] + '.log'
    write_log('INFO', '策略初始化开始')

    # 我的默认参数
    g_security = context.setting.get('security', '000001.SZ')
    g_base_price = float(context.setting.get('base_price', '10.0'))

    # 订阅行情
    subscribe(g_security, MarketDataType.KLINE_1M)
```

## 模板2：我的风控函数

```python
def check_risk_limits(context, price, amount):
    '''我自己的风控检查函数'''
    positions = get_positions()
    # ... 在这里添加你的风控逻辑
    pass
```

## 我的常用标的

- 600519.SH - 茅台，我的主力标的
- 000001.SZ - 平安，测试用

## 我的编码习惯

- 全局变量使用 g_ 前缀
- 日志级别：DEBUG 用于详细数据，INFO 用于关键事件
- 所有策略必须包含错误处理

## 我的常见错误

- 忘记在 initialize 中订阅行情
- get_positions() 返回的是字典不是列表
- 订阅日线要用 KLINE_1M 累积，不能直接用 '1d'

## 个人笔记

（在这里记录你的交易心得、策略思路等）
