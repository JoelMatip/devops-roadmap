from flask import Flask, render_template, request, redirect, url_for
from redis import Redis
from datetime import datetime
import os

app = Flask(__name__)
r = Redis.from_url(os.environ.get("REDIS_URL"))


@app.route("/")
def index():
    count = r.incr("hits")
    names = r.lrange("usernames", 0, -1)
    names = [name.decode("utf-8") for name in names]
    return render_template("index.html", count=count, names=names)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{username} ({timestamp})"
    r.rpush("usernames", entry)
    return redirect(url_for("index"))

@app.route("/reset", methods=["POST"])
def reset():
    r.set("hits", 0)
    return redirect(url_for("index"))

@app.route("/clear", methods=["POST"])
def clear():
    r.delete("usernames")
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html", name="Ajay", version="1.0", redis_status=r.ping())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))