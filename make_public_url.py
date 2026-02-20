"""
EU AI Act PWA — QR Code & Public URL Generator
================================================
1. Shows QR code for local WiFi access
2. Optionally creates a public ngrok tunnel URL

Usage: python make_public_url.py
"""

import sys
import time
import socket
import os

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    PORT = 8080
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:{PORT}"

    print()
    print("=" * 56)
    print("  EU AI Act Compliance — Mobile Access")
    print("=" * 56)
    print()

    # Check if server is running
    try:
        import requests
        r = requests.get(f"http://127.0.0.1:{PORT}/api/stats", timeout=3)
        data = r.json()
        print(f"  ✅ Server OK — {data['days_remaining']} days remaining")
    except Exception:
        print("  ⚠️  Server not detected. Starting it...")
        import subprocess
        subprocess.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__), "eu_ai_act_server.py")],
            creationflags=0x00000010  # CREATE_NEW_CONSOLE
        )
        time.sleep(4)
        print("  ✅ Server started!")

    print()

    # ── Always show WiFi QR Code ──
    print("  " + "─" * 50)
    print(f"  📶 WiFi URL: {local_url}")
    print("  " + "─" * 50)
    print()

    # Generate & save QR image
    try:
        import qrcode
        qr_path = os.path.join(os.path.dirname(__file__), "web", "qr.png")
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(local_url)
        qr.make(fit=True)
        qr.make_image(fill_color="white", back_color="#0f1117").save(qr_path)
        print(f"  📁 QR image saved: {qr_path}")
    except ImportError:
        print("  ⚠️  pip install qrcode[pil] for QR image")

    # Print QR in terminal
    try:
        import qrcode as qrc
        qr2 = qrc.QRCode(version=1, box_size=1, border=1)
        qr2.add_data(local_url)
        qr2.make(fit=True)
        print()
        print("  📱 Scannez ce QR code avec votre téléphone:")
        print()
        qr2.print_ascii(invert=True)
    except Exception:
        print(f"\n  Open: {local_url}")

    print()
    print("  " + "─" * 50)
    print("  📲 COMMENT INSTALLER SUR VOTRE TÉLÉPHONE:")
    print()
    print(f"    1. Même WiFi que ce PC")
    print(f"    2. Scannez le QR ou ouvrez {local_url}")
    print(f"    3. Chrome: ⋮ > 'Installer l'application'")
    print(f"    4. Safari: ↑ > 'Sur l'écran d'accueil'")
    print("  " + "─" * 50)
    print()

    # ── Try public URL via ngrok ──
    try:
        from pyngrok import ngrok
        print("  🌍 Création du tunnel public (ngrok)...")
        tunnel = ngrok.connect(PORT, "http", bind_tls=True)
        public_url = tunnel.public_url

        # Save public QR
        try:
            import qrcode
            qr_pub_path = os.path.join(os.path.dirname(__file__), "web", "qr_public.png")
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(public_url)
            qr.make(fit=True)
            qr.make_image(fill_color="white", back_color="#0f1117").save(qr_pub_path)
        except Exception:
            pass

        print()
        print("  " + "=" * 50)
        print(f"  🌐 PUBLIC URL: {public_url}")
        print("  " + "=" * 50)
        print()
        print("  This URL works from ANYWHERE — no WiFi needed!")
        print("  Share it by SMS, WhatsApp, email...")
        print()

        # Print public QR
        try:
            import qrcode as qrc
            qr3 = qrc.QRCode(version=1, box_size=1, border=1)
            qr3.add_data(public_url)
            qr3.make(fit=True)
            print("  QR code public:")
            print()
            qr3.print_ascii(invert=True)
        except Exception:
            pass

        print()
        print("  Press Ctrl+C to stop the tunnel")
        print()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            ngrok.kill()
            print("\n  Tunnel stopped.")

    except Exception as e:
        err = str(e)
        if "authtoken" in err.lower() or "ERR_NGROK" in err:
            print("  ℹ️  Pour un URL public (optionnel):")
            print("    1. Créez un compte gratuit: https://ngrok.com")
            print("    2. Copiez votre authtoken")
            print("    3. ngrok config add-authtoken VOTRE_TOKEN")
            print("    4. Relancez ce script")
        else:
            print(f"  ℹ️  Tunnel public non disponible: {e}")
        
        print()
        print(f"  👉 Utilisez l'URL WiFi: {local_url}")
        print()

if __name__ == "__main__":
    main()
