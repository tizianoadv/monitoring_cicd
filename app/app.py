from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import redis, os
import pytz


class MonitoringApp:


    def __init__(self):
        """
        This code initializes the MonitoringApp class 
        and creates an instance of the Flask class named app
        """
        self.app = Flask(__name__)

        # Connect to Redis database
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")
        redis_password = os.getenv("REDIS_PASSWORD")
        redis_db = os.getenv("REDIS_DB")

        try:
            self.redis_conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)
            print("Connection to Redis database Sucessfull")
        except redis.exceptions.ConnectionError as e:
            print("Error connection to Redis database", e)

        # Set timezone GMT+2
        self.timezone = pytz.timezone('Europe/Paris')

        # Routes
        self.app.route('/', methods=['GET'])(self.get_all_data)
        self.app.route('/data/<id>', methods=['GET'])(self.get_data_by_id)
        self.app.route('/data/hour', methods=['GET'])(self.get_data_last_hour)
        self.app.route('/data/day', methods=['GET'])(self.get_data_last_day)
        self.app.route('/data/week', methods=['GET'])(self.get_data_last_week)
        self.app.route('/data/month', methods=['GET'])(self.get_data_last_month)
        self.app.route('/data/year', methods=['GET'])(self.get_data_last_year)
        self.app.route('/data', methods=['POST'])(self.post_data)
        self.app.route('/flush', methods=['GET'])(self.flush_database)


    def get_all_data(self):
        """
        Retrieves all data from the Redis database, 
        sorts it in descending order by key and renders it in an HTML template
        """
        try:
            data = {}
            for key in self.redis_conn.scan_iter():
                key_str = key.decode()
                data[key_str] = {k.decode(): v.decode() for k, v in self.redis_conn.hgetall(key).items()}
            sorted_data = dict(sorted(data.items(), reverse=True))
            num_records = len(sorted_data)
            return render_template('index.html', data=sorted_data, num_records=num_records, error_code=200)
        except Exception as e:
            error_msg = f"An error occurred while fetching data from database: {str(e)}"
            return render_template('index.html', error=error_msg, error_code=500)
 

    def get_data_by_id(self, id):
        """
        This function retrieves data from Redis database by its ID and stores it in a dictionary
        It then returns a template that displays the retrieved data
        """
        data = {}
        if self.redis_conn.exists(id):
            data[id] = {k.decode(): v.decode() for k, v in self.redis_conn.hgetall(id).items()}
        return render_template('index.html', data=data)
    

    def get_data_last_hour(self):
        """
        This function retrieves data from Redis database that was added within the last hour
        It then returns a template that displays the retrieved data
        """
        sorted_data = self.get_data_by_time_delta(hours=1)
        return render_template('index.html', data=sorted_data)


    def get_data_last_day(self):
        """
        This function retrieves data from Redis database that was added within the last 24 hours
        It then returns a template that displays the retrieved data
        """
        sorted_data = self.get_data_by_time_delta(hours=24)
        return render_template('index.html', data=sorted_data)
    

    def get_data_last_week(self):
        """
        This function retrieves data from Redis database that was added within the last week
        It then returns a template that displays the retrieved data
        """
        sorted_data = self.get_data_by_time_delta(weeks=1)
        return render_template('index.html', data=sorted_data)
    

    def get_data_last_month(self):
        """
        This function retrieves data from Redis database that was added within the last month
        It then returns a template that displays the retrieved data
        """
        sorted_data = self.get_data_by_time_delta(months=1)
        return render_template('index.html', data=sorted_data)
    

    def get_data_last_year(self):
        """
        This function retrieves data from Redis database that was added within the last year
        It then returns a template that displays the retrieved data
        """
        sorted_data = self.get_data_by_time_delta(months=12)
        return render_template('index.html', data=sorted_data)
    

    def get_data_by_time_delta(self, hours=0, weeks=0, months=0):
        """This function retrieves data from Redis database within a specified time delta 
        (hours, weeks, months or year) based on the timestamp associated with each key in the database
         It returns the sorted data in reverse order
         """
        data = {}
        now_str = datetime.now(self.timezone).strftime('%d-%m-%Y %H:%M:%S')
        now_obj = datetime.strptime(now_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=self.timezone)
        delta = timedelta(hours=hours, weeks=weeks, days=30*months)
        timestamp_threshold = (now_obj - delta)

        for key in self.redis_conn.scan_iter():
            key_str = key.decode()
            timestamp_str = self.redis_conn.hget(key, 'timestamp').decode()
            timestamp_obj = datetime.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=self.timezone)
            if timestamp_obj >= timestamp_threshold and timestamp_obj <= now_obj:
                data[key_str] = {k.decode(): v.decode() for k, v in self.redis_conn.hgetall(key).items()}

        sorted_data = dict(sorted(data.items(), reverse=True))
        return sorted_data


        
    def post_data(self):
        """
        This function receives a JSON payload, extracts data from it
        generates a new unique key for Redis
        and stores the data in Redis with the new key
        """
        payload = request.json
        data = {
            'temperature': payload['temperature'],
            'luminosity': payload['luminosity'],
            'humidity': payload['humidity'],
            'timestamp': payload['timestamp']
        }
        keys = self.redis_conn.keys()
        if len(keys) > 0:
            max_key = max(map(int, keys))
            new_key = max_key + 1
        else:
            new_key = 1
        self.redis_conn.hmset(str(new_key), data)
        data['id'] = str(new_key)
        return jsonify(data), 200


    def flush_database(self):
        try:
            self.redis_conn.flushdb()
            return jsonify({'message': 'DB flush successfully.'}), 200
        except Exception as e:
            error_msg = f"Failed to flush DB: {str(e)}"
            return jsonify({'message': error_msg}), 500


    def run(self):
        self.app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    monitoring_app = MonitoringApp()
    monitoring_app.run()
