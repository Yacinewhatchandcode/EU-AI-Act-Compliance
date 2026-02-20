"""Quick demo of upgraded Android-native PWA using Selenium."""
import os, time, glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

OUT = os.path.join(os.path.dirname(__file__), "demo_android")
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, "*.png")):
    os.remove(f)

opts = Options()
opts.add_argument("--window-size=390,844")
opts.add_argument("--force-device-scale-factor=2")
opts.add_experimental_option("mobileEmulation", {
    "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 2},
    "userAgent": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36"
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
step = 0

def shot(name):
    global step
    step += 1
    path = os.path.join(OUT, f"{step:02d}_{name}.png")
    driver.save_screenshot(path)
    print(f"  {step:02d} {name}")
    return path

try:
    print("\n  EU AI Act PWA — Android Demo\n")

    driver.get("http://127.0.0.1:8080")
    time.sleep(1)
    shot("splash")
    time.sleep(2)
    shot("home_top")

    # Scroll down on home
    driver.execute_script("document.querySelector('.screen.active .screen-scroll').scrollBy(0, 400)")
    time.sleep(0.5)
    shot("home_scroll")

    # Click Classifier via bottom nav
    driver.execute_script("document.querySelectorAll('.nav-item')[1].click()")
    time.sleep(0.8)
    shot("classify_screen")

    # Fill and classify
    driver.execute_script("document.querySelectorAll('.chip')[1].click()")
    time.sleep(0.3)
    shot("classify_filled")
    driver.execute_script("document.getElementById('classifyBtn').click()")
    time.sleep(2)
    shot("classify_result")

    # Scroll to see result
    driver.execute_script("document.querySelector('.screen.active .screen-scroll').scrollBy(0, 300)")
    time.sleep(0.5)
    shot("classify_obligations")

    # Audit via bottom nav
    driver.execute_script("document.querySelectorAll('.nav-item')[2].click()")
    time.sleep(0.8)
    shot("audit_screen")

    # Fill audit
    driver.execute_script("""
        document.getElementById('auditName').value = 'MonIA Recrutement';
        document.getElementById('aud-R1').value = 'PARTIAL';
        document.getElementById('aud-R2').value = 'COMPLIANT';
        document.getElementById('aud-R3').value = 'NON_COMPLIANT';
        document.getElementById('aud-R6').value = 'PARTIAL';
    """)
    time.sleep(0.3)
    driver.execute_script("document.querySelector('#screen-audit .btn-main').click()")
    time.sleep(1.5)
    shot("audit_result")

    # Report via bottom nav
    driver.execute_script("document.querySelectorAll('.nav-item')[3].click()")
    time.sleep(0.8)
    shot("report_screen")

    # Generate report
    driver.execute_script("""
        document.getElementById('reportName').value = 'MonIA Recrutement';
        document.getElementById('reportDesc').value = 'IA de tri de CV pour le recrutement';
    """)
    driver.execute_script("document.querySelector('#screen-report .btn-main').click()")
    time.sleep(2)
    shot("report_result")

    # Scroll report
    driver.execute_script("document.querySelector('.screen.active .screen-scroll').scrollBy(0, 400)")
    time.sleep(0.5)
    shot("report_scroll")

    # Knowledge base via bottom nav
    driver.execute_script("document.querySelectorAll('.nav-item')[4].click()")
    time.sleep(0.8)
    shot("kb_screen")

    # Scroll KB
    driver.execute_script("document.querySelector('.screen.active .screen-scroll').scrollBy(0, 500)")
    time.sleep(0.5)
    shot("kb_scroll")

    # Navigate via action card to agents
    driver.execute_script("document.querySelectorAll('.nav-item')[0].click()")
    time.sleep(0.5)
    driver.execute_script("go('agents')")
    time.sleep(0.8)
    shot("agents_screen")

    # Scroll agents
    driver.execute_script("document.querySelector('.screen.active .screen-scroll').scrollBy(0, 400)")
    time.sleep(0.5)
    shot("agents_arch")

    # Roadmap
    driver.execute_script("go('roadmap')")
    time.sleep(0.8)
    driver.execute_script("""
        document.getElementById('roadmapName').value = 'MonIA Recrutement';
        document.querySelector('#screen-roadmap .btn-main').click();
    """)
    time.sleep(1.5)
    shot("roadmap_result")

    # Scroll roadmap
    driver.execute_script("document.querySelector('.screen.active .screen-scroll').scrollBy(0, 500)")
    time.sleep(0.5)
    shot("roadmap_scroll")

    # Back to home
    driver.execute_script("document.querySelectorAll('.nav-item')[0].click()")
    time.sleep(0.8)
    shot("home_final")

    print(f"\n  Done! {step} screenshots in {OUT}")

    # Create GIF
    try:
        from PIL import Image
        imgs = sorted(glob.glob(os.path.join(OUT, "*.png")))
        frames = [Image.open(f) for f in imgs]
        gif_path = os.path.join(os.path.dirname(__file__), "demo_android.gif")
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=2000, loop=0, optimize=True)
        print(f"  GIF: {gif_path} ({os.path.getsize(gif_path) / 1e6:.1f} MB)")
    except Exception as e:
        print(f"  GIF error: {e}")

finally:
    driver.quit()
