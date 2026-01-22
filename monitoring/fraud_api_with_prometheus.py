from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from functools import wraps
import time

app = Flask(__name__)
MODEL_FILE = 'fraud_detection_model.pkl'

# ========== MÉTRIQUES PROMETHEUS ==========
# Compteur de requêtes HTTP par endpoint et status
http_requests_total = Counter(
    'flask_http_request_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogramme du temps de réponse
http_request_duration_seconds = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Compteur de prédictions de fraude
fraud_detection_total = Counter(
    'fraud_detection_total',
    'Total fraud predictions',
    ['is_fraud']
)

# Gauge du score de fraude moyen
fraud_score_gauge = Gauge(
    'fraud_score_average',
    'Average fraud score of recent predictions'
)

# Compteur d'erreurs
api_errors_total = Counter(
    'flask_api_errors_total',
    'Total API errors',
    ['error_type']
)

# ========== DÉCORATEUR POUR MÉTRIQUES ==========
def track_metrics(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        endpoint = request.endpoint
        method = request.method
        
        try:
            response = f(*args, **kwargs)
            status = response[1] if isinstance(response, tuple) else 200
            
            # Enregistrer la requête
            http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
            
            return response
        except Exception as e:
            http_requests_total.labels(method=method, endpoint=endpoint, status=500).inc()
            api_errors_total.labels(error_type=type(e).__name__).inc()
            raise
        finally:
            # Enregistrer le temps de réponse
            duration = time.time() - start_time
            http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
    
    return decorated_function

# ========== MAPPINGS ==========
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

# ========== ENDPOINT MÉTRIQUES PROMETHEUS ==========
@app.route('/metrics')
def metrics():
    """Endpoint pour Prometheus scraping"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# ========== HEALTH CHECK ==========
@app.route('/', methods=['GET'])
@track_metrics
def health_check():
    return jsonify({
        'status': 'API is running',
        'message': 'Use /predict endpoint to analyze transactions',
        'model_loaded': model is not None,
        'available_categories': list(CATEGORY_MAPPING.keys()),
        'available_locations': list(LOCATION_MAPPING.keys())
    })

# ========== PRÉDICTION ==========
@app.route('/predict', methods=['POST'])
@track_metrics
def predict():
    if not model:
        api_errors_total.labels(error_type='ModelNotLoaded').inc()
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        raw_features = data['features']
        
        amount = float(raw_features[0])
        
        merchant = raw_features[1]
        if isinstance(merchant, str):
            merchant_encoded = CATEGORY_MAPPING.get(merchant, None)
            if merchant_encoded is None:
                api_errors_total.labels(error_type='InvalidCategory').inc()
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
                api_errors_total.labels(error_type='InvalidLocation').inc()
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
        
        # Prédiction
        prediction = model.predict(encoded_features)
        probability = model.predict_proba(encoded_features)[0][1]
        
        is_fraud = bool(prediction[0])
        
        # Enregistrer les métriques
        fraud_detection_total.labels(is_fraud=str(is_fraud).lower()).inc()
        fraud_score_gauge.set(probability)

        return jsonify({
            'is_fraud': is_fraud,
            'fraud_score': float(probability),
            'encoded_features': {
                'amount': amount,
                'merchant_code': merchant_encoded,
                'location_code': location_encoded,
                'hour_of_day': hour
            }
        })
        
    except KeyError as e:
        api_errors_total.labels(error_type='MissingField').inc()
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except IndexError:
        api_errors_total.labels(error_type='InvalidFeatures').inc()
        return jsonify({'error': 'Features array must have 4 elements'}), 400
    except Exception as e:
        api_errors_total.labels(error_type='UnknownError').inc()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
