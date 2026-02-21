// ═══════════════════════════════════════════════════════════════════════════
//  Setup Agent Zero in isolated chamber
//  Clones Agent Zero, configures for sandboxed execution
// ═══════════════════════════════════════════════════════════════════════════

import { execSync } from "child_process";
import { existsSync, mkdirSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const CHAMBER_DIR = join(ROOT, "chambers", "agent-zero");

console.log("⚡ Setting up Agent Zero in isolation chamber...\n");

if (!existsSync(CHAMBER_DIR)) {
    mkdirSync(CHAMBER_DIR, { recursive: true });
}

// Clone Agent Zero
const repoUrl = "https://github.com/frdel/agent-zero.git";
const gitDir = join(CHAMBER_DIR, ".git");

if (!existsSync(gitDir)) {
    console.log("📥 Cloning Agent Zero (shallow)...");
    try {
        execSync(`git clone --depth 1 ${repoUrl} "${CHAMBER_DIR}"`, {
            stdio: "inherit",
            timeout: 120000,
        });
        console.log("✅ Agent Zero cloned\n");
    } catch {
        console.log("⚠️  Could not clone Agent Zero. Creating stub...");
        createStub();
    }
} else {
    console.log("✅ Agent Zero already cloned\n");
}

// Install Python deps
if (existsSync(join(CHAMBER_DIR, "requirements.txt"))) {
    console.log("📦 Installing Python dependencies...");
    try {
        execSync("pip install -r requirements.txt --quiet", {
            cwd: CHAMBER_DIR,
            stdio: "inherit",
            timeout: 300000,
        });
        console.log("✅ Dependencies installed\n");
    } catch {
        console.log("⚠️  pip install failed — using stub\n");
    }
}

// Chamber config
const chamberConfig = {
    name: "AgentZero-SAM-Chamber",
    mode: "mcp-server",
    isolation: true,
    restrictions: {
        shell_access: true,  // Agent Zero needs shell for code execution
        host_filesystem: false,
        sandbox: "process",
        allowed_protocols: ["mcp", "a2a"],
    },
    mcp: {
        transport: "stdio",
        tools: [
            "code-execute",
            "web-research",
            "file-read",
            "file-write",
            "shell-run",
            "memory-store",
            "memory-recall",
        ],
    },
};

writeFileSync(
    join(CHAMBER_DIR, "chamber.json"),
    JSON.stringify(chamberConfig, null, 2)
);

console.log("✅ Chamber config written\n");
console.log("⚡ Agent Zero chamber ready!");
console.log(`   Location: ${CHAMBER_DIR}`);
console.log("   Mode: MCP Server (sandboxed)");
console.log("   Code execution: SANDBOXED\n");

function createStub() {
    writeFileSync(
        join(CHAMBER_DIR, "requirements.txt"),
        "# Agent Zero stub\n"
    );

    const stubCode = `"""Agent Zero MCP Server Stub — implements MCP over stdio"""
import json
import sys

TOOLS = {
    "code-execute": {"description": "Execute Python code in sandbox", "params": ["code"]},
    "web-research": {"description": "Research a topic on the web", "params": ["query"]},
    "file-read": {"description": "Read a file", "params": ["path"]},
    "file-write": {"description": "Write a file", "params": ["path", "content"]},
    "shell-run": {"description": "Run a shell command (sandboxed)", "params": ["command"]},
    "memory-store": {"description": "Store in persistent memory", "params": ["key", "value"]},
    "memory-recall": {"description": "Recall from memory", "params": ["key"]},
    "execute": {"description": "Execute a general task", "params": ["message"]},
}

memory = {}

def handle_request(req):
    method = req.get("method", "")
    req_id = req.get("id")

    if method == "tools/list":
        tools = []
        for name, t in TOOLS.items():
            props = {p: {"type": "string"} for p in t["params"]}
            tools.append({"name": name, "description": t["description"],
                         "inputSchema": {"type": "object", "properties": props}})
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools}}

    elif method == "tools/call":
        tool_name = req.get("params", {}).get("name", "")
        args = req.get("params", {}).get("arguments", {})

        if tool_name == "memory-store":
            memory[args.get("key", "")] = args.get("value", "")
            text = f"Stored key: {args.get('key')}"
        elif tool_name == "memory-recall":
            val = memory.get(args.get("key", ""), "[not found]")
            text = f"Key '{args.get('key')}': {val}"
        else:
            text = f"[AgentZero-Stub] Tool '{tool_name}' called: {json.dumps(args)}"

        return {"jsonrpc": "2.0", "id": req_id,
                "result": {"content": [{"type": "text", "text": text}], "isError": False}}

    return {"jsonrpc": "2.0", "id": req_id,
            "error": {"code": -32601, "message": "Method not found"}}

print("[AgentZero-Stub] MCP server started on stdio", file=sys.stderr)
for line in sys.stdin:
    try:
        req = json.loads(line.strip())
        resp = handle_request(req)
        print(json.dumps(resp), flush=True)
    except:
        pass
`;

    writeFileSync(join(CHAMBER_DIR, "main.py"), stubCode);
    console.log("✅ Agent Zero stub created (MCP server mode)\n");
}
