from flask import Flask, jsonify
from flask_cors import CORS
import hashlib
import json
import os
from functools import lru_cache
from dotenv import load_dotenv

# ==========================================
# 1. VERİ İÇE AKTARMA (MODÜLLERDEN)
# ==========================================
from data.haber_kaynaklari import NEWS_SOURCES
from data.takimlar import TAKIMLAR
from data.kesfet import KESFET_CONFIG
from data.diger_ayarlar import PIYASA_CONFIG, MANSETLER_CONFIG, ADS_CONFIG

load_dotenv()
app = Flask(__name__)
CORS(app)

# ==========================================
# 2. ÖNBELLEKLEME (CACHE LAYER)
# ==========================================
@lru_cache(maxsize=1)
def get_all_configs_data():
    return {
        "haber_kaynaklari": NEWS_SOURCES,
        "piyasa": PIYASA_CONFIG,
        "mansetler": MANSETLER_CONFIG,
        "kesfet": KESFET_CONFIG,
        "takimlar": TAKIMLAR,
        "ads": ADS_CONFIG
    }

@lru_cache(maxsize=1)
def get_version_cached():
    data = get_all_configs_data()
    config_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(config_str.encode()).hexdigest()

# ==========================================
# 3. HTTP YÖNLENDİRMELERİ (ROUTE LAYER)
# ==========================================
@app.route('/haber-kaynaklari', methods=['GET'])
def get_news_config(): return jsonify(NEWS_SOURCES), 200

@app.route('/config/piyasa', methods=['GET'])
def get_piyasa_config_route(): return jsonify(PIYASA_CONFIG), 200

@app.route('/config/mansetler', methods=['GET'])
def get_mansetler_config_route(): return jsonify({"mansetler": MANSETLER_CONFIG}), 200

@app.route('/config/kesfet', methods=['GET'])
def get_kesfet_config_route(): return jsonify(KESFET_CONFIG), 200

@app.route('/config/takimlar', methods=['GET'])
def get_takimlar_config_route(): return jsonify({"takimlar": TAKIMLAR}), 200

@app.route('/config/ads', methods=['GET'])
def get_ads_config_route(): return jsonify(ADS_CONFIG), 200

@app.route('/config/version', methods=['GET'])
def get_version(): return jsonify({"version": get_version_cached()}), 200
    
@app.route('/config/all', methods=['GET'])
def get_all_configs():
    data = get_all_configs_data().copy()
    data["version"] = get_version_cached()
    return jsonify(data), 200

# ==========================================
# 4. SUNUCU BAŞLATMA
# ==========================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", '0.0.0.0')
    app.run(host=host, port=port)