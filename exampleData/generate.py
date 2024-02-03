import pandas as pd
import numpy as np
import random
import sqlite3

total_minutes = 3 * 24 * 60

data = {
    "time": pd.date_range(start="2023-01-01", periods=total_minutes, freq='T'),
    "temperature": np.random.normal(15, 25, total_minutes),
    "humidity": np.random.normal(40, 60, total_minutes),
    "water_flow": np.random.normal(0, 30, total_minutes),
    "air_quality_index": np.random.normal(0, 501, total_minutes),
    "flex_pressure": np.random.normal(0, 100, total_minutes)
}

df = pd.DataFrame(data)

df.head()

db_file = 'exampleData/sensor_data.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time DATETIME NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    water_flow REAL NOT NULL,
    air_quality_index INTEGER NOT NULL,
    flex_pressure REAL NOT NULL
);
"""
cursor.execute(query)

df.to_sql('sensor_data', conn, if_exists='replace', index=True, index_label='id', method='multi')

conn.close()

print('끝남')