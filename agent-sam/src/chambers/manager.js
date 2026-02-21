// ═══════════════════════════════════════════════════════════════════════════
//  Chamber Manager — Manages isolated agent processes
//  Each chamber is a sandboxed child process with limited capabilities
// ═══════════════════════════════════════════════════════════════════════════

import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync } from "fs";
import { join } from "path";

export class ChamberManager {
    constructor(rootDir, log) {
        this.rootDir = rootDir;
        this.log = log;
        this.chambers = new Map();
        this.chambersDir = join(rootDir, "chambers");
    }

    async init() {
        if (!existsSync(this.chambersDir)) mkdirSync(this.chambersDir, { recursive: true });

        // Auto-discover chambers
        const openclawEnabled = process.env.OPENCLAW_ENABLED === "true";
        const agentZeroEnabled = process.env.AGENT_ZERO_ENABLED === "true";
        const picoClawEnabled = process.env.PICOCLAW_ENABLED === "true";

        if (openclawEnabled) {
            await this.registerChamber("openclaw", {
                name: "OpenClaw",
                type: "openclaw",
                port: parseInt(process.env.OPENCLAW_PORT || "3101"),
                home: process.env.OPENCLAW_HOME || join(this.chambersDir, "openclaw"),
                transport: process.env.OPENCLAW_MCP_TRANSPORT || "stdio",
            });
        }

        if (agentZeroEnabled) {
            await this.registerChamber("agent-zero", {
                name: "Agent Zero",
                type: "agent-zero",
                port: parseInt(process.env.AGENT_ZERO_PORT || "3102"),
                home: process.env.AGENT_ZERO_HOME || join(this.chambersDir, "agent-zero"),
                transport: "stdio",
            });
        }

        if (picoClawEnabled) {
            await this.registerChamber("picoclaw", {
                name: "PicoClaw",
                type: "picoclaw",
                port: parseInt(process.env.PICOCLAW_PORT || "3103"),
                home: process.env.PICOCLAW_HOME || join(this.chambersDir, "picoclaw"),
                transport: "stdio",
            });
        }

        this.log("info", `Chambers initialized: ${this.chambers.size}`);
    }

    async registerChamber(id, config) {
        const chamberDir = config.home;
        if (!existsSync(chamberDir)) mkdirSync(chamberDir, { recursive: true });

        const chamber = {
            id,
            config,
            process: null,
            status: "registered",
            agentCard: this._buildAgentCard(id, config),
            tools: [],
        };

        this.chambers.set(id, chamber);
        this.log("info", `Chamber registered: ${config.name} (${id}) — isolation: process`);

        // Try to start the chamber
        try {
            await this._startChamber(id);
        } catch (err) {
            this.log("warn", `Chamber ${id} not started (will start on demand): ${err.message}`);
            chamber.status = "standby";
        }
    }

    _buildAgentCard(id, config) {
        const cards = {
            openclaw: {
                id: "openclaw",
                name: "OpenClaw 🦞",
                description: "Autonomous AI agent — messaging, email, calendar, web automation, 100+ skills. Isolated in SAM chamber.",
                version: "2026.2",
                protocols: ["mcp/1.0", "a2a/1.0"],
                capabilities: [
                    "whatsapp-messaging",
                    "discord-messaging",
                    "email-send",
                    "calendar-manage",
                    "web-browse",
                    "file-manage",
                    "skill-execute",
                ],
                endpoint: `http://localhost:${config.port}`,
                authentication: { type: "bearer" },
                isolation: "process-sandbox",
            },
            "agent-zero": {
                id: "agent-zero",
                name: "Agent Zero ⚡",
                description: "Autonomous coding & research agent — self-correcting, tool-using, Docker-native. Isolated in SAM chamber.",
                version: "0.8.0",
                protocols: ["mcp/1.0", "a2a/1.0"],
                capabilities: [
                    "code-execution",
                    "web-research",
                    "file-system",
                    "shell-commands",
                    "self-correction",
                    "memory-persistent",
                ],
                endpoint: `http://localhost:${config.port}`,
                authentication: { type: "bearer" },
                isolation: "process-sandbox",
            },
            picoclaw: {
                id: "picoclaw",
                name: "PicoClaw 🐾",
                description: "Ultra-lightweight AI agent (<10MB) — chat, search, summarize, translate, reminders. Runs on minimal hardware.",
                version: "0.1.2",
                protocols: ["mcp/1.0", "a2a/1.0"],
                capabilities: [
                    "chat",
                    "web-search",
                    "summarize",
                    "translate",
                    "remind",
                    "note",
                ],
                endpoint: `http://localhost:${config.port}`,
                authentication: { type: "bearer" },
                isolation: "process-sandbox",
            },
        };
        return cards[id] || { id, name: config.name, protocols: ["mcp/1.0"] };
    }

    async _startChamber(id) {
        const chamber = this.chambers.get(id);
        if (!chamber) throw new Error(`Chamber ${id} not found`);

        const config = chamber.config;
        const chamberDir = config.home;

        // Check if the agent runtime is installed
        const hasPackage = existsSync(join(chamberDir, "package.json"));
        const hasPython = existsSync(join(chamberDir, "requirements.txt"));

        if (!hasPackage && !hasPython) {
            chamber.status = "not-installed";
            this.log("info", `Chamber ${id}: agent not installed yet — run 'npm run setup:${id}' to install`);
            return;
        }

        // Start as a child process with restricted env
        const env = {
            ...process.env,
            // Isolation: don't inherit sensitive host vars
            HOME: chamberDir,
            USERPROFILE: chamberDir,
            NODE_ENV: "production",
            // Chamber-specific port
            PORT: String(config.port),
            // Restrict network (conceptual — real isolation needs Docker)
            CHAMBER_ID: id,
            CHAMBER_ISOLATION: "true",
        };

        // Remove host secrets from chamber env
        delete env.SAM_SECRET;
        delete env.GITHUB_TOKEN;
        delete env.GH_TOKEN;

        this.log("info", `Starting chamber ${id} on port ${config.port}...`);

        if (hasPackage) {
            chamber.process = spawn("node", ["index.js"], {
                cwd: chamberDir,
                env,
                stdio: ["pipe", "pipe", "pipe"],
            });
        } else if (hasPython) {
            chamber.process = spawn("python", ["main.py"], {
                cwd: chamberDir,
                env,
                stdio: ["pipe", "pipe", "pipe"],
            });
        }

        if (chamber.process) {
            chamber.status = "running";

            chamber.process.stdout.on("data", (data) => {
                this.log("debug", `[${id}] ${data.toString().trim()}`);
            });

            chamber.process.stderr.on("data", (data) => {
                this.log("warn", `[${id}] ${data.toString().trim()}`);
            });

            chamber.process.on("exit", (code) => {
                chamber.status = "stopped";
                this.log("info", `Chamber ${id} exited with code ${code}`);
            });

            this.log("info", `Chamber ${id} started (PID: ${chamber.process.pid})`);
        }
    }

    async stopChamber(id) {
        const chamber = this.chambers.get(id);
        if (chamber?.process) {
            chamber.process.kill("SIGTERM");
            chamber.status = "stopped";
            this.log("info", `Chamber ${id} stopped`);
        }
    }

    getStatus() {
        const status = {};
        for (const [id, chamber] of this.chambers) {
            status[id] = {
                name: chamber.config.name,
                status: chamber.status,
                port: chamber.config.port,
                isolation: "process-sandbox",
                pid: chamber.process?.pid || null,
            };
        }
        return status;
    }

    getChamber(id) {
        return this.chambers.get(id);
    }
}
