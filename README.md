# Real-Time IoT-Based Temperature Analytics and Forecasting

![ProjectOverivew](image.png)

## 1. Overview

##### Use case

- Analyzing U.S nationwide temperature from IoT sensors in real-time

##### Project Scenario:

- Multiple temperature sensors are deployed in each U.S state
- Each sensor regularly sends temperature data to a Kafka server in AWS Cloud (Simulated by feeding 10,000 JSON data by using kafka-console-producer)
- Kafka client retrieves the streaming data every 3 seconds
- PySpark processes and analizes them in real-time by using Spark Streming, and show the results

## 2. Format of sensor data

I used the simulated data for this project. `iotsimulator.py` generates JSON data as below format.

```
<Example>

{
    "guid": "0-ZZZ12345678-08K",
    "destination": "0-AAA12345678",
    "state": "CA",
    "eventTime": "2016-11-16T13:26:39.447974Z",
    "payload": {
        "format": "urn:example:sensor:temp",
        "data":{
            "temperature": 59.7
        }
    }
}

## 3. Analysis of data

In this project, I achieved 4 types of real-time analysis.

- Average temperature by each state (Values sorted in descending order)
- Total messages processed
- Number of sensors by each state (Keys sorted in ascending order)
- Total number of sensors

```
