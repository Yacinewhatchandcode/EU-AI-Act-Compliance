// ═══════════════════════════════════════════════════════════════════════════
//  Antigravity → SAM MCP Client
//  Allows calling any agent's tools from the terminal (or me)
//  Usage: node sam-cli.js <tool> [args as JSON]
//  Example: node sam-cli.js openclaw.discord-send '{"channel":"#general","message":"Hello!"}'
// ═══════════════════════════════════════════════════════════════════════════

const SAM_URL = process.env.SAM_URL || "http://localhost:3100";

const args = process.argv.slice(2);
const command = args[0] || "status";

async function call(path, method = "GET", body = null) {
    const opts = {
        method,
        headers: { "Content-Type": "application/json" },
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(`${SAM_URL}${path}`, opts);
    return res.json();
}

async function main() {
    switch (command) {
        case "status":
        case "health": {
            const health = await call("/health");
            console.log("\n🛡️  Agent SAM — Status");
            console.log("═".repeat(50));
            console.log(`  Status: ${health.status}`);
            console.log(`  Uptime: ${Math.floor(health.uptime)}s`);
            console.log(`  Agents: ${health.agents}`);
            console.log("\n  Chambers:");
            for (const [id, c] of Object.entries(health.chambers || {})) {
                const icon = c.status === "running" ? "✅" : "❌";
                console.log(`    ${icon} ${c.name} — ${c.status} (PID: ${c.pid || "N/A"}, port: ${c.port})`);
            }
            console.log();
            break;
        }

        case "agents": {
            const data = await call("/a2a/agents");
            console.log("\n🤖 Registered Agents");
            console.log("═".repeat(50));
            for (const a of data.agents) {
                const icon = a.status === "online" ? "✅" : "⭕";
                console.log(`  ${icon} ${a.name} (${a.id})`);
                console.log(`     ${a.description}`);
                console.log(`     Capabilities: ${(a.capabilities || []).join(", ")}`);
                console.log();
            }
            break;
        }

        case "tools": {
            const data = await call("/mcp/tools");
            console.log("\n🛠️  Available MCP Tools");
            console.log("═".repeat(50));
            const grouped = {};
            for (const t of data.tools) {
                if (!grouped[t.chamber]) grouped[t.chamber] = [];
                grouped[t.chamber].push(t);
            }
            for (const [chamber, tools] of Object.entries(grouped)) {
                console.log(`\n  📦 ${chamber}:`);
                for (const t of tools) {
                    console.log(`    • ${t.name} — ${t.description}`);
                }
            }
            console.log(`\n  Total: ${data.count} tools\n`);
            break;
        }

        case "call": {
            const toolName = args[1];
            const toolArgs = args[2] ? JSON.parse(args[2]) : {};
            if (!toolName) {
                console.log("Usage: sam-cli call <tool-name> [args-json]");
                process.exit(1);
            }
            console.log(`\n🔧 Calling tool: ${toolName}`);
            const result = await call("/mcp/tools/call", "POST", { tool: toolName, args: toolArgs });
            console.log("Result:", JSON.stringify(result, null, 2));
            break;
        }

        case "send": {
            const target = args[1];
            const message = args.slice(2).join(" ");
            if (!target || !message) {
                console.log("Usage: sam-cli send <agent-id> <message>");
                process.exit(1);
            }
            console.log(`\n📨 Sending task to ${target}: "${message}"`);
            const result = await call("/a2a/tasks/send", "POST", {
                targetAgent: target,
                task: { description: message, message },
            });
            console.log("Result:", JSON.stringify(result, null, 2));
            break;
        }

        case "discover": {
            const card = await call("/.well-known/agent.json");
            console.log("\n🔍 A2A Agent Card");
            console.log("═".repeat(50));
            console.log(JSON.stringify(card, null, 2));
            break;
        }

        default:
            console.log(`
🛡️  SAM CLI — Agent Command Center
═══════════════════════════════════════════════

  Usage: node sam-cli.js <command> [args]

  Commands:
    status              Show gateway health & chamber status
    agents              List all registered agents
    tools               List all available MCP tools
    call <tool> [json]  Call a specific MCP tool
    send <agent> <msg>  Send a task to an agent via A2A
    discover            Show SAM's A2A agent card

  Examples:
    node sam-cli.js status
    node sam-cli.js tools
    node sam-cli.js call sam.list_agents
    node sam-cli.js call openclaw.discord-send '{"channel":"#general","message":"Hello!"}'
    node sam-cli.js send openclaw "Notify team on Discord: deployment complete"
    node sam-cli.js send agent-zero "Research best practices for MCP security"
`);
    }
}

main().catch((err) => {
    console.error("❌ Error:", err.message);
    process.exit(1);
});
