// 火烧云预报查询与监控脚本
// 使用 JavaScript evaluate 方式操作 DOM，更通用

// ============ 配置 ============
const fs = require('fs');
const path = require('path');

// Skill 目录结构
const SKILL_DIR = path.dirname(__dirname);
const DATA_DIR = path.join(SKILL_DIR, 'data');
const CONFIG_FILE = path.join(SKILL_DIR, 'config', 'config.json');

// 读取配置文件（只包含通知配置）
let userConfig = {};
if (fs.existsSync(CONFIG_FILE)) {
  try {
    userConfig = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } catch (e) {
    console.warn('[sunsetbot-monitor] 配置文件读取失败，使用默认值');
  }
}

// 日志文件路径
const LOG_FILE = path.join(DATA_DIR, 'sunsetbot-monitor.log');

const CONFIG = {
  CITY: '深圳',  // 城市参数由 cron 或调用时传入
  SOURCE: 'GFS',  // 数据源参数由 cron 或调用时传入
  LOG_FILE: LOG_FILE,
  DEFAULT_USER_OPEN_ID: userConfig.userOpenId || '',
  NOTIFY_CHANNEL: userConfig.notifyChannel || 'feishu',
  
  getNotificationTitle(colorfulness) {
    if (colorfulness < 0.2) return null;
    if (colorfulness <= 0.5) return '【注意：明日中小烧】';
    if (colorfulness <= 1.0) return '【号外！中大烧】';
    if (colorfulness < 2.0) return '【大烧！大烧】';
    return '【世纪大烧！冲！冲！冲】';
  }
};

// ============ 使用 JavaScript evaluate 操作 DOM ============

// 选择日期类型
async function selectDateType(dateType) {
  // 日期类型映射（对应 select option 的 value）
  const dateTypeMap = {
    '今天日出': 'rise_1',
    '今天日落': 'set_1',
    '明天日出': 'rise_2',
    '明天日落': 'set_2'
  };
  
  const value = dateTypeMap[dateType] || dateType;
  
  await browser({
    action: 'act',
    profile: 'openclaw',
    request: {
      kind: 'evaluate',
      fn: `
        const select = document.querySelector('#event_selector');
        if (select) {
          select.value = '${value}';
          select.dispatchEvent(new Event('change', { bubbles: true }));
          'OK';
        } else {
          'ERROR: event_selector not found';
        }
      `
    }
  });
}

// 选择数据源
async function selectSource(source) {
  const sourceMap = {
    'GFS': 'GFS',
    'EC': 'EC',
    '数据源: GFS': 'GFS',
    '数据源: EC': 'EC'
  };
  
  const value = sourceMap[source] || source;
  
  await browser({
    action: 'act',
    profile: 'openclaw',
    request: {
      kind: 'evaluate',
      fn: `
        const select = document.querySelector('#model_selector');
        if (select) {
          select.value = '${value}';
          select.dispatchEvent(new Event('change', { bubbles: true }));
          'OK';
        } else {
          'ERROR: model_selector not found';
        }
      `
    }
  });
}

// 输入城市
async function inputCity(city) {
  await browser({
    action: 'act',
    profile: 'openclaw',
    request: {
      kind: 'evaluate',
      fn: `
        const input = document.querySelector('#city_input');
        if (input) {
          input.value = '${city}';
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
          'OK';
        } else {
          'ERROR: city_input not found';
        }
      `
    }
  });
}

// 点击搜索按钮
async function clickSearch() {
  await browser({
    action: 'act',
    profile: 'openclaw',
    request: {
      kind: 'evaluate',
      fn: `
        const btn = document.querySelector('#srch_btn');
        if (btn) {
          btn.click();
          'OK';
        } else {
          'ERROR: srch_btn not found';
        }
      `
    }
  });
}

// 读取结果
async function getResults() {
  const result = await browser({
    action: 'act',
    profile: 'openclaw',
    request: {
      kind: 'evaluate',
      fn: `
        const result = {};
        
        // 获取日期
        const dateEl = document.querySelector('.result-date, [class*="date"]');
        if (dateEl) result.date = dateEl.textContent;
        
        // 获取时间
        const timeEl = document.querySelector('.result-time, [class*="time"]');
        if (timeEl) result.time = timeEl.textContent;
        
        // 获取鲜艳度
        const colorEl = document.querySelector('[class*="colorfulness"], [class*="鲜艳度"]');
        if (colorEl) {
          const match = colorEl.textContent.match(/(\d+\.?\d*)/);
          if (match) result.colorfulness = parseFloat(match[1]);
        }
        
        // 获取气溶胶
        const aerosolEl = document.querySelector('[class*="aerosol"], [class*="气溶胶"]');
        if (aerosolEl) {
          const match = aerosolEl.textContent.match(/(\d+\.?\d*)/);
          if (match) result.aerosol = parseFloat(match[1]);
        }
        
        // 如果找不到特定元素，尝试获取整个页面文本
        if (!result.colorfulness) {
          const text = document.body.innerText;
          const colorMatch = text.match(/鲜艳度[：:\s]*(\d+\.?\d*)/);
          const aerosolMatch = text.match(/气溶胶[：:\s]*(\d+\.?\d*)/);
          if (colorMatch) result.colorfulness = parseFloat(colorMatch[1]);
          if (aerosolMatch) result.aerosol = parseFloat(aerosolMatch[1]);
        }
          
        JSON.stringify(result);
      `
    }
  });
  
  try {
    return JSON.parse(result || '{}');
  } catch (e) {
    return { colorfulness: 0, aerosol: 0 };
  }
}

// ============ 查询功能 ============
async function checkSunsetBot({ city = CONFIG.CITY, dateType, source = CONFIG.SOURCE }) {
  if (!dateType) {
    throw new Error('缺少 dateType 参数，请指定 明天日出 或 明天日落');
  }
  
  try {
    return await doQueryWithJS(city, dateType, source);
  } catch (error) {
    console.error('[sunsetbot-monitor] 查询失败: ' + error.message);
    throw error;
  }
}

async function doQueryWithJS(city, dateType, source) {
  // 导航到网站
  const navResult = await browser({ 
    action: 'navigate', 
    profile: 'openclaw', 
    targetUrl: 'https://sunsetbot.top/' 
  });
  const openedTabId = navResult.targetId;
  
  await new Promise(r => setTimeout(r, 2000));
  
  // 执行操作
  await selectDateType(dateType);
  await new Promise(r => setTimeout(r, 500));
  
  await selectSource(source);
  await new Promise(r => setTimeout(r, 500));
  
  await inputCity(city);
  await new Promise(r => setTimeout(r, 500));
  
  await clickSearch();
  await new Promise(r => setTimeout(r, 3000));
  
  // 获取结果
  const result = await getResults();
  
  // 关闭页签
  if (openedTabId) {
    await browser({ action: 'close', profile: 'openclaw', targetId: openedTabId });
  }
  
  return { 
    city, 
    type: dateType, 
    source, 
    colorfulness: result.colorfulness || 0, 
    aerosol: result.aerosol || 0 
  };
}

async function queryMultiple({ city, dateTypes = ['明天日出', '明天日落'], source }) {
  const results = [];
  for (const dateType of dateTypes) {
    const result = await checkSunsetBot({ city, dateType, source });
    results.push(result);
  }
  return results;
}

// ============ 日志功能（JSONL 格式）============
async function writeLog(results, error = null) {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  const now = new Date().toISOString().slice(0, 19).replace('T', ' ');
  let logLine;
  if (error) {
    logLine = JSON.stringify({ ts: now, level: 'error', message: error.message, city: results && results[0] ? results[0].city : null, type: results && results[0] ? results[0].type : null });
  } else if (results && results.length > 0) {
    for (const r of results) {
      const notifyTitle = CONFIG.getNotificationTitle(r.colorfulness);
      logLine = JSON.stringify({ ts: now, level: 'info', city: r.city, type: r.type, source: r.source, colorfulness: r.colorfulness, aerosol: r.aerosol, notified: notifyTitle ? true : false });
      fs.appendFileSync(CONFIG.LOG_FILE, logLine + '\n');
    }
    return;
  } else {
    logLine = JSON.stringify({ ts: now, level: 'warning', message: 'No results and no error' });
  }
  fs.appendFileSync(CONFIG.LOG_FILE, logLine + '\n');
}

// ============ 通知功能 - 飞书渠道 ============
async function sendViaFeishu(results, userOpenId = CONFIG.DEFAULT_USER_OPEN_ID) {
  if (!userOpenId || userOpenId === '你的飞书Open ID') {
    return { notified: false, reason: '未配置 userOpenId' };
  }
  
  let maxColorfulness = 0;
  let maxTitle = null;
  let maxCity = '';
  for (const r of results) {
    const title = CONFIG.getNotificationTitle(r.colorfulness);
    if (title && r.colorfulness > maxColorfulness) {
      maxColorfulness = r.colorfulness;
      maxTitle = title;
      maxCity = r.city;
    }
  }
  if (!maxTitle) {
    return { notified: false, reason: '没有达到通知阈值' };
  }
  let message = maxTitle + '\n\n🌅 ' + maxCity + ' 火烧云预报\n';
  for (const r of results) {
    const title = CONFIG.getNotificationTitle(r.colorfulness);
    message += '\n' + r.type + ':\n  鲜艳度: ' + r.colorfulness + '\n  气溶胶: ' + r.aerosol + '\n';
    if (title) message += '  ' + title + '\n';
  }
  await feishu_im_user_message({ action: 'send', receive_id_type: 'open_id', receive_id: userOpenId, msg_type: 'text', content: JSON.stringify({ text: message }) });
  return { notified: true, title: maxTitle };
}

// ============ 通知功能 - 通用接口 ============
async function sendNotification(results, userOpenId, channel = CONFIG.NOTIFY_CHANNEL) {
  switch (channel) {
    case 'feishu':
      return await sendViaFeishu(results, userOpenId);
    case 'telegram':
      console.log('[sunsetbot-monitor] Telegram 通知尚未实现');
      return { notified: false, reason: 'Telegram 渠道未实现' };
    case 'none':
      console.log('[sunsetbot-monitor] 通知已禁用');
      return { notified: false, reason: '通知已禁用' };
    default:
      console.warn('[sunsetbot-monitor] 未知通知渠道: ' + channel + '，使用飞书');
      return await sendViaFeishu(results, userOpenId);
  }
}

async function notify({ results, userOpenId, skipLog = false, skipNotify = false, error = null }) {
  const output = {};
  if (!skipLog) {
    await writeLog(results, error);
    output.logged = true;
  }
  if (!skipNotify && !error) {
    const notifyResult = await sendNotification(results, userOpenId);
    output.notified = notifyResult.notified;
    output.notifyReason = notifyResult.reason;
    output.notifyTitle = notifyResult.title;
  }
  return output;
}

// ============ 主入口 ============
async function handler(params) {
  const { city = CONFIG.CITY, dates = ['明天日出', '明天日落'], source = CONFIG.SOURCE, needNotify = false, userOpenId = CONFIG.DEFAULT_USER_OPEN_ID, dryRun = false } = params;
  
  // 检查通知配置
  if (needNotify && (!userOpenId || userOpenId === '你的飞书Open ID')) {
    console.warn('[sunsetbot-monitor] 警告：needNotify=true 但未配置有效的 userOpenId，请在 config/config.json 中配置你的飞书 Open ID');
  }
  
  let queryError = null;
  let results = [];
  try {
    console.log('[sunsetbot-monitor] 查询 ' + city + '，日期: ' + dates.join(', ') + '，数据源: ' + source);
    results = await queryMultiple({ city, dateTypes: dates, source });
  } catch (error) {
    queryError = error;
    console.error('[sunsetbot-monitor] 查询失败: ' + error.message);
  }
  let response = { city, error: queryError ? queryError.message : null, results: results.map ? results.map(r => ({ type: r.type, colorfulness: r.colorfulness, aerosol: r.aerosol, level: CONFIG.getNotificationTitle(r.colorfulness) || '无烧' })) : [] };
  if (needNotify && !dryRun) {
    const notifyResult = await notify({ results, userOpenId, skipLog: false, skipNotify: false, error: queryError });
    response.notification = { logged: notifyResult.logged, notified: notifyResult.notified, reason: notifyResult.notifyReason, title: notifyResult.notifyTitle, error: queryError ? queryError.message : null };
  }
  let text = '';
  if (queryError) {
    text = '⚠️ 查询出错\n\n' + queryError.message + '\n\n日志已记录';
  } else {
    text = '🌅 ' + response.city + ' 火烧云预报\n';
    for (const r of response.results) {
      text += '\n' + r.type + ':\n  鲜艳度: ' + r.colorfulness + '\n  气溶胶: ' + r.aerosol + '\n  级别: ' + r.level + '\n';
    }
    if (needNotify && response.notification) {
      if (response.notification.notified) {
        text += '\n✅ 已发送通知: ' + response.notification.title;
      } else {
        text += '\nℹ️ 未达到通知阈值（< 0.2）';
      }
      text += '\n📝 日志已记录';
    }
  }
  response.text = text;
  return response;
}

// 支持命令行调用
if (typeof require !== 'undefined' && require.main === module) {
  const args = process.argv.slice(2);
  const params = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--city') params.city = args[++i];
    else if (args[i] === '--dateType') params.dateType = args[++i];
    else if (args[i] === '--source') params.source = args[++i];
    else if (args[i] === '--needNotify') params.needNotify = true;
    else if (args[i] === '--userOpenId') params.userOpenId = args[++i];
    else if (args[i] === '--dryRun') params.dryRun = true;
  }
  handler(params).then(result => { console.log(JSON.stringify(result, null, 2)); }).catch(err => { console.error(err); process.exit(1); });
}

module.exports = { handler, CONFIG };