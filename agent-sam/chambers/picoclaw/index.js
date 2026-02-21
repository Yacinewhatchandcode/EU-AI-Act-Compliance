// ═══════════════════════════════════════════════════════════════════════════
//  PicoClaw Chamber — Ultra-lightweight AI agent (<10MB)
//  MCP server stub implementing PicoClaw's core capabilities
//  In production: replace with the real picoclaw binary
// ═══════════════════════════════════════════════════════════════════════════

import { createInterface } from "readline";

const TOOLS = {
    "chat": {
        description: "Chat with PicoClaw AI",
        params: { message: "string" },
    },
    "web-search": {
        description: "Search the web (lightweight)",
        params: { query: "string" },
    },
    "summarize": {
        description: "Summarize text or URL content",
        params: { text: "string" },
    },
    "translate": {
        description: "Translate text between languages",
        params: { text: "string", from: "string", to: "string" },
    },
    "remind": {
        description: "Set a reminder",
        params: { message: "string", when: "string" },
    },
    "note": {
        description: "Save a note to local memory",
        params: { title: "string", content: "string" },
    },
    "execute": {
        description: "Execute a general task",
        params: { message: "string" },
    },
};

const memory = new Map();

const rl = createInterface({ input: process.stdin });

rl.on("line", (line) => {
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
            if (toolName === "note") {
                memory.set(args.title || "untitled", args.content || "");
                text = `📝 Note saved: "${args.title}" (${memory.size} notes total)`;
            } else if (toolName === "remind") {
                text = `⏰ Reminder set: "${args.message}" at ${args.when}`;
            } else {
                text = `[PicoClaw] ${toolName}: ${JSON.stringify(args)}`;
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

console.error("[PicoClaw-MCP] Ultra-lightweight server started on stdio (<10MB footprint)");
