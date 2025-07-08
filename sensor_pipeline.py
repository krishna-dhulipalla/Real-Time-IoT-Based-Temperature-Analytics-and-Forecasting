import json
import random
import hashlib
import datetime
from kafka import KafkaProducer
from jsonschema import validate, ValidationError

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

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
STATES = [
    'WA','DE','DC','WI','WV','HI','FL','WY','NH','NJ','NM','TX','LA','NC','ND','NE',
    'TN','NY','PA','CA','NV','VA','CO','AK','AL','AR','VT','IL','GA','IN','IA','OK',
    'AZ','ID','CT','ME','MD','MA','OH','UT','MO','MN','MI','RI','KS','MT','MS','SC',
    'KY','OR','SD'
]


def generate_event():
    guid = f"0-ZZZ{random.randint(100000,999999)}-{random.choice(LETTERS)}"
    state = random.choice(STATES)
    event_time = datetime.datetime.utcnow().isoformat() + 'Z'
    temperature = round(random.uniform(-20, 120), 2)
    event = {
        "guid": guid,
        "state": state,
        "eventTime": event_time,
        "temperature": temperature
    }
    return event


def send_event():
    event = generate_event()
    try:
        validate(instance=event, schema=SCHEMA)
    except ValidationError as exc:
        raise RuntimeError(f"Schema validation failed: {exc}")
    payload = json.dumps(event).encode('utf-8')
    checksum = hashlib.sha256(payload).hexdigest()
    event['checksum'] = checksum
    producer.send('sensor-readings', event)
    producer.flush()


if __name__ == '__main__':
    for _ in range(10):
        send_event()
