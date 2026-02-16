import json
import os

FILE = "seen_jobs.json"

def load_seen():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return []

def save_seen(data):
    with open(FILE, "w") as f:
        json.dump(data, f)
