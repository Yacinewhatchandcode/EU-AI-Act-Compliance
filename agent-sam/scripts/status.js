// ═══════════════════════════════════════════════════════════════════════════
//  Status checker — show all agents and chambers
// ═══════════════════════════════════════════════════════════════════════════

import { existsSync, readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");

const AGENTS = [
    {
        id: "agent-sam",
        name: "🛡️  Agent SAM",
        type: "orchestrator",
        location: ROOT,
        check: () => existsSync(join(ROOT, "src", "gateway.js")),
    },
    {
        id: "openclaw",
        name: "🦞 OpenClaw",
        type: "chamber",
        location: join(ROOT, "chambers", "openclaw"),
        check: () =>
            existsSync(join(ROOT, "chambers", "openclaw", "index.js")) ||
            existsSync(join(ROOT, "chambers", "openclaw", "package.json")),
    },
    {
        id: "agent-zero",
        name: "⚡ Agent Zero",
        type: "chamber",
        location: join(ROOT, "chambers", "agent-zero"),
        check: () =>
            existsSync(join(ROOT, "chambers", "agent-zero", "main.py")) ||
            existsSync(join(ROOT, "chambers", "agent-zero", "requirements.txt")),
    },
];

console.log("\n═══════════════════════════════════════════════════");
console.log("  Agent SAM — System Status");
console.log("═══════════════════════════════════════════════════\n");

for (const agent of AGENTS) {
    const installed = agent.check();
    const icon = installed ? "✅" : "❌";
    const status = installed ? "INSTALLED" : "NOT INSTALLED";
    console.log(`  ${agent.name}`);
    console.log(`    ${icon} Status: ${status}`);
    console.log(`    📂 Location: ${agent.location}`);
    console.log(`    🔌 Type: ${agent.type}`);

    if (installed && existsSync(join(agent.location, "chamber.json"))) {
        const config = JSON.parse(readFileSync(join(agent.location, "chamber.json"), "utf-8"));
        console.log(`    🔒 Isolation: ${config.isolation ? "YES" : "NO"}`);
        console.log(`    🛠️  Tools: ${config.mcp?.tools?.length || 0}`);
    }
    console.log();
}

console.log("═══════════════════════════════════════════════════");
console.log("  To install agents:");
console.log("    npm run setup:openclaw");
console.log("    npm run setup:agent-zero");
console.log("  To start SAM gateway:");
console.log("    npm start");
console.log("═══════════════════════════════════════════════════\n");
