"""
Lead Generation & Email Campaign System for PRIME.AI
Searches the web for prospects, collects emails, sends personalized campaigns.
"""
import smtplib
import csv
import time
import os
import sys
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


# ============================================================
# CONFIGURATION - Update these before first use
# ============================================================
SMTP_CONFIG = {
    "server": "smtp.gmail.com",
    "port": 587,
    "email": "info.primeai@gmail.com",
    "password": "",  # Use Gmail App Password (NOT your regular password)
}

CAMPAIGN_CONFIG = {
    "sender_name": "PRIME.AI",
    "sender_email": "info.primeai@gmail.com",
    "subject": "🚀 Boostez votre business avec des visuels pro IA — Offre exclusive 149€",
    "delay_between_emails": 15,  # seconds between each email (anti-spam)
    "max_per_session": 50,       # max emails per run
    "flyer_path": r"C:\Users\Mr Robot\YBE\WhatsApp Image 2026-02-18 at 11.38.32.jpeg",
}


# ============================================================
# HTML EMAIL TEMPLATE
# ============================================================
def get_email_html(prospect_name, prospect_company=""):
    """Generate personalized HTML email for PRIME.AI campaign."""
    
    company_line = f" et {prospect_company}" if prospect_company else ""
    
    return f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:0; background-color:#f4f4f8; font-family: Arial, Helvetica, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f8; padding:20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding:30px 40px; text-align:center;">
                            <h1 style="color:#ffffff; margin:0; font-size:28px; letter-spacing:1px;">🚀 PRIME.AI</h1>
                            <p style="color:#a0a0cc; margin:8px 0 0; font-size:14px;">Visuels professionnels propulsés par l'IA</p>
                        </td>
                    </tr>
                    
                    <!-- Greeting -->
                    <tr>
                        <td style="padding:30px 40px 10px;">
                            <p style="font-size:16px; color:#333; margin:0;">
                                Bonjour <strong>{prospect_name}</strong>{company_line},
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Body -->
                    <tr>
                        <td style="padding:10px 40px;">
                            <p style="font-size:15px; color:#555; line-height:1.7;">
                                Vous cherchez à <strong>booster votre visibilité</strong> avec des visuels de qualité professionnelle — 
                                sans photographe et à un prix imbattable ?
                            </p>
                            <p style="font-size:15px; color:#555; line-height:1.7;">
                                Chez <strong>PRIME.AI</strong>, nous utilisons l'intelligence artificielle pour créer 
                                des contenus visuels <strong>haut de gamme</strong> pour votre entreprise :
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Features -->
                    <tr>
                        <td style="padding:10px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="padding:12px 15px; background:#f8f9ff; border-radius:8px; margin-bottom:8px;">
                                        <span style="font-size:20px;">🎨</span>
                                        <strong style="color:#1a1a2e; font-size:15px;"> 25 visuels professionnels</strong>
                                        <span style="color:#777; font-size:13px;"> — adaptés à votre marque</span>
                                    </td>
                                </tr>
                                <tr><td style="height:8px;"></td></tr>
                                <tr>
                                    <td style="padding:12px 15px; background:#f8f9ff; border-radius:8px;">
                                        <span style="font-size:20px;">🎬</span>
                                        <strong style="color:#1a1a2e; font-size:15px;"> 3 vidéos courtes</strong>
                                        <span style="color:#777; font-size:13px;"> — prêtes pour les réseaux sociaux</span>
                                    </td>
                                </tr>
                                <tr><td style="height:8px;"></td></tr>
                                <tr>
                                    <td style="padding:12px 15px; background:#f8f9ff; border-radius:8px;">
                                        <span style="font-size:20px;">⚡</span>
                                        <strong style="color:#1a1a2e; font-size:15px;"> Livraison rapide</strong>
                                        <span style="color:#777; font-size:13px;"> — résultats en quelques jours</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Price CTA -->
                    <tr>
                        <td style="padding:25px 40px; text-align:center;">
                            <div style="background: linear-gradient(135deg, #e63946 0%, #c1121f 100%); border-radius:12px; padding:25px; display:inline-block; width:80%;">
                                <p style="color:#fff; font-size:13px; margin:0 0 5px; text-decoration:line-through; opacity:0.8;">239€ HT</p>
                                <p style="color:#fff; font-size:32px; font-weight:bold; margin:0;">149€ HT</p>
                                <p style="color:#ffccd5; font-size:13px; margin:5px 0 0;">OFFRE EXCLUSIVE — Durée limitée</p>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- CTA Button -->
                    <tr>
                        <td style="padding:10px 40px 30px; text-align:center;">
                            <a href="mailto:info.primeai@gmail.com?subject=Je%20suis%20intéressé%20par%20l'offre%20PRIME.AI"
                               style="display:inline-block; background:#1a1a2e; color:#ffffff; padding:15px 40px; border-radius:8px; text-decoration:none; font-size:16px; font-weight:bold; letter-spacing:0.5px;">
                                ✉️ Je suis intéressé(e)
                            </a>
                        </td>
                    </tr>
                    
                    <!-- Flyer Image -->
                    <tr>
                        <td style="padding:0 40px 20px; text-align:center;">
                            <img src="cid:flyer_image" alt="PRIME.AI Offre" style="width:100%; max-width:500px; border-radius:10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);"/>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background:#f8f9ff; padding:20px 40px; text-align:center; border-top:1px solid #eee;">
                            <p style="color:#999; font-size:12px; margin:0;">
                                PRIME.AI — Production sans photographe | Équipe française 🇫🇷
                            </p>
                            <p style="color:#bbb; font-size:11px; margin:8px 0 0;">
                                Pour ne plus recevoir nos emails, répondez "STOP" à ce message.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


# ============================================================
# EMAIL SENDING
# ============================================================
def send_email(to_email, prospect_name, prospect_company=""):
    """Send a personalized PRIME.AI campaign email with embedded flyer."""
    
    msg = MIMEMultipart("related")
    msg["From"] = f"{CAMPAIGN_CONFIG['sender_name']} <{CAMPAIGN_CONFIG['sender_email']}>"
    msg["To"] = to_email
    msg["Subject"] = CAMPAIGN_CONFIG["subject"]
    
    # Attach HTML body
    html_content = get_email_html(prospect_name, prospect_company)
    html_part = MIMEMultipart("alternative")
    html_part.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(html_part)
    
    # Embed flyer image
    flyer_path = CAMPAIGN_CONFIG["flyer_path"]
    if os.path.exists(flyer_path):
        with open(flyer_path, "rb") as f:
            img = MIMEImage(f.read(), _subtype="jpeg")
            img.add_header("Content-ID", "<flyer_image>")
            img.add_header("Content-Disposition", "inline", filename="PRIME_AI_Offre.jpg")
            msg.attach(img)
    
    # Send
    try:
        server = smtplib.SMTP(SMTP_CONFIG["server"], SMTP_CONFIG["port"])
        server.starttls()
        server.login(SMTP_CONFIG["email"], SMTP_CONFIG["password"])
        server.send_message(msg)
        server.quit()
        return True, "Sent"
    except Exception as e:
        return False, str(e)


def run_campaign(csv_path, log_path=None):
    """Run email campaign from a CSV prospect list."""
    
    if not log_path:
        log_path = os.path.join(os.path.dirname(csv_path), "campaign_log.json")
    
    # Load previously sent (avoid duplicates)
    sent_emails = set()
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            log_data = json.load(f)
            sent_emails = set(log_data.get("sent", []))
    
    # Read prospects
    prospects = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            prospects.append(row)
    
    print(f"\n{'='*60}")
    print(f"  PRIME.AI Email Campaign")
    print(f"  Prospects: {len(prospects)}")
    print(f"  Already sent: {len(sent_emails)}")
    print(f"  Delay: {CAMPAIGN_CONFIG['delay_between_emails']}s between emails")
    print(f"{'='*60}\n")
    
    results = {"sent": list(sent_emails), "failed": [], "skipped": []}
    count = 0
    
    for i, prospect in enumerate(prospects):
        email = prospect.get("email", "").strip()
        name = prospect.get("name", prospect.get("nom", "")).strip()
        company = prospect.get("company", prospect.get("entreprise", "")).strip()
        
        if not email:
            print(f"  [{i+1}/{len(prospects)}] ⚠️  No email — skipped")
            results["skipped"].append({"name": name, "reason": "no email"})
            continue
        
        if email in sent_emails:
            print(f"  [{i+1}/{len(prospects)}] ⏭️  {email} — already sent")
            results["skipped"].append({"email": email, "reason": "duplicate"})
            continue
        
        if count >= CAMPAIGN_CONFIG["max_per_session"]:
            print(f"\n  ⚠️  Max per session ({CAMPAIGN_CONFIG['max_per_session']}) reached. Stopping.")
            break
        
        success, message = send_email(email, name or "Madame, Monsieur", company)
        
        if success:
            print(f"  [{i+1}/{len(prospects)}] ✅ {email} — {name} ({company})")
            results["sent"].append(email)
            sent_emails.add(email)
            count += 1
        else:
            print(f"  [{i+1}/{len(prospects)}] ❌ {email} — {message}")
            results["failed"].append({"email": email, "error": message})
        
        # Save progress after each email
        with open(log_path, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Delay to avoid spam filters
        if i < len(prospects) - 1:
            time.sleep(CAMPAIGN_CONFIG["delay_between_emails"])
    
    # Final report
    print(f"\n{'='*60}")
    print(f"  Campaign Complete!")
    print(f"  ✅ Sent: {len(results['sent'])}")
    print(f"  ❌ Failed: {len(results['failed'])}")
    print(f"  ⏭️  Skipped: {len(results['skipped'])}")
    print(f"  📄 Log: {log_path}")
    print(f"{'='*60}\n")
    
    return results


# ============================================================
# CLI INTERFACE
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("PRIME.AI Email Campaign Tool")
        print("=" * 40)
        print()
        print("Usage:")
        print("  python email_campaign.py send <prospects.csv>     Send campaign")
        print("  python email_campaign.py test <email>             Send test email")
        print("  python email_campaign.py preview                  Show HTML preview")
        print()
        print("CSV format (semicolon separated):")
        print("  name;company;email;industry;city")
        print("  Jean Dupont;ImmoPlus;jean@immoplus.fr;real_estate;Paris")
        print()
        print("⚠️  Set your Gmail App Password in SMTP_CONFIG first!")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "send":
        if len(sys.argv) < 3:
            print("Error: specify CSV file path")
            sys.exit(1)
        csv_file = sys.argv[2]
        if not os.path.exists(csv_file):
            print(f"Error: file not found: {csv_file}")
            sys.exit(1)
        run_campaign(csv_file)
    
    elif cmd == "test":
        if len(sys.argv) < 3:
            print("Error: specify test email address")
            sys.exit(1)
        test_email = sys.argv[2]
        print(f"Sending test email to {test_email}...")
        success, message = send_email(test_email, "Test User", "Test Company")
        print(f"Result: {'✅ Sent!' if success else f'❌ Failed: {message}'}")
    
    elif cmd == "preview":
        html = get_email_html("Jean Dupont", "ImmoPlus Paris")
        preview_path = os.path.join(os.path.dirname(__file__), "email_preview.html")
        with open(preview_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Preview saved: {preview_path}")
        os.startfile(preview_path)
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
