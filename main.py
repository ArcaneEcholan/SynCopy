from pathlib import Path
import pyperclip
import time
import hashlib
from datetime import datetime, timezone, timedelta
import threading
import argparse


shared_state = {"seen_hash": None, "lock": threading.Lock()}


def generate_filename():
    now = datetime.now().astimezone()
    timestamp = now.strftime("%Y%m%dT%H%M%S")
    ns = time.time_ns() % 1_000_000_000
    return f"{timestamp}_{ns:09d}.txt"


def clipboard_monitor_loop(sync_dir):
    while True:
        content = pyperclip.paste()
        h = hashlib.md5(content.encode()).hexdigest()
        with shared_state["lock"]:
            if content and h != shared_state["seen_hash"]:
                print(f"detect clipboard changed: {content}")
                fname = generate_filename()
                path = Path(sync_dir) / "items" / fname
                path.write_text(content, encoding="utf-8")
                shared_state["seen_hash"] = h
        time.sleep(0.1)


def clipboard_apply_loop(sync_dir):
    applied_item_record_file = Path.home() / "synccopymeta" / "last_applied.txt"
    while True:
        applied_item_name = (
            applied_item_record_file.read_text().strip()
            if applied_item_record_file.exists()
            else ""
        )

        items = sorted(Path(sync_dir).joinpath("items").glob("*.txt"))
        for item in reversed(items):  # newest item first
            if item.name == applied_item_name:
                break

            # found item never applied to clipboard, apply it to clipboard then
            item_content = item.read_text(encoding="utf-8")
            print(
                f"found file to apply, copy to clipboard: {item.name}, {item_content}"
            )
            # overwrite clipboard with new item
            pyperclip.copy(item_content)

            # record the item as applied(so next time it probably won't be applied again)
            applied_item_record_file.write_text(item.name)

            # tell clipboard monitor thread not to create new item on this clipboard change
            with shared_state["lock"]:
                shared_state["seen_hash"] = hashlib.md5(
                    item_content.encode()
                ).hexdigest()
            break

        time.sleep(0.1)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--sync-dir",
    type=str,
    required=True,
    help="path to sync directory where clipboard text files is stored",
)
args = parser.parse_args()

sync_dir = args.sync_dir

Path(sync_dir, "items").mkdir(parents=True, exist_ok=True)
Path(Path.home(), "synccopymeta").mkdir(parents=True, exist_ok=True)

threading.Thread(target=clipboard_monitor_loop, args=(sync_dir,), daemon=True).start()
threading.Thread(target=clipboard_apply_loop, args=(sync_dir,), daemon=True).start()

while True:
    time.sleep(60)
