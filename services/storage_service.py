"""Kafka consumer that stores events into SQLite.

Author: Bob
"""

import json
import sqlite3
from kafka import KafkaConsumer

DB_PATH = 'sensor_events.db'

class EventStorage:
    """Persist incoming events to a local SQLite database."""
    def __init__(self, brokers=None, topic='sensor-readings'):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=brokers or ['localhost:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            consumer_timeout_ms=1000
        )
        self.conn = sqlite3.connect(DB_PATH)
        self._ensure_table()

    def _ensure_table(self):
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS events (guid TEXT, state TEXT, eventTime TEXT, temperature REAL, checksum TEXT)"
            )

    def consume(self):
        for msg in self.consumer:
            event = msg.value
            with self.conn:
                self.conn.execute(
                    "INSERT INTO events VALUES (?, ?, ?, ?, ?)",
                    (event['guid'], event['state'], event['eventTime'], event['temperature'], event.get('checksum'))
                )

if __name__ == '__main__':
    storage = EventStorage()
    storage.consume()
