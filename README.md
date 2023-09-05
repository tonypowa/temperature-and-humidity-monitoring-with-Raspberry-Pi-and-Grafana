# Temperature and humidity monitoring with Raspberry Pi and Grafana

This repo contains the code files, and the commands to run a Python app for monitoring temperature and humidity with a Raspberry Pi and Grafana.

For the full step-by-step instructions including hardware and software requirements, Raspberry Pi sensor wiring, code explanation, and overview of the tech stack needed (Python, Prometheus, Docker,..), see this [blog post](). 

## How to use the files

Below are the simplified steps that you need to take: 

- Step 1: Interact with your sensor, enable and export your sensor data through a port with the help of an exporter. For this part we will use Python. 

- Step 2: Scrape your sensor data with Prometheus
- Step 3: Monitor your data from Grafana

### Step 1 - Python

1. Clone this repo into your Raspberry Pi. 

    ``` git
    git clone https://github.com/tonypowa/Temperature-and-humidity-monitoring-with-Raspberry-Pi-and-Grafana.git
    ```

2. Open the console from the folder containing the cloned files.

3. Install the Python libraries in your Raspberry Pi.

    ```shell
    sudo pip3 install Adafruit_DHT flask prometheus_client
    ```

4. Get your own API key from [openWeatherMap](https://openweathermap.org/price#weather), so we can also monitor the outside temperature of our location.

5. In the file `flask_temps.py`, line 7, enter your openWeatherMap API key:

    ```
    "appid": "your-api-key"
    ```

6. Run it.

    ```python
    python3 flask_temps.py
    ```

    Your Python web server should be up and running.

    If you send a request to  http://localhost:5000/metrics , or visit http://{you-raspberry-pi-IP-address}:5000/metrics from another machine in your network, you should be able to see the exported metrics.

### Step 2 - Prometheus

1. Edit the `prometheus.yml` file, and enter the IP address of your Raspberry Pi in targets:

    ``` yml
    scrape_configs:
    - job_name: 'temperature-exporter'
        scrape_interval: 15s
        static_configs:
        - targets: ['192.168.x.x:5000']
        labels:
            instance: 'my-pi'
            room: 'study'
    ```

2. Run Prometheus on Docker

Run this `prometheus.yml` file. If you moved this file, remember to tell Docker the path to it.

``` shell
docker run \
    -p 9090:9090 \
    -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```


### Step 3 - Monitor your data from Grafana

From your machine, access your Raspberry PI by entering the IP address into the browser address: http://192.168.x.x:3000 . The Grafana login page should appear.

DONE! Go ahead and [Explore]() [LINK TO LAST SECTION OF THE BLOG]() your data and create your own dashboards.
