from flask import Flask, request, jsonify
import pandas as pd
from geopy.distance import geodesic
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/get_accident_prone_areas": {"origins": "*"}})


# Load accident data
accident_data = pd.read_csv(r"D:\python\accident_data.csv")

# function to calculate the distance between two points
def calculate_distance(point1, point2):
    return geodesic(point1, point2).miles

#  function to check accident-prone area nearby
def get_accident_prone_areas(location):
    nearby_area = []
    for index, row in accident_data.iterrows():  
        distance = calculate_distance(location, (row['Latitudes'], row['Longitude ']))
        if distance < 1:                              # within 1 mile
            nearby_area.append({
                'Hot Spots': row['Hot Spots'],
                'Area': row['Area'],  
                'location': (row['Latitudes'], row['Longitude ']),
            })
            print("Warning!!"
          "   Accident prone area ahead  "
          "Please Drive Slow And  Obey the Traffic Rules ")
    return nearby_area
   

# route to get accident-prone areas
@app.route('/get_accident_prone_areas', methods=['POST'])
def get_areas():
    location = (request.json['Latitudes'], request.json['Longitude '])
    nearby_areas = get_accident_prone_areas(location)
    return jsonify(nearby_areas)

@app.route('/')
def home():
    return "Accindet Prone Area Warning System"

if __name__ == '__main__':
    app.run(debug=True)
