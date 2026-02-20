"""
OpenClaw Desktop Control Bridge
Provides mouse, keyboard, and screenshot capabilities
for OpenClaw to control the full desktop via WhatsApp.
"""
import pyautogui
import subprocess
import sys
import json
import time
import os

# Safety: don't fail instantly on edge of screen
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def screenshot(filename="screenshot.png"):
    """Take a screenshot and save it."""
    path = os.path.join(os.path.dirname(__file__), filename)
    img = pyautogui.screenshot()
    img.save(path)
    return f"Screenshot saved: {path}"

def click(x, y, button="left"):
    """Click at screen coordinates."""
    pyautogui.click(x, y, button=button)
    return f"Clicked ({x}, {y}) with {button} button"

def double_click(x, y):
    """Double click at screen coordinates."""
    pyautogui.doubleClick(x, y)
    return f"Double-clicked ({x}, {y})"

def type_text(text, interval=0.02):
    """Type text with keyboard."""
    pyautogui.typewrite(text, interval=interval)
    return f"Typed: {text[:50]}..."

def hotkey(*keys):
    """Press hotkey combination (e.g., ctrl, c)."""
    pyautogui.hotkey(*keys)
    return f"Pressed: {'+'.join(keys)}"

def press_key(key):
    """Press a single key."""
    pyautogui.press(key)
    return f"Pressed: {key}"

def move_to(x, y):
    """Move mouse to coordinates."""
    pyautogui.moveTo(x, y)
    return f"Moved to ({x}, {y})"

def scroll(clicks, x=None, y=None):
    """Scroll up (positive) or down (negative)."""
    pyautogui.scroll(clicks, x, y)
    return f"Scrolled {clicks} at ({x}, {y})"

def get_screen_size():
    """Get screen resolution."""
    w, h = pyautogui.size()
    return f"Screen size: {w}x{h}"

def get_mouse_position():
    """Get current mouse position."""
    x, y = pyautogui.position()
    return f"Mouse at ({x}, {y})"

def find_window(title):
    """Find a window by title and bring it to front."""
    try:
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            win = windows[0]
            win.activate()
            time.sleep(0.5)
            return f"Found and activated window: {win.title} at ({win.left}, {win.top}) size {win.width}x{win.height}"
        return f"Window '{title}' not found"
    except Exception as e:
        return f"Error finding window: {e}"

def open_app(command):
    """Open an application via shell command."""
    try:
        subprocess.Popen(command, shell=True)
        time.sleep(1)
        return f"Opened: {command}"
    except Exception as e:
        return f"Error opening app: {e}"

def write_to_antigravity(message):
    """Write a message to the Antigravity IDE bridge file."""
    bridge_path = os.path.join(os.path.expanduser("~"), "YBE", "bridge_input.md")
    with open(bridge_path, "w", encoding="utf-8") as f:
        f.write(f"# Task from WhatsApp\n\n{message}\n\n---\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    return f"Written to bridge: {bridge_path}"

def read_antigravity_response():
    """Read the response from Antigravity IDE bridge file."""
    bridge_path = os.path.join(os.path.expanduser("~"), "YBE", "bridge_output.md")
    if os.path.exists(bridge_path):
        with open(bridge_path, "r", encoding="utf-8") as f:
            return f.read()
    return "No response yet."

# CLI interface for OpenClaw shell_exec
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python desktop_control.py <command> [args...]")
        print("Commands: screenshot, click, double_click, type, hotkey, press,")
        print("          move, scroll, screen_size, mouse_pos, find_window,")
        print("          open_app, write_bridge, read_bridge")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "screenshot": lambda: screenshot(args[0] if args else "screenshot.png"),
        "click": lambda: click(int(args[0]), int(args[1]), args[2] if len(args) > 2 else "left"),
        "double_click": lambda: double_click(int(args[0]), int(args[1])),
        "type": lambda: type_text(" ".join(args)),
        "hotkey": lambda: hotkey(*args),
        "press": lambda: press_key(args[0]),
        "move": lambda: move_to(int(args[0]), int(args[1])),
        "scroll": lambda: scroll(int(args[0]), int(args[1]) if len(args) > 1 else None, int(args[2]) if len(args) > 2 else None),
        "screen_size": lambda: get_screen_size(),
        "mouse_pos": lambda: get_mouse_position(),
        "find_window": lambda: find_window(" ".join(args)),
        "open_app": lambda: open_app(" ".join(args)),
        "write_bridge": lambda: write_to_antigravity(" ".join(args)),
        "read_bridge": lambda: read_antigravity_response(),
    }

    if cmd in commands:
        result = commands[cmd]()
        print(result)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
