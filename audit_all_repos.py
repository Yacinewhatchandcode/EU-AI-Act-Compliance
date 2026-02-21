#!/usr/bin/env python3
"""
COMPREHENSIVE REPO AUDIT
=========================
Scans all 21 GitHub repos for:
1. CYBERSECURITY — exposed secrets, API keys, tokens, hardcoded passwords
2. LEGALITY — LICENSE files, copyright, GDPR, data handling
3. COMPLETENESS — README, .gitignore, tests, CI/CD, dependencies
4. TRUTHFULNESS — README claims vs actual code/files
5. EU AI ACT — AI risk classification, transparency, documentation
6. RESILIENCE — error handling, dependency pinning, security headers
"""
import os, re, json
from pathlib import Path
from collections import defaultdict

BASE = Path(r"C:\Users\Mr Robot\YBE\github_repos")
REPORT = Path(r"C:\Users\Mr Robot\YBE\AUDIT_REPORT.md")

# Patterns for REAL secret detection (excludes variable names, focuses on actual values)
SECRET_PATTERNS = [
    # Only match when there's a real value (quoted string with actual content)
    (r'(?i)(?:api[_-]?key|apikey)\s*[=:]\s*["\'][a-zA-Z0-9_\-\.]{20,}["\']', "API Key (hardcoded)"),
    (r'(?i)(?:secret|password|passwd|pwd)\s*[=:]\s*["\'][^"\'\n]{8,}["\']', "Password/Secret (hardcoded)"),
    (r'sk-[A-Za-z0-9]{32,}', "OpenAI API Key"),
    (r'ghp_[A-Za-z0-9]{36}', "GitHub Personal Access Token"),
    (r'gho_[A-Za-z0-9]{36}', "GitHub OAuth Token"),
    (r'AIza[A-Za-z0-9_\-]{35}', "Google API Key"),
    (r'AKIA[A-Z0-9]{16}', "AWS Access Key"),
    (r'eyJhbGci[A-Za-z0-9_\-\.]{50,}', "JWT Token (hardcoded)"),
    (r'(?i)mongodb(?:\+srv)?://[^\s"\'/][^\s"\']{15,}', "MongoDB Connection String"),
    (r'(?i)postgres(?:ql)?://[^\s"\'/][^\s"\']{15,}', "PostgreSQL Connection String"),
    (r'(?i)mysql://[^\s"\'/][^\s"\']{15,}', "MySQL Connection String"),
    (r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----', "Private Key"),
]

# Files that are DOCUMENTATION of env vars, not real secrets
SAFE_FILE_NAMES = {".env.example", ".env.template", ".env.sample", ".env.defaults"}

# Files that should NOT be in repos
DANGEROUS_FILES = [
    ".env", ".env.local", ".env.production", ".env.development",
    "id_rsa", "id_ed25519", "*.pem", "*.key",
    "credentials.json", "service-account.json",
    "*.sqlite", "*.db",
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".next", "dist", "build", ".venv", "venv", "env"}
SKIP_EXTS = {".pyc", ".pyo", ".so", ".dll", ".exe", ".bin", ".png", ".jpg", ".jpeg",
             ".gif", ".svg", ".ico", ".mp4", ".webm", ".mp3", ".wav", ".woff", ".woff2",
             ".ttf", ".eot", ".pdf", ".zip", ".tar", ".gz", ".lock"}


def scan_file_for_secrets(filepath):
    """Scan a single file for exposed secrets."""
    findings = []
    # Skip documentation/example env files
    if filepath.name.lower() in SAFE_FILE_NAMES:
        return []
    # Skip markdown documentation files for most patterns
    is_doc = filepath.suffix.lower() in {".md", ".rst", ".txt"}
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        for pattern, label in SECRET_PATTERNS:
            # Skip generic patterns in documentation
            if is_doc and "hardcoded" in label:
                continue
            matches = re.findall(pattern, content)
            if matches:
                for m in matches[:3]:
                    match_str = m if isinstance(m, str) else m[0]
                    # Skip env var references, examples, placeholders
                    if any(fp in match_str.lower() for fp in
                           ["your_", "your-", "xxx", "placeholder", "example",
                            "process.env", "os.environ", "os.getenv", "import.meta",
                            "deno.env", "${}", "config[", "settings.",
                            "user:password@", "user:pass@", "username:password@",
                            "localhost", "${{", "${db_", "${admin",
                            "host.docker.internal", "docker.internal",
                            "${postgres", "${minio"]):
                        continue
                    # Skip Railway/Docker template variables like ${{VARIABLE}} or ${VAR:-default}
                    if re.search(r'\$\{\{|\$\{[A-Z_]+:-', match_str):
                        continue
                    # Skip if the match is just a variable name (all uppercase, no real value)
                    if re.match(r'^[A-Z_]+$', match_str):
                        continue
                    findings.append({
                        "type": label,
                        "file": str(filepath.name),
                        "match_preview": match_str[:50] + "..." if len(str(match_str)) > 50 else str(match_str)
                    })
    except Exception:
        pass
    return findings


def check_dangerous_files(repo_dir):
    """Check for dangerous files that are actually TRACKED in git."""
    import subprocess
    found = []
    # Get list of tracked files from git
    try:
        result = subprocess.run(
            ["git", "ls-files"], cwd=str(repo_dir),
            capture_output=True, text=True, timeout=10
        )
        tracked_files = set(result.stdout.strip().splitlines())
    except Exception:
        tracked_files = set()

    for f in repo_dir.rglob("*"):
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        rel = str(f.relative_to(repo_dir)).replace("\\", "/")
        if rel not in tracked_files:
            continue  # Only flag tracked files
        name = f.name.lower()
        if name in [d.lower() for d in DANGEROUS_FILES if not d.startswith("*")]:
            found.append(str(f.relative_to(repo_dir)))
        for pattern in [d for d in DANGEROUS_FILES if d.startswith("*")]:
            ext = pattern.replace("*", "")
            if name.endswith(ext) and ".git" not in str(f):
                found.append(str(f.relative_to(repo_dir)))
    return found


def audit_completeness(repo_dir):
    """Check repo completeness."""
    issues = []
    checks = {
        "README.md": repo_dir / "README.md",
        "LICENSE": repo_dir / "LICENSE",
        ".gitignore": repo_dir / ".gitignore",
    }
    for name, path in checks.items():
        if not path.exists():
            issues.append(f"Missing {name}")

    # Check for package/dependency files
    has_deps = any((repo_dir / f).exists() for f in
                   ["requirements.txt", "pyproject.toml", "setup.py",
                    "package.json", "go.mod", "Cargo.toml", "Gemfile",
                    "pom.xml", "build.gradle"])
    if not has_deps:
        # Check if there's actual code
        code_files = list(repo_dir.rglob("*.py")) + list(repo_dir.rglob("*.js")) + \
                     list(repo_dir.rglob("*.ts")) + list(repo_dir.rglob("*.go"))
        code_files = [f for f in code_files if ".git" not in str(f) and "node_modules" not in str(f)]
        if code_files:
            issues.append("Missing dependency/package file (requirements.txt, package.json, etc.)")

    # Check for tests
    has_tests = any(repo_dir.rglob("test_*.py")) or any(repo_dir.rglob("*.test.*")) or \
                any(repo_dir.rglob("*.spec.*")) or (repo_dir / "tests").exists() or \
                (repo_dir / "__tests__").exists()
    if not has_tests:
        issues.append("No tests found")

    # Check for CI/CD
    has_ci = (repo_dir / ".github" / "workflows").exists() or \
             (repo_dir / ".gitlab-ci.yml").exists() or \
             (repo_dir / "Jenkinsfile").exists()
    if not has_ci:
        issues.append("No CI/CD pipeline")

    # Check for CONTRIBUTING / CODE_OF_CONDUCT
    if not (repo_dir / "CONTRIBUTING.md").exists():
        issues.append("Missing CONTRIBUTING.md")
    if not (repo_dir / "SECURITY.md").exists():
        issues.append("Missing SECURITY.md (vulnerability disclosure policy)")

    return issues


def audit_readme_truthfulness(repo_dir):
    """Check README for potentially misleading claims."""
    issues = []
    readme = repo_dir / "README.md"
    if not readme.exists():
        return ["No README to audit"]

    content = readme.read_text(encoding="utf-8", errors="ignore").lower()

    # Check claimed tech vs actual files
    tech_claims = {
        "docker": [repo_dir / "Dockerfile", repo_dir / "docker-compose.yml", repo_dir / "docker-compose.yaml"],
        "kubernetes": [repo_dir / "k8s", repo_dir / "kubernetes"],
        "terraform": [repo_dir / "main.tf", repo_dir / "terraform"],
        "github actions": [repo_dir / ".github" / "workflows"],
    }
    for tech, paths in tech_claims.items():
        if tech in content:
            if not any(p.exists() for p in paths):
                issues.append(f"README mentions '{tech}' but no {tech} files found")

    # Check for live demo URLs
    url_pattern = re.findall(r'https?://[^\s\)\]"\']+', content)
    if url_pattern:
        for url in url_pattern[:5]:
            if "localhost" in url or "127.0.0.1" in url:
                issues.append(f"README contains localhost URL: {url[:50]}")

    # Check badge claims
    if "100%" in content and "coverage" in content:
        if not any(repo_dir.rglob("*.test.*")) and not any(repo_dir.rglob("test_*.py")):
            issues.append("Claims 100% coverage but no test files found")

    return issues


def audit_eu_ai_act(repo_dir):
    """Check EU AI Act compliance indicators."""
    issues = []
    all_code = ""
    for ext in ["*.py", "*.js", "*.ts", "*.tsx"]:
        for f in repo_dir.rglob(ext):
            if any(skip in str(f) for skip in SKIP_DIRS):
                continue
            try:
                all_code += f.read_text(encoding="utf-8", errors="ignore")
            except:
                pass

    readme = ""
    if (repo_dir / "README.md").exists():
        readme = (repo_dir / "README.md").read_text(encoding="utf-8", errors="ignore").lower()

    # Check if project uses AI/ML
    ai_indicators = ["openai", "anthropic", "langchain", "transformers", "torch",
                     "tensorflow", "sklearn", "gpt", "claude", "llm", "model",
                     "embedding", "vector", "neural", "prediction", "classification"]
    uses_ai = any(ind in all_code.lower() for ind in ai_indicators)

    if not uses_ai:
        return []  # Not an AI system, EU AI Act likely not applicable

    # EU AI Act checks for AI systems
    if "risk" not in readme and "classification" not in readme:
        issues.append("AI system lacks risk classification documentation (EU AI Act Art. 6)")

    if "transparency" not in readme and "disclosure" not in readme:
        issues.append("Missing AI transparency statement (EU AI Act Art. 52)")

    if "data" not in readme or "training" not in readme:
        issues.append("Missing data governance documentation (EU AI Act Art. 10)")

    # Check for human oversight documentation
    if "human" not in readme or ("oversight" not in readme and "review" not in readme):
        issues.append("Missing human oversight documentation (EU AI Act Art. 14)")

    # Check for bias/fairness considerations
    if "bias" not in readme and "fairness" not in readme and "discriminat" not in readme:
        issues.append("No bias/fairness documentation (EU AI Act Art. 10(2)(f))")

    # Check for logging/monitoring
    has_logging = "logging" in all_code.lower() or "logger" in all_code.lower() or \
                  "audit" in all_code.lower() or "telemetry" in all_code.lower()
    if not has_logging:
        issues.append("No logging/auditing system detected (EU AI Act Art. 12)")

    # Check for GDPR data handling
    if "personal" in all_code.lower() or "user" in all_code.lower():
        if "gdpr" not in readme and "privacy" not in readme and "data protection" not in readme:
            issues.append("Handles user data but no GDPR/privacy documentation")

    return issues


def audit_resilience(repo_dir):
    """Check code resilience and security practices."""
    issues = []

    # Check for pinned dependencies
    req = repo_dir / "requirements.txt"
    if req.exists():
        content = req.read_text(encoding="utf-8", errors="ignore")
        unpinned = [l.strip() for l in content.splitlines()
                    if l.strip() and not l.startswith("#")
                    and "==" not in l and ">=" not in l and "<=" not in l]
        if unpinned:
            issues.append(f"Unpinned dependencies in requirements.txt: {', '.join(unpinned[:5])}")

    pkg = repo_dir / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            wildcard = [k for k, v in deps.items() if v in ["*", "latest"]]
            if wildcard:
                issues.append(f"Wildcard/latest dependencies: {', '.join(wildcard[:5])}")
        except:
            pass

    # Check for error handling in Python files
    py_files = [f for f in repo_dir.rglob("*.py")
                if not any(skip in str(f) for skip in SKIP_DIRS)]
    if py_files:
        bare_excepts = 0
        for f in py_files[:20]:
            try:
                code = f.read_text(encoding="utf-8", errors="ignore")
                bare_excepts += len(re.findall(r'except\s*:', code))
            except:
                pass
        if bare_excepts > 3:
            issues.append(f"Found {bare_excepts} bare 'except:' blocks (should catch specific exceptions)")

    # Check for security headers in web apps
    for ext in ["*.py", "*.js", "*.ts"]:
        for f in repo_dir.rglob(ext):
            if any(skip in str(f) for skip in SKIP_DIRS):
                continue
            try:
                code = f.read_text(encoding="utf-8", errors="ignore")
                if "flask" in code.lower() or "express" in code.lower() or "fastapi" in code.lower():
                    if "cors" not in code.lower() and "helmet" not in code.lower():
                        issues.append(f"Web server in {f.name} lacks CORS/security middleware")
                    break
            except:
                pass

    # Check for input validation
    for f in py_files[:15]:
        try:
            code = f.read_text(encoding="utf-8", errors="ignore")
            if "request" in code and "sql" in code.lower():
                if "parameterize" not in code and "?" not in code and "%s" not in code:
                    issues.append(f"Potential SQL injection risk in {f.name}")
        except:
            pass

    return issues


def audit_repo(repo_dir):
    """Run full audit on a single repo."""
    name = repo_dir.name
    result = {
        "name": name,
        "secrets": [],
        "dangerous_files": [],
        "completeness": [],
        "truthfulness": [],
        "eu_ai_act": [],
        "resilience": [],
        "severity": "OK",
    }

    # 1. Scan for secrets (only in git-tracked files)
    import subprocess
    try:
        _r = subprocess.run(
            ["git", "ls-files"], cwd=str(repo_dir),
            capture_output=True, text=True, timeout=10
        )
        tracked = set(_r.stdout.strip().splitlines())
    except Exception:
        tracked = None  # Fall back to scanning all

    for f in repo_dir.rglob("*"):
        if f.is_dir() or any(skip in f.parts for skip in SKIP_DIRS):
            continue
        if f.suffix.lower() in SKIP_EXTS:
            continue
        if f.stat().st_size > 500_000:  # Skip files > 500KB
            continue
        # Only scan tracked files
        if tracked is not None:
            rel = str(f.relative_to(repo_dir)).replace("\\", "/")
            if rel not in tracked:
                continue
        result["secrets"].extend(scan_file_for_secrets(f))

    # 2. Check dangerous files
    result["dangerous_files"] = check_dangerous_files(repo_dir)

    # 3. Completeness
    result["completeness"] = audit_completeness(repo_dir)

    # 4. Truthfulness
    result["truthfulness"] = audit_readme_truthfulness(repo_dir)

    # 5. EU AI Act
    result["eu_ai_act"] = audit_eu_ai_act(repo_dir)

    # 6. Resilience
    result["resilience"] = audit_resilience(repo_dir)

    # Calculate severity
    total_issues = (len(result["secrets"]) * 3 +  # Critical
                    len(result["dangerous_files"]) * 3 +
                    len(result["eu_ai_act"]) * 2 +
                    len(result["resilience"]) +
                    len(result["completeness"]) +
                    len(result["truthfulness"]))

    if result["secrets"] or result["dangerous_files"]:
        result["severity"] = "CRITICAL"
    elif total_issues > 10:
        result["severity"] = "HIGH"
    elif total_issues > 5:
        result["severity"] = "MEDIUM"
    elif total_issues > 0:
        result["severity"] = "LOW"

    return result


def generate_report(results):
    """Generate markdown audit report."""
    lines = [
        "# 🔍 COMPREHENSIVE GITHUB PORTFOLIO AUDIT",
        f"**Date:** 2026-02-20 22:00 CET",
        f"**Repos Audited:** {len(results)}",
        f"**Auditor:** Multi-Agent Autonomous System",
        "",
        "## Executive Summary",
        "",
    ]

    # Summary table
    critical = sum(1 for r in results if r["severity"] == "CRITICAL")
    high = sum(1 for r in results if r["severity"] == "HIGH")
    medium = sum(1 for r in results if r["severity"] == "MEDIUM")
    low = sum(1 for r in results if r["severity"] == "LOW")
    ok = sum(1 for r in results if r["severity"] == "OK")
    total_secrets = sum(len(r["secrets"]) for r in results)
    total_dangerous = sum(len(r["dangerous_files"]) for r in results)

    lines.extend([
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| 🔴 CRITICAL repos | **{critical}** |",
        f"| 🟠 HIGH risk repos | **{high}** |",
        f"| 🟡 MEDIUM risk repos | **{medium}** |",
        f"| 🟢 LOW risk repos | **{low}** |",
        f"| ✅ Clean repos | **{ok}** |",
        f"| 🔑 Exposed secrets found | **{total_secrets}** |",
        f"| ⚠️ Dangerous files found | **{total_dangerous}** |",
        "",
        "---",
        "",
    ])

    # Group by severity
    severity_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢", "OK": "✅"}
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "OK"]:
        repos = [r for r in results if r["severity"] == sev]
        if not repos:
            continue
        lines.append(f"## {severity_emoji[sev]} {sev} — {len(repos)} repos")
        lines.append("")

        for r in repos:
            lines.append(f"### `{r['name']}` {severity_emoji[sev]}")
            lines.append("")

            if r["secrets"]:
                lines.append("**🔑 EXPOSED SECRETS:**")
                for s in r["secrets"][:10]:
                    lines.append(f"- ⚠️ `{s['type']}` in `{s['file']}`: `{s['match_preview']}`")
                lines.append("")

            if r["dangerous_files"]:
                lines.append("**⚠️ DANGEROUS FILES (should not be in repo):**")
                for f in r["dangerous_files"][:10]:
                    lines.append(f"- 🚫 `{f}`")
                lines.append("")

            if r["completeness"]:
                lines.append("**📋 COMPLETENESS:**")
                for c in r["completeness"]:
                    lines.append(f"- ❌ {c}")
                lines.append("")

            if r["truthfulness"]:
                lines.append("**🔍 TRUTHFULNESS:**")
                for t in r["truthfulness"]:
                    lines.append(f"- ⚠️ {t}")
                lines.append("")

            if r["eu_ai_act"]:
                lines.append("**🇪🇺 EU AI ACT COMPLIANCE:**")
                for e in r["eu_ai_act"]:
                    lines.append(f"- 📜 {e}")
                lines.append("")

            if r["resilience"]:
                lines.append("**🛡️ RESILIENCE:**")
                for res in r["resilience"]:
                    lines.append(f"- 🔧 {res}")
                lines.append("")

            if not any([r["secrets"], r["dangerous_files"], r["completeness"],
                        r["truthfulness"], r["eu_ai_act"], r["resilience"]]):
                lines.append("✅ No issues found")
                lines.append("")

            lines.append("---")
            lines.append("")

    return "\n".join(lines)


def main():
    print("=" * 60)
    print("  COMPREHENSIVE GITHUB PORTFOLIO AUDIT")
    print("  Security · Legal · Completeness · EU AI Act")
    print("=" * 60)

    results = []
    repos = sorted([d for d in BASE.iterdir() if d.is_dir() and d.name != ".git"])
    print(f"\n  Scanning {len(repos)} repos...\n")

    for repo in repos:
        print(f"  [{len(results)+1}/{len(repos)}] {repo.name}...", end=" ")
        r = audit_repo(repo)
        results.append(r)
        issues = sum(len(v) for k, v in r.items() if isinstance(v, list))
        sev = r["severity"]
        emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢", "OK": "✅"}
        print(f"{emoji.get(sev, '?')} {sev} ({issues} issues)")

    # Generate report
    report = generate_report(results)
    REPORT.write_text(report, encoding="utf-8")
    print(f"\n  Report saved: {REPORT}")
    print(f"  Total repos: {len(results)}")
    print(f"  CRITICAL: {sum(1 for r in results if r['severity'] == 'CRITICAL')}")
    print(f"  HIGH:     {sum(1 for r in results if r['severity'] == 'HIGH')}")
    print(f"  MEDIUM:   {sum(1 for r in results if r['severity'] == 'MEDIUM')}")
    print(f"  LOW:      {sum(1 for r in results if r['severity'] == 'LOW')}")
    print(f"  OK:       {sum(1 for r in results if r['severity'] == 'OK')}")
    print("\n  DONE")


if __name__ == "__main__":
    main()
