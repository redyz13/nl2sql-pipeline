import subprocess
import signal
import sys
import dotenv
import os
from watchfiles import watch
from threading import Thread
from zero_shot.schema.extract_schema import generate_schema_prompt
import time

# 📄 Extracts table and column descriptions from metadata and formats them for LLM prompts (skips if file exists)
generate_schema_prompt()

dotenv.load_dotenv()

ENTRY_MODULE = os.getenv("ENTRY_MODULE", "zero_shot.api.app")
UI_MODULE = os.getenv("UI_MODULE", "zero_shot.ui.app")

python_executable = sys.executable

commands = [
    [python_executable, '-m', ENTRY_MODULE],
    [python_executable, '-m', UI_MODULE]
]

processes = []

def start_processes():
    stop_processes()
    processes.clear()
    for cmd in commands:
        print(f"\n🚀 Starting: {' '.join(cmd)}")
        p = subprocess.Popen(cmd)
        processes.append(p)

def stop_processes():
    for p in processes:
        if p.poll() is None:
            try:
                print(f"🔻 Terminating process {p.pid}")
                p.terminate()
            except Exception:
                pass

def watch_and_reload():
    print("👀 Watching for .py, .json, .env changes...")
    for _ in watch('.', watch_filter=lambda _, path: path.endswith(('.py', '.json', '.env'))):
        print("🔄 Change detected, restarting processes...")
        start_processes()

def handle_exit(signum=None, frame=None):
    print("\n🔻 Stopping processes...")
    stop_processes()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    print(f"🐍 Using interpreter: {python_executable}")
    start_processes()

    watch_thread = Thread(target=watch_and_reload, daemon=True)
    watch_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle_exit()
