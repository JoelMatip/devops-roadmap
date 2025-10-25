from flask import Flask, render_template
import redis
import os

app = Flask(__name__)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(redis_url)

@app.route("/")
def index():
    count = r.incr("hits")
    return render_template("index.html", count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))