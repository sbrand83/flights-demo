from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../flight_delay_model.joblib')
model = joblib.load(MODEL_PATH)

@app.route('/predict', methods=['GET'])
def predict():
    # Get parameters from query string
    day_of_week = request.args.get('day_of_week', type=int)
    origin_airport_id = request.args.get('origin_airport_id', type=int)

    # Validate input
    if day_of_week is None or origin_airport_id is None:
        return jsonify({'error': 'Missing required parameters'}), 400
    if not (1 <= day_of_week <= 7):
        return jsonify({'error': 'day_of_week must be between 1 and 7'}), 400

    # Prepare input for model
    input_df = pd.DataFrame({
        'DayOfWeek': [day_of_week],
        'OriginAirportID': [origin_airport_id]
    })

    # Predict probability
    probability = model.predict_proba(input_df)[:, 1][0]
    confidence_percent = round(probability * 100, 2)
    return jsonify({
        'day_of_week': day_of_week,
        'origin_airport_id': origin_airport_id,
        'delay_probability': probability,
        'confidence_percent': confidence_percent
    })

@app.route('/airports', methods=['GET'])
def get_airports():
    # Load airports.csv
    airports_path = os.path.join(os.path.dirname(__file__), '../data/airports.csv')
    airports_df = pd.read_csv(airports_path)
    # Sort by AirportName alphabetically and select only AirportID and AirportName
    airports_df = airports_df[['AirportID', 'AirportName']].sort_values('AirportName')
    # Convert to list of dicts
    airports_list = airports_df.to_dict(orient='records')
    return jsonify(airports_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0')