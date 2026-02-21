// ═══════════════════════════════════════════════════════════════════════════
//  MCP Bridge — Model Context Protocol client for chamber agents
//  Exposes chamber tools as MCP-compatible endpoints
// ═══════════════════════════════════════════════════════════════════════════

export class MCPBridge {
    constructor(chamberMgr, log) {
        this.chamberMgr = chamberMgr;
        this.log = log;
        this.toolRegistry = new Map();

        // Built-in SAM tools
        this._registerBuiltinTools();
    }

    _registerBuiltinTools() {
        const builtins = [
            {
                name: "sam.list_agents",
                description: "List all registered agents and their status",
                chamber: "agent-sam",
                inputSchema: { type: "object", properties: {} },
                handler: async () => {
                    const agents = [];
                    const mgr = this.chamberMgr;
                    for (const [id, chamber] of mgr.chambers) {
                        agents.push({
                            id,
                            name: chamber.config.name,
                            status: chamber.status,
                            port: chamber.config.port,
                        });
                    }
                    return { agents };
                },
            },
            {
                name: "sam.route_task",
                description: "Route a task to the best-suited agent",
                chamber: "agent-sam",
                inputSchema: {
                    type: "object",
                    properties: {
                        message: { type: "string", description: "Task description" },
                    },
                    required: ["message"],
                },
                handler: async (args) => {
                    return { message: args.message, routed: true, note: "Task queued for routing" };
                },
            },
            {
                name: "sam.chamber_status",
                description: "Get the status of all isolation chambers",
                chamber: "agent-sam",
                inputSchema: { type: "object", properties: {} },
                handler: async () => {
                    return this.chamberMgr.getStatus();
                },
            },
        ];

        for (const tool of builtins) {
            this.toolRegistry.set(tool.name, tool);
        }
    }

    // ── Register tools from a chamber agent ─────────────────────────
    registerChamberTools(chamberId, tools) {
        for (const tool of tools) {
            const namespaced = `${chamberId}.${tool.name}`;
            this.toolRegistry.set(namespaced, {
                ...tool,
                name: namespaced,
                chamber: chamberId,
            });
            this.log("debug", `Tool registered: ${namespaced}`);
        }
    }

    // ── List all available tools ────────────────────────────────────
    async listAllTools() {
        const tools = [];
        for (const [name, tool] of this.toolRegistry) {
            tools.push({
                name,
                description: tool.description,
                chamber: tool.chamber,
                inputSchema: tool.inputSchema,
            });
        }

        // Also add chamber-declared tools
        for (const [id, chamber] of this.chamberMgr.chambers) {
            if (chamber.agentCard?.capabilities) {
                for (const cap of chamber.agentCard.capabilities) {
                    const toolName = `${id}.${cap}`;
                    if (!this.toolRegistry.has(toolName)) {
                        tools.push({
                            name: toolName,
                            description: `${chamber.config.name} capability: ${cap}`,
                            chamber: id,
                            inputSchema: {
                                type: "object",
                                properties: {
                                    message: { type: "string" },
                                },
                            },
                        });
                    }
                }
            }
        }
        return tools;
    }

    // ── Call a tool ─────────────────────────────────────────────────
    async callTool(toolName, args = {}) {
        const tool = this.toolRegistry.get(toolName);

        if (tool?.handler) {
            // Built-in tool with handler
            return await tool.handler(args);
        }

        // Forward to chamber via its process stdin (MCP stdio transport)
        const [chamberId] = toolName.split(".");
        const chamber = this.chamberMgr.getChamber(chamberId);

        if (!chamber) {
            throw new Error(`No chamber found for tool: ${toolName}`);
        }

        if (chamber.status !== "running") {
            throw new Error(`Chamber ${chamberId} is not running (status: ${chamber.status})`);
        }

        // MCP JSON-RPC over stdio
        const request = {
            jsonrpc: "2.0",
            id: Date.now(),
            method: "tools/call",
            params: { name: toolName.replace(`${chamberId}.`, ""), arguments: args },
        };

        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => reject(new Error("Tool call timeout")), 30000);

            const onData = (data) => {
                try {
                    const response = JSON.parse(data.toString());
                    clearTimeout(timeout);
                    chamber.process.stdout.removeListener("data", onData);
                    if (response.error) reject(new Error(response.error.message));
                    else resolve(response.result);
                } catch {
                    // Not JSON yet, wait for more data
                }
            };

            chamber.process.stdout.on("data", onData);
            chamber.process.stdin.write(JSON.stringify(request) + "\n");
        });
    }
}
