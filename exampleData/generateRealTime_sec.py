import pandas as pd
import numpy as np
import sqlite3
import datetime
import time

def create_currentData():
    current_time = datetime.datetime.now()
    data = {
        "time": [current_time],
        "temperature": np.random.normal(15, 25, 1),
        "humidity": np.random.normal(40, 60, 1),
        "water_flow": np.random.normal(0, 30, 1),
        "air_quality_index": np.random.normal(0, 501, 1),
        "flex_pressure": np.random.normal(0, 100, 1)
    }
    return pd.DataFrame(data)

db_file = 'exampleData/sensor_data.db'
conn = sqlite3.connect(db_file)

while True:
    df = create_currentData()
    df.to_sql('sensor_data', conn, if_exists='append', index=False)
    print(f"{df['time'].iloc[0]} 데이터 추가") 
    time.sleep(2)
