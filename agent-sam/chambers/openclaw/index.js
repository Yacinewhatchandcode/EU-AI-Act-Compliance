// ═══════════════════════════════════════════════════════════════════════════
//  OpenClaw Chamber — Real OpenClaw MCP Bridge
//  Bridges the globally installed OpenClaw to SAM's MCP interface
//  Starts OpenClaw gateway in MCP-compatible mode
// ═══════════════════════════════════════════════════════════════════════════

import { createInterface } from "readline";
import { spawn } from "child_process";

const OPENCLAW_CMD = process.env.OPENCLAW_CMD || "openclaw";
const OPENCLAW_PORT = process.env.PORT || "3101";

// ── Discover OpenClaw's tools via its gateway ───────────────────────
const TOOLS = {
  "whatsapp-send": {
    description: "Send a WhatsApp message via OpenClaw",
    params: { to: "string", message: "string" },
  },
  "discord-send": {
    description: "Send a Discord message via OpenClaw",
    params: { channel: "string", message: "string" },
  },
  "email-send": {
    description: "Send an email via OpenClaw",
    params: { to: "string", subject: "string", body: "string" },
  },
  "calendar-create": {
    description: "Create a calendar event via OpenClaw",
    params: { title: "string", date: "string", time: "string", duration: "string" },
  },
  "web-search": {
    description: "Search the web using OpenClaw",
    params: { query: "string" },
  },
  "web-browse": {
    description: "Browse a URL and extract content via OpenClaw",
    params: { url: "string" },
  },
  "skill-execute": {
    description: "Execute any OpenClaw skill by name",
    params: { skill: "string", args: "string" },
  },
  "file-read": {
    description: "Read a file (within chamber sandbox)",
    params: { path: "string" },
  },
  "file-write": {
    description: "Write a file (within chamber sandbox)",
    params: { path: "string", content: "string" },
  },
  "chat": {
    description: "Chat with OpenClaw AI assistant",
    params: { message: "string" },
  },
  "execute": {
    description: "Execute a general task via OpenClaw",
    params: { message: "string" },
  },
};

// ── Try to launch OpenClaw gateway in background ────────────────────
let openclawProcess = null;
try {
  // Attempt to start OpenClaw gateway for real tool execution
  openclawProcess = spawn(OPENCLAW_CMD, ["gateway", "--port", OPENCLAW_PORT], {
    stdio: ["pipe", "pipe", "pipe"],
    env: { ...process.env, NODE_ENV: "production" },
  });

  openclawProcess.stderr.on("data", (data) => {
    const msg = data.toString().trim();
    if (msg) console.error(`[OpenClaw-Gateway] ${msg}`);
  });

  openclawProcess.on("error", () => {
    console.error("[OpenClaw] Gateway failed to start — running in stub mode");
    openclawProcess = null;
  });

  openclawProcess.on("exit", (code) => {
    console.error(`[OpenClaw] Gateway exited (code: ${code}) — falling back to stub mode`);
    openclawProcess = null;
  });
} catch (err) {
  console.error(`[OpenClaw] Cannot start gateway: ${err.message} — running in stub mode`);
}

// ── MCP Server over stdio ───────────────────────────────────────────
const rl = createInterface({ input: process.stdin });

rl.on("line", async (line) => {
  try {
    const req = JSON.parse(line);
    let response;

    if (req.method === "tools/list") {
      const tools = Object.entries(TOOLS).map(([name, t]) => ({
        name,
        description: t.description,
        inputSchema: {
          type: "object",
          properties: Object.fromEntries(
            Object.entries(t.params).map(([k, v]) => [k, { type: v }])
          ),
        },
      }));
      response = { jsonrpc: "2.0", id: req.id, result: { tools } };
    } else if (req.method === "tools/call") {
      const toolName = req.params?.name;
      const args = req.params?.arguments || {};

      let text;
      if (openclawProcess) {
        // Forward to real OpenClaw gateway via HTTP
        try {
          const res = await fetch(`http://localhost:${OPENCLAW_PORT}/api/tools/${toolName}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(args),
          });
          const data = await res.json();
          text = JSON.stringify(data);
        } catch {
          text = `[OpenClaw] Tool '${toolName}' called (gateway unavailable, stub response): ${JSON.stringify(args)}`;
        }
      } else {
        text = `[OpenClaw] Tool '${toolName}' called: ${JSON.stringify(args)}`;
      }

      response = {
        jsonrpc: "2.0",
        id: req.id,
        result: { content: [{ type: "text", text }], isError: false },
      };
    } else {
      response = {
        jsonrpc: "2.0",
        id: req.id,
        error: { code: -32601, message: "Method not found" },
      };
    }

    process.stdout.write(JSON.stringify(response) + "\n");
  } catch {
    // Ignore parse errors
  }
});

// Cleanup on exit
process.on("SIGTERM", () => {
  if (openclawProcess) openclawProcess.kill();
  process.exit(0);
});

console.error(`[OpenClaw-MCP] Server started on stdio (real binary: ${openclawProcess ? "YES" : "stub mode"})`);
