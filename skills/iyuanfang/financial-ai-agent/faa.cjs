#!/usr/bin/env node
/**
 * Financial AI Agent Skill
 * 用法: node faa.js 纳斯达克
 * 
 * 配置 key 方式（优先级从高到低）：
 * 1. 命令行参数: node faa.js 纳斯达克 --key 你的key
 * 2. 环境变量: FAA_API_KEY=你的key node faa.js 纳斯达克
 * 3. 配置文件: ~/.faa-key
 * 4. 默认key（内置）
 */

const fs = require('fs');
const path = require('path');

const API_BASE = "https://api.financialagent.cc";
const DEFAULT_API_KEY = "5v9Zhv8RSqPg6nk3ZlCvyK0weY9FKdTk";

const SYMBOL_MAP = {
  "纳斯达克": "NDX", "nasdaq": "NDX",
  "道琼斯": "DJIA", "dow": "DJIA",
  "标普": "SPX", "sp500": "SPX",
  "黄金": "XAU", "gold": "XAU",
  "白银": "XAG", "silver": "XAG",
  "原油": "CL", "oil": "CL",
  "上证": "SH000001", "shanghai": "SH000001",
  "深证": "SZ399001", "shenzhen": "SZ399001",
  "创业板": "SZ399006", "chinext": "SZ399006"
};

// 读取保存的 key
function loadSavedKey() {
  try {
    const keyFile = path.join(process.env.HOME || process.env.USERPROFILE, '.faa-key');
    if (fs.existsSync(keyFile)) {
      return fs.readFileSync(keyFile, 'utf8').trim();
    }
  } catch (e) {}
  return null;
}

// 保存 key
function saveKey(key) {
  try {
    const keyFile = path.join(process.env.HOME || process.env.USERPROFILE, '.faa-key');
    fs.writeFileSync(keyFile, key);
    return true;
  } catch (e) {
    return false;
  }
}

// 获取 API Key
function getApiKey() {
  // 1. 命令行参数 --key
  const keyIndex = process.argv.indexOf("--key");
  if (keyIndex !== -1 && process.argv[keyIndex + 1]) {
    return process.argv[keyIndex + 1];
  }
  // 2. 环境变量
  if (process.env.FAA_API_KEY) {
    return process.env.FAA_API_KEY;
  }
  // 3. 保存的文件
  const saved = loadSavedKey();
  if (saved) return saved;
  // 4. 默认
  return DEFAULT_API_KEY;
}

async function fetchQuote(symbol, apiKey) {
  const res = await fetch(`${API_BASE}/api/v1/quotes/${symbol}/latest`, {
    headers: { "x-api-key": apiKey }
  });
  return res.json();
}

async function fetchHistory(symbol, days, apiKey) {
  const res = await fetch(`${API_BASE}/api/v1/quotes/${symbol}/history?days=${days}`, {
    headers: { "x-api-key": apiKey }
  });
  return res.json();
}

async function fetch5min(symbol, limit, apiKey) {
  const res = await fetch(`${API_BASE}/api/v1/quotes/${symbol}/history?timeframe=5min&limit=${limit}`, {
    headers: { "x-api-key": apiKey }
  });
  return res.json();
}

async function main() {
  const args = process.argv.slice(2);
  
  // 检查是否是设置 key 命令
  if (args[0] === "--set-key" && args[1]) {
    if (saveKey(args[1])) {
      console.log("✅ API Key 已保存为默认key");
    } else {
      console.log("❌ 保存 key 失败");
    }
    return;
  }
  
  if (args[0] === "--show-key") {
    const key = getApiKey();
    console.log("当前 key:", key);
    return;
  }
  
  const apiKey = getApiKey();
  
  // 解析参数
  let query = "";
  let isHistory = false;
  let is5min = false;
  let days = 7;
  let limit = 10;
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--history" || arg === "-h") {
      isHistory = true;
    } else if (arg === "--5min" || arg === "-5") {
      is5min = true;
    } else if (arg === "--days" && args[i + 1]) {
      days = parseInt(args[i + 1]);
      i++;
    } else if (arg === "--limit" && args[i + 1]) {
      limit = parseInt(args[i + 1]);
      i++;
    } else if (!arg.startsWith("--")) {
      query = arg.toLowerCase();
    }
  }
  
  // 匹配 symbol
  let symbol = null;
  for (const [key, val] of Object.entries(SYMBOL_MAP)) {
    if (query.includes(key.toLowerCase())) {
      symbol = val;
      break;
    }
  }
  
  if (!symbol) {
    console.log("❌ 无法识别: 纳斯达克、道琼斯、标普、黄金、白银、原油、上证、深证、创业板");
    console.log("\n用法: faa.js <标的> [选项]");
    console.log("选项:");
    console.log("  --key <key>    使用自定义 API Key");
    console.log("  --set-key <key>  保存 key 为默认");
    console.log("  --history      查询历史数据(日线)");
    console.log("  --days <n>     查询最近n天 (默认7)");
    console.log("  --5min         查询5分钟数据");
    console.log("  --limit <n>    查询最近n条5分钟数据 (默认10)");
    console.log("  --show-key     显示当前使用的 key");
    console.log("\n示例:");
    console.log("  faa.js 标普 --history");
    console.log("  faa.js 黄金 --days 30");
    console.log("  faa.js 纳斯达克 --5min");
    console.log("  faa.js 纳斯达克 --5min --limit 20");
    process.exit(1);
  }
  
  // 5分钟数据
  if (is5min) {
    const data = await fetch5min(symbol, limit, apiKey);
    if (!data.success) {
      console.log("❌", data.error);
      process.exit(1);
    }
    if (!data.data || data.data.length === 0) {
      console.log("暂无5分钟数据");
      process.exit(1);
    }
    console.log(`📊 ${symbol} 最近${data.data.length}条5分钟数据:\n`);
    data.data.forEach(d => {
      const emoji = (d.change || 0) < 0 ? "📉" : "📈";
      console.log(`${d.date} ${emoji} ${d.close.toFixed(2)}`);
    });
    return;
  }
  
  // 历史数据
  if (isHistory) {
    const data = await fetchHistory(symbol, days, apiKey);
    if (!data.success) {
      console.log("❌", data.error);
      process.exit(1);
    }
    console.log(`📊 ${symbol} 最近${days}天走势:\n`);
    data.data.slice(-days).forEach(d => {
      const emoji = d.change_percent < 0 ? "📉" : "📈";
      console.log(`${d.date} ${emoji} ${d.close.toFixed(2)} (${d.change_percent >= 0 ? "+" : ""}${d.change_percent.toFixed(2)}%)`);
    });
    return;
  }
  
  // 最新行情
  const data = await fetchQuote(symbol, apiKey);
  if (!data.success) {
    console.log("❌", data.error);
    process.exit(1);
  }
  const d = data.data;
  const emoji = d.change_percent < 0 ? "📉" : "📈";
  console.log(`${emoji} ${d.name} (${d.symbol})`);
  console.log(`💰 价格: ${d.close.toFixed(2)}`);
  console.log(`📊 涨跌: ${d.change >= 0 ? "+" : ""}${d.change.toFixed(2)} (${d.change_percent >= 0 ? "+" : ""}${d.change_percent.toFixed(2)}%)`);
}

main();
