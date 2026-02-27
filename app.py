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

@app.route('/piyasa-verileri')
def get_market_data():
    try:
        # 1. Döviz Verileri
        r_finans = requests.get('https://finans.truncgil.com/today.json')
        data_finans = r_finans.json()
        
        # 2. Hava Durumu (Hızlı ve anahtarsız bir servis örneği)
        # Not: wttr.in servisi JSON formatında çok temiz veri verir
        r_weather = requests.get('https://wttr.in/Istanbul?format=j1')
        data_weather = r_weather.json()
        temp = data_weather['current_condition'][0]['temp_C']
        desc = data_weather['current_condition'][0]['lang_tr'][0]['value'] if 'lang_tr' in data_weather['current_condition'][0] else "Açık"

        result = {
            "USD": data_finans.get("USD", {}).get("Selling", "0.00"),
            "EUR": data_finans.get("EUR", {}).get("Selling", "0.00"),
            "ALTIN": data_finans.get("Gram Altın", {}).get("Selling", "0.00"),
            "BIST": data_finans.get("BIST 100", {}).get("Selling", "0.00"),
            "WEATHER": f"{temp}°C",
            "W_DESC": desc.upper()
        }
        return jsonify(result)
    except Exception as e:
        print(f"Hata: {e}")
        return jsonify({"error": "Veri alınamadı"}), 500
# 7. Uygulamayı Çalıştır
if __name__ == '__main__':
    # Port'u ortam değişkeninden al, yoksa 5000 kullan (Deploy için şart!)
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)