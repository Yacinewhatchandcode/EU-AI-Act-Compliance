// ═══════════════════════════════════════════════════════════════════════════
//  A2A Protocol Server — Agent-to-Agent Communication (v1.0 RC)
//  Implements: Discovery, Handshake, Task Sending, Streaming
// ═══════════════════════════════════════════════════════════════════════════

export class A2AServer {
    constructor(agentRegistry, log) {
        this.agents = agentRegistry;
        this.log = log;
        this.tasks = new Map();
    }

    // ── Discovery: Find agent by capability ─────────────────────────
    findAgentByCapability(capability) {
        for (const [id, agent] of this.agents) {
            if (agent.capabilities?.includes(capability)) {
                return agent;
            }
        }
        return null;
    }

    // ── Discovery: Find agent by name or ID ─────────────────────────
    findAgent(query) {
        // Direct ID match
        if (this.agents.has(query)) return this.agents.get(query);
        // Name match (case-insensitive)
        for (const [id, agent] of this.agents) {
            if (agent.name.toLowerCase().includes(query.toLowerCase())) {
                return agent;
            }
        }
        return null;
    }

    // ── Route: Determine which agent should handle a task ───────────
    routeTask(task) {
        const message = (task.description || task.message || "").toLowerCase();

        // OpenClaw routing keywords
        const openclawKeywords = [
            "whatsapp", "discord", "telegram", "email", "calendar",
            "notify", "message", "send", "schedule", "reminder",
        ];

        // Agent Zero routing keywords
        const agentZeroKeywords = [
            "research", "code", "execute", "analyze", "browse",
            "search web", "find information", "run script",
        ];

        for (const kw of openclawKeywords) {
            if (message.includes(kw)) return "openclaw";
        }

        for (const kw of agentZeroKeywords) {
            if (message.includes(kw)) return "agent-zero";
        }

        // Default: SAM handles it
        return "agent-sam";
    }

    // ── Task lifecycle ──────────────────────────────────────────────
    createTask(id, payload) {
        const task = {
            id,
            status: "submitted",
            payload,
            createdAt: Date.now(),
            updatedAt: Date.now(),
            result: null,
            artifacts: [],
            history: [{ status: "submitted", at: Date.now() }],
        };
        this.tasks.set(id, task);
        return task;
    }

    updateTask(id, status, result = null) {
        const task = this.tasks.get(id);
        if (!task) return null;
        task.status = status;
        task.updatedAt = Date.now();
        task.history.push({ status, at: Date.now() });
        if (result) task.result = result;
        return task;
    }

    getTask(id) {
        return this.tasks.get(id);
    }
}
