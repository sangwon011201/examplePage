import pandas as pd
import numpy as np
import sqlite3

total_seconds = 3 * 24 * 60 * 60

data = {
    "time": pd.date_range(start="2023-01-01", periods=total_seconds, freq='2S'),
    "temperature": np.random.normal(15, 25, total_seconds),
    "humidity": np.random.normal(40, 60, total_seconds),
    "water_flow": np.random.normal(0, 30, total_seconds),
    "air_quality_index": np.random.normal(0, 501, total_seconds),
    "flex_pressure": np.random.normal(0, 100, total_seconds)
}

df = pd.DataFrame(data)

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

chunksize = 1000
for i in range(0, len(df), chunksize):
    df.iloc[i:i+chunksize].to_sql('sensor_data', conn, if_exists='append', index=True, index_label='id', method='multi')

conn.close()
