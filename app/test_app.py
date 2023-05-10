from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import pytz


ENDPOINT = "http://localhost:5000"
TIMEZONE = pytz.timezone('Europe/Paris')


def test_can_call_endpoint():
    """Test if the API endpoint can be called"""

    response = requests.get(ENDPOINT + "/")
    assert response.status_code == 200


def test_flush_database():
    """Test if the API can flush the database"""

    response = requests.get(ENDPOINT + "/flush")
    assert response.status_code == 200


def test_get_all_data_format():
    """Test if the API can get all data in a specific format"""

    response = requests.get(ENDPOINT + "/")
    data = parse_html_row(response.text)
    # Check if all values are strings
    assert all(isinstance(value, str) for row in data for value in row.values())
    # Check if only valid keys
    assert all(set(row.keys()) == {'id', 'temperature', 'luminosity', 'humidity', 'timestamp'} for row in data)


def test_post_new_data():
    """Test if the API can post new data and retrieve it"""

    now = datetime.now(TIMEZONE)
    post_data_response = send_post_data(now)
    assert post_data_response.status_code == 200
    post_data_response = post_data_response.json()
    data_id = post_data_response["id"]

    get_data_by_id_response = requests.get(ENDPOINT + f"/data/{data_id}")
    assert get_data_by_id_response.status_code == 200

    get_data_by_id_response = parse_html_row(get_data_by_id_response.text)
    get_data_by_id_response = get_data_by_id_response[0]
    assert get_data_by_id_response['id']            == post_data_response['id']
    assert get_data_by_id_response['temperature']   == post_data_response['temperature']
    assert get_data_by_id_response['humidity']      == post_data_response['humidity']
    assert get_data_by_id_response['luminosity']    == post_data_response['luminosity']
    assert get_data_by_id_response['timestamp']     == post_data_response['timestamp']


def test_get_data_last_hour():
    """Test if the API can get all data registered within the last hour"""

    assert flush_database()
    now = datetime.now(TIMEZONE)
    # Generate data older than 1 hour
    old_data = [ (now - timedelta(days=2)),(now - timedelta(hours=2))]
    for timestamp in old_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    # Generate data within the last hour
    new_data = [(now - timedelta(minutes=30)), (now) ]
    for timestamp in new_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    
    response = requests.get(ENDPOINT + "/data/hour")
    assert response.status_code == 200
    data = parse_html_row(response.text)
    assert len(data) == 2  # Only new data should be returned

    now_str = datetime.now(TIMEZONE).strftime('%d-%m-%Y %H:%M:%S')
    now_obj = datetime.strptime(now_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
    timestamp_threshold = (now_obj - timedelta(hours=1))
    for entry in data:
        entry['timestamp']
        timestamp_str = entry['timestamp']
        timestamp_obj = datetime.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
        assert timestamp_obj >= timestamp_threshold and timestamp_obj <= now_obj


def test_get_data_last_day():
    """Test if the API can get all data registered within the last day"""

    assert flush_database()
    now = datetime.now(TIMEZONE)
    # Generate data older than 1 day
    old_data = [ (now - timedelta(days=5)),(now - timedelta(days=3))]
    for timestamp in old_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    # Generate data within the last hour
    new_data = [(now - timedelta(hours=23)), (now - timedelta(hours=1)) ]
    for timestamp in new_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    
    response = requests.get(ENDPOINT + "/data/day")
    assert response.status_code == 200
    data = parse_html_row(response.text)
    assert len(data) == 2  # Only new data should be returned

    now_str = datetime.now(TIMEZONE).strftime('%d-%m-%Y %H:%M:%S')
    now_obj = datetime.strptime(now_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
    timestamp_threshold = (now_obj - timedelta(hours=24))

    for entry in data:
        entry['timestamp']
        timestamp_str = entry['timestamp']
        timestamp_obj = datetime.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
        assert timestamp_obj >= timestamp_threshold and timestamp_obj <= now_obj


def test_get_data_last_week():
    """Test if the API can get all data registered within the last week"""

    assert flush_database()
    now = datetime.now(TIMEZONE)

    # Generate data older than 1 week
    old_data = [ (now - timedelta(weeks=3)),(now - timedelta(weeks=2))]
    for timestamp in old_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    # Generate data within the last week
    new_data = [(now - timedelta(days=6)), (now - timedelta(hours=2)) ]
    for timestamp in new_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    
    response = requests.get(ENDPOINT + "/data/week")
    assert response.status_code == 200
    data = parse_html_row(response.text)
    assert len(data) == 2  # Only new data should be returned

    now_str = datetime.now(TIMEZONE).strftime('%d-%m-%Y %H:%M:%S')
    now_obj = datetime.strptime(now_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
    timestamp_threshold = (now_obj - timedelta(weeks=1))

    for entry in data:
        entry['timestamp']
        timestamp_str = entry['timestamp']
        timestamp_obj = datetime.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
        assert timestamp_obj >= timestamp_threshold and timestamp_obj <= now_obj


def test_get_data_last_month():
    """Test if the API can get all data registered within the last month"""

    assert flush_database()
    now = datetime.now(TIMEZONE)
    # Generate data older than 1 month
    old_data = [ (now - timedelta(weeks=10)),(now - timedelta(weeks=5))]
    for timestamp in old_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    # Generate data within the last month
    new_data = [(now - timedelta(weeks=3)), (now - timedelta(hours=2)) ]
    for timestamp in new_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    
    response = requests.get(ENDPOINT + "/data/month")
    assert response.status_code == 200
    data = parse_html_row(response.text)
    assert len(data) == 2  # Only new data should be returned

    now_str = datetime.now(TIMEZONE).strftime('%d-%m-%Y %H:%M:%S')
    now_obj = datetime.strptime(now_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
    timestamp_threshold = (now_obj - timedelta(weeks=4))

    for entry in data:
        entry['timestamp']
        timestamp_str = entry['timestamp']
        timestamp_obj = datetime.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
        assert timestamp_obj >= timestamp_threshold and timestamp_obj <= now_obj


def test_get_data_last_year():
    """Test if the API can get all data registered within the last year"""

    assert flush_database()
    now = datetime.now(TIMEZONE)
    # Generate data older than 1 year
    old_data = [ (now - timedelta(weeks=4*20)),(now - timedelta(weeks=4*13))]
    for timestamp in old_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    # Generate data within the last year
    new_data = [(now - timedelta(weeks=4*12)), (now - timedelta(hours=2)) ]
    for timestamp in new_data:
        response = send_post_data(timestamp)
        assert response.status_code == 200
    
    response = requests.get(ENDPOINT + "/data/year")
    assert response.status_code == 200
    data = parse_html_row(response.text)
    assert len(data) == 2  # Only new data should be returned

    now_str = datetime.now(TIMEZONE).strftime('%d-%m-%Y %H:%M:%S')
    now_obj = datetime.strptime(now_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
    timestamp_threshold = (now_obj - timedelta(weeks=4*12))

    for entry in data:
        entry['timestamp']
        timestamp_str = entry['timestamp']
        timestamp_obj = datetime.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S').replace(tzinfo=TIMEZONE)
        assert timestamp_obj >= timestamp_threshold and timestamp_obj <= now_obj




def send_post_data(timestamp):
    """Send Post data to the API with a specific time"""
    payload = {
        "temperature": str(20.0), 
        "luminosity": str(30.0),
        "humidity": str(40.0),
        "timestamp": timestamp.strftime("%d-%m-%Y %H:%M:%S")
    }
    return requests.post(ENDPOINT + "/data", json=payload)


def flush_database():
    """Flush the database"""
    return requests.get(ENDPOINT + "/flush")


def parse_html_row(html):
    """Parse the HTML and retrieve a list of dict that contains 
    id, temp, lum, hum, timestamp"""

    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.findAll('tr')
    data = list()
    id_data = list()
    temperature_data = list()
    luminosity_data = list()
    humidity_data = list()
    timestamp_data = list()
    for row in rows:
        td_tags = [tag.text for tag in row.findAll('td')]
        i=0
        for tag in td_tags:
            if i == 0:
                id_data.append(tag)
            if i == 1:
                temperature_data.append(tag)
            if i == 2:
                luminosity_data.append(tag)
            if i == 3:
                humidity_data.append(tag)
            if i == 4:
                timestamp_data.append(tag)
            i+=1
        
    i=0
    while i < len(id_data):
        data.append({
            'id': id_data[i],
            'temperature': temperature_data[i],
            'luminosity': luminosity_data[i],
            'humidity': humidity_data[i],
            'timestamp': timestamp_data[i]
        })
        i+=1
    return data