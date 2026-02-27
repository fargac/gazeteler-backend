from flask import Flask, jsonify,request
from flask_cors import CORS
import requests
import yfinance as yf 
from time import time
from datetime import datetime
import pytz


# 1. Flask Uygulamasını ve CORS Ayarlarını Tanımla
app = Flask(__name__)
CORS(app)

# Frontend'in 404 almaması için boş config route'u
@app.route('/config/takimlar', methods=['GET'])
def get_config():
    return jsonify([])



@app.route('/haber-kaynaklari', methods=['GET'])
def get_news_config():
    # rules (kurallar) sözlüğü ile her siteye özel kazıma mantığı gönderiyoruz.
    # Kuralları olmayanlar, React Native içindeki standart "Yedek Paraşüt" ile kazınacak.
    config = [
        {"id": "fenerbahce", "name": "Fenerbahçe", "rss": "https://www.fotomac.com.tr/rss/fenerbahce.xml"},
        {"id": "galatasaray", "name": "Galatasaray", "rss": "https://www.fotomac.com.tr/rss/galatasaray.xml"},
        {"id": "besiktas", "name": "Beşiktaş", "rss": "https://www.fotomac.com.tr/rss/besiktas.xml"},
        {"id": "trabzonspor", "name": "Trabzonspor", "rss": "https://www.fotomac.com.tr/rss/trabzonspor.xml"},
        {"id": "hurriyet", "name": "Hürriyet", "rss": "https://www.hurriyet.com.tr/rss/anasayfa"},
        
        # SÖZCÜ: Resimleri <enclosure> değil, sadece url="..." içinde tutar
        {"id": "sozcu", "name": "Sözcü", "rss": "https://www.sozcu.com.tr/feeds-son-dakika",
         "rules": { "image": r'url=["\'](https?:\/\/.*?\.(?:jpg|jpeg|png|webp|gif|bmp).*?)["\']' }},
         
        {"id": "sabah", "name": "Sabah", "rss": "https://www.sabah.com.tr/rss/anasayfa.xml"},
        
        # MİLLİYET: Resim HTML içinde img src ile, link ise <atom:link> ile gelir
        {"id": "milliyet", "name": "Milliyet", "rss": "https://www.milliyet.com.tr/rss/rssnew/sondakikarss.xml",
         "rules": { "image": r'<img[^>]+src=["\'](.*?)["\']', "link": r'<(?:atom:)?link[^>]+href=["\'](.*?)["\']' }},
         
        # HABERTÜRK: Kendine has <image> etiketi kullanır
        {"id": "haberturk", "name": "Habertürk", "rss": "https://www.haberturk.com/rss",
         "rules": { "image": r'<image>(.*?)</image>' }},
         
        {"id": "ensonhaber", "name": "En Son Haber", "rss": "https://www.ensonhaber.com/rss/ensonhaber.xml"},
        
        # MYNET: Gelişmiş resim için <img640x360> kullanır
        {"id": "mynet", "name": "Mynet", "rss": "https://www.mynet.com/haber/rss/sondakika",
         "rules": { "image": r'<img640x360>(.*?)</img640x360>' }},
         
        {"id": "sondakika", "name": "Son Dakika", "rss": "https://rss.sondakika.com/rss_standart.asp"},
        {"id": "cnnturk", "name": "CNN Türk", "rss": "https://www.cnnturk.com/feed/rss/all/news"},
        
        # NTV SPOR: Standart RSS değil, Atom yapısındadır
        {"id": "ntvspor", "name": "NTV Spor", "rss": "https://www.ntvspor.net/rss/anasayfa",
         "rules": { "link": r'<link[^>]+href=["\'](.*?)["\']' }},
         
        {"id": "fotomac", "name": "Fotomaç", "rss": "https://www.fotomac.com.tr/rss/son24saat.xml"},
        {"id": "ekonomim", "name": "Ekonomim", "rss": "https://www.ekonomim.com/rss"},
    ]
    return jsonify(config)





cache = {}
CACHE_DURATION = 60  # saniye

def format_tr(value):
    return (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

@app.route('/piyasa-verileri')
def get_market_data():

    # 📍 Kullanıcıdan koordinat al (fallback İstanbul)
    lat = request.args.get("lat", "41.0138")
    lon = request.args.get("lon", "28.9497")

    cache_key = f"{lat}-{lon}"

    # 🔥 Cache kontrolü
    if cache_key in cache:
        if time() - cache[cache_key]["time"] < CACHE_DURATION:
            return jsonify(cache[cache_key]["data"]), 200

    result = {
        "USD": "-",
        "EUR": "-",
        "ALTIN": "-",
        "BIST": "-",
        "WEATHER": "-",
        "W_DESC": "-",
        "MARKET_OPEN": False
    }

    # =========================
    # 1️⃣ YAHOO FINANCE
    # =========================
    try:
        symbols = ["TRY=X", "EURTRY=X", "XU100.IS", "XAU=X"]

        data = yf.download(
            symbols,
            period="7d",
            interval="1d",
            group_by="ticker",
            progress=False
        )

        def get_close(symbol):
            try:
                closes = data[symbol]["Close"].dropna()
                if not closes.empty:
                    return closes.iloc[-1]
                return None
            except:
                return None

        def get_close_with_status(symbol):
            try:
                closes = data[symbol]["Close"].dropna()
                if closes.empty:
                    return None, False

                last_date = closes.index[-1].date()

                turkey_tz = pytz.timezone("Europe/Istanbul")
                today = datetime.now(turkey_tz).date()

                price = closes.iloc[-1]

                if last_date == today:
                    return price, True
                else:
                    return price, False

            except:
                return None, False

        # Döviz
        usd_price = get_close("TRY=X")
        eur_price = get_close("EURTRY=X")

        # BIST
        bist_price, market_open = get_close_with_status("XU100.IS")

        # Ons
        ons_price = get_close("XAU=X")

        if usd_price is not None:
            result["USD"] = f"{usd_price:.2f}"

        if eur_price is not None:
            result["EUR"] = f"{eur_price:.2f}"

        if bist_price is not None:
            result["BIST"] = format_tr(bist_price)

        result["MARKET_OPEN"] = market_open

        # 🧠 Gram Altın
        if ons_price is not None and usd_price is not None:
            gram_altin = (ons_price * usd_price) / 31.1034
            result["ALTIN"] = format_tr(gram_altin)

    except Exception as e:
        print("Finance error:", e)

    # =========================
    # 2️⃣ HAVA DURUMU
    # =========================
    try:
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )

        r_weather = requests.get(weather_url, timeout=5)

        if r_weather.status_code == 200:
            data_weather = r_weather.json()
            temp = data_weather.get("current_weather", {}).get("temperature")

            if temp is not None:
                result["WEATHER"] = f"{temp}°C"
                result["W_DESC"] = f"{lat},{lon}"

    except Exception as e:
        print("Weather error:", e)

    # 🔥 Cache güncelle
    cache[cache_key] = {
        "data": result,
        "time": time()
    }

    return jsonify(result), 200

# ... (app.run kısmı aynı kalıyor) ...
# 7. Uygulamayı Çalıştır
if __name__ == '__main__':
    # Port'u ortam değişkeninden al, yoksa 5000 kullan (Deploy için şart!)
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)