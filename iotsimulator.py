#!/usr/bin/env python3
"""Generate JSON sensor events.

Usage:
    ./iotsimulator.py [count]

Outputs `count` events to stdout following the same schema used in
`sensor_pipeline.py`.
"""

import sys
import datetime as dt
import random
import json

# Number of events to generate
num_msgs = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# Mapping of guid -> state
DEVICE_STATE_MAP = {}

# Average annual temperature for each US state
TEMP_BASE = {
    'WA': 48.3, 'DE': 55.3, 'DC': 58.5, 'WI': 43.1, 'WV': 51.8, 'HI': 70.0,
    'FL': 70.7, 'WY': 42.0, 'NH': 43.8, 'NJ': 52.7, 'NM': 53.4, 'TX': 64.8,
    'LA': 66.4, 'NC': 59.0, 'ND': 40.4, 'NE': 48.8, 'TN': 57.6, 'NY': 45.4,
    'PA': 48.8, 'CA': 59.4, 'NV': 49.9, 'VA': 55.1, 'CO': 45.1, 'AK': 26.6,
    'AL': 62.8, 'AR': 60.4, 'VT': 42.9, 'IL': 51.8, 'GA': 63.5, 'IN': 51.7,
    'IA': 47.8, 'OK': 59.6, 'AZ': 60.3, 'ID': 44.4, 'CT': 49.0, 'ME': 41.0,
    'MD': 54.2, 'MA': 47.9, 'OH': 50.7, 'UT': 48.6, 'MO': 54.5, 'MN': 41.2,
    'MI': 44.4, 'RI': 50.1, 'KS': 54.3, 'MT': 42.7, 'MS': 63.4, 'SC': 62.4,
    'KY': 55.6, 'OR': 48.4, 'SD': 45.2
}

# Latest temperature by guid
CURRENT_TEMP = {}

GUID_PREFIX = "0-ZZZ"
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def generate_event():
    rand_num = f"{random.randint(0, 99):02d}"
    rand_letter = random.choice(LETTERS)
    guid = f"{GUID_PREFIX}{random.randint(100000,999999)}-{rand_letter}"
    state = random.choice(list(TEMP_BASE.keys()))

    if guid not in DEVICE_STATE_MAP:
        DEVICE_STATE_MAP[guid] = state
        CURRENT_TEMP[guid] = TEMP_BASE[state] + random.uniform(-5, 5)
    else:
        state = DEVICE_STATE_MAP[guid]

    temperature = CURRENT_TEMP[guid] + random.uniform(-1, 1)
    CURRENT_TEMP[guid] = temperature

    return {
        "guid": guid,
        "state": state,
        "eventTime": dt.datetime.utcnow().isoformat() + 'Z',
        "temperature": round(temperature, 1)
    }


if __name__ == '__main__':
    for _ in range(num_msgs):
        print(json.dumps(generate_event()))
