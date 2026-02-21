// ═══════════════════════════════════════════════════════════════════════════
//  Task Router — Intelligent routing between agents
//  Uses A2A discovery + capability matching to delegate work
// ═══════════════════════════════════════════════════════════════════════════

export class TaskRouter {
    constructor(agentRegistry, chamberMgr, mcpBridge, log) {
        this.agents = agentRegistry;
        this.chamberMgr = chamberMgr;
        this.mcpBridge = mcpBridge;
        this.log = log;
        this.taskLog = [];
    }

    async route(targetAgent, task) {
        const agent = this.agents.get(targetAgent);

        if (!agent) {
            // Try intelligent routing based on task content
            const bestAgent = this._findBestAgent(task);
            if (bestAgent) {
                this.log("info", `Auto-routed task to: ${bestAgent.name}`);
                return this._executeOnAgent(bestAgent.id, task);
            }
            throw new Error(`Agent '${targetAgent}' not found and no suitable agent available`);
        }

        return this._executeOnAgent(targetAgent, task);
    }

    _findBestAgent(task) {
        const message = (task.description || task.message || "").toLowerCase();

        // Scoring-based routing
        const scores = new Map();

        for (const [id, agent] of this.agents) {
            if (id === "agent-sam") continue; // SAM doesn't execute, it routes
            let score = 0;
            for (const cap of agent.capabilities || []) {
                const keywords = cap.split("-");
                for (const kw of keywords) {
                    if (message.includes(kw)) score += 10;
                }
            }
            if (score > 0) scores.set(id, { agent, score });
        }

        // Return highest scoring agent
        let best = null;
        let bestScore = 0;
        for (const [id, { agent, score }] of scores) {
            if (score > bestScore) {
                best = agent;
                bestScore = score;
            }
        }
        return best;
    }

    async _executeOnAgent(agentId, task) {
        const chamber = this.chamberMgr.getChamber(agentId);

        // Log the routing decision
        this.taskLog.push({
            taskId: task.id,
            agent: agentId,
            message: task.description || task.message,
            at: Date.now(),
        });

        if (!chamber || chamber.status === "not-installed") {
            return {
                status: "pending",
                message: `Agent ${agentId} is not installed yet. Run setup first.`,
                task: task,
            };
        }

        if (chamber.status !== "running") {
            return {
                status: "queued",
                message: `Agent ${agentId} is in ${chamber.status} state. Task queued.`,
                task: task,
            };
        }

        // Execute via MCP tool call
        const toolName = `${agentId}.execute`;
        try {
            const result = await this.mcpBridge.callTool(toolName, {
                message: task.description || task.message,
                ...task,
            });
            return { status: "completed", result };
        } catch (err) {
            return { status: "failed", error: err.message };
        }
    }
}
