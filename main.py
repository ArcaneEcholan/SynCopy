from pathlib import Path
import pyperclip, time, hashlib, uuid
from datetime import datetime
import threading


def clipboard_monitor_loop(shared_dir, host_id):
    seen_hash = None
    while True:
        content = pyperclip.paste()
        h = hashlib.md5(content.encode()).hexdigest()
        if content and h != seen_hash:
            print(f"detect clipboard changed: {content}")
            timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            fname = f"{timestamp}__{host_id}.txt"
            path = Path(shared_dir) / "items" / fname
            path.write_text(content, encoding="utf-8")
            seen_hash = h
        time.sleep(0.1)


def init_shared_dirs(shared_dir):
    Path(shared_dir, "items").mkdir(parents=True, exist_ok=True)
    Path(Path.home(), "synccopymeta").mkdir(parents=True, exist_ok=True)

    # host_file = Path(shared_dir) / 'meta' / 'host_id.txt'
    # if not host_file.exists():
    # host_file.write_text(str(uuid.uuid4()))
    # return host_file.read_text().strip()
    return ""


def clipboard_apply_loop(shared_dir, host_id):
    applied_file = Path.home() / "synccopymeta" / "last_applied.txt"
    while True:
        applied = applied_file.read_text().strip() if applied_file.exists() else ""
        # print(f"last_applied file: {applied}")

        items = sorted(Path(shared_dir).joinpath("items").glob("*.txt"))
        for item in reversed(items):  # newest first
            if item.name == applied:
                break
            # if host_id in item.name:
            #     continue  # skip own entries
            content = item.read_text(encoding="utf-8")
            print(f"found file to apply, copy to clipboard: {item.name}, {content}")
            pyperclip.copy(content)
            applied_file.write_text(item.name)
            break
        time.sleep(0.1)


shared_dir = str(Path.home() / "nutfiles" / "docs")
host_id = init_shared_dirs(shared_dir)

threading.Thread(
    target=clipboard_monitor_loop, args=(shared_dir, host_id), daemon=True
).start()
threading.Thread(
    target=clipboard_apply_loop, args=(shared_dir, host_id), daemon=True
).start()

while True:
    time.sleep(60)
