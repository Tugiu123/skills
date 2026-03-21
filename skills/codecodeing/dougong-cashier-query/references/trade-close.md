## 目录

- [接口概述](#接口概述)
- [SDK Request 类字段](#sdk-request-类字段)
- [返回参数](#返回参数)
- [完整 SDK 调用示例](#完整-sdk-调用示例)
- [注意事项](#注意事项)
- [补充返回参数](#补充返回参数完整版)
- [异步通知参数](#异步通知参数)
- [常见错误码](#常见错误码)

# 托管交易关单

## 接口概述

| 属性 | 值 |
|-----|-----|
| 汇付 API 端点 | `v2/trade/hosting/payment/close` |
| 请求方式 | POST |
| SDK Request 类 | `V2TradeHostingPaymentCloseRequest` |
| 建议业务接口 | `POST /hfpay/closeOrder` |

## SDK Request 类字段

`V2TradeHostingPaymentCloseRequest` 的专属字段：

| 字段 | setter 方法 | 类型 | 必填 | 说明 |
|------|-----------|------|------|------|
| reqSeqId | setReqSeqId() | String(64) | Y | 本次关单的请求流水号 |
| reqDate | setReqDate() | String(8) | Y | 本次关单的请求日期 |
| huifuId | setHuifuId() | String(32) | Y | 商户号 |
| orgReqDate | setOrgReqDate() | String(8) | Y | 原交易的请求日期 |
| orgReqSeqId | setOrgReqSeqId() | String(64) | Y | 原交易的请求流水号 |

通过 `setExtendInfo(Map)` 传入的扩展字段：

| 字段 | 说明 |
|------|------|
| notify_url | 关单结果异步通知地址（可选） |

## 返回参数

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | `00000000` 表示关单成功 |
| resp_desc | String(128) | 响应描述 |
| huifu_id | String(32) | 商户号 |
| org_req_date | String(8) | 原交易请求日期 |
| org_req_seq_id | String(64) | 原交易请求流水号 |
| close_stat | String(1) | 关单状态：P=处理中、S=成功、F=失败 |
| org_trans_stat | String(1) | 原交易状态：P=处理中、S=成功、F=失败 |

## 完整 SDK 调用示例

```java
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentCloseRequest;
import com.huifu.bspay.sdk.opps.core.utils.DateTools;
import com.huifu.bspay.sdk.opps.core.utils.SequenceTools;

// 1. 构建请求
V2TradeHostingPaymentCloseRequest request = new V2TradeHostingPaymentCloseRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());
request.setReqSeqId(SequenceTools.getReqSeqId32());
request.setHuifuId("6666000123123123");
request.setOrgReqDate("20240514");                         // 原交易日期
request.setOrgReqSeqId("20240514165442868h32ss2g3s7vnxq"); // 原交易流水号

// 2. 发起请求
Map<String, Object> response = BasePayClient.request(request, false);

// 3. 处理响应
String respCode = (String) response.get("resp_code");
if ("00000000".equals(respCode)) {
    // 关单成功
}
```

## 请求 JSON 示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "req_date": "20240515",
        "req_seq_id": "20240515101010868close001",
        "huifu_id": "6666000109133323",
        "org_req_date": "20240514",
        "org_req_seq_id": "20240514165442868h32ss2g3s7vnxq"
    }
}
```

## 返回 JSON 示例

```json
{
    "data": {
        "resp_code": "00000000",
        "resp_desc": "处理成功",
        "huifu_id": "6666000109133323",
        "org_req_date": "20240514",
        "org_req_seq_id": "20240514165442868h32ss2g3s7vnxq",
        "trans_stat": "S"
    }
}
```

## 注意事项

1. **只能关闭未支付的订单**，已支付成功的订单无法关单，只能走退款流程
2. 关单前建议先调用**查询接口**确认订单状态，避免关闭已支付订单
3. 关单后用户将无法再对该订单进行支付
4. 如果用户在关单请求发出的同时完成了支付，以最终交易状态为准
5. `orgReqDate` 和 `orgReqSeqId` 来自预下单返回

## 补充返回参数（完整版）

官方文档完整同步返回字段：

| 参数 | 类型 | 说明 |
|------|------|------|
| org_trans_stat | String(1) | 原交易状态：P=处理中、S=成功、F=失败 |
| close_stat | String(1) | 关单状态：P=处理中、S=成功、F=失败 |

## 异步通知参数

关单结果可能通过异步通知回调：

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | 业务响应码 |
| resp_desc | String(512) | 响应描述 |
| huifu_id | String(32) | 商户号 |
| org_req_date | String(8) | 原交易请求日期 |
| org_req_seq_id | String(64) | 原交易请求流水号 |
| org_trans_stat | String(1) | 原交易状态 |
| close_stat | String(1) | 关单状态：S=成功、F=失败 |

## 常见错误码

| 返回码 | 说明 |
|-------|------|
| 00000000 | 处理成功 |
| 00000100 | 交易处理中 |
| 10000000 | 无效参数 |
| 10000015 | 不允许关闭一分钟以内的订单 |
| 99010003 | 交易不存在 |
| 30000001 | 原交易已终态，不允许关单 / 关单状态已终态 |
| 99999999 | 系统异常，请稍后重试 |
