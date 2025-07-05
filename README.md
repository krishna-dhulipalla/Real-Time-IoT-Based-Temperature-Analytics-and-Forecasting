# Real-Time IoT-Based Temperature Analytics and Forecasting

![ProjectOverivew](image.png)

## Overview

This project explores real-time temperature analytics using simulated IoT sensors. A Kafka-based pipeline streams over 10,000 sensor readings, which are processed with PySpark Streaming. Deep learning models forecast future temperatures with **91% accuracy**, outperforming an ARIMA baseline by **15%**.

## Use Cases

- Monitoring nationwide temperature trends in real time
- Detecting anomalies in sensor readings
- Predicting near-term temperature to optimize energy usage

## Architecture

1. Sensors (simulated) send JSON events to a Kafka broker every few seconds.
2. PySpark consumes the stream and performs live aggregations.
3. LSTM and CNN models train on the generated series for forecasting.
4. An Airflow DAG refreshes data and a small Dash dashboard visualizes the results.

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

## Simulation Workflow

- `sensor_pipeline.py` streams simulated messages to Kafka, validates them against a JSON schema and appends a checksum.
- `train_models.py` trains LSTM and CNN models and reports an ARIMA baseline.
- An Airflow DAG (`dags/data_refresh.py`) refreshes data hourly.
- `dashboard.py` renders an interactive Plotly Dash chart from `sensor_data.csv`.

## Future Plans

- Deploy the pipeline on managed cloud services for scalability
- Add more complex anomaly detection models
- Incorporate real sensor hardware for data collection
