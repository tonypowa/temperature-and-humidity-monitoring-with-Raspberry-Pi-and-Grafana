import Adafruit_DHT as dht_sensor
import time
from flask import Flask, Response
from prometheus_client import Counter, Gauge, start_http_server, generate_latest
import requests

params = {"lat": "36.52978", "lon": "-6.29465", "units": "metric", "appid": "your-api-key"}
# Hola from sunny "Cadizfornia"!
# Here you should enter your own latitude, and longuitude coordinates,
# plus your own openwheatherapi api key

baseurl = "https://api.openweathermap.org/data/2.5/weather"
content_type = str('text/plain; version=0.0.4; charset=utf-8')

def get_temperature_readings():
    humidity, temperature = dht_sensor.read_retry(dht_sensor.DHT22, 4)
    humidity = format(humidity, ".2f")
    temperature = format(temperature, ".2f")
    outside_temp = get_outside_weather()
    if all(v is not None for v in [humidity, temperature, outside_temp]):
        response = {"temperature": temperature, "humidity": humidity, "outside_temp": outside_temp}
        return response
    else:
        time.sleep(0.2)
        humidity, temperature = dht_sensor.read_retry(dht_sensor.DHT22, 4)
        humidity = format(humidity, ".2f")
        temperature = format(temperature, ".2f")
        outside_temp = get_outside_weather()
        response = {"temperature": temperature, "humidity": humidity, "outside_temp": outside_temp}
        return response

def get_outside_weather():
    response = requests.get(baseurl, params=params)
    temp = response.json()['main']['temp']
    return temp

app = Flask(__name__)

current_humidity = Gauge(
        'current_humidity',
        'the current humidity percentage, this is a gauge as the value can increase or decrease',
        ['room']
)

current_temperature = Gauge(
        'current_temperature',
        'the current temperature in celsius, this is a gauge as the value can increase or decrease',
        ['room']
)

current_temperature_outside = Gauge(
        'current_temperature_outside',
        'the current outside temperature in celsius, this is a gauge as the value can increase or decrease',
        ['location']
)

@app.route('/metrics')
def metrics():
    metrics = get_temperature_readings()
    current_humidity.labels('study').set(metrics['humidity'])
    current_temperature.labels('study').set(metrics['temperature'])
    current_temperature_outside.labels('za_ct').set(metrics['outside_temp'])
    return Response(generate_latest(), mimetype=content_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)