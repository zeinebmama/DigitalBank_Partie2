from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)
MODEL_FILE = 'fraud_detection_model.pkl'

# ========== MAPPINGS EXACTS DU MODÈLE ==========
CATEGORY_MAPPING = {
    "Clothing": 0,
    "Cryptocurrency": 1,
    "Electronics": 2,
    "Entertainment": 3,
    "Food & Beverage": 4,
    "Fuel": 5,
    "Gambling": 6,
    "Groceries": 7,
    "Health": 8,
    "Jewelry": 9,
    "Travel": 10,
    "Utilities": 11,
}

# ========== LOCALISATION SIMPLIFIÉE ==========
LOCATION_MAPPING = {
    "France": 9,
    "Dubai": 0,
    "Hong Kong": 1,
    "Las Vegas": 2,
    "London": 3,
    "Nigeria": 7,
    "Online": 8,
    "Russia": 10,
}

# Chargement du modèle
if os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)
        print(f"✅ Modèle chargé : {MODEL_FILE}")
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        model = None
else:
    print(f"⚠️ Fichier introuvable : {MODEL_FILE}")
    model = None
    
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'API is running',
        'message': 'Use /predict endpoint to analyze transactions',
        'model_loaded': model is not None,
        'available_categories': list(CATEGORY_MAPPING.keys()),
        'available_locations': list(LOCATION_MAPPING.keys())
    })

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        raw_features = data['features']
        
        amount = float(raw_features[0])
        
        merchant = raw_features[1]
        if isinstance(merchant, str):
            merchant_encoded = CATEGORY_MAPPING.get(merchant, None)
            if merchant_encoded is None:
                return jsonify({
                    'error': f'Unknown merchant category: {merchant}',
                    'available_categories': list(CATEGORY_MAPPING.keys())
                }), 400
        else:
            merchant_encoded = int(merchant)
        
        location = raw_features[2]
        if isinstance(location, str):
            location_encoded = LOCATION_MAPPING.get(location, None)
            if location_encoded is None:
                return jsonify({
                    'error': f'Unknown location: {location}',
                    'available_locations': list(LOCATION_MAPPING.keys())
                }), 400
        else:
            location_encoded = int(location)
        
        hour = float(raw_features[3])
        
        encoded_features = np.array([[amount, merchant_encoded, location_encoded, hour]])
        
        print(f"🔍 Features reçues : {raw_features}")
        print(f"🔢 Features encodées : {encoded_features[0]}")
        
        prediction = model.predict(encoded_features)
        probability = model.predict_proba(encoded_features)[0][1]

        return jsonify({
            'is_fraud': bool(prediction[0]),
            'fraud_score': float(probability),
            'encoded_features': {
                'amount': amount,
                'merchant_code': merchant_encoded,
                'location_code': location_encoded,
                'hour_of_day': hour
            }
        })
        
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except IndexError:
        return jsonify({'error': 'Features array must have 4 elements'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)