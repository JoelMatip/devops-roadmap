from flask import Flask
import redis
import os

app = Flask(__name__)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(redis_url)

@app.route("/")
def index():
    count = r.incr("hits")
    return f"Hello! This page has been visited {count} times."

@app.route("/health")
def health():
    return "App is healthy!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)