from flask import Flask, render_template
from flask import redirect, url_for
from flask import request
import redis
import os

app = Flask(__name__)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(redis_url)

@app.route("/")
def index():
    count = r.incr("hits")
    names = r.lrange("usernames", 0, -1)
    names = [name.decode("utf-8") for name in names]
    return render_template("index.html", count=count, names=names)

@app.route("/reset", methods=["POST"])
def reset():
    r.set("hits", 0)
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html", name="Ajay", version="1.0", redis_status=r.ping())

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    r.rpush("usernames", username)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))