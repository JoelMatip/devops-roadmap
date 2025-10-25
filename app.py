from flask import Flask, render_template
from flask import redirect, url_for
import redis
import os

app = Flask(__name__)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(redis_url)

@app.route("/")
def index():
    count = r.incr("hits")
    return render_template("index.html", count=count)

@app.route("/reset", methods=["POST"])
def reset():
    r.set("hits", 0)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))