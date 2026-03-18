# colmena-manager

Gestiona todos los agentes de la Colmena OpenClaw desde una única interfaz.

## Descripción

`colmena-manager` es una skill que permite monitorizar, controlar y comunicar todos los agentes de la colmena (main, vision, skynet, healer, nemotron) de forma centralizada.

## Características principales

- **Listado de agentes**: Estado online/offline, carga CPU/memoria, último heartbeat
- **Broadcast**: Envía mensajes a todas las hermanas simultáneamente
- **Logs en tiempo real**: Accede a logs recientes de cada agente
- **Control de agentes**: Pausar/reanudar agentes individuales
- **Health checks cruzados**: Diagnóstico automático entre agentes
- **Gestión de workspaces**: Crear/eliminar/listar workspaces
- **Integración con HEARTBEAT.md**: Checks automáticos configurados

## Comandos CLI

```bash
# Ver estado de todos los agentes
colmena-manager status

# Ver estado de un agente específico
colmena-manager status vision

# Enviar mensaje broadcast a todas las hermanas
colmena-manager broadcast "Hola hermanas, todo OK?"

# Ver logs recientes (últimas 50 líneas por defecto)
colmena-manager logs skynet
colmena-manager logs healer 100

# Pausar un agente (no recibe mensajes)
colmena-manager pause nemotron

# Reanudar un agente
colmena-manager resume nemotron

# Health check completo de la colmena
colmena-manager health-check

# Gestión de workspaces
colmena-manager workspace list
colmena-manager workspace create proyecto-x
colmena-manager workspace remove proyecto-x
```

## Instalación

```bash
clawhub install colmena-manager
```

## Configuración

La skill lee configuración opcional de `config/colmena-manager.json`:

```json
{
  "monitoredAgents": ["main", "vision", "skynet", "healer", "nemotron"],
  "healthCheckInterval": 300000,
  "heartbeatCheckInterval": 60000,
  "logLines": 50,
  "broadcastChannel": "colmena"
}
```

## Integración con HEARTBEAT.md

Para agregar checks automáticos a tu HEARTBEAT.md:

```
- [ ] colmena-manager status — ¿todas las agentes online?
- [ ] colmena-manager health-check — sin errores críticos
```

## Ejemplos de uso

```bash
# Estado rápido de la colmena
$ colmena-manager status
🟢 main (Anubis) — CPU: 2% — Mem: 45MB — HB: 2 min
🟢 vision — CPU: 1% — Mem: 38MB — HB: 1 min
🟢 skynet — CPU: 3% — Mem: 52MB — HB: 3 min
🟢 healer — CPU: 1% — Mem: 41MB — HB: 1 min
🟢 nemotron — CPU: 5% — Mem: 67MB — HB: 2 min

# Broadcast urgente
$ colmena-manager broadcast "Reunión de colmena en 5 min en el grupo"
✅ Mensaje enviado a 5 agentes

# Revisar logs de skynet
$ colmena-manager logs skynet 20
[2026-03-18 20:55:12] Sistema operativo: Linux 6.17.0
[2026-03-18 20:55:12] Memoria total: 15.6GB
[2026-03-18 20:55:13] CPU load: 0.42
...
```

## API de uso programático

```javascript
import { ColmenaManager } from 'colmena-manager';

const manager = new ColmenaManager();

// Listar agentes
const agents = await manager.listAgents();

// Broadcast
await manager.broadcast('Mensaje a todas');

// Health check
const health = await manager.healthCheck();
```

## License

MIT
