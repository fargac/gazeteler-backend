from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from time import time

app = Flask(__name__)
CORS(app)

# --- 1. TÜM HABER KAYNAKLARI (16 Adet - Tam Liste) ---
@app.route('/haber-kaynaklari', methods=['GET'])
def get_news_config():
    config = [
        {"id": "fenerbahce", "name": "Fenerbahçe", "rss": "https://www.fotomac.com.tr/rss/fenerbahce.xml"},
        {"id": "galatasaray", "name": "Galatasaray", "rss": "https://www.fotomac.com.tr/rss/galatasaray.xml"},
        {"id": "besiktas", "name": "Beşiktaş", "rss": "https://www.besiktas.com.tr/rss"},
        {"id": "trabzonspor", "name": "Trabzonspor", "rss": "https://www.fotomac.com.tr/rss/trabzonspor.xml"},
        {"id": "hurriyet", "name": "Hürriyet", "rss": "https://www.hurriyet.com.tr/rss/anasayfa"},
        {"id": "sozcu", "name": "Sözcü", "rss": "https://www.sozcu.com.tr/feeds-son-dakika"},
        {"id": "sabah", "name": "Sabah", "rss": "https://www.sabah.com.tr/rss/anasayfa.xml"},
        {"id": "milliyet", "name": "Milliyet", "rss": "https://www.milliyet.com.tr/rss/rssnew/sondakikarss.xml"},
        {"id": "haberturk", "name": "Habertürk", "rss": "https://www.haberturk.com/rss"},
        {"id": "ensonhaber", "name": "En Son Haber", "rss": "https://www.ensonhaber.com/rss/ensonhaber.xml"},
        {"id": "mynet", "name": "Mynet", "rss": "https://www.mynet.com/haber/rss/sondakika"},
        {"id": "sondakika", "name": "Son Dakika", "rss": "https://rss.sondakika.com/rss_standart.asp"},
        {"id": "cnnturk", "name": "CNN Türk", "rss": "https://www.cnnturk.com/feed/rss/all/news"},
        {"id": "ntvspor", "name": "NTV Spor", "rss": "https://www.ntvspor.net/rss/anasayfa"},
        {"id": "fotomac", "name": "Fotomaç", "rss": "https://www.fotomac.com.tr/rss/son24saat.xml"},
        {"id": "ekonomim", "name": "Ekonomim", "rss": "https://www.ekonomim.com/rss"}
    ]
    return jsonify(config)

@app.route('/config/takimlar', methods=['GET'])
def get_config(): return jsonify([])

def format_tr(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- 2. ANA PİYASA VERİSİ VE HAVA DURUMU ---
@app.route('/piyasa-verileri', methods=['GET'])
def get_market_data():
    lat = request.args.get("lat", "41.0138")
    lon = request.args.get("lon", "28.9497")
    
    result = {
        "USD": "-", "EUR": "-", "ALTIN": "-", "CEYREK": "-",
        "WEATHER": "-", "W_DESC": "İSTANBUL"
    }

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        t_res = requests.get("https://finans.truncgil.com/today.json", headers=headers, timeout=8)
        if t_res.status_code == 200:
            data = t_res.json()
            def parse_val(key):
                try:
                    # JSON'undaki "7.435,91" formatını temizler
                    raw = data.get(key, {}).get("Satış", "0")
                    clean = str(raw).replace(".", "").replace(",", ".")
                    return float(clean)
                except: return 0.0

            usd = parse_val("USD")
            eur = parse_val("EUR")
            gold = parse_val("gram-altin")
            ceyrek = parse_val("ceyrek-altin")

            if usd > 0: result["USD"] = f"{usd:.2f}"
            if eur > 0: result["EUR"] = f"{eur:.2f}"
            if gold > 0: result["ALTIN"] = format_tr(gold)
            if ceyrek > 0: result["CEYREK"] = format_tr(ceyrek)
            
            print(f"✅ VERİLER GELDİ -> USD: {result['USD']} | GRAM: {result['ALTIN']} | ÇEYREK: {result['CEYREK']}")
    except Exception as e:
        print(f"❌ PİYASA HATASI: {e}")

    try:
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(w_url, timeout=5)
        temp = w_res.json().get("current_weather", {}).get("temperature")
        if temp: result["WEATHER"] = f"{temp}°C"
    except: pass

    return jsonify(result), 200

# --- 2. PİYASA VE HAVA DURUMU KONFİGÜRASYONU (REMOTE CONFIG) ---
@app.route('/config/piyasa', methods=['GET'])
def get_piyasa_config():
    config = {
        "market_api": "https://finans.truncgil.com/today.json",
        "market_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        "market_keys": {
            "usd": "USD",
            "eur": "EUR",
            "gold": "gram-altin",
            "ceyrek": "ceyrek-altin"
        },
        "weather_api_base": "https://api.open-meteo.com/v1/forecast"
    }
    return jsonify(config), 200
if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=5000)