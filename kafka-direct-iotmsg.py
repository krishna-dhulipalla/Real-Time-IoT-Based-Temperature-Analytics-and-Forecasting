#!/usr/bin/env python3
"""Consume IoT messages from Kafka and compute simple statistics."""

import sys
import re
import json
from operator import add
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka-direct-iotmsg.py <broker_list> <topic>", file=sys.stderr)
        sys.exit(-1)

    brokers, topic = sys.argv[1:]

    sc = SparkContext(appName="IoT")
    ssc = StreamingContext(sc, 3)

    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})

    jsonRDD = kvs.map(lambda kv: json.loads(kv[1]))

    ##### Processing #####
    avgTempByState = (
        jsonRDD.map(lambda x: (x['state'], (x['temperature'], 1)))
               .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
               .map(lambda x: (x[0], x[1][0] / x[1][1]))
    )
    sortedTemp = avgTempByState.transform(lambda rdd: rdd.sortBy(lambda y: y[1], ascending=False))
    sortedTemp.pprint(num=100000)

    messageCount = jsonRDD.map(lambda x: 1).reduce(add).map(lambda x: f"Total number of messages: {x}")
    messageCount.pprint()

    numSensorsByState = (
        jsonRDD.map(lambda x: (f"{x['state']}:{x['guid']}", 1))
               .reduceByKey(lambda a, b: a * b)
               .map(lambda x: (re.sub(r":.*", "", x[0]), x[1]))
               .reduceByKey(lambda a, b: a + b)
    )
    sortedSensorCount = numSensorsByState.transform(lambda rdd: rdd.sortBy(lambda y: y[0]))
    sortedSensorCount.pprint(num=10000)

    sensorCount = (
        jsonRDD.map(lambda x: (x['guid'], 1))
               .reduceByKey(lambda a, b: a * b)
               .map(lambda x: 1)
               .reduce(add)
               .map(lambda x: f"Total number of sensors: {x}")
    )
    sensorCount.pprint(num=10000)

    ssc.start()
    ssc.awaitTermination()
