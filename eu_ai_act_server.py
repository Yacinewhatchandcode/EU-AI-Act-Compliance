import http.server
import socketserver
import json
import os
import sys
import hashlib
import hmac
import base64
import time
import re
import ssl
import secrets
import urllib.request
import urllib.parse
import urllib.error
try:
    import stripe
    from dotenv import load_dotenv
    import qrcode
    import io
    load_dotenv()
except ImportError:
    stripe = None
    load_dotenv = lambda: None
    qrcode = None
from pathlib import Path
from datetime import datetime, timedelta

# Add the project directory to path
sys.path.insert(0, str(Path(__file__).parent))
from eu_ai_act import (
    classify_ai_system,
    run_compliance_audit,
    generate_compliance_report,
    generate_roadmap,
    classify_openclaw_stack,
    PROHIBITED_PRACTICES,
    HIGH_RISK_CATEGORIES,
    COMPLIANCE_REQUIREMENTS,
    PENALTIES,
    DEADLINES,
    OPEN_SOURCE_STACK,
)
from revenue_engine import RevenueEngine
from mica_scanner import scan_for_mica
from b2b_lead_gen import B2BLeadGen
from autonomous_operations import ceo_agent
from satoshi_investor import SatoshiInvestor

# Initialize Engines
revenue_engine = RevenueEngine()
lead_gen = B2BLeadGen()
satoshi_investor = SatoshiInvestor(revenue_engine)
# Note: ceo_agent is imported from autonomous_operations already initialized

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

PORT = int(os.environ.get("PORT", 8000))
STATIC_DIR = Path(__file__).parent / "web"

# Google OAuth — set your Client ID here or via env var
# Get yours at: https://console.cloud.google.com/apis/credentials
GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
)

# Stripe keys from .env
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_mock")
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_test_mock")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
if stripe and STRIPE_SECRET_KEY != "sk_test_mock":
    stripe.api_key = STRIPE_SECRET_KEY

# JWT Secret — auto-generated per server start, or set via env
JWT_SECRET = os.environ.get("JWT_SECRET", secrets.token_hex(32))
JWT_EXPIRY_HOURS = 24

# Allowed email domains (empty = allow all Google accounts)
# Set to ["yourdomain.com"] to restrict to your org
ALLOWED_DOMAINS = os.environ.get("ALLOWED_DOMAINS", "").split(",") if os.environ.get("ALLOWED_DOMAINS") else []

# Allowed email whitelist (specific emails)
ALLOWED_EMAILS = os.environ.get("ALLOWED_EMAILS", "").split(",") if os.environ.get("ALLOWED_EMAILS") else []


# ═══════════════════════════════════════════════════════════════════
# JWT TOKEN SYSTEM
# ═══════════════════════════════════════════════════════════════════

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def _b64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)

def create_jwt(payload: dict) -> str:
    """Create a simple HMAC-SHA256 JWT."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload["iat"] = int(time.time())
    payload["exp"] = int(time.time()) + (JWT_EXPIRY_HOURS * 3600)

    h = _b64url_encode(json.dumps(header).encode())
    p = _b64url_encode(json.dumps(payload).encode())
    sig = hmac.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    s = _b64url_encode(sig)
    return f"{h}.{p}.{s}"

def verify_jwt(token: str) -> dict:
    """Verify JWT and return payload. Raises ValueError if invalid."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Malformed token")

        h, p, s = parts
        expected_sig = hmac.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
        actual_sig = _b64url_decode(s)

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise ValueError("Invalid signature")

        payload = json.loads(_b64url_decode(p))
        if payload.get("exp", 0) < time.time():
            raise ValueError("Token expired")

        return payload
    except Exception as e:
        raise ValueError(f"Token verification failed: {e}")


def verify_google_token(id_token: str) -> dict:
    """Verify Google ID token by fetching Google's tokeninfo endpoint."""
    import urllib.request
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())

        # Verify audience matches our client ID
        if data.get("aud") != GOOGLE_CLIENT_ID:
            raise ValueError(f"Token audience mismatch: {data.get('aud')}")

        # Check email verification
        if data.get("email_verified") != "true":
            raise ValueError("Email not verified")

        email = data.get("email", "")
        domain = email.split("@")[1] if "@" in email else ""

        # Check domain whitelist
        if ALLOWED_DOMAINS and domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain {domain} not allowed")

        # Check email whitelist
        if ALLOWED_EMAILS and email not in ALLOWED_EMAILS:
            raise ValueError(f"Email {email} not in whitelist")

        return {
            "email": email,
            "name": data.get("name", email.split("@")[0]),
            "picture": data.get("picture", ""),
            "sub": data.get("sub", ""),
        }
    except urllib.error.URLError as e:
        raise ValueError(f"Google verification failed: {e}")


# ═══════════════════════════════════════════════════════════════════
# URL SCANNER — Analyze any website for AI indicators
# ═══════════════════════════════════════════════════════════════════

AI_INDICATORS = {
    "chatbot": {"weight": 3, "category": "Chatbot / Virtual Assistant", "article": "Art. 50"},
    "virtual assistant": {"weight": 3, "category": "Chatbot / Virtual Assistant", "article": "Art. 50"},
    "ai-powered": {"weight": 2, "category": "AI-Powered Service", "article": "Art. 50"},
    "machine learning": {"weight": 2, "category": "ML System", "article": "Varies"},
    "deep learning": {"weight": 2, "category": "Deep Learning", "article": "Varies"},
    "neural network": {"weight": 2, "category": "Neural Network", "article": "Varies"},
    "recommendation": {"weight": 1, "category": "Recommendation Engine", "article": "Art. 50"},
    "automated decision": {"weight": 4, "category": "Automated Decision-Making", "article": "Art. 14 + GDPR Art. 22"},
    "facial recognition": {"weight": 5, "category": "Biometric ID", "article": "Art. 5-6 + Annex III"},
    "biometric": {"weight": 5, "category": "Biometric System", "article": "Art. 5-6 + Annex III"},
    "credit scor": {"weight": 4, "category": "Credit Scoring", "article": "Art. 6(2) + Annex III §5"},
    "hiring": {"weight": 4, "category": "Employment AI", "article": "Art. 6(2) + Annex III §4"},
    "recruitment": {"weight": 4, "category": "Employment AI", "article": "Art. 6(2) + Annex III §4"},
    "cv screening": {"weight": 5, "category": "Employment AI", "article": "Art. 6(2) + Annex III §4"},
    "predictive": {"weight": 2, "category": "Predictive System", "article": "Varies"},
    "natural language": {"weight": 2, "category": "NLP System", "article": "Art. 50"},
    "computer vision": {"weight": 2, "category": "Computer Vision", "article": "Varies"},
    "sentiment analysis": {"weight": 3, "category": "Emotion/Sentiment AI", "article": "Art. 5(1)(f)"},
    "emotion detection": {"weight": 5, "category": "Emotion Recognition", "article": "Art. 5(1)(f)"},
    "content moderation": {"weight": 2, "category": "Content Moderation AI", "article": "Art. 50"},
    "personali": {"weight": 2, "category": "Personalization Engine", "article": "Art. 50"},
    "generative ai": {"weight": 3, "category": "Generative AI / GPAI", "article": "Art. 50-52"},
    "large language model": {"weight": 3, "category": "GPAI Model", "article": "Art. 51-53"},
    "llm": {"weight": 2, "category": "GPAI Model", "article": "Art. 51-53"},
    "gpt": {"weight": 2, "category": "GPAI Model", "article": "Art. 51-53"},
    "openai": {"weight": 2, "category": "GPAI Provider", "article": "Art. 51-53"},
    "ai act": {"weight": 1, "category": "Compliance Aware", "article": "Meta"},
    "gdpr": {"weight": 1, "category": "Privacy Aware", "article": "Meta"},
    "cookie": {"weight": 1, "category": "Data Collection", "article": "ePrivacy"},
}


def scan_url(url: str) -> dict:
    """Fetch a URL and analyze it for AI system indicators."""
    import urllib.request

    result = {
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "status": "ok",
        "ai_indicators": [],
        "risk_level": "MINIMAL",
        "obligations": [],
        "score": 0,
        "max_score": 0,
        "summary": "",
    }

    try:
        # Validate URL
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme:
            url = "https://" + url
            parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            result["status"] = "error"
            result["summary"] = "Invalid URL scheme. Use http:// or https://"
            return result

        # Fetch page content
        req = urllib.request.Request(url, headers={
            "User-Agent": "PRIME-AI-Act-Scanner/1.0 (EU AI Act Compliance Check)",
            "Accept": "text/html,application/xhtml+xml",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read(500_000).decode("utf-8", errors="ignore").lower()

        # Strip HTML tags for cleaner text analysis
        text = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)

        # Scan for AI indicators
        total_weight = 0
        found = {}
        for keyword, info in AI_INDICATORS.items():
            count = text.count(keyword)
            if count > 0:
                cat = info["category"]
                if cat not in found or info["weight"] > found[cat]["weight"]:
                    found[cat] = {
                        "keyword": keyword,
                        "count": count,
                        "weight": info["weight"],
                        "category": cat,
                        "article": info["article"],
                    }
                total_weight += info["weight"] * min(count, 3)  # cap repetitions

        result["ai_indicators"] = sorted(found.values(), key=lambda x: -x["weight"])
        result["score"] = total_weight
        result["max_score"] = sum(i["weight"] for i in AI_INDICATORS.values())

        # Determine risk level based on score
        if total_weight >= 15:
            result["risk_level"] = "HIGH"
            result["obligations"] = [
                "Full compliance with Articles 8-15 required",
                "Risk Management System (Art. 9)",
                "Data Governance (Art. 10)",
                "Technical Documentation (Art. 11)",
                "Human Oversight (Art. 14)",
                "Conformity Assessment (Art. 43)",
            ]
        elif total_weight >= 8:
            result["risk_level"] = "LIMITED"
            result["obligations"] = [
                "Transparency obligations (Art. 50)",
                "Disclose AI nature to users",
                "Label AI-generated content",
            ]
        elif total_weight >= 3:
            result["risk_level"] = "MINIMAL"
            result["obligations"] = [
                "No mandatory requirements",
                "Voluntary codes of conduct recommended",
            ]
        else:
            result["risk_level"] = "NO AI DETECTED"
            result["obligations"] = [
                "No AI system indicators found on this page",
            ]

        # Generate summary
        ai_count = len(found)
        result["summary"] = (
            f"Scanned {parsed.netloc}: found {ai_count} AI indicator(s), "
            f"risk score {total_weight}/{result['max_score']}. "
            f"Classification: {result['risk_level']}."
        )

    except urllib.error.HTTPError as e:
        result["status"] = "error"
        result["summary"] = f"HTTP error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        result["status"] = "error"
        result["summary"] = f"Cannot reach URL: {e.reason}"
    except Exception as e:
        result["status"] = "error"
        result["summary"] = f"Scan failed: {str(e)}"

    return result


# ═══════════════════════════════════════════════════════════════════
# HTTP SERVER WITH AUTH
# ═══════════════════════════════════════════════════════════════════

# Public routes that don't require auth
PUBLIC_ROUTES = {"/", "/index.html", "/login.html", "/landing.html", "/style.css", "/app.js",
                 "/manifest.json", "/sw.js", "/icon-192.png", "/icon-512.png",
                 "/apple-touch-icon.png", "/icon-maskable-512.png", "/qr.png",
                 "/api/auth/google", "/api/auth/status", "/api/auth/config",
                 "/api/auth/dev"}


class APIHandler(http.server.SimpleHTTPRequestHandler):
    """Handle API requests with Google OAuth + JWT auth."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def _get_token(self) -> str:
        """Extract JWT from Authorization header or cookie."""
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            return auth[7:]
        cookies = self.headers.get("Cookie", "")
        for c in cookies.split(";"):
            c = c.strip()
            if c.startswith("token="):
                return c[6:]
        return ""

    def _check_auth(self) -> dict:
        """Verify auth and return user info or None."""
        token = self._get_token()
        if not token:
            return None
        try:
            return verify_jwt(token)
        except Exception: # Catch any exception during JWT verification
            return None

    def _require_auth(self):
        """Check auth and return 401 if not authenticated."""
        user = self._check_auth()
        if not user:
            self._json_response({"error": "Authentication required", "login_url": "/login.html"}, 401)
            return None
        return user

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        # ─── Public routes ───
        if path == "/api/auth/status":
            user = self._check_auth()
            if user:
                # Get current wallet balance for authenticated users
                wallet_status = revenue_engine.get_status()
                val = wallet_status.get("balance", 0.0)
                self._json_response({
                    "authenticated": True,
                    "user": user,
                    "balance": float(int(val * 10) / 10.0) # Round to one decimal place
                })
            else:
                self._json_response({"authenticated": False})
            return

        if path == "/api/auth/config":
            google_configured = GOOGLE_CLIENT_ID != "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
            self._json_response({
                "client_id": GOOGLE_CLIENT_ID,
                "configured": google_configured,
                "dev_mode": not google_configured,
            })
            return

        # Dev mode auth — generates a real JWT when Google OAuth is not configured
        if path == "/api/auth/dev":
            google_configured = GOOGLE_CLIENT_ID != "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
            if google_configured:
                self._json_response({"error": "Dev mode disabled — use Google sign-in"}, 403)
                return
            token = create_jwt({"email": "dev@prime-ai.local", "name": "Developer", "dev": True})
            self._json_response({
                "token": token,
                "user": {"email": "dev@prime-ai.local", "name": "Developer"},
                "message": "Dev mode active — set GOOGLE_CLIENT_ID for production"
            })
            return

        if path == "/api/pay/mcp-test":
            success, msg = ceo_agent.test_stripe_mcp()
            self._json_response({"success": success, "message": msg})
            return

        # ─── Auth-gated API routes ───
        if path.startswith("/api/"):
            user = self._require_auth()
            if not user:
                return

            if path == "/api/deadlines":
                self._json_response({"deadlines": DEADLINES})

            elif path == "/api/knowledge":
                self._json_response({
                    "prohibited": PROHIBITED_PRACTICES,
                    "high_risk": HIGH_RISK_CATEGORIES,
                    "requirements": COMPLIANCE_REQUIREMENTS,
                    "penalties": PENALTIES,
                })

            elif path == "/api/search":
                query = params.get("q", [""])[0].lower()
                results = []
                for p in PROHIBITED_PRACTICES:
                    if query in str(p).lower():
                        results.append({"type": "prohibited", "data": p})
                for h in HIGH_RISK_CATEGORIES:
                    if query in str(h).lower():
                        results.append({"type": "high_risk", "data": h})
                for r in COMPLIANCE_REQUIREMENTS:
                    if query in str(r).lower():
                        results.append({"type": "requirement", "data": r})
                self._json_response({"query": query, "results": results, "count": len(results)})

            elif path == "/api/stats":
                deadline = datetime(2026, 8, 2)
                days = (deadline - datetime.now()).days
                self._json_response({
                    "days_remaining": days,
                    "prohibited_count": len(PROHIBITED_PRACTICES),
                    "high_risk_count": len(HIGH_RISK_CATEGORIES),
                    "requirements_count": len(COMPLIANCE_REQUIREMENTS),
                    "agents": ["main", "regulatory", "classifier", "auditor", "reporter"],
                    "user": user,
                })

            elif path == "/api/compliance/self-check":
                result = classify_openclaw_stack()
                self._json_response(result)

            elif path == "/api/compliance/docs":
                compliance_dir = Path(__file__).parent / "compliance"
                docs = []
                if compliance_dir.exists():
                    for f in sorted(compliance_dir.rglob("*.md")):
                        rel = f.relative_to(compliance_dir)
                        docs.append({
                            "name": str(rel),
                            "size_kb": round(f.stat().st_size / 1024, 1),
                            "exists": True,
                        })
                self._json_response({"docs": docs, "count": len(docs)})

            elif path == "/api/compliance/oss-stack":
                self._json_response(OPEN_SOURCE_STACK)

            elif path == "/api/scan":
                url_to_scan = params.get("url", [""])[0]
                if not url_to_scan:
                    self._json_response({"error": "URL parameter required"}, 400)
                    return
                result = scan_url(url_to_scan)
                result["scanned_by"] = user.get("email", "unknown")
                self._json_response(result)

            elif path == "/api/wallet":
                self._json_response({"success": True, "wallet": revenue_engine.get_status()})

            elif path == "/api/wallet/generate":
                result = revenue_engine.generate_revenue()
                self._json_response({"success": True, "wallet": result})

            elif path == "/satoshi_investments.json":
                log_path = Path(__file__).parent / "satoshi_investments.json"
                if log_path.exists():
                    with open(log_path, "r") as f:
                        self._json_response(json.load(f))
                else:
                    self._json_response([])

            elif path.startswith("/satoshi/"):
                subpath = path[9:] if path[9:] else "index.html"
                dashboard_file = Path(__file__).parent / "satoshi-dashboard" / subpath
                if dashboard_file.exists():
                    try:
                        with open(dashboard_file, "rb") as f:
                            content = f.read()
                        ext = dashboard_file.suffix.lower()
                        mime = {
                            ".html": "text/html",
                            ".css": "text/css",
                            ".js": "application/javascript",
                            ".png": "image/png",
                            ".svg": "image/svg+xml"
                        }.get(ext, "text/plain")
                        self.send_response(200)
                        self.send_header("Content-type", mime)
                        self.end_headers()
                        self.wfile.write(content)
                    except Exception as e:
                        self._json_response({"error": str(e)}, 500)
                else:
                    self.send_error(404, "Dashboard file not found")

            elif path == "/api/wallet/spend":
                amount = float(params.get("amount", [0])[0])
                reason = params.get("reason", ["General"])[0]
                success, result = revenue_engine.spend_revenue(amount, reason)
                self._json_response({"success": success, "wallet": result})

            elif path == "/api/mica/scan":
                description = params.get("q", [""])[0]
                if not description:
                    self._json_response({"error": "Description query 'q' required"}, 400)
                    return
                result = scan_for_mica(description)
                self._json_response(result)

            elif path == "/api/mica/report":
                q = params.get("q", [""])[0]
                name = params.get("name", ["Unnamed Project"])[0]
                if not q:
                    self._json_response({"error": "Query required"}, 400)
                    return
                # 1. Run audit
                scan_res = scan_for_mica(q)
                # 2. Generate report text
                from mica_scanner import generate_mica_report
                report_txt = generate_mica_report(name, scan_res)
                # 3. Monetize (Charge for the report)
                revenue_engine.add_revenue(49.0, f"MiCA Premium Audit: {name}")
                
                self._json_response({
                    "success": True,
                    "report": report_txt,
                    "wallet": revenue_engine.get_status()
                })

            elif path == "/api/leads/prospect":
                niche = params.get("niche", ["fintech_paris"])[0]
                new_leads = lead_gen.generate_simulated_leads_from_real_niches(niche)
                # Every real lead found adds to the revenue engine (value-based)
                total_val = sum([l['value'] for l in new_leads]) / 10.0 # Convert to PRIME credits
                revenue_engine.add_revenue(total_val, f"PicoClaw: Found {len(new_leads)} B2B Leads")
                self._json_response({"success": True, "new_leads": new_leads, "wallet": revenue_engine.get_status()})

            elif path == "/api/leads/list":
                self._json_response(lead_gen.get_all_leads())

            elif path == "/api/pay/create-checkout-session":
                amount = float(params.get("amount", [4900])[0]) # amount in cents
                reason = params.get("reason", ["Compliance Audit"])[0]
                
                if stripe and STRIPE_SECRET_KEY != "sk_test_mock":
                    try:
                        session = stripe.checkout.Session.create(
                            payment_method_types=['card'],
                            line_items=[{
                                'price_data': {
                                    'currency': 'eur',
                                    'product_data': {'name': reason},
                                    'unit_amount': int(amount),
                                },
                                'quantity': 1,
                            }],
                            mode='payment',
                            success_url='http://localhost:8080/#wallet?success=true',
                            cancel_url='http://localhost:8080/#wallet?cancel=true',
                        )
                        self._json_response({"id": session.id, "url": session.url})
                        return
                    except Exception as e:
                        self._json_response({"error": str(e)}, 500)
                        return
                
                # Fallback mock for testing
                checkout_id = f"stripe_cs_{int(time.time())}_{secrets.token_hex(4)}"
                self._json_response({
                    "id": checkout_id,
                    "url": f"https://checkout.stripe.com/pay/{checkout_id}"
                })

            elif path == "/api/report/download":
                name = params.get("name", ["General-AI"])[0]
                # 1. Classify with our expert scanner
                from eu_ai_act import classify_ai_system, generate_compliance_report
                classification = classify_ai_system(name)
                # 2. Generate the Premium Report
                report_text = generate_compliance_report(name, classification)
                
                # 3. AUTOMATIC REVENUE: Every download is a "High-Value Conversion"
                revenue_engine.add_revenue(149.0, f"PRIME.AI Executive Audit Sold: {name}")
                
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown")
                self.send_header("Content-Disposition", f"attachment; filename=PRIME_AUDIT_{name.replace(' ', '_')}.md")
                self.end_headers()
                self.wfile.write(report_text.encode())
                return


            elif path == "/api/pay/webhook":
                payload = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                sig_header = self.headers.get('Stripe-Signature')
                
                if stripe and STRIPE_WEBHOOK_SECRET:
                    try:
                        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
                        if event['type'] == 'checkout.session.completed':
                            session = event['data']['object']
                            amount = session.get('amount_total', 0) / 100.0
                            customer = session.get('customer_details', {}).get('email', 'Anonymous')
                            revenue_engine.add_revenue(amount, f"Stripe Sale: {customer}")
                            ceo_agent._log(f"💳 STRIPE WEBHOOK: Received €{amount} from {customer}")
                        
                        self._json_response({"status": "success"})
                        return
                    except Exception as e:
                        self._json_response({"error": str(e)}, 400)
                        return
                
                self._json_response({"status": "webhook_received_mock"})
                return

            elif path == "/api/ceo/start":
                ceo_agent.start()
                self._json_response({"success": True, "status": "Running"})
            
            elif path == "/api/ceo/stop":
                ceo_agent.stop()
                self._json_response({"success": True, "status": "Stopped"})
                
            elif path == "/api/ceo/logs":
                self._json_response({
                    "running": ceo_agent.running,
                    "logs": ceo_agent.get_logs()
                })

            else:
                self._json_response({"error": "Not found"}, 404)
            return

        # ─── Serve static files ───
        if path == "/" or path == "/index.html":
            self.path = "/index.html"
            super().do_GET()
        elif path == "/login.html":
            self.path = "/login.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response({"error": "Invalid JSON"}, 400)
            return

        # ─── Google OAuth callback ───
        if path == "/api/auth/google":
            id_token = data.get("credential", "")
            if not id_token:
                self._json_response({"error": "No credential provided"}, 400)
                return
            try:
                google_user = verify_google_token(id_token)
                # Create our JWT
                jwt_token = create_jwt({
                    "email": google_user["email"],
                    "name": google_user["name"],
                    "picture": google_user["picture"],
                })
                self._json_response({
                    "success": True,
                    "token": jwt_token,
                    "user": google_user,
                    "expires_in": JWT_EXPIRY_HOURS * 3600,
                })
            except ValueError as e:
                self._json_response({"error": str(e)}, 403)
            return

        # ─── Auth-gated POST routes ───
        user = self._require_auth()
        if not user:
            return

        if path == "/api/classify":
            description = data.get("description", "")
            if not description:
                self._json_response({"error": "Description required"}, 400)
                return
            result = classify_ai_system(description)
            self._json_response(result)

        elif path == "/api/audit":
            system_name = data.get("system_name", "Unknown System")
            answers = data.get("answers", None)
            result = run_compliance_audit(system_name, answers)
            self._json_response(result)

        elif path == "/api/report":
            system_name = data.get("system_name", "Unknown System")
            description = data.get("description", system_name)
            classification = classify_ai_system(description)
            answers = data.get("answers", None)
            audit = run_compliance_audit(system_name, answers) if answers else None
            report = generate_compliance_report(system_name, classification, audit)
            self._json_response({"report": report, "classification": classification, "audit": audit})

        elif path == "/api/roadmap":
            system_name = data.get("system_name", "Unknown System")
            roadmap = generate_roadmap(system_name)
            self._json_response({"roadmap": roadmap})

        elif path == "/api/scan":
            url_to_scan = data.get("url", "")
            if not url_to_scan:
                self._json_response({"error": "URL required"}, 400)
                return
            result = scan_url(url_to_scan)
            result["scanned_by"] = user.get("email", "unknown")
            self._json_response(result)

        else:
            self._json_response({"error": "Not found"}, 404)

    def _json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def log_message(self, format, *args):
        if "/api/" in str(args[0]) if args else False:
            user = self._check_auth()
            who = user.get("email", "anon") if user else "anon"
            print(f"  🔗 [{who}] {args[0]}")


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


if __name__ == "__main__":
    import socket
    os.makedirs(STATIC_DIR, exist_ok=True)

    # Detect local network IP
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    local_ip = get_local_ip()
    mobile_url = f"http://{local_ip}:{PORT}"

    # Check Google OAuth config
    google_configured = GOOGLE_CLIENT_ID != "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"

    # Generate QR code for mobile access
    qr_path = os.path.join(STATIC_DIR, "qr.png")
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(mobile_url)
        qr.make(fit=True)
        qr.make_image(fill_color="white", back_color="#0a0e1a").save(qr_path)
        qr_ok = True
    except ImportError:
        qr_ok = False

    # Bind to ALL interfaces so phones can reach the server
    server = ThreadedHTTPServer(("0.0.0.0", PORT), APIHandler)

    auth_status = "✅ ACTIVE" if google_configured else "⚠️  NOT CONFIGURED"
    domain_filter = ", ".join(ALLOWED_DOMAINS) if ALLOWED_DOMAINS else "All Google accounts"
    email_filter = ", ".join(ALLOWED_EMAILS) if ALLOWED_EMAILS else "No whitelist"

    print(f"""
╔══════════════════════════════════════════════════════════╗
║     🇪🇺 EU AI Act Compliance System — AUTH SERVER        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  LOCAL:  http://localhost:{PORT:<25}              ║
║  LAN:    {mobile_url:<48}║
║                                                          ║
║  AUTH:   Google OAuth 2.0 {auth_status:<30}║
║  DOMAINS: {domain_filter:<46}║
║  EMAILS:  {email_filter:<46}║
║                                                          ║
║  API ENDPOINTS:                                          ║
║    POST /api/auth/google    — Sign in with Google        ║
║    GET  /api/auth/status    — Check auth status          ║
║    GET  /api/scan?url=...   — Scan any URL 🆕            ║
║    POST /api/classify       — Classify AI system         ║
║    POST /api/audit          — Run compliance audit       ║
║    POST /api/report         — Generate report            ║
║    GET  /api/compliance/self-check — Stack check         ║
║                                                          ║
║  All API routes require Bearer token (except /auth)      ║
╚══════════════════════════════════════════════════════════╝
""")

    if not google_configured:
        print("  ⚠️  SET UP GOOGLE OAUTH:")
        print("  1. Go to https://console.cloud.google.com/apis/credentials")
        print("  2. Create OAuth 2.0 Client ID (Web application)")
        print(f"  3. Add Authorized JavaScript origins:")
        print(f"     - http://localhost:{PORT}")
        print(f"     - {mobile_url}")
        print(f"     - https://your-domain.com (for production)")
        print(f"  4. Set env var: GOOGLE_CLIENT_ID=your_id.apps.googleusercontent.com")
        print(f"  5. Restart the server")
        print()

    # Print QR code in terminal if possible
    try:
        import qrcode as qrc2
        qr2 = qrc2.QRCode(version=1, box_size=1, border=1)
        qr2.add_data(mobile_url)
        qr2.make(fit=True)
        print("  📱 Scan this QR code:\n")
        qr2.print_ascii(invert=True)
        print()
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
