"""
Browser Research Tools for OpenClaw
Opens Perplexity for deep search and ChatGPT for AI reasoning.
Uses Chrome/Edge via shell and PyAutoGUI for interaction.
"""
import pyautogui
import subprocess
import sys
import time
import os
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def open_url_robust(url):
    """Open a URL using explicit browser commands (Chrome then Edge)."""
    # Try Chrome
    try:
        subprocess.Popen(["start", "chrome", url], shell=True)
        return
    except:
        pass
    
    # Try Edge
    try:
        subprocess.Popen(["start", "msedge", url], shell=True)
        return
    except:
        pass
        
    # Fallback to default
    subprocess.Popen(["start", url], shell=True)

def open_perplexity(query=None):
    """Open Perplexity AI for deep research."""
    url = "https://www.perplexity.ai/"
    if query:
        url = f"https://www.perplexity.ai/search?q={query.replace(' ', '+')}"
    
    open_url_robust(url)
    time.sleep(3)
    return f"Opened Perplexity: {url}"

def open_chatgpt(message=None):
    """Open ChatGPT for powerful AI reasoning."""
    url = "https://chat.openai.com/"
    
    open_url_robust(url)
    time.sleep(3)
    
    if message:
        # Wait for page to load, then type
        time.sleep(3)
        pyautogui.typewrite(message, interval=0.02)
        return f"Opened ChatGPT and typed: {message[:50]}..."
    return "Opened ChatGPT"

def search_perplexity(query):
    """Open Perplexity, type query, and submit for deep search."""
    open_perplexity()
    time.sleep(4)
    
    # Click the search box (center-ish of screen)
    screen_w, screen_h = pyautogui.size()
    pyautogui.click(screen_w // 2, screen_h // 2)
    time.sleep(0.5)
    
    # Type the query using clipboard (supports all characters)
    pyperclip.copy(query)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # Press Enter to search
    pyautogui.press('enter')
    
    # Wait for results
    time.sleep(8)
    
    # Take screenshot of results
    screenshot_path = os.path.join(os.path.dirname(__file__), "perplexity_result.png")
    img = pyautogui.screenshot()
    img.save(screenshot_path)
    
    return f"Searched Perplexity for: '{query}'. Screenshot saved: {screenshot_path}"

def chat_with_gpt(message):
    """Open ChatGPT, type message, and send."""
    open_chatgpt()
    time.sleep(5)
    
    # ChatGPT input is usually at the bottom
    screen_w, screen_h = pyautogui.size()
    pyautogui.click(screen_w // 2, int(screen_h * 0.85))
    time.sleep(0.5)
    
    # Type using clipboard (supports all characters including unicode)
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # Send
    pyautogui.press('enter')
    
    # Wait for response
    time.sleep(15)
    
    # Take screenshot
    screenshot_path = os.path.join(os.path.dirname(__file__), "chatgpt_result.png")
    img = pyautogui.screenshot()
    img.save(screenshot_path)
    
    return f"Sent to ChatGPT: '{message[:50]}...'. Screenshot saved: {screenshot_path}"

def open_url(url):
    """Open any URL."""
    open_url_robust(url)
    time.sleep(3)
    return f"Opened: {url}"

def google_search(query):
    """Quick Google search."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    open_url_robust(url)
    time.sleep(3)
    
    screenshot_path = os.path.join(os.path.dirname(__file__), "google_result.png")
    img = pyautogui.screenshot()
    img.save(screenshot_path)
    
    return f"Google searched: '{query}'. Screenshot: {screenshot_path}"

# CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python browser_tools.py <command> [args...]")
        print("Commands:")
        print("  perplexity [query]     - Open Perplexity (optional search)")
        print("  deep_search <query>    - Deep search on Perplexity")
        print("  chatgpt [message]      - Open ChatGPT (optional message)")
        print("  ask_gpt <message>      - Send message to ChatGPT")
        print("  google <query>         - Google search")
        print("  open <url>             - Open any URL")
        sys.exit(1)

    cmd = sys.argv[1]
    args = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None

    commands = {
        "perplexity": lambda: open_perplexity(args),
        "deep_search": lambda: search_perplexity(args) if args else "Error: query required",
        "chatgpt": lambda: open_chatgpt(args),
        "ask_gpt": lambda: chat_with_gpt(args) if args else "Error: message required",
        "google": lambda: google_search(args) if args else "Error: query required",
        "open": lambda: open_url(args) if args else "Error: URL required",
    }

    if cmd in commands:
        result = commands[cmd]()
        print(result)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
