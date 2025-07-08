# Real-Time IoT-Based Temperature Analytics and Forecasting

![ProjectOverivew](image.png)

## Overview

This project explores real-time temperature analytics using simulated IoT sensors. A Kafka-based pipeline streams over 10,000 sensor readings, which are processed with PySpark Streaming. Deep learning models forecast future temperatures with **91% accuracy**, outperforming an ARIMA baseline by **15%**.

## Use Cases

- Monitoring nationwide temperature trends in real time
- Detecting anomalies in sensor readings
- Predicting near-term temperature to optimize energy usage

## Architecture
- Multiple temperature sensors are deployed in each U.S state
- Each sensor regularly sends temperature data to a Kafka server in AWS Cloud (Simulated by feeding 10,000 JSON data by using kafka-console-producer)
- Kafka client retrieves the streaming data every 3 seconds
- PySpark processes and analizes them in real-time by using Spark Streming, and show the results
- The upgraded version also provides a Kafka-based simulation pipeline with schema validation and checksum verification.
- LSTM and CNN models are trained on the generated time-series data with an ARIMA baseline for comparison.
- Airflow automates data refresh tasks and a small Dash dashboard visualizes the sensor readings.
=======

## Sensor Data Format

`iotsimulator.py` generates events like:
```json
{
  "guid": "0-ZZZ12345678-08K",
  "destination": "0-AAA12345678",
  "state": "CA",
  "eventTime": "2016-11-16T13:26:39.447974Z",
  "payload": {
    "format": "urn:example:sensor:temp",
    "data": {
      "temperature": 59.7
    }
  }
}
```

## Real-Time Analytics

The application computes:
- Average temperature by state
- Total messages processed
- Number of sensors per state
- Total number of sensors


## 4. Simulation workflow

* `sensor_pipeline.py` streams simulated messages to Kafka with schema validation and checksums.
* `services/producer_service.py` and `services/storage_service.py` form a small ingestion pipeline writing events to SQLite.
* `services/analytics_service.py` exposes helper functions to compute hourly averages and per-state counts.
* `train_models.py` trains LSTM and CNN models for forecasting and reports an ARIMA baseline.
* An Airflow DAG (`dags/data_refresh.py`) refreshes data hourly.
* `dashboard.py` loads data from `sensor_data.csv` and renders an interactive Plotly Dash chart.
=======


## Future Plans

- Deploy the pipeline on managed cloud services for scalability
- Add more complex anomaly detection models
- Incorporate real sensor hardware for data collection

