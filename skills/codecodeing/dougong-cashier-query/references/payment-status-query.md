## 目录

- [接口概述](#接口概述)
- [SDK Request 类字段](#sdk-request-类字段)
- [返回参数](#返回参数)
- [完整 SDK 调用示例](#完整-sdk-调用示例)
- [请求 JSON 示例](#请求-json-示例)
- [返回 JSON 示例](#返回-json-示例)
- [注意事项](#注意事项)
- [补充返回参数](#补充返回参数完整版)

# 托管交易查询

## 接口概述

| 属性 | 值 |
|-----|-----|
| 汇付 API 端点 | `v2/trade/hosting/payment/queryorderinfo` |
| 请求方式 | POST |
| SDK Request 类 | `V2TradeHostingPaymentQueryorderinfoRequest` |
| 建议业务接口 | `POST /hfpay/queryorderinfo` |

## SDK Request 类字段

`V2TradeHostingPaymentQueryorderinfoRequest` 的专属字段：

| 字段 | setter 方法 | 类型 | 必填 | 说明 |
|------|-----------|------|------|------|
| reqDate | setReqDate() | String(8) | Y | **本次查询**的请求日期（SDK 自动生成） |
| reqSeqId | setReqSeqId() | String(64) | Y | **本次查询**的请求流水号（SDK 自动生成） |
| huifuId | setHuifuId() | String(32) | C | 商户号（与 partyOrderId 二选一） |
| orgReqDate | setOrgReqDate() | String(8) | C | **原交易**的请求日期（与 partyOrderId 二选一） |
| orgReqSeqId | setOrgReqSeqId() | String(64) | C | **原交易**的请求流水号（与 partyOrderId 二选一） |
| partyOrderId | setPartyOrderId() | String(64) | N | 用户账单上的商户订单号（可选查询条件） |

> **注意**：`orgReqDate` 和 `orgReqSeqId` 二选一即可查询，但建议两个都传以确保精确匹配。也可以使用 `partyOrderId` 查询。

## 返回参数

| 参数 | 类型 | 说明 |
|------|------|------|
| resp_code | String(8) | `00000000` 表示查询成功 |
| resp_desc | String(128) | 响应描述 |
| huifu_id | String(32) | 商户号 |
| trans_stat | String(1) | **交易状态**：P=处理中、S=成功、F=失败 |
| trans_amt | String(12) | 交易金额 |
| org_req_date | String(8) | 原交易请求日期 |
| org_req_seq_id | String(64) | 原交易请求流水号 |
| org_hf_seq_id | String(128) | 汇付全局流水号 |
| out_trans_id | String(64) | 用户账单上的交易订单号 |
| party_order_id | String(64) | 用户账单上的商户订单号 |
| pay_type | String(16) | 交易类型（T_JSAPI、T_MINIAPP、A_JSAPI 等） |
| trans_time | String(14) | 交易时间 yyyyMMddHHmmss |
| fee_amt | String(14) | 手续费金额（元） |



## 完整 SDK 调用示例

```java
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.request.V2TradeHostingPaymentQueryorderinfoRequest;
import com.huifu.bspay.sdk.opps.core.utils.DateTools;
import com.huifu.bspay.sdk.opps.core.utils.SequenceTools;

// 1. 构建请求
V2TradeHostingPaymentQueryorderinfoRequest request = new V2TradeHostingPaymentQueryorderinfoRequest();
request.setReqDate(DateTools.getCurrentDateYYYYMMDD());  // 本次查询的日期
request.setReqSeqId(SequenceTools.getReqSeqId32());      // 本次查询的流水号
request.setHuifuId("6666000123123123");                   // 商户号
request.setOrgReqDate("20240514");                         // 原交易日期（来自预下单返回）
request.setOrgReqSeqId("20240514165442868h32ss2g3s7vnxq"); // 原交易流水号（来自预下单返回）

// 2. 发起请求
Map<String, Object> response = BasePayClient.request(request, false);

// 3. 处理响应
String respCode = (String) response.get("resp_code");
String transStat = (String) response.get("trans_stat");

if ("00000000".equals(respCode)) {
    switch (transStat) {
        case "S": // 支付成功
            break;
        case "F": // 支付失败
            break;
        case "P": // 处理中，稍后重试
            break;
    }
}
```

## 请求 JSON 示例

```json
{
    "sys_id": "6666000108840829",
    "product_id": "YYZY",
    "data": {
        "req_date": "20240515",
        "req_seq_id": "20240515101010868query001",
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
        "trans_stat": "S",
        "trans_amt": "1.00",
        "org_req_date": "20240514",
        "org_req_seq_id": "20240514165442868h32ss2g3s7vnxq",
        "hf_seq_id": "00470topo1A240514165442P090ac132fef00000",
        "trans_type": "T_MINIAPP",
        "end_time": "20240514170000"
    }
}
```

## 注意事项

1. `reqDate` 和 `reqSeqId` 是**本次查询请求**的日期和流水号，由系统自动生成
2. `orgReqDate` 和 `orgReqSeqId` 是**原交易**的日期和流水号，从预下单返回中获取
3. 建议在收到异步通知后调用查询接口做**二次确认**
4. `trans_stat = P` 时应稍后重试查询，不要直接判断为失败
5. 查询结果可能包含敏感信息，日志中避免打印完整响应体

## 补充返回参数（完整版）

以下为官方文档中额外返回的字段：

| 参数 | 类型 | 说明 |
|------|------|------|
| order_stat | String(1) | 预下单状态：1=已支付、2=支付中、3=已退款、4=处理中、5=失败、6=部分退款 |
| close_stat | String(1) | 关单状态：P=处理中、S=成功、F=失败 |
| pre_order_id | String(64) | 预下单订单号 |
| ref_amt | String(14) | 可退金额（元） |
| fee_flag | Int(1) | 手续费标识：1=外扣、2=内扣 |
| fee_amt | String(14) | 手续费金额（元） |
| wx_response | String(6000) | 微信返回的响应报文（JSON） |
| alipay_response | String(6000) | 支付宝返回的响应报文（JSON） |
| unionpay_response | String(6000) | 银联返回的响应报文（JSON） |
