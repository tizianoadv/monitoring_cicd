from flask import Flask, request, jsonify, render_template
import redis, os

app = Flask(__name__)

# Connect to Redis database
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")
redis_db = os.getenv("REDIS_DB")

try:
    redis_conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)
except redis.exceptions.ConnectionError as e:
    print("Redis connection error:", e)

@app.route('/flush', methods=['GET'])
def flush_db():
    redis_conn.flushdb()
    return jsonify({'message': 'DB flush successfully.'}), 200

# POST endpoint to receive data and store it to Redis database
@app.route('/data', methods=['POST'])
def post_data():
    payload = request.json
    data = {
        'temperature': str(payload['temperature']),
        'humidity': str(payload['humidity']),
        'luminosity': str(payload['luminosity']),
        'timestamp': str(payload['timestamp'])
    }
    redis_conn.hmset(data['timestamp'], data)
    return jsonify({'message': 'Data stored successfully.'}), 200   

# GET endpoint to fetch data from Redis database and transmit it to user's browser
@app.route('/data', methods=['GET'])
def get_data():
    data = {}
    for key in redis_conn.scan_iter():
        key_str = key.decode()
        data[key_str] = {k.decode(): v.decode() for k, v in redis_conn.hgetall(key).items()}
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)