# 🐺 Colmena Manager Skill

Skill para gestionar todos los agentes de la Colmena OpenClaw desde una única interfaz.

## Características

- 🟢 Listar estado de agentes (online/offline, CPU, mem, heartbeat)
- 📢 Broadcast a todas las hermanas
- 📋 Ver logs de agentes
- ⏸️ Pausar/reanudar agentes
- 💓 Health checks automáticos
- 📁 Gestión de workspaces
- 🔗 Integración con HEARTBEAT.md

## Instalación

```bash
clawhub install colmena-manager
```

## Uso rápido

```bash
# Estado de toda la colmena
colmena-manager status

# Enviar mensaje a todas las agentes
colmena-manager broadcast "Hola hermanas!"

# Health check completo
colmena-manager health-check

# Ver logs de skynet
colmena-manager logs skynet 100
```

## Comandos

| Comando | Descripción |
|---------|-------------|
| `status [agent]` | Muestra estado de todos o un agente específico |
| `broadcast <msg>` | Envía mensaje a todas las agentes |
| `logs <agent> [lines]` | Muestra logs recientes del agente |
| `pause <agent>` | Pausa un agente |
| `resume <agent>` | Reanuda un agente pausado |
| `health-check` | Diagnóstico completo de la colmena |
| `workspace list` | Lista workspaces |
| `workspace create <name>` | Crea workspace nuevo |
| `workspace remove <name>` | Elimina workspace |

## Configuración

Opcional: crea `~/.openclaw/config/colmena-manager.json`:

```json
{
  "monitoredAgents": ["main", "vision", "skynet", "healer", "nemotron"],
  "healthCheckInterval": 300000,
  "heartbeatCheckInterval": 60000,
  "logLines": 50,
  "healthCheckCommands": [
    "node -v",
    "openclaw status"
  ]
}
```

## Para desarrolladores

```bash
# Clonar y enlazar
cd colmena-manager
npm link

# Probar
colmena-manager status
```

## License

MIT © 2026 Anubis
