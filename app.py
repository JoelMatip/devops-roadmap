import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Secret key (must be set in environment for sessions)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret-key")

# Redis connection
REDIS_URL = os.environ.get("REDIS_URL")
if not REDIS_URL:
    raise RuntimeError("REDIS_URL environment variable is not set.")
r = Redis.from_url(REDIS_URL)

# Optional simple admin password for protected actions
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", None)


def parse_entry(decoded: str):
    """
    Safely parse Redis entry in one of two formats:
    - New format: JSON list string '["Ajay", "2025-11-09 15:35"]'
    - Old format: 'Ajay (2025-11-09 15:35)'

    Returns [name, timestamp] or None if unparsable.
    """
    # Try JSON first
    try:
        data = json.loads(decoded)
        if isinstance(data, list) and len(data) == 2 and all(isinstance(x, str) for x in data):
            return [data[0], data[1]]
    except Exception:
        pass

    # Fallback old format: "Name (timestamp)"
    if "(" in decoded and ")" in decoded:
        try:
            name_part, time_part = decoded.rsplit("(", 1)
            name = name_part.strip()
            timestamp = time_part.strip(") ").strip()
            if name and timestamp:
                return [name, timestamp]
        except Exception:
            pass

    return None


@app.route("/")
def index():
    # Increment total visits counter
    count = r.incr("hits")

    # Read and parse all username entries
    raw_entries = r.lrange("usernames", 0, -1)
    names = []
    for entry in raw_entries:
        decoded = entry.decode("utf-8")
        parsed = parse_entry(decoded)
        if parsed:
            names.append(parsed)

    # Current session username
    username = session.get("username")

    # Last visitor tile
    last_visitor = names[-1] if names else None  # [name, timestamp] or None

    # Welcome back tile (find last visit for current user)
    last_visit = None
    if username:
        for name, timestamp in reversed(names):
            if name == username:
                last_visit = timestamp
                break

    # Analytics
    unique_users = len(set([n[0] for n in names]))
    repeat_visits = max(0, count - unique_users)

    return render_template(
        "index.html",
        count=count,
        names=names,
        username=username,
        last_visitor=last_visitor,
        last_visit=last_visit,
        unique_users=unique_users,
        repeat_visits=repeat_visits,
        admin_enabled=bool(ADMIN_PASSWORD),
    )


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username", "").strip()
    if not username:
        return redirect(url_for("index"))

    session["username"] = username
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store in JSON format going forward
    entry = json.dumps([username, timestamp])
    r.rpush("usernames", entry)

    return redirect(url_for("index"))


@app.route("/clear", methods=["POST"])
def clear():
    """
    Admin-only action: Clear usernames list.
    Requires ADMIN_PASSWORD to be set and provided in form.
    """
    if not ADMIN_PASSWORD:
        # If not configured, do nothing
        return redirect(url_for("index"))

    provided = request.form.get("admin_password", "")
    if provided != ADMIN_PASSWORD:
        # Silently fail or show a message (kept silent for simplicity)
        return redirect(url_for("index"))

    r.delete("usernames")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Render expects binding to 0.0.0.0 and reading PORT from env
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)