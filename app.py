from flask import Flask, render_template, request, redirect, url_for, session
from redis import Redis
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
r = Redis.from_url(os.environ.get("REDIS_URL"))

@app.route("/")
def index():
    count = r.incr("hits")
    raw_entries = r.lrange("usernames", 0, -1)

    names = []
    for entry in raw_entries:
        decoded = entry.decode("utf-8")
        if decoded.startswith("[") and decoded.endswith("]"):
            try:
                name, timestamp = eval(decoded)
                names.append([name, timestamp])
            except:
                continue
        else:
            # fallback for old format: "AJAY (2025-10-26 16:28:09)"
            if "(" in decoded and ")" in decoded:
                name_part, time_part = decoded.rsplit("(", 1)
                name = name_part.strip()
                timestamp = time_part.strip(") ")
                names.append([name, timestamp])

    username = session.get("username")
    return render_template("index.html", count=count, names=names, username=username)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    session["username"] = username
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    r.rpush("usernames", str([username, timestamp]))
    return redirect(url_for("index"))

@app.route("/clear")
def clear():
    r.delete("usernames")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)