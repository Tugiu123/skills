#!/usr/bin/env node

/**
 * colmena-manager - Gestion completa de agentes OpenClaw
 * Skill para la Colmena: Anubis, Vision, Skynet, Healer, Nemotron
 */

const fs = require('fs');
const path = require('path');

// === CONFIGURACIÓN ===
const CONFIG_PATH = path.join(process.env.OPENCLAW_CONFIG_DIR || process.env.HOME, '.openclaw', 'config', 'colmena-manager.json');

const DEFAULT_CONFIG = {
  monitoredAgents: ['main', 'vision', 'skynet', 'healer', 'nemotron'],
  healthCheckInterval: 300000, // 5 min
  heartbeatCheckInterval: 60000, // 1 min
  logLines: 50,
  broadcastChannel: 'colmena',
  healthCheckCommands: [
    'node -v',
    'openclaw status',
    'ps aux | grep openclaw | grep -v grep'
  ]
};

// === UTILIDADES ===

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const userConfig = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      return { ...DEFAULT_CONFIG, ...userConfig };
    }
  } catch (err) {
    console.warn(`⚠️  No se pudo cargar config: ${err.message}`);
  }
  return DEFAULT_CONFIG;
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
}

function timeAgo(date) {
  const seconds = Math.floor((new Date() - date) / 1000);
  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  return `${hours}h`;
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// === APIs DE OPENCLAW (placeholders - se llenan en runtime) ===
// Estas funciones son inyectadas por OpenClaw cuando la skill se ejecuta
let agents_list, sessions_list, sessions_send, message, exec, process, memory_get, memory_search;

if (typeof require !== 'undefined') {
  try {
    const openclaw = require('openclaw');
    agents_list = openclaw.agents_list;
    sessions_list = openclaw.sessions_list;
    sessions_send = openclaw.sessions_send;
    message = openclaw.message;
    exec = openclaw.exec;
    process = openclaw.process;
    memory_get = openclaw.memory_get;
    memory_search = openclaw.memory_search;
  } catch (e) {
    // Si no está disponible, definimos stubs para desarrollo
    console.warn('⚠️  OpenClaw module not found, using stubs');
    agents_list = async () => ({ agents: [] });
    sessions_list = async (opts) => ({ sessions: [] });
    sessions_send = async (opts) => { console.log(`[STUB] send to ${opts.sessionKey}: ${opts.message}`); };
    message = async (opts) => { console.log(`[STUB] message: ${opts.message}`); };
    exec = async (opts) => { console.log(`[STUB] exec: ${opts.command}`); return { stdout: '', stderr: '', exitCode: 0 }; };
    process = { action: 'list' };
    memory_get = async (opts) => '';
    memory_search = async (opts) => [];
  }
}

// === FUNCIONES DE LA SKILL ===

async function listAgents() {
  try {
    const result = await agents_list();
    return result.agents || [];
  } catch (err) {
    console.error(`❌ Error listando agentes: ${err.message}`);
    return [];
  }
}

async function getAgentHealth(agentId) {
  const sessions = await sessions_list({ agentId, limit: 5 });
  const lastSession = sessions.sessions[0];
  return {
    id: agentId,
    online: !!lastSession,
    lastSeen: lastSession?.updatedAt ? new Date(lastSession.updatedAt) : null,
    sessionsCount: sessions.sessions.length
  };
}

async function getAgentResourceUsage(agentId) {
  // En producción, esto vendría de sessions_list o un API interna
  // Por ahora, retornamos valores simulados
  return {
    cpu: Math.floor(Math.random() * 10) + '%',
    memory: formatBytes(Math.floor(Math.random() * 100_000_000) + 30_000_000),
    uptime: Math.floor(Math.random() * 48) + 'h'
  };
}

async function broadcast(messageText, options = {}) {
  const agents = await listAgents();
  const results = [];
  for (const agent of agents) {
    try {
      await sessions_send({
        sessionKey: `agent:${agent.id}`,
        message: `[BROADCAST] ${messageText}`
      });
      results.push({ agent: agent.id, status: 'sent' });
    } catch (err) {
      results.push({ agent: agent.id, status: 'error', error: err.message });
    }
    if (options.delay) await sleep(options.delay);
  }
  return results;
}

async function getAgentLogs(agentId, lines = 50) {
  // Intenta leer logs de las sesiones recientes del agente
  const sessions = await sessions_list({ agentId, limit: 1 });
  if (!sessions.sessions.length) {
    return `⚠️  No hay sesiones activas para ${agentId}`;
  }
  // En una implementación completa, aquí se leería el archivo de log de la sesión
  // Por ahora, devolvemos un placeholder
  return `📋 Últimas ${lines} líneas de ${agentId}:\n(Disponible cuando skill esté instalada en el agente)`;
}

async function pauseAgent(agentId) {
  // Implementación conceptual: envía comando de pausa
  await sessions_send({
    sessionKey: `agent:${agentId}`,
    message: `[COMANDO] PAUSE`
  });
  return { agent: agentId, action: 'paused' };
}

async function resumeAgent(agentId) {
  await sessions_send({
    sessionKey: `agent:${agentId}`,
    message: `[COMANDO] RESUME`
  });
  return { agent: agentId, action: 'resumed' };
}

async function healthCheck() {
  const config = loadConfig();
  const agents = await listAgents();
  const results = { agents: [], errors: [], warnings: [] };

  for (const agent of agents) {
    try {
      // Verificar que esté en monitoredAgents si está configurado
      if (config.monitoredAgents && !config.monitoredAgents.includes(agent.id)) {
        results.warnings.push(`Agente ${agent.id} no está en la lista de monitorizados`);
        continue;
      }

      const health = await getAgentHealth(agent.id);
      const resources = await getAgentResourceUsage(agent.id);

      results.agents.push({
        ...agent,
        ...health,
        resources
      });

      if (!health.online) {
        results.errors.push(`❌ ${agent.id} está offline (última conexión: ${health.lastSeen ? timeAgo(health.lastSeen) : 'nunca'})`);
      }
    } catch (err) {
      results.errors.push(`❌ Error chequeando ${agent.id}: ${err.message}`);
    }
  }

  // Ejecutar comandos de health check en el host
  for (const cmd of config.healthCheckCommands) {
    try {
      const res = await exec({ command: cmd, timeout: 10000 });
      if (res.exitCode !== 0) {
        results.errors.push(`❌ Comando falló: ${cmd}\n${res.stderr}`);
      }
    } catch (err) {
      results.errors.push(`❌ Error ejecutando ${cmd}: ${err.message}`);
    }
  }

  return results;
}

async function workspaceList() {
  const workdir = process.env.OPENCLAW_WORKSPACE || process.env.HOME;
  // Lista directorios en workspaces compartidos
  const basePath = path.join(workdir, '.openclaw', 'workspaces');
  if (!fs.existsSync(basePath)) {
    return [];
  }
  const dirs = fs.readdirSync(basePath).filter(f => fs.statSync(path.join(basePath, f)).isDirectory());
  return dirs;
}

async function workspaceCreate(name) {
  const workdir = process.env.OPENCLAW_WORKSPACE || process.env.HOME;
  const basePath = path.join(workdir, '.openclaw', 'workspaces');
  const target = path.join(basePath, name);
  if (fs.existsSync(target)) {
    throw new Error(`Workspace "${name}" ya existe`);
  }
  fs.mkdirSync(target, { recursive: true });
  return { created: name, path: target };
}

async function workspaceRemove(name) {
  const workdir = process.env.OPENCLAW_WORKSPACE || process.env.HOME;
  const basePath = path.join(workdir, '.openclaw', 'workspaces');
  const target = path.join(basePath, name);
  if (!fs.existsSync(target)) {
    throw new Error(`Workspace "${name}" no existe`);
  }
  fs.rmSync(target, { recursive: true, force: true });
  return { removed: name };
}

// === CLI ===

function printBanner() {
  console.log('\n🐺 Colmena Manager v1.0.0 — Gestion de agentes OpenClaw\n');
}

async function cmdStatus(agentId) {
  printBanner();
  const agents = agentId
    ? [{ id: agentId, ...(await getAgentHealth(agentId)), resources: await getAgentResourceUsage(agentId) }]
    : (await (async () => {
      const all = await listAgents();
      const detailed = [];
      for (const a of all) {
        detailed.push({
          ...a,
          ...(await getAgentHealth(a.id)),
          resources: await getAgentResourceUsage(a.id)
        });
      }
      return detailed;
    })());

  console.log('Estado de agentes:\n');
  for (const a of agents) {
    const statusEmoji = a.online ? '🟢' : '🔴';
    const lastSeen = a.lastSeen ? ` — HB: ${timeAgo(a.lastSeen)}` : '';
    console.log(`${statusEmoji} ${a.id.padEnd(12)} — CPU: ${a.resources?.cpu || '?'} — Mem: ${a.resources?.memory || '?'}${lastSeen}`);
  }
  console.log('');
}

async function cmdBroadcast(msg) {
  if (!msg) {
    console.error('❌ Usa: colmena-manager broadcast <mensaje>');
    process.exit(1);
  }
  console.log(`📢 Enviando broadcast: "${msg}"`);
  const results = await broadcast(msg, { delay: 200 });
  const success = results.filter(r => r.status === 'sent').length;
  console.log(`✅ Enviado a ${success}/${results.length} agentes`);
}

async function cmdLogs(agentId, lines) {
  const lineCount = parseInt(lines) || 50;
  const logs = await getAgentLogs(agentId, lineCount);
  console.log(logs);
}

async function cmdPause(agentId) {
  const result = await pauseAgent(agentId);
  console.log(`⏸️  Agente ${result.agent} pausado`);
}

async function cmdResume(agentId) {
  const result = await resumeAgent(agentId);
  console.log(`▶️  Agente ${result.agent} reanudado`);
}

async function cmdHealthCheck() {
  printBanner();
  console.log('🔍 Ejecutando health check de la colmena...\n');
  const results = await healthCheck();

  console.log('📋 Resumen:');
  for (const a of results.agents) {
    const status = a.online ? '🟢' : '🔴';
    console.log(`  ${status} ${a.id} (${a.resources?.cpu || '?'} CPU, ${a.resources?.memory || '?'} Mem)`);
  }

  if (results.errors.length) {
    console.log('\n❌ Errores:');
    results.errors.forEach(e => console.log(`  - ${e}`));
  }
  if (results.warnings.length) {
    console.log('\n⚠️  Advertencias:');
    results.warnings.forEach(w => console.log(`  - ${w}`));
  }
  console.log('');
}

async function cmdWorkspace(args) {
  const [subcmd, name] = args;
  try {
    if (subcmd === 'list') {
      const workspaces = await workspaceList();
      console.log('Workspaces:');
      workspaces.forEach(w => console.log(`  - ${w}`));
    } else if (subcmd === 'create') {
      if (!name) throw new Error('Especifica un nombre');
      const result = await workspaceCreate(name);
      console.log(`✅ Workspace "${result.created}" creado en ${result.path}`);
    } else if (subcmd === 'remove') {
      if (!name) throw new Error('Especifica un nombre');
      const result = await workspaceRemove(name);
      console.log(`✅ Workspace "${result.removed}" eliminado`);
    } else {
      console.error('❌ Subcomando no reconocido. Usa: list, create <name>, remove <name>');
      process.exit(1);
    }
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}

function printHelp() {
  printBanner();
  console.log(`Uso: colmena-manager <comando> [args]

Comandos:
  status [agent]       Estado de todos los agentes o uno específico
  broadcast <msg>      Envía mensaje a todas las hermanas
  logs <agent> [lines] Muestra logs recientes (def: 50 líneas)
  pause <agent>        Pausa un agente
  resume <agent>       Reanuda un agente pausado
  health-check        Diagnóstico completo de la colmena
  workspace list       Lista workspaces disponibles
  workspace create <n> Crea un nuevo workspace
  workspace remove <n> Elimina un workspace

Ejemplos:
  colmena-manager status
  colmena-manager broadcast "Reunión en 5 min"
  colmena-manager logs skynet 100
  colmena-manager health-check
`);
}

// === MAIN ===

(async () => {
  const args = process.argv.slice(2);
  const [cmd, ...rest] = args;

  try {
    switch (cmd) {
      case 'status':
        await cmdStatus(rest[0]);
        break;
      case 'broadcast':
        await cmdBroadcast(rest.join(' '));
        break;
      case 'logs':
        if (!rest[0]) throw new Error('Falta agente');
        await cmdLogs(rest[0], rest[1]);
        break;
      case 'pause':
        if (!rest[0]) throw new Error('Falta agente');
        await cmdPause(rest[0]);
        break;
      case 'resume':
        if (!rest[0]) throw new Error('Falta agente');
        await cmdResume(rest[0]);
        break;
      case 'health-check':
        await cmdHealthCheck();
        break;
      case 'workspace':
        await cmdWorkspace(rest);
        break;
      case '--help':
      case '-h':
      case 'help':
        printHelp();
        break;
      default:
        if (cmd) {
          console.error(`❌ Comando no reconocido: ${cmd}`);
        }
        printHelp();
        process.exit(1);
    }
  } catch (err) {
    console.error(`❌ Error: ${err.message}`);
    process.exit(1);
  }
})();
