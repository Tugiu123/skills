# dougong-cashier-query — 交易查询与关单

支付状态查询和托管交易关单，用于确认支付结果和处理超时未支付订单。

> **前置依赖**：首次接入请先完成 [dougong-pay-base](../dougong-pay-base/) 的 SDK 初始化。

## 本 Skill 解决什么问题

| 场景 | 问题 | 解决方案 |
|------|------|---------|
| 支付后页面未跳转 | 用户不确定是否支付成功 | 调用**查询接口**确认 trans_stat |
| 收到异步通知 | 通知可能被伪造 | 调用**查询接口**做二次确认 |
| trans_stat=P | 交易还在处理中 | **轮询查询**：间隔 5 秒，最多 30 次 |
| 用户长时间未支付 | 订单占用库存 | 调用**关单接口**释放资源 |

## 文件结构

```
dougong-cashier-query/
├── SKILL.md                          # Skill 定义（触发词、场景路由、注意事项）
├── README.md                         # 本文件
└── references/
    ├── payment-status-query.md       # 支付状态查询（完整参数 + SDK 示例）
    └── trade-close.md                # 托管交易关单（完整参数 + SDK 示例）
```

## 快速接入

### 支付状态查询

```java
V2TradeHostingPaymentQueryorderinfoRequest request = new V2TradeHostingPaymentQueryorderinfoRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setOrgReqDate("原交易日期");       // 来自预下单响应的 req_date
request.setOrgReqSeqId("原交易流水号");     // 来自预下单响应的 req_seq_id

Map<String, Object> response = BasePayClient.request(request, false);
String transStat = (String) response.get("trans_stat");
// S=成功, F=失败, P=处理中（需继续轮询）
```

### 托管交易关单

```java
V2TradeHostingPaymentCloseRequest request = new V2TradeHostingPaymentCloseRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("你的商户号");
request.setOrgReqDate("原交易日期");
request.setOrgReqSeqId("原交易流水号");

Map<String, Object> response = BasePayClient.request(request, false);
```

完整参数和 JSON 示例见各 reference 文档。

## trans_stat=P 轮询策略

当查询结果为 `trans_stat=P`（处理中）时，**不可当作失败处理**：

```
1. 前端展示"支付处理中"
2. 后端轮询查询接口：间隔 5 秒，最多 30 次（150 秒）
3. 同时监听异步通知，以先到者为准
4. 150 秒后仍为 P → 记录异常日志，人工介入，不要自动关单
```

## 关键约束

- 查询和关单都需要原交易的 `org_req_date` + `org_req_seq_id`（来自预下单响应，务必保存）
- **已支付成功的订单无法关单**，只能走退款流程
- 关单前建议先查询确认订单确实未支付，避免"关单瞬间用户完成支付"的竞态问题
- 关单成功后用户将无法再对该订单支付

## 下一步

| 查询结果 | 下一步操作 |
|---------|-----------|
| trans_stat=S | 执行业务成功逻辑（发货等） |
| trans_stat=F | 提示用户重新发起支付 |
| trans_stat=P 超时 | 人工介入排查 |
| 需要退款 | 前往 [dougong-cashier-refund](../dougong-cashier-refund/) |
