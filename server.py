from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import os
from sqlalchemy.sql import text


app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'exampleData', 'sensor_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    water_flow = db.Column(db.Float, nullable=False)
    air_quality_index = db.Column(db.Integer, nullable=False)
    flex_pressure = db.Column(db.Float, nullable=False)

@app.route('/test_db')
def test_db():
    try:
        with db.engine.connect() as connection:
            query = text("SELECT * FROM sensor_data")
            result = connection.execute(query)
            
            row = result.fetchone()
            column_names = result.keys()

            data_str = ", ".join([f"{name}: {row[idx]}" for idx, name in enumerate(column_names)])
            return data_str
    except Exception as e:
        return str(e)

@app.route('/data')
def get_data():
    data = SensorData.query.order_by(SensorData.time.desc()).limit(10).all()# 10분간 데이터
    return jsonify([{
        'time': d.time.strftime('%Y-%m-%d %H:%M:%S'),
        'temperature': d.temperature,
        'humidity': d.humidity,
        'water_flow': d.water_flow,
        'air_quality_index': d.air_quality_index,
        'flex_pressure': d.flex_pressure
    } for d in data])
    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
