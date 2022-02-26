from flask import Flask, request
from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/get_data', methods=['GET'])
def get_data():
    return json.dumps({"data": "Hello World"})
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
