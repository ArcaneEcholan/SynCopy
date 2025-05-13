from pathlib import Path
import pyperclip
import time
import hashlib
from datetime import datetime, timezone, timedelta
import threading
import argparse

def generate_filename():
    now = datetime.now().astimezone()
    timestamp = now.strftime("%Y%m%dT%H%M%S")
    ns = time.time_ns() % 1_000_000_000
    return f"{timestamp}_{ns:09d}.txt"


def clipboard_monitor_loop(shared_dir):
    seen_hash = None
    while True:
        content = pyperclip.paste()
        h = hashlib.md5(content.encode()).hexdigest()
        if content and h != seen_hash:
            print(f"detect clipboard changed: {content}")
            fname = generate_filename()
            path = Path(shared_dir) / "items" / fname
            path.write_text(content, encoding="utf-8")
            seen_hash = h
        time.sleep(0.1)


def clipboard_apply_loop(shared_dir):
    applied_file = Path.home() / "synccopymeta" / "last_applied.txt"
    while True:
        applied = applied_file.read_text().strip() if applied_file.exists() else ""

        items = sorted(Path(shared_dir).joinpath("items").glob("*.txt"))
        for item in reversed(items):  # newest first
            if item.name == applied:
                break
            content = item.read_text(encoding="utf-8")
            print(f"found file to apply, copy to clipboard: {item.name}, {content}")
            pyperclip.copy(content)
            applied_file.write_text(item.name)
            break
        time.sleep(0.1)


parser = argparse.ArgumentParser()
parser.add_argument('--shared-dir', type=str, required=True, help='path to sync directory where clipboard text files is stored')
args = parser.parse_args()

shared_dir = args.shared_dir

Path(shared_dir, "items").mkdir(parents=True, exist_ok=True)
Path(Path.home(), "synccopymeta").mkdir(parents=True, exist_ok=True)

threading.Thread(target=clipboard_monitor_loop, args=(shared_dir,), daemon=True).start()
threading.Thread(target=clipboard_apply_loop, args=(shared_dir,), daemon=True).start()

while True:
    time.sleep(60)
