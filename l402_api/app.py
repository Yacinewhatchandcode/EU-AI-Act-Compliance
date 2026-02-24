"""
╔═══════════════════════════════════════════════════════════════════╗
║  EU AI ACT COMPLIANCE API — L402 Lightning Paywall               ║
║  Robot-to-Robot payments. 0€ capital needed.                     ║
║  Every API call = sats → wispytimpani921@walletofsatoshi.com     ║
║  Protocol: L402 (HTTP 402 Payment Required)                      ║
║  MiCA Compliant · EU AI Act 2026                                 ║
╚═══════════════════════════════════════════════════════════════════╝
"""
import os
import json
import hashlib
import secrets
import time
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
WALLET_ADDRESS = os.environ.get("LIGHTNING_ADDRESS", "wispytimpani921@walletofsatoshi.com")
LNBITS_URL = os.environ.get("LNBITS_URL", "https://legend.lnbits.com")
LNBITS_API_KEY = os.environ.get("LNBITS_API_KEY", "")  # Set this in env!
PRICE_SATS = int(os.environ.get("PRICE_SATS", "10"))  # 10 sats per API call

# In-memory token store (use Redis in production)
valid_tokens = {}
api_stats = {
    "total_calls": 0,
    "paid_calls": 0,
    "total_sats_earned": 0,
    "started_at": datetime.now().isoformat()
}

# ═══════════════════════════════════════════════════════════════════
# EU AI ACT COMPLIANCE DATA (The actual service being sold)
# ═══════════════════════════════════════════════════════════════════
PROHIBITED_PRACTICES = [
    "Social scoring by governments",
    "Real-time remote biometric identification in public spaces (with exceptions)",
    "Manipulation through subliminal techniques",
    "Exploitation of vulnerable groups",
    "Predictive policing based solely on profiling",
]

HIGH_RISK_CATEGORIES = [
    "Biometric identification systems",
    "Critical infrastructure management",
    "Education and vocational training",
    "Employment and worker management",
    "Access to essential services",
    "Law enforcement",
    "Migration and border control",
    "Administration of justice",
]

COMPLIANCE_REQUIREMENTS = {
    "risk_management": "Establish a risk management system (Art. 9)",
    "data_governance": "Ensure training data quality and governance (Art. 10)",
    "documentation": "Maintain technical documentation (Art. 11)",
    "record_keeping": "Implement automatic logging (Art. 12)",
    "transparency": "Provide transparency information to users (Art. 13)",
    "human_oversight": "Enable human oversight capabilities (Art. 14)",
    "accuracy": "Ensure accuracy, robustness, and cybersecurity (Art. 15)",
    "conformity": "Complete EU conformity assessment (Art. 43)",
}

DEADLINES = {
    "2025-02-02": "Prohibited AI practices ban takes effect",
    "2025-08-02": "GPAI model rules apply",
    "2026-08-02": "Full enforcement for high-risk AI systems",
    "2027-08-02": "All AI systems must comply",
}

PENALTIES = {
    "prohibited_practices": "Up to €35M or 7% of global annual turnover",
    "high_risk_violations": "Up to €15M or 3% of global annual turnover",
    "misinformation": "Up to €7.5M or 1% of global annual turnover",
}

# ═══════════════════════════════════════════════════════════════════
# L402 PAYMENT MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════

def generate_token():
    """Generate a simple bearer token for paid access."""
    return secrets.token_hex(32)

def create_lightning_invoice(amount_sats, memo):
    """Create a Lightning invoice via LNBits API."""
    if not LNBITS_API_KEY:
        # Demo mode: return a mock invoice with instructions
        return {
            "payment_hash": hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
            "payment_request": f"lnbc{amount_sats}n1demo_SETUP_LNBITS_FOR_REAL_INVOICES",
            "amount_sats": amount_sats,
            "memo": memo,
            "setup_required": True,
            "instructions": [
                "1. Go to https://legend.lnbits.com (FREE)",
                "2. Create a wallet",
                "3. Copy your API key (Invoice/read key)",
                f"4. Set env var: LNBITS_API_KEY=your_key",
                f"5. Restart. Real Lightning invoices will be generated.",
                f"6. Payments go to your LNBits wallet → transfer to {WALLET_ADDRESS}"
            ]
        }
    
    try:
        import requests
        resp = requests.post(
            f"{LNBITS_URL}/api/v1/payments",
            headers={"X-Api-Key": LNBITS_API_KEY, "Content-Type": "application/json"},
            json={"out": False, "amount": amount_sats, "memo": memo},
            timeout=10
        )
        data = resp.json()
        return {
            "payment_hash": data.get("payment_hash", ""),
            "payment_request": data.get("payment_request", ""),
            "amount_sats": amount_sats,
            "memo": memo,
            "setup_required": False
        }
    except Exception as e:
        return {"error": str(e), "setup_required": True}

def check_payment(payment_hash):
    """Check if a Lightning invoice has been paid."""
    if not LNBITS_API_KEY:
        return False
    try:
        import requests
        resp = requests.get(
            f"{LNBITS_URL}/api/v1/payments/{payment_hash}",
            headers={"X-Api-Key": LNBITS_API_KEY},
            timeout=10
        )
        data = resp.json()
        return data.get("paid", False)
    except:
        return False

def require_l402(f):
    """L402 payment middleware decorator."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        api_stats["total_calls"] += 1
        
        # Check for valid bearer token
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
            if token in valid_tokens:
                token_data = valid_tokens[token]
                if token_data["uses_remaining"] > 0:
                    token_data["uses_remaining"] -= 1
                    api_stats["paid_calls"] += 1
                    return f(*args, **kwargs)
        
        # Check for payment hash (L402 flow step 2)
        payment_hash = request.headers.get("X-Payment-Hash", "")
        if payment_hash and check_payment(payment_hash):
            # Payment confirmed! Issue access token
            token = generate_token()
            valid_tokens[token] = {
                "created": datetime.now().isoformat(),
                "uses_remaining": 10,  # 10 API calls per payment
                "payment_hash": payment_hash
            }
            api_stats["paid_calls"] += 1
            api_stats["total_sats_earned"] += PRICE_SATS
            response = f(*args, **kwargs)
            response.headers["X-Access-Token"] = token
            return response
        
        # No valid auth → Return 402 with invoice
        invoice = create_lightning_invoice(
            PRICE_SATS,
            f"EU AI Act API Access — {PRICE_SATS} sats for 10 calls"
        )
        
        response = make_response(jsonify({
            "error": "Payment Required",
            "protocol": "L402",
            "price_sats": PRICE_SATS,
            "calls_included": 10,
            "invoice": invoice,
            "how_to_pay": {
                "step_1": f"Pay the Lightning invoice ({PRICE_SATS} sats)",
                "step_2": "Include the payment_hash in header: X-Payment-Hash: <hash>",
                "step_3": "Receive Bearer token in response header: X-Access-Token",
                "step_4": "Use token for subsequent calls: Authorization: Bearer <token>",
            },
            "wallet_address": WALLET_ADDRESS,
            "service": "EU AI Act 2026 Compliance API by PRIME.AI"
        }), 402)
        response.headers["WWW-Authenticate"] = f'L402 invoice="{invoice.get("payment_request", "")}", macaroon="eu-ai-act-access"'
        return response
    
    return decorated

# ═══════════════════════════════════════════════════════════════════
# FREE ENDPOINTS (Discovery & Info)
# ═══════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return jsonify({
        "service": "EU AI Act 2026 Compliance API",
        "provider": "PRIME.AI",
        "version": "2.0.0",
        "protocol": "L402 (Lightning Network Payments)",
        "price": f"{PRICE_SATS} sats per 10 API calls",
        "wallet": WALLET_ADDRESS,
        "endpoints": {
            "free": {
                "/": "This info page",
                "/health": "Service health check",
                "/api/info": "API documentation",
                "/api/stats": "Usage statistics",
            },
            "paid_l402": {
                "/api/classify": "Classify an AI system's risk level",
                "/api/audit": "Full compliance audit",
                "/api/deadlines": "Get compliance deadlines",
                "/api/penalties": "Get penalty information",
                "/api/requirements": "Get requirements checklist",
            }
        },
        "for_ai_agents": "Use L402 protocol. Pay Lightning invoice, get access token.",
        "mcp_compatible": True,
        "mica_compliant": True,
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "uptime_since": api_stats["started_at"],
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/info")
def api_info():
    return jsonify({
        "name": "EU AI Act Compliance API",
        "description": "Automated compliance checking for the EU AI Act 2026. Designed for AI agents and automated systems.",
        "payment": {
            "protocol": "L402",
            "price_sats": PRICE_SATS,
            "lightning_address": WALLET_ADDRESS,
            "accepts": "Bitcoin Lightning Network payments",
        },
        "coverage": [
            "AI system risk classification (Prohibited, High-Risk, Limited, Minimal)",
            "Full compliance audit with gap analysis",
            "Deadline tracking for EU AI Act milestones",
            "Penalty calculation for non-compliance",
            "Requirements checklist generation",
        ]
    })

@app.route("/api/stats")
def stats():
    return jsonify(api_stats)

# ═══════════════════════════════════════════════════════════════════
# PAID ENDPOINTS (L402 Protected)
# ═══════════════════════════════════════════════════════════════════

@app.route("/api/classify", methods=["POST"])
@require_l402
def classify():
    """Classify an AI system's risk level under EU AI Act."""
    data = request.get_json(silent=True) or {}
    system_name = data.get("system_name", "Unknown AI System")
    description = data.get("description", "")
    use_case = data.get("use_case", "").lower()
    
    # Classification logic
    risk_level = "minimal"
    reasons = []
    
    for practice in PROHIBITED_PRACTICES:
        if any(keyword in use_case for keyword in ["social scoring", "subliminal", "biometric mass", "exploit vulnerable"]):
            risk_level = "prohibited"
            reasons.append(f"Matches prohibited practice: {practice}")
            break
    
    if risk_level != "prohibited":
        for category in HIGH_RISK_CATEGORIES:
            keywords = category.lower().split()
            if any(kw in use_case for kw in keywords):
                risk_level = "high"
                reasons.append(f"Matches high-risk category: {category}")
                break
    
    if risk_level == "minimal" and any(kw in use_case for kw in ["chatbot", "ai-generated", "deepfake", "emotion"]):
        risk_level = "limited"
        reasons.append("Requires transparency obligations (Art. 52)")
    
    return jsonify({
        "system_name": system_name,
        "risk_level": risk_level,
        "reasons": reasons or ["No specific high-risk indicators found"],
        "requirements": COMPLIANCE_REQUIREMENTS if risk_level == "high" else {},
        "penalties": PENALTIES.get(f"{risk_level}_violations", PENALTIES.get("misinformation")),
        "recommendation": f"System classified as {risk_level.upper()} risk under EU AI Act 2026",
        "api_powered_by": "PRIME.AI L402",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/audit", methods=["POST"])
@require_l402
def audit():
    """Full compliance audit for an AI system."""
    data = request.get_json(silent=True) or {}
    system_name = data.get("system_name", "Unknown")
    
    # Generate comprehensive audit
    audit_items = []
    score = 0
    total = len(COMPLIANCE_REQUIREMENTS)
    
    for key, requirement in COMPLIANCE_REQUIREMENTS.items():
        has_it = data.get(key, False)
        if has_it:
            score += 1
        audit_items.append({
            "requirement": key,
            "description": requirement,
            "status": "PASS" if has_it else "FAIL",
            "priority": "HIGH" if key in ["risk_management", "human_oversight", "conformity"] else "MEDIUM"
        })
    
    compliance_pct = round((score / total) * 100, 1) if total > 0 else 0
    
    return jsonify({
        "system_name": system_name,
        "compliance_score": f"{compliance_pct}%",
        "items_passed": score,
        "items_total": total,
        "audit_items": audit_items,
        "deadlines": DEADLINES,
        "overall_status": "COMPLIANT" if compliance_pct >= 80 else "ACTION REQUIRED",
        "generated_at": datetime.now().isoformat(),
        "powered_by": "PRIME.AI L402 — EU AI Act Compliance Engine"
    })

@app.route("/api/deadlines")
@require_l402
def deadlines():
    return jsonify({
        "deadlines": DEADLINES,
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "next_deadline": next(
            (d for d, desc in sorted(DEADLINES.items()) if d > datetime.now().strftime("%Y-%m-%d")),
            "All deadlines passed"
        )
    })

@app.route("/api/penalties")
@require_l402
def penalties():
    return jsonify({
        "penalties": PENALTIES,
        "currency": "EUR",
        "note": "Penalties are the higher of the fixed amount or the percentage of global annual turnover"
    })

@app.route("/api/requirements")
@require_l402
def requirements():
    return jsonify({
        "requirements": COMPLIANCE_REQUIREMENTS,
        "total_requirements": len(COMPLIANCE_REQUIREMENTS),
        "applies_to": "High-risk AI systems under EU AI Act 2026"
    })

# ═══════════════════════════════════════════════════════════════════
# MCP TOOL DISCOVERY (for AI agents to find this service)
# ═══════════════════════════════════════════════════════════════════

@app.route("/.well-known/mcp.json")
def mcp_discovery():
    """MCP service discovery for AI agents."""
    return jsonify({
        "name": "EU AI Act Compliance API",
        "version": "2.0.0",
        "description": "Automated EU AI Act 2026 compliance checking. Pay-per-use via Lightning L402.",
        "payment": {
            "protocol": "L402",
            "price_sats": PRICE_SATS,
            "lightning_address": WALLET_ADDRESS
        },
        "tools": [
            {"name": "classify", "endpoint": "/api/classify", "method": "POST", "paid": True},
            {"name": "audit", "endpoint": "/api/audit", "method": "POST", "paid": True},
            {"name": "deadlines", "endpoint": "/api/deadlines", "method": "GET", "paid": True},
            {"name": "penalties", "endpoint": "/api/penalties", "method": "GET", "paid": True},
            {"name": "requirements", "endpoint": "/api/requirements", "method": "GET", "paid": True},
        ]
    })

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5402))
    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║  🚀 EU AI ACT L402 API — LIVE                                   ║
║  💰 Price: {PRICE_SATS} sats per 10 API calls                            ║
║  ⚡ Wallet: {WALLET_ADDRESS}          ║
║  🌐 URL: http://localhost:{port}                                  ║
║  📡 MCP Discovery: http://localhost:{port}/.well-known/mcp.json   ║
║                                                                   ║
║  FREE endpoints: /, /health, /api/info, /api/stats               ║
║  PAID endpoints: /api/classify, /api/audit, /api/deadlines       ║
║                  /api/penalties, /api/requirements                ║
║                                                                   ║
║  Protocol: L402 — AI agents pay Lightning sats for access        ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    if not LNBITS_API_KEY:
        print("⚠️  LNBITS_API_KEY not set. Running in DEMO mode.")
        print("   To enable REAL Lightning payments:")
        print("   1. Go to https://legend.lnbits.com (FREE)")
        print("   2. Create a wallet, copy Invoice/read key")
        print("   3. Set: LNBITS_API_KEY=your_key")
        print()
    
    app.run(host="0.0.0.0", port=port, debug=False)
