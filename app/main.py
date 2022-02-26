from flask import Flask, request
from flask_cors import CORS
import database as db


import json

app = Flask(__name__)
CORS(app)



@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    date = request.args.get('date')
    
    features = []
    objects = db.get_objects_by_date(date)

    for obj in objects:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [obj["x_coordinate"], obj["y_coordinate"]]
            },
            "properties": {
                "classification": obj["classification"],
                "date": obj["date"]
            }
        })

    return json.dumps({
        "type": "FeatureCollection",
        "features": features
    })  

@app.route('/api/v1/add_object', methods=['POST'])
def add_object():
    classification = request.args.get('classification')
    x_coordinate = request.args.get('x')
    y_coordinate = request.args.get('y')
    date = request.args.get('date')

    db.add_object(classification, x_coordinate, y_coordinate, date)
    
    return "OK"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

