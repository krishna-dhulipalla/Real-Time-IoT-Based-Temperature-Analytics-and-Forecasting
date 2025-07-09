"""Kafka producer service for simulated sensor data.

Author: Alice
"""

import json
import random
import hashlib
import datetime
from kafka import KafkaProducer
from jsonschema import validate

SCHEMA = {
    "type": "object",
    "properties": {
        "guid": {"type": "string"},
        "state": {"type": "string"},
        "eventTime": {"type": "string"},
        "temperature": {"type": "number"}
    },
    "required": ["guid", "state", "eventTime", "temperature"]
}

class SensorProducer:
    """Send validated sensor events to Kafka."""
    def __init__(self, brokers=None, topic='sensor-readings'):
        self.producer = KafkaProducer(
            bootstrap_servers=brokers or ['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def generate_event(self):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        states = [
            'WA','DE','DC','WI','WV','HI','FL','WY','NH','NJ','NM','TX','LA','NC','ND','NE',
            'TN','NY','PA','CA','NV','VA','CO','AK','AL','AR','VT','IL','GA','IN','IA','OK',
            'AZ','ID','CT','ME','MD','MA','OH','UT','MO','MN','MI','RI','KS','MT','MS','SC',
            'KY','OR','SD'
        ]
        guid = f"0-ZZZ{random.randint(100000,999999)}-{random.choice(letters)}"
        state = random.choice(states)
        event_time = datetime.datetime.utcnow().isoformat() + 'Z'
        temperature = round(random.uniform(-20, 120), 2)
        return {
            "guid": guid,
            "state": state,
            "eventTime": event_time,
            "temperature": temperature
        }

    def send_event(self):
        event = self.generate_event()
        validate(instance=event, schema=SCHEMA)
        payload = json.dumps(event).encode('utf-8')
        event['checksum'] = hashlib.sha256(payload).hexdigest()
        self.producer.send(self.topic, event)
        self.producer.flush()

if __name__ == '__main__':
    sp = SensorProducer()
    for _ in range(10):
        sp.send_event()
