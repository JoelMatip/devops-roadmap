from flask import Flask
import redis
import osSet-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

app = Flask(__name__)

# Use environment variables with defaults
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

r = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def hello():
    count = r.incr('hits')
    return f"Hello from Flask + Redis! This page has been visited {count} times."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('FLASK_PORT', 5000)))