from flask import Flask
import redis
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello():
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        r = redis.Redis.from_url(redis_url)
        r.incr('hits')
        count = r.get('hits').decode('utf-8')
        return f'Hello from Flask + Redis! I have been seen {count} times.'
    except Exception as e:
        app.logger.error(f"Redis error: {e}")
        return f'Redis error: {e}', 500

@app.route('/health')
def health():
    return "App is healthy!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)