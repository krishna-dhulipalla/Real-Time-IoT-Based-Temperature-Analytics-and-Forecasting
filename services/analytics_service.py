"""Analytics routines to query stored sensor events.

Author: Charlie
"""

import sqlite3
import pandas as pd

DB_PATH = 'sensor_events.db'

class EventAnalytics:
    """Provide analysis methods on stored events."""
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)

    def hourly_average(self):
        query = "SELECT substr(eventTime, 1, 13) as hour, AVG(temperature) as avg_temp FROM events GROUP BY hour"
        return pd.read_sql_query(query, self.conn)

    def state_counts(self):
        query = "SELECT state, COUNT(*) as count FROM events GROUP BY state"
        return pd.read_sql_query(query, self.conn)

if __name__ == '__main__':
    analytics = EventAnalytics()
    print(analytics.hourly_average().head())
    print(analytics.state_counts().head())
