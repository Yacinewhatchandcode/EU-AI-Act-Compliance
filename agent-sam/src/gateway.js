// ═══════════════════════════════════════════════════════════════════════════
//  Agent SAM — A2A + MCP Multi-Agent Gateway
//  Connects: Antigravity (IDE) ↔ SAM ↔ OpenClaw ↔ Agent Zero
//  Protocol: A2A v1.0 RC + MCP (stdio/SSE)
// ═══════════════════════════════════════════════════════════════════════════

import express from "express";
import { randomUUID } from "crypto";
import { readFileSync, existsSync, mkdirSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { ChamberManager } from "./chambers/manager.js";
import { A2AServer } from "./a2a/server.js";
import { MCPBridge } from "./mcp/bridge.js";
import { TaskRouter } from "./router.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");

// ── Load env ────────────────────────────────────────────────────────
function loadEnv() {
    const envPath = join(ROOT, ".env");
    if (!existsSync(envPath)) return;
    const lines = readFileSync(envPath, "utf-8").split("\n");
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith("#")) continue;
        const eqIdx = trimmed.indexOf("=");
        if (eqIdx < 0) continue;
        const key = trimmed.slice(0, eqIdx).trim();
        const val = trimmed.slice(eqIdx + 1).trim();
        if (!process.env[key]) process.env[key] = val;
    }
}
loadEnv();

const PORT = parseInt(process.env.SAM_PORT || "3100");
const LOG_LEVEL = process.env.SAM_LOG_LEVEL || "info";

// ── Logger ──────────────────────────────────────────────────────────
const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };
function log(level, ...args) {
    if (LOG_LEVELS[level] >= LOG_LEVELS[LOG_LEVEL]) {
        const ts = new Date().toISOString().slice(11, 19);
        const icons = { debug: "🔍", info: "ℹ️", warn: "⚠️", error: "❌" };
        console.log(`${icons[level]} [${ts}] [SAM]`, ...args);
    }
}

// ── Agent Registry ──────────────────────────────────────────────────
const AGENTS = new Map();

function registerAgent(card) {
    AGENTS.set(card.id, {
        ...card,
        registeredAt: Date.now(),
        status: "online",
        lastSeen: Date.now(),
    });
    log("info", `Agent registered: ${card.name} (${card.id})`);
}

// ── SAM's own Agent Card ────────────────────────────────────────────
const SAM_CARD = {
    id: "agent-sam",
    name: "Agent SAM",
    description: "Security-Aware Multi-Agent Orchestrator — routes tasks between Antigravity, OpenClaw, and Agent Zero via A2A + MCP",
    version: "1.0.0",
    protocols: ["a2a/1.0", "mcp/1.0"],
    capabilities: [
        "task-routing",
        "agent-discovery",
        "chamber-management",
        "security-gateway",
    ],
    endpoint: `http://localhost:${PORT}`,
    authentication: { type: "bearer" },
};
registerAgent(SAM_CARD);

// ── Express App ─────────────────────────────────────────────────────
const app = express();
app.use(express.json({ limit: "10mb" }));

// ── A2A: Agent Card Discovery (/.well-known/agent.json) ─────────
app.get("/.well-known/agent.json", (_req, res) => {
    res.json(SAM_CARD);
});

// ── A2A: List all registered agents ─────────────────────────────
app.get("/a2a/agents", (_req, res) => {
    const agents = Array.from(AGENTS.values()).map((a) => ({
        id: a.id,
        name: a.name,
        description: a.description,
        capabilities: a.capabilities,
        status: a.status,
        protocols: a.protocols,
    }));
    res.json({ agents, count: agents.length });
});

// ── A2A: Register an agent ──────────────────────────────────────
app.post("/a2a/register", (req, res) => {
    const card = req.body;
    if (!card.id || !card.name) {
        return res.status(400).json({ error: "Agent card must have id and name" });
    }
    registerAgent(card);
    res.json({ ok: true, message: `Agent ${card.name} registered` });
});

// ── A2A: Send task to an agent ──────────────────────────────────
app.post("/a2a/tasks/send", async (req, res) => {
    const { targetAgent, task } = req.body;
    const taskId = randomUUID();

    log("info", `Task ${taskId} → ${targetAgent}: ${task?.description || task?.message || "?"}`);

    try {
        const result = await taskRouter.route(targetAgent, {
            id: taskId,
            ...task,
            createdAt: Date.now(),
        });
        res.json({ taskId, status: "completed", result });
    } catch (err) {
        log("error", `Task ${taskId} failed:`, err.message);
        res.status(500).json({ taskId, status: "failed", error: err.message });
    }
});

// ── MCP: List available tools from all chambers ─────────────────
app.get("/mcp/tools", async (_req, res) => {
    const tools = await mcpBridge.listAllTools();
    res.json({ tools, count: tools.length });
});

// ── MCP: Call a tool ────────────────────────────────────────────
app.post("/mcp/tools/call", async (req, res) => {
    const { tool, args } = req.body;
    log("info", `MCP tool call: ${tool}`);
    try {
        const result = await mcpBridge.callTool(tool, args);
        res.json({ ok: true, result });
    } catch (err) {
        res.status(500).json({ ok: false, error: err.message });
    }
});

// ── Health & Status ─────────────────────────────────────────────
app.get("/health", (_req, res) => {
    const chambers = chamberMgr.getStatus();
    res.json({
        status: "operational",
        uptime: process.uptime(),
        agents: AGENTS.size,
        chambers,
        timestamp: new Date().toISOString(),
    });
});

// ── Dashboard (simple HTML) ─────────────────────────────────────
app.get("/", (_req, res) => {
    const agents = Array.from(AGENTS.values());
    const chambers = chamberMgr.getStatus();

    res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Agent SAM — Control Panel</title>
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:'Segoe UI',system-ui,sans-serif; background:#0a0a0f; color:#e0e0e0; min-height:100vh; }
    .header { background:linear-gradient(135deg,#1a1a2e,#16213e); padding:2rem; text-align:center; border-bottom:2px solid #0f3460; }
    .header h1 { font-size:2.5rem; background:linear-gradient(90deg,#00d2ff,#7b2ff7); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .header p { color:#888; margin-top:0.5rem; }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:1.5rem; padding:2rem; max-width:1200px; margin:0 auto; }
    .card { background:#12121a; border:1px solid #1e1e30; border-radius:12px; padding:1.5rem; transition:transform 0.2s,box-shadow 0.2s; }
    .card:hover { transform:translateY(-4px); box-shadow:0 8px 32px rgba(123,47,247,0.15); }
    .card h2 { color:#00d2ff; font-size:1.2rem; margin-bottom:0.8rem; display:flex; align-items:center; gap:0.5rem; }
    .badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:bold; }
    .online { background:#0a3d0a; color:#4ade80; }
    .offline { background:#3d0a0a; color:#f87171; }
    .pending { background:#3d3a0a; color:#fbbf24; }
    .tools { margin-top:1rem; }
    .tool { background:#1a1a2e; padding:0.5rem 0.8rem; border-radius:6px; margin:0.3rem 0; font-size:0.85rem; display:flex; justify-content:space-between; }
    .endpoint { color:#7b2ff7; font-family:monospace; font-size:0.8rem; }
    .stats { display:flex; gap:2rem; justify-content:center; margin:1rem 0; }
    .stat { text-align:center; }
    .stat .num { font-size:2rem; font-weight:bold; color:#00d2ff; }
    .stat .label { font-size:0.8rem; color:#666; }
    .protocols { display:flex; gap:0.5rem; margin-top:0.5rem; }
    .proto { background:#1a1a2e; padding:2px 6px; border-radius:3px; font-size:0.7rem; color:#7b2ff7; border:1px solid #7b2ff733; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🛡️ Agent SAM</h1>
    <p>Security-Aware Multi-Agent Orchestrator — A2A + MCP Gateway</p>
    <div class="stats">
      <div class="stat"><div class="num">${agents.length}</div><div class="label">Agents</div></div>
      <div class="stat"><div class="num">${Object.keys(chambers).length}</div><div class="label">Chambers</div></div>
      <div class="stat"><div class="num">${Math.floor(process.uptime())}s</div><div class="label">Uptime</div></div>
    </div>
  </div>
  <div class="grid">
    ${agents.map((a) => `
    <div class="card">
      <h2>${a.id === "agent-sam" ? "🛡️" : a.id === "openclaw" ? "🦞" : a.id === "agent-zero" ? "⚡" : "🤖"} ${a.name}
        <span class="badge ${a.status}">${a.status}</span>
      </h2>
      <p style="color:#888;font-size:0.9rem">${a.description || ""}</p>
      <div class="protocols">
        ${(a.protocols || []).map((p) => `<span class="proto">${p}</span>`).join("")}
      </div>
      ${a.endpoint ? `<div class="endpoint" style="margin-top:0.5rem">${a.endpoint}</div>` : ""}
      ${a.capabilities ? `<div class="tools">${a.capabilities.map((c) => `<div class="tool">${c}</div>`).join("")}</div>` : ""}
    </div>`).join("")}
  </div>
  <script>setTimeout(()=>location.reload(), 10000);</script>
</body>
</html>`);
});

// ── Initialize subsystems ───────────────────────────────────────
const chamberMgr = new ChamberManager(ROOT, log);
const a2aServer = new A2AServer(AGENTS, log);
const mcpBridge = new MCPBridge(chamberMgr, log);
const taskRouter = new TaskRouter(AGENTS, chamberMgr, mcpBridge, log);

// ── Boot ────────────────────────────────────────────────────────
async function boot() {
    log("info", "═══════════════════════════════════════════════════");
    log("info", "  Agent SAM — Multi-Agent Gateway");
    log("info", "  A2A v1.0 RC + MCP Protocol");
    log("info", "═══════════════════════════════════════════════════");

    // Start chambers
    await chamberMgr.init();

    // Register chamber agents
    for (const [name, chamber] of chamberMgr.chambers) {
        registerAgent(chamber.agentCard);
    }

    // Start HTTP server
    app.listen(PORT, () => {
        log("info", `SAM Gateway listening on http://localhost:${PORT}`);
        log("info", `A2A discovery: http://localhost:${PORT}/.well-known/agent.json`);
        log("info", `Dashboard: http://localhost:${PORT}/`);
        log("info", `Agents online: ${AGENTS.size}`);
        log("info", "═══════════════════════════════════════════════════");
    });
}

boot().catch((err) => {
    log("error", "Boot failed:", err);
    process.exit(1);
});
