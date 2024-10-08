from flask import Flask, request, jsonify
import json
import pandas as pd
import folium
from folium.plugins import HeatMap

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the Employee API'

@app.route('/api/getdemand', methods=['POST'])
def generate_demand():
    record = json.loads(request.data)
    print(record)
    startHour = record['startHour']
    endHour = record['endHour']
    demand = generate_map(startHour, endHour)
    return jsonify({'demand': demand})

def generate_map(startHour, endHour):
    timestamp = '2024-03-12T00:00:00Z'

    if startHour < 10:
        startHour = timestamp[:11] + '0' + str(startHour) + timestamp[13:]
    else:
        startHour = timestamp[:11] + str(startHour) + timestamp[13:]

    if endHour < 10:
        endHour = timestamp[:11] + '0' + str(endHour) + timestamp[13:]
    else:
        endHour = timestamp[:11] + str(endHour) + timestamp[13:]
        
    df = pd.read_csv('anonymized-taxi-data.csv')
    df['StartDateTime'] = pd.to_datetime(df['StartDateTime'])
    filtered_df = df[(df['StartDateTime'] >= pd.to_datetime(startHour)) & (df['StartDateTime'] <= pd.to_datetime(endHour))]
    filtered_df = filtered_df.dropna(subset=['StartLat', 'StartLon'])
    dubai_map = folium.Map(location=[25.276987, 55.296249], zoom_start=12)
    heat_data = filtered_df[['StartLat', 'StartLon']].values.tolist()
    HeatMap(heat_data, radius=10, max_zoom=13).add_to(dubai_map)
    
    return dubai_map._repr_html_()
    
    
    



if __name__ == '__main__':
    app.run()


