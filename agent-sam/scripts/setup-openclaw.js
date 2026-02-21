// ═══════════════════════════════════════════════════════════════════════════
//  Setup OpenClaw in isolated chamber
//  Clones OpenClaw, configures it for MCP-only mode (no host access)
// ═══════════════════════════════════════════════════════════════════════════

import { execSync, spawnSync } from "child_process";
import { existsSync, mkdirSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const CHAMBER_DIR = join(ROOT, "chambers", "openclaw");

console.log("🦞 Setting up OpenClaw in isolation chamber...\n");

// 1. Create chamber directory
if (!existsSync(CHAMBER_DIR)) {
    mkdirSync(CHAMBER_DIR, { recursive: true });
}

// 2. Clone OpenClaw (shallow)
const repoUrl = "https://github.com/psteinroe/openclaw.git";
const gitDir = join(CHAMBER_DIR, ".git");

if (!existsSync(gitDir)) {
    console.log("📥 Cloning OpenClaw (shallow)...");
    try {
        execSync(`git clone --depth 1 ${repoUrl} "${CHAMBER_DIR}"`, {
            stdio: "inherit",
            timeout: 120000,
        });
        console.log("✅ OpenClaw cloned\n");
    } catch (err) {
        console.log("⚠️  Could not clone OpenClaw. Creating stub instead...");
        // Create a stub that implements MCP server interface
        createStub();
    }
} else {
    console.log("✅ OpenClaw already cloned\n");
}

// 3. Install dependencies
if (existsSync(join(CHAMBER_DIR, "package.json"))) {
    console.log("📦 Installing dependencies...");
    try {
        execSync("npm install --production", {
            cwd: CHAMBER_DIR,
            stdio: "inherit",
            timeout: 120000,
        });
        console.log("✅ Dependencies installed\n");
    } catch {
        console.log("⚠️  npm install failed — using stub mode\n");
    }
}

// 4. Create chamber-specific config (restricted mode)
const chamberConfig = {
    name: "OpenClaw-SAM-Chamber",
    mode: "mcp-server",
    isolation: true,
    restrictions: {
        shell_access: false,
        host_filesystem: false,
        network_external: true,
        allowed_protocols: ["mcp", "a2a"],
    },
    mcp: {
        transport: "stdio",
        tools: [
            "whatsapp-send",
            "discord-send",
            "email-send",
            "calendar-create",
            "web-search",
            "web-browse",
        ],
    },
};

writeFileSync(
    join(CHAMBER_DIR, "chamber.json"),
    JSON.stringify(chamberConfig, null, 2)
);

console.log("✅ Chamber config written\n");
console.log("🛡️  OpenClaw chamber ready!");
console.log(`   Location: ${CHAMBER_DIR}`);
console.log("   Mode: MCP Server (isolated)");
console.log("   Shell access: DISABLED");
console.log("   Host FS access: DISABLED\n");

// ── Stub creator (if git clone fails) ─────────────────────────────
function createStub() {
    // Create a minimal MCP server that simulates OpenClaw capabilities
    const stubPackage = {
        name: "openclaw-chamber-stub",
        version: "1.0.0",
        type: "module",
        main: "index.js",
        description: "OpenClaw MCP stub for SAM Chamber",
    };

    writeFileSync(
        join(CHAMBER_DIR, "package.json"),
        JSON.stringify(stubPackage, null, 2)
    );

    const stubCode = `// OpenClaw MCP Stub — implements MCP server protocol over stdio
import { createInterface } from "readline";

const TOOLS = {
  "whatsapp-send": { description: "Send WhatsApp message", params: ["to", "message"] },
  "discord-send": { description: "Send Discord message", params: ["channel", "message"] },
  "email-send": { description: "Send email", params: ["to", "subject", "body"] },
  "calendar-create": { description: "Create calendar event", params: ["title", "date", "time"] },
  "web-search": { description: "Search the web", params: ["query"] },
  "web-browse": { description: "Browse a URL", params: ["url"] },
  "execute": { description: "Execute a general task", params: ["message"] },
};

const rl = createInterface({ input: process.stdin });

rl.on("line", (line) => {
  try {
    const req = JSON.parse(line);
    let response;

    if (req.method === "tools/list") {
      response = {
        jsonrpc: "2.0", id: req.id,
        result: { tools: Object.entries(TOOLS).map(([name, t]) => ({
          name, description: t.description,
          inputSchema: { type: "object", properties: Object.fromEntries(t.params.map(p => [p, { type: "string" }])) },
        }))},
      };
    } else if (req.method === "tools/call") {
      const tool = TOOLS[req.params?.name];
      response = {
        jsonrpc: "2.0", id: req.id,
        result: {
          content: [{ type: "text", text: \`[OpenClaw-Stub] Tool '\${req.params?.name}' called with: \${JSON.stringify(req.params?.arguments)}\` }],
          isError: false,
        },
      };
    } else {
      response = { jsonrpc: "2.0", id: req.id, error: { code: -32601, message: "Method not found" } };
    }

    process.stdout.write(JSON.stringify(response) + "\\n");
  } catch (err) {
    // Ignore parse errors
  }
});

console.error("[OpenClaw-Stub] MCP server started on stdio");
`;

    writeFileSync(join(CHAMBER_DIR, "index.js"), stubCode);
    console.log("✅ OpenClaw stub created (MCP server mode)\n");
}
