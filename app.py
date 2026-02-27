from flask import Flask, jsonify
from flask_cors import CORS
import requests

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

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import yfinance as yf # 🚀 YENİ: Yahoo Finance eklendi!

# ... (Uygulama tanımlamaları ve haber rotaları aynı kalıyor) ...

@app.route('/piyasa-verileri')
def get_market_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    result = {
        "USD": "-", "EUR": "-", "ALTIN": "-", 
        "BIST": "-", "WEATHER": "-", "W_DESC": "-"
    }

    # 1. GLOBAL FİNANS (Yahoo Finance)
    try:
        # Fonksiyon: Verilen sembolün son kapanış fiyatını güvenli şekilde çeker
        def get_price(symbol):
            try:
                data = yf.Ticker(symbol).history(period="1d")
                return data['Close'].iloc[-1]
            except:
                return None

        # Fiyatları çekiyoruz
        usd_price = get_price("TRY=X")      # USD/TRY
        eur_price = get_price("EURTRY=X")   # EUR/TRY
        bist_price = get_price("XU100.IS")  # BIST 100
        ons_price = get_price("XAU=X")      # Altın Ons (USD)

        if usd_price:
            result["USD"] = f"{usd_price:.2f}"
        if eur_price:
            result["EUR"] = f"{eur_price:.2f}"
        if bist_price:
            # BIST için binlik ayırıcı (Örn: 9.240,50)
            result["BIST"] = f"{bist_price:,.2f}".replace(',', '.')
        
        # 🧠 SENIOR HİLESİ: Gram Altın Hesaplama
        # 1 Ons Altın = 31.1034 gramdır. Formül: (Ons Fiyatı * Dolar Kuru) / 31.1034
        if ons_price and usd_price:
            gram_altin = (ons_price * usd_price) / 31.1034
            result["ALTIN"] = f"{gram_altin:,.2f}".replace(',', '.')

    except Exception as e:
        print(f"Yahoo Finance API Hatası: {e}")

    # 2. HAVA DURUMU (Yine tamamen izole, çökerse borsayı etkilemez)
    try:
        # İstanbul'un koordinatları: Enlem 41.01, Boylam 28.95
        r_weather = requests.get('https://api.open-meteo.com/v1/forecast?latitude=41.0138&longitude=28.9497&current_weather=true', timeout=5)
        data_weather = r_weather.json()
        
        temp = data_weather.get('current_weather', {}).get('temperature', '-')
        
        result["WEATHER"] = f"{temp}°C"
        result["W_DESC"] = "İSTANBUL" # Open-Meteo direkt net derece verir
    except Exception as e:
        print(f"Hava Durumu API Hatası: {e}")

    return jsonify(result), 200

# ... (app.run kısmı aynı kalıyor) ...
# 7. Uygulamayı Çalıştır
if __name__ == '__main__':
    # Port'u ortam değişkeninden al, yoksa 5000 kullan (Deploy için şart!)
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)