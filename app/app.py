from flask import Flask, request, jsonify, render_template
import redis, os

class MonitoringApp:
    def __init__(self):
        self.app = Flask(__name__)

        # Connect to Redis database
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")
        redis_password = os.getenv("REDIS_PASSWORD")
        redis_db = os.getenv("REDIS_DB")

        try:
            self.redis_conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)
        except redis.exceptions.ConnectionError as e:
            print("Redis connection error:", e)

        self.app.route('/flush', methods=['GET'])(self.flush_db)
        self.app.route('/data', methods=['POST'])(self.post_data)
        self.app.route('/data', methods=['GET'])(self.get_data)

    def flush_db(self):
        print("Flushing database")
        self.redis_conn.flushdb()
        print("Database flushed")
        return jsonify({'message': 'DB flush successfully.'}), 200

    def post_data(self):
        payload = request.json
        data = {
            'temperature': str(payload['temperature']),
            'humidity': str(payload['humidity']),
            'luminosity': str(payload['luminosity']),
            'timestamp': str(payload['timestamp'])
        }
        self.redis_conn.hmset(data['timestamp'], data)
        return jsonify({'message': 'Data stored successfully.'}), 200   

    def get_data(self):
        data = {}
        for key in self.redis_conn.scan_iter():
            key_str = key.decode()
            data[key_str] = {k.decode(): v.decode() for k, v in self.redis_conn.hgetall(key).items()}
        return render_template('index.html', data=data)

    def run(self):
        self.app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    monitoring_app = MonitoringApp()
    monitoring_app.run()
