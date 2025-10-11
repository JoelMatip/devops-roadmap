from flask import Flask
import redis
import os

app = Flask(__name__)

# Connect to Redis using environment variables
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def hello():
    r.incr('hits')
    count = r.get('hits').decode('utf-8')
    return f'Hello from Flask + Redis! I have been seen {count} times.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)