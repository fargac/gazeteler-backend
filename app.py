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
      
{
        "id": "fenerbahce",
        "name": "Fenerbahçe",
        "rss": "https://www.fotomac.com.tr/rss/fenerbahce.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "cnnturk",
        "name": "CNN Türk",
        "rss": "https://www.cnnturk.com/feed/rss/all/news",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<image>([\\s\\S]*?)<\\/image>",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "besiktas",
        "name": "Beşiktaş",
        "rss": "https://www.besiktas.com.tr/rss",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "url=[\"'](https?:\\/\\/.*?\\.(?:jpg|jpeg|png|webp|gif|bmp).*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "trabzonspor",
        "name": "Trabzonspor",
        "rss": "https://www.fotomac.com.tr/rss/trabzonspor.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "hurriyet",
        "name": "Hürriyet",
        "rss": "https://www.hurriyet.com.tr/rss/anasayfa",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "sozcu",
        "name": "Sözcü",
        "rss": "https://www.sozcu.com.tr/feeds-son-dakika",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<media:content[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "sabah",
        "name": "Sabah",
        "rss": "https://www.sabah.com.tr/rss/anasayfa.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "milliyet",
        "name": "Milliyet",
        "rss": "https://www.milliyet.com.tr/rss/rssnew/sondakikarss.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "url=[\"'](https?:\\/\\/.*?\\.(?:jpg|jpeg|png|webp|gif|bmp).*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "haberturk",
        "name": "Habertürk",
        "rss": "https://www.haberturk.com/rss/manset.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "ensonhaber",
        "name": "En Son Haber",
        "rss": "https://www.ensonhaber.com/rss/ensonhaber.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<media:content[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "mynet",
        "name": "Mynet",
        "rss": "https://www.mynet.com/haber/rss/sondakika",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<img640x360>(.*?)<\\/img640x360>",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "sondakika",
        "name": "Son Dakika",
        "rss": "https://rss.sondakika.com/rss_standart.asp",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<media:content[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "cnnturk",
        "name": "CNN Türk",
        "rss": "https://www.cnnturk.com/feed/rss/all/news",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "url=[\"'](https?:\\/\\/.*?\\.(?:jpg|jpeg|png|webp|gif|bmp).*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "ntvspor",
        "name": "NTV Spor",
        "rss": "https://www.ntvspor.net/rss/anasayfa",
        "rules": {
            "item": "<entry[\\s\\S]*?>([\\s\\S]*?)<\\/entry>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<(?:atom:)?link[^>]+href=[\"'](.*?)[\"']",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<published[^>]*>([\\s\\S]*?)<\\/published>"
        }
    },
    {
        "id": "fotomac",
        "name": "Fotomaç",
        "rss": "https://www.fotomac.com.tr/rss/son24saat.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "ekonomim",
        "name": "Ekonomim",
        "rss": "https://www.ekonomim.com/rss",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    }


    ]
    return jsonify(config)

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

# --- 3. PİYASA VE HAVA DURUMU KONFİGÜRASYONU (REMOTE CONFIG) ---
@app.route('/config/piyasa', methods=['GET'])
def get_piyasa_config():
    config = {
        "market_api": "https://finans.truncgil.com/today.json",
        "market_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        "market_rules": {
            "usd": {"key": "USD", "subKey": "Satış", "format": "tr_currency"},
            "eur": {"key": "EUR", "subKey": "Satış", "format": "tr_currency"},
            "gold": {"key": "gram-altin", "subKey": "Satış", "format": "tr_currency"},
            "ceyrek": {"key": "ceyrek-altin", "subKey": "Satış", "format": "tr_currency"}
        },
        "weather_api_base": "https://api.open-meteo.com/v1/forecast"
    }
    return jsonify(config), 200

# --- 4. MANŞETLER KONFİGÜRASYONU ---
# --- 4. MANŞETLER KONFİGÜRASYONU ---
@app.route('/config/mansetler', methods=['GET'])
def get_mansetler_config():
    base = "https://i13.haber7.net/haber7/gazete"
    config = [
        {"id": "manset_hurriyet", "name": "Hürriyet", "pattern": f"{base}/hurriyet"},
        {"id": "manset_sabah", "name": "Sabah", "pattern": f"{base}/sabah"},
        {"id": "manset_milliyet", "name": "Milliyet", "pattern": f"{base}/milliyet"},
        {"id": "manset_turkiye", "name": "Türkiye", "pattern": f"{base}/turkiye"},
        {"id": "manset_aksam", "name": "Akşam", "pattern": f"{base}/aksam"},
        {"id": "manset_yeni_safak", "name": "Yeni Şafak", "pattern": f"{base}/yeni-safak"},
        {"id": "manset_yeni_akit", "name": "Yeni Akit", "pattern": f"{base}/yeni-akit"},
        {"id": "manset_dirilis_postasi", "name": "Diriliş P.", "pattern": f"{base}/dirilis-postasi"},
        {"id": "manset_milat", "name": "Milat", "pattern": f"{base}/milat"},
        {"id": "manset_turkgun", "name": "Türkgün", "pattern": f"{base}/turkgun"},
        {"id": "manset_yeni_birlik", "name": "Yeni Birlik", "pattern": f"{base}/yeni-birlik"},
        {"id": "manset_milli_gazete", "name": "Milli Gazete", "pattern": f"{base}/milli-gazete"},
        {"id": "manset_dunya", "name": "Dünya", "pattern": f"{base}/dunya"},
        {"id": "manset_yeni_cag", "name": "Yeniçağ", "pattern": f"{base}/yenicag"},
        {"id": "manset_yeni_soz", "name": "Yenisöz", "pattern": f"{base}/yenisoz"},
        {"id": "manset_aydinlik", "name": "Aydınlık", "pattern": f"{base}/aydinlik"},
        {"id": "manset_dogru-haber", "name": "Doğru Haber", "pattern": f"{base}/dogru-haber"},
        {"id": "manset_takvim", "name": "Takvim", "pattern": f"{base}/takvim-gazetesi"},
        {"id": "manset_fanatik", "name": "Fanatik", "pattern": f"{base}/fanatik"},
        {"id": "manset_fotomac", "name": "Fotomaç", "pattern": f"{base}/fotomac"},
    ]
    return jsonify({"mansetler": config}), 200

# --- 5. KEŞFET KONFİGÜRASYONU ---
@app.route('/config/kesfet', methods=['GET'])
def get_kesfet_config():
    config = {
        "ulusal": [
            {"id": "hurriyet", "name": "Hürriyet", "link": "https://www.hurriyet.com.tr"},
            {"id": "sabah", "name": "Sabah", "link": "https://m.sabah.com.tr"},
            {"id": "milliyet", "name": "Milliyet", "link": "https://m.milliyet.com.tr"},
            {"id": "sozcu", "name": "Sözcü", "link": "https://www.sozcu.com.tr"},
            {"id": "haberturk", "name": "Habertürk", "link": "https://m.haberturk.com"},
            {"id": "posta", "name": "Posta", "link": "https://www.posta.com.tr"},
            {"id": "yenisafak", "name": "Yeni Şafak", "link": "https://www.yenisafak.com"},
            {"id": "turkiye", "name": "Türkiye", "link": "http://m.turkiyegazetesi.com.tr"},
            {"id": "aksam", "name": "Akşam", "link": "http://www.aksam.com.tr"},
            {"id": "takvim", "name": "Takvim", "link": "https://m.takvim.com.tr"},
            {"id": "star", "name": "Star", "link": "http://m.star.com.tr"},
            {"id": "karar", "name": "Karar", "link": "https://m.karar.com/"},
            {"id": "korkusuz", "name": "Korkusuz", "link": "https://www.korkusuz.com.tr/"},
            {"id": "cumhuriyet", "name": "Cumhuriyet", "link": "http://www.cumhuriyet.com.tr/m/"},
            {"id": "yeni_akit", "name": "Yeni Akit", "link": "http://m.yeniakit.com.tr"},
            {"id": "milli_gazete", "name": "Milli Gazete", "link": "https://www.milligazete.com.tr/"},
            {"id": "yenicag", "name": "Yeni Çağ", "link": "https://www.yenicaggazetesi.com.tr/mobi/"},
            {"id": "dirilis_postasi", "name": "Diriliş Postası", "link": "https://www.dirilispostasi.com/"},
            {"id": "dunya", "name": "Dünya", "link": "https://m.dunya.com"},
            {"id": "birgun", "name": "Birgün", "link": "http://www.birgun.net"},
            {"id": "evrensel", "name": "Evrensel", "link": "https://www.evrensel.net"},
            {"id": "aydinlik", "name": "Aydınlık", "link": "http://www.aydinlikgazete.com"},
            {"id": "sol", "name": "Sol", "link": "https://haber.sol.org.tr/"},
            {"id": "yeni_asya", "name": "Yeni Asya", "link": "https://www.yeniasya.com.tr"},
            {"id": "milat", "name": "Milat", "link": "http://www.milatgazetesi.com"},
            {"id": "istiklal", "name": "İstiklal", "link": "https://www.istiklal.com.tr/"}
        ],
        "haber_siteleri": [
            {"id": "ntv", "name": "NTV", "link": "https://www.ntv.com.tr"},
            {"id": "cnnturk", "name": "CNN Türk", "link": "https://www.cnnturk.com"},
            {"id": "trt", "name": "TRT Haber", "link": "https://www.trthaber.com/m/"},
            {"id": "ahaber", "name": "A Haber", "link": "https://www.ahaber.com.tr"},
            {"id": "haber7", "name": "Haber 7", "link": "https://m.haber7.com"},
            {"id": "ensonhaber", "name": "Enson Haber", "link": "https://m.ensonhaber.com"},
            {"id": "haberler", "name": "Haberler", "link": "https://m.haberler.com"},
            {"id": "sondakika", "name": "Son Dakika", "link": "https://www.sondakika.com/"},
            {"id": "internethaber", "name": "İnternet Haber", "link": "https://www.internethaber.com"},
            {"id": "t24", "name": "T24", "link": "https://t24.com.tr/"},
            {"id": "odatv", "name": "Oda TV", "link": "https://odatv4.com/mob.php"},
            {"id": "diken", "name": "Diken", "link": "http://www.diken.com.tr"},
            {"id": "bbc_turkce", "name": "BBC Türkçe", "link": "https://www.bbc.com/turkce"},
            {"id": "sputnik", "name": "Sputnik Türkiye", "link": "https://tr.sputniknews.com"},
            {"id": "aa", "name": "Anadolu Ajansı", "link": "https://www.aa.com.tr/tr"},
            {"id": "dha", "name": "DHA", "link": "https://www.dha.com.tr"}
        ],
        "spor": [
            {"id": "fotomac", "name": "Fotomaç", "link": "https://m.fotomac.com.tr"},
            {"id": "fanatik", "name": "Fanatik", "link": "https://www.fanatik.com.tr"},
            {"id": "aspor", "name": "A Spor", "link": "https://www.aspor.com.tr/?ismobile=true"},
            {"id": "ntvspor", "name": "NTV Spor", "link": "https://www.ntvspor.net/"},
            {"id": "bein_sports", "name": "beIN Sports", "link": "https://m.tr.beinsports.com"},
            {"id": "bein_ozet", "name": "Süper Lig Özetleri", "link": "https://beinsports.com.tr/mac-ozetleri-goller/super-lig"},
            {"id": "skor_sozcu", "name": "Skor Sözcü", "link": "https://skor.sozcu.com.tr"},
            {"id": "sporx", "name": "Sporx", "link": "https://m.sporx.com"},
            {"id": "ajans_spor", "name": "Ajans Spor", "link": "https://www.ajansspor.com"},
            {"id": "goal", "name": "Goal", "link": "https://www.goal.com/tr"},
            {"id": "mackolik", "name": "Maçkolik", "link": "https://www.mackolik.com/canli-sonuclar"},
            {"id": "sahadan", "name": "Sahadan", "link": "https://www.sahadan.com/"},
            {"id": "futbol_arena", "name": "Futbol Arena", "link": "https://www.futbolarena.com"},
            {"id": "motorsports", "name": "Motorsports", "link": "https://tr.motorsport.com/"}
        ],
        "teknoloji": [
            {"id": "donanim_haber", "name": "Donanım Haber", "link": "https://m.donanimhaber.com"},
            {"id": "shift_delete", "name": "Shift Delete", "link": "https://shiftdelete.net"},
            {"id": "chip_online", "name": "Chip Online", "link": "https://www.chip.com.tr"},
            {"id": "teknoblog", "name": "Teknoblog", "link": "https://www.teknoblog.com"},
            {"id": "technopat", "name": "Technopat", "link": "https://www.technopat.net"},
            {"id": "webrazzi", "name": "Webrazzi", "link": "https://webrazzi.com"},
            {"id": "teknoloji_oku", "name": "Teknoloji Oku", "link": "https://www.teknolojioku.com"},
            {"id": "log", "name": "Log", "link": "https://www.log.com.tr"},
            {"id": "tekno_seyir", "name": "Tekno Seyir", "link": "https://teknoseyir.com"},
            {"id": "vatan_bilg", "name": "Vatan Bilgisayar", "link": "https://www.vatanbilgisayar.com"}
        ],
        "populer": [
            {"id": "eksi_sozluk", "name": "Ekşi Sözlük", "link": "https://eksisozluk.com"},
            {"id": "memurlar_net", "name": "Memurlar Net", "link": "https://www.memurlar.net"},
            {"id": "sahibinden", "name": "Sahibinden", "link": "https://www.sahibinden.com"},
            {"id": "kizlarsoruyor", "name": "Kızlar Soruyor", "link": "https://www.kizlarsoruyor.com"},
            {"id": "hepsiburada", "name": "Hepsi Burada", "link": "https://www.hepsiburada.com"},
            {"id": "n11", "name": "N11", "link": "https://www.n11.com/"},
            {"id": "kamu_ilan", "name": "Kamu İlanları", "link": "https://kamuilan.sbb.gov.tr/"},
            {"id": "zaytung", "name": "Zaytung", "link": "http://www.zaytung.com"},
            {"id": "ilac_rehberi", "name": "İlaç Rehberi", "link": "https://www.ilacrehberi.com"},
            {"id": "yemek", "name": "Yemek.com", "link": "https://yemek.com"}
        ],
        "yabanci": [
            {"id": "bbc", "name": "BBC", "link": "https://www.bbc.co.uk/news"},
            {"id": "cnn", "name": "CNN", "link": "https://edition.cnn.com"},
            {"id": "nytimes", "name": "New York Times", "link": "https://www.nytimes.com"},
            {"id": "washington_post", "name": "Washington Post", "link": "https://www.washingtonpost.com/"},
            {"id": "usa_today", "name": "USA Today", "link": "https://www.usatoday.com"},
            {"id": "wsj", "name": "Wall Street Journal", "link": "https://www.wsj.com"},
            {"id": "spiegel", "name": "Spiegel", "link": "https://m.spiegel.de"},
            {"id": "bild", "name": "Bild", "link": "https://m.bild.de"},
            {"id": "the_sun", "name": "The Sun", "link": "https://www.thesun.co.uk/"},
            {"id": "the_guardian", "name": "The Guardian", "link": "https://www.theguardian.com"},
            {"id": "le_monde", "name": "Le Monde", "link": "https://www.lemonde.fr"},
            {"id": "le_figaro", "name": "Le Figaro", "link": "https://www.lefigaro.fr"},
            {"id": "the_moscow_times", "name": "The Moscow Times", "link": "https://www.themoscowtimes.com"},
            {"id": "corriere", "name": "Corriere", "link": "https://www.corriere.it"},
            {"id": "al_jazeera", "name": "Al Jazeera", "link": "https://www.aljazeera.com/"}
        ],
        "yazarlar": [
            {"id": "yilmaz_ozdil", "name": "Yılmaz Özdil", "link": "https://www.sozcu.com.tr/yilmaz-ozdil-a2158"},
            {"id": "ahmet_hakan", "name": "Ahmet Hakan", "link": "https://m.hurriyet.com.tr/yazarlar/ahmet-hakan/"},
            {"id": "abdulkadir_selvi", "name": "Abdülkadir Selvi", "link": "https://m.hurriyet.com.tr/yazarlar/abdulkadir-selvi/"},
            {"id": "fatih_altayli", "name": "Fatih Altaylı", "link": "https://m.haberturk.com/htyazar/fatih-altayli-1001"},
            {"id": "ugur_dundar", "name": "Uğur Dündar", "link": "https://www.sozcu.com.tr/kategori/ugur-dundar-a27"},
            {"id": "emin_colasan", "name": "Emin Çölaşan", "link": "https://www.sozcu.com.tr/kategori/emin-colasan-a26/"},
            {"id": "ertugrul_ozkok", "name": "Ertuğrul Özkök", "link": "https://m.hurriyet.com.tr/yazarlar/ertugrul-ozkok/"},
            {"id": "ilber_ortayli", "name": "İlber Ortaylı", "link": "https://m.hurriyet.com.tr/yazarlar/ilber-ortayli/"},
            {"id": "gulse_birsel", "name": "Gülse Birsel", "link": "https://m.hurriyet.com.tr/yazarlar/gulse-birsel/"},
            {"id": "murat_bardakci", "name": "Murat Bardakçı", "link": "https://m.haberturk.com/htyazar/murat-bardakci"},
            {"id": "nagehan_alci", "name": "Nagehan Alçı", "link": "https://m.haberturk.com/htyazar/nagehan-alci"},
            {"id": "osman_muftuoglu", "name": "Osman Müftüoğlu", "link": "https://m.hurriyet.com.tr/yazarlar/osman-muftuoglu/"},
            {"id": "soner_yalcin", "name": "Soner Yalçın", "link": "https://www.sozcu.com.tr/kategori/soner-yalcin-a31"},
            {"id": "ismail_saymaz", "name": "İsmail Saymaz", "link": "https://www.sozcu.com.tr/ismail-saymaz-a36"},
            {"id": "ahmet_cakar", "name": "Ahmet Çakar", "link": "https://m.sabah.com.tr/yazarlar/cakar/arsiv?getall=true"},
            {"id": "erman_toroglu", "name": "Erman Toroğlu", "link": "https://m.fotomac.com.tr/yazarlar/erman.toroglu/arsiv"},
            {"id": "mehmet_demirkol", "name": "Mehmet Demirkol", "link": "https://www.fanatik.com.tr/yazarlar/mehmet-demirkol"},
            {"id": "sansal_buyuka", "name": "Şansal Büyüka", "link": "https://www.milliyet.com.tr/yazarlar/sansal-buyuka/"}
        ],
        "gazete_yazarlari": [
            {"id": "hurriyet", "name": "Hürriyet Yazarlar", "link": "https://m.hurriyet.com.tr/yazarlar/"},
            {"id": "sabah", "name": "Sabah Yazarlar", "link": "https://m.sabah.com.tr/yazarlar"},
            {"id": "sozcu", "name": "Sözcü Yazarlar", "link": "https://www.sozcu.com.tr/yazarlar/"},
            {"id": "milliyet", "name": "Milliyet Yazarlar", "link": "https://m.milliyet.com.tr/yazarlar/"},
            {"id": "haberturk", "name": "Habertürk Yazarlar", "link": "https://m.haberturk.com/yazarlar"},
            {"id": "posta", "name": "Posta Yazarlar", "link": "https://www.posta.com.tr/yazarlar/"},
            {"id": "yenisafak", "name": "Yeni Şafak Yazarlar", "link": "https://www.yenisafak.com/yazarlar"},
            {"id": "turkiye", "name": "Türkiye Yazarlar", "link": "https://www.turkiyegazetesi.com.tr/yazarlar"},
            {"id": "aksam", "name": "Akşam Yazarlar", "link": "https://www.aksam.com.tr/yazarlar/"},
            {"id": "takvim", "name": "Takvim Yazarlar", "link": "https://m.takvim.com.tr/yazarlar"},
            {"id": "karar", "name": "Karar Yazarlar", "link": "https://www.karar.com/yazarlar"},
            {"id": "cumhuriyet", "name": "Cumhuriyet Yazarlar", "link": "https://www.cumhuriyet.com.tr/yazarlar"},
            {"id": "yeni_akit", "name": "Yeni Akit Yazarlar", "link": "https://m.yeniakit.com.tr/yazarlar"},
            {"id": "milli_gazete", "name": "Milli Gazete Yazarlar", "link": "https://www.milligazete.com.tr/yazarlar"}
        ],
        "yerel": [
            {"id": "yerel_adana", "name": "Adana", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel"},
            {"id": "yerel_adiyaman", "name": "Adıyaman", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=11"},
            {"id": "yerel_afyon", "name": "Afyonkarahisar", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=12"},
            {"id": "yerel_agri", "name": "Ağrı", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=13"},
            {"id": "yerel_aksaray", "name": "Aksaray", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=14"},
            {"id": "yerel_amasya", "name": "Amasya", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=15"},
            {"id": "yerel_ankara", "name": "Ankara", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=16"},
            {"id": "yerel_antalya", "name": "Antalya", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=17"},
            {"id": "yerel_ardahan", "name": "Ardahan", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=18"},
            {"id": "yerel_artvin", "name": "Artvin", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=19"},
            {"id": "yerel_aydin", "name": "Aydın", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=20"},
            {"id": "yerel_balikesir", "name": "Balıkesir", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=21"},
            {"id": "yerel_bartin", "name": "Bartın", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=22"},
            {"id": "yerel_batman", "name": "Batman", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=23"},
            {"id": "yerel_bayburt", "name": "Bayburt", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=24"},
            {"id": "yerel_bilecik", "name": "Bilecik", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=25"},
            {"id": "yerel_bingol", "name": "Bingöl", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=26"},
            {"id": "yerel_bitlis", "name": "Bitlis", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=27"},
            {"id": "yerel_bolu", "name": "Bolu", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=28"},
            {"id": "yerel_burdur", "name": "Burdur", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=29"},
            {"id": "yerel_bursa", "name": "Bursa", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=30"},
            {"id": "yerel_canakkale", "name": "Çanakkale", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=31"},
            {"id": "yerel_cankiri", "name": "Çankırı", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=32"},
            {"id": "yerel_corum", "name": "Çorum", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=33"},
            {"id": "yerel_denizli", "name": "Denizli", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=34"},
            {"id": "yerel_diyarbakir", "name": "Diyarbakır", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=35"},
            {"id": "yerel_duzce", "name": "Düzce", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=36"},
            {"id": "yerel_edirne", "name": "Edirne", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=37"},
            {"id": "yerel_elazig", "name": "Elazığ", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=38"},
            {"id": "yerel_erzincan", "name": "Erzincan", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=39"},
            {"id": "yerel_erzurum", "name": "Erzurum", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=40"},
            {"id": "yerel_eskisehir", "name": "Eskişehir", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=41"},
            {"id": "yerel_gaziantep", "name": "Gaziantep", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=42"},
            {"id": "yerel_giresun", "name": "Giresun", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=43"},
            {"id": "yerel_gumushane", "name": "Gümüşhane", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=44"},
            {"id": "yerel_hakkari", "name": "Hakkari", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=45"},
            {"id": "yerel_hatay", "name": "Hatay", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=46"},
            {"id": "yerel_igdir", "name": "Iğdır", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=47"},
            {"id": "yerel_isparta", "name": "Isparta", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=48"},
            {"id": "yerel_istanbul", "name": "İstanbul", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=49"},
            {"id": "yerel_izmir", "name": "İzmir", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=50"},
            {"id": "yerel_kahramanmaras", "name": "Kahramanmaraş", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=51"},
            {"id": "yerel_karabuk", "name": "Karabük", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=52"},
            {"id": "yerel_karaman", "name": "Karaman", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=53"},
            {"id": "yerel_kars", "name": "Kars", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=54"},
            {"id": "yerel_kastamonu", "name": "Kastamonu", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=55"},
            {"id": "yerel_kayseri", "name": "Kayseri", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=56"},
            {"id": "yerel_kirikkale", "name": "Kırıkkale", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=57"},
            {"id": "yerel_kirklareli", "name": "Kırklareli", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=58"},
            {"id": "yerel_kirsehir", "name": "Kırşehir", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=59"},
            {"id": "yerel_kilis", "name": "Kilis", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=60"},
            {"id": "yerel_kocaeli", "name": "Kocaeli", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=61"},
            {"id": "yerel_konya", "name": "Konya", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=62"},
            {"id": "yerel_kutahya", "name": "Kütahya", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=63"},
            {"id": "yerel_malatya", "name": "Malatya", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=64"},
            {"id": "yerel_manisa", "name": "Manisa", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=65"},
            {"id": "yerel_mardin", "name": "Mardin", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=66"},
            {"id": "yerel_mersin", "name": "Mersin", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=67"},
            {"id": "yerel_mugla", "name": "Muğla", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=68"},
            {"id": "yerel_mus", "name": "Muş", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=69"},
            {"id": "yerel_nevsehir", "name": "Nevşehir", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=70"},
            {"id": "yerel_nigde", "name": "Niğde", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=71"},
            {"id": "yerel_ordu", "name": "Ordu", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=72"},
            {"id": "yerel_osmaniye", "name": "Osmaniye", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=73"},
            {"id": "yerel_rize", "name": "Rize", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=74"},
            {"id": "yerel_sakarya", "name": "Sakarya", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=75"},
            {"id": "yerel_samsun", "name": "Samsun", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=76"},
            {"id": "yerel_sanliurfa", "name": "Şanlıurfa", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=77"},
            {"id": "yerel_siirt", "name": "Siirt", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=78"},
            {"id": "yerel_sinop", "name": "Sinop", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=79"},
            {"id": "yerel_sirnak", "name": "Şırnak", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=80"},
            {"id": "yerel_sivas", "name": "Sivas", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=81"},
            {"id": "yerel_tekirdag", "name": "Tekirdağ", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=82"},
            {"id": "yerel_tokat", "name": "Tokat", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=83"},
            {"id": "yerel_trabzon", "name": "Trabzon", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=84"},
            {"id": "yerel_tunceli", "name": "Tunceli", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=85"},
            {"id": "yerel_usak", "name": "Uşak", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=86"},
            {"id": "yerel_van", "name": "Van", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=87"},
            {"id": "yerel_yalova", "name": "Yalova", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=88"},
            {"id": "yerel_yozgat", "name": "Yozgat", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=89"},
            {"id": "yerel_zonguldak", "name": "Zonguldak", "link": "https://gazete.bik.gov.tr/Uygulamalar/GazeteIlkSayfalar?kapsam=yerel&il=90"}
        ],
        "yerel_haber": [
            {"id": "adana_h", "name": "Adana", "link": "https://www.haberler.com/adana/"},
            {"id": "adiyaman_h", "name": "Adıyaman", "link": "https://www.haberler.com/adiyaman/"},
            {"id": "afyon_h", "name": "Afyonkarahisar", "link": "https://www.haberler.com/afyonkarahisar/"},
            {"id": "agri_h", "name": "Ağrı", "link": "https://www.haberler.com/agri/"},
            {"id": "aksaray_h", "name": "Aksaray", "link": "https://www.haberler.com/aksaray/"},
            {"id": "amasya_h", "name": "Amasya", "link": "https://www.haberler.com/amasya/"},
            {"id": "ankara_h", "name": "Ankara", "link": "https://www.haberler.com/ankara/"},
            {"id": "antalya_h", "name": "Antalya", "link": "https://www.haberler.com/antalya/"},
            {"id": "ardahan_h", "name": "Ardahan", "link": "https://www.haberler.com/ardahan/"},
            {"id": "artvin_h", "name": "Artvin", "link": "https://www.haberler.com/artvin/"},
            {"id": "aydin_h", "name": "Aydın", "link": "https://www.haberler.com/aydin/"},
            {"id": "balikesir_h", "name": "Balıkesir", "link": "https://www.haberler.com/balikesir/"},
            {"id": "bartin_h", "name": "Bartın", "link": "https://www.haberler.com/bartin/"},
            {"id": "batman_h", "name": "Batman", "link": "https://www.haberler.com/batman/"},
            {"id": "bayburt_h", "name": "Bayburt", "link": "https://www.haberler.com/bayburt/"},
            {"id": "bilecik_h", "name": "Bilecik", "link": "https://www.haberler.com/bilecik/"},
            {"id": "bingol_h", "name": "Bingöl", "link": "https://www.haberler.com/bingol/"},
            {"id": "bitlis_h", "name": "Bitlis", "link": "https://www.haberler.com/bitlis/"},
            {"id": "bolu_h", "name": "Bolu", "link": "https://www.haberler.com/bolu/"},
            {"id": "burdur_h", "name": "Burdur", "link": "https://www.haberler.com/burdur/"},
            {"id": "bursa_h", "name": "Bursa", "link": "https://www.haberler.com/bursa/"},
            {"id": "canakkale_h", "name": "Çanakkale", "link": "https://www.haberler.com/canakkale/"},
            {"id": "cankiri_h", "name": "Çankırı", "link": "https://www.haberler.com/cankiri/"},
            {"id": "corum_h", "name": "Çorum", "link": "https://www.haberler.com/corum/"},
            {"id": "denizli_h", "name": "Denizli", "link": "https://www.haberler.com/denizli/"},
            {"id": "diyarbakir_h", "name": "Diyarbakır", "link": "https://www.haberler.com/diyarbakir/"},
            {"id": "duzce_h", "name": "Düzce", "link": "https://www.haberler.com/duzce/"},
            {"id": "edirne_h", "name": "Edirne", "link": "https://www.haberler.com/edirne/"},
            {"id": "elazig_h", "name": "Elazığ", "link": "https://www.haberler.com/elazig/"},
            {"id": "erzincan_h", "name": "Erzincan", "link": "https://www.haberler.com/erzincan/"},
            {"id": "erzurum_h", "name": "Erzurum", "link": "https://www.haberler.com/erzurum/"},
            {"id": "eskisehir_h", "name": "Eskişehir", "link": "https://www.haberler.com/eskisehir/"},
            {"id": "gaziantep_h", "name": "Gaziantep", "link": "https://www.haberler.com/gaziantep/"},
            {"id": "giresun_h", "name": "Giresun", "link": "https://www.haberler.com/giresun/"},
            {"id": "gumushane_h", "name": "Gümüşhane", "link": "https://www.haberler.com/gumushane/"},
            {"id": "hakkari_h", "name": "Hakkari", "link": "https://www.haberler.com/hakkari/"},
            {"id": "hatay_h", "name": "Hatay", "link": "https://www.haberler.com/hatay/"},
            {"id": "igdir_h", "name": "Iğdır", "link": "https://www.haberler.com/igdir/"},
            {"id": "isparta_h", "name": "Isparta", "link": "https://www.haberler.com/isparta/"},
            {"id": "istanbul_h", "name": "İstanbul", "link": "https://www.haberler.com/istanbul/"},
            {"id": "izmir_h", "name": "İzmir", "link": "https://www.haberler.com/izmir/"},
            {"id": "kahramanmaras_h", "name": "Kahramanmaraş", "link": "https://www.haberler.com/kahramanmaras/"},
            {"id": "karabuk_h", "name": "Karabük", "link": "https://www.haberler.com/karabuk/"},
            {"id": "karaman_h", "name": "Karaman", "link": "https://www.haberler.com/karaman/"},
            {"id": "kars_h", "name": "Kars", "link": "https://www.haberler.com/kars/"},
            {"id": "kastamonu_h", "name": "Kastamonu", "link": "https://www.haberler.com/kastamonu/"},
            {"id": "kayseri_h", "name": "Kayseri", "link": "https://www.haberler.com/kayseri/"},
            {"id": "kirikkale_h", "name": "Kırıkkale", "link": "https://www.haberler.com/kirikkale/"},
            {"id": "kirklareli_h", "name": "Kırklareli", "link": "https://www.haberler.com/kirklareli/"},
            {"id": "kirsehir_h", "name": "Kırşehir", "link": "https://www.haberler.com/kirsehir/"},
            {"id": "kilis_h", "name": "Kilis", "link": "https://www.haberler.com/kilis/"},
            {"id": "kocaeli_h", "name": "Kocaeli", "link": "https://www.haberler.com/kocaeli/"},
            {"id": "konya_h", "name": "Konya", "link": "https://www.haberler.com/konya/"},
            {"id": "kutahya_h", "name": "Kütahya", "link": "https://www.haberler.com/kutahya/"},
            {"id": "malatya_h", "name": "Malatya", "link": "https://www.haberler.com/malatya/"},
            {"id": "manisa_h", "name": "Manisa", "link": "https://www.haberler.com/manisa/"},
            {"id": "mardin_h", "name": "Mardin", "link": "https://www.haberler.com/mardin/"},
            {"id": "mersin_h", "name": "Mersin", "link": "https://www.haberler.com/mersin/"},
            {"id": "mugla_h", "name": "Muğla", "link": "https://www.haberler.com/mugla/"},
            {"id": "mus_h", "name": "Muş", "link": "https://www.haberler.com/mus/"},
            {"id": "nevsehir_h", "name": "Nevşehir", "link": "https://www.haberler.com/nevsehir/"},
            {"id": "nigde_h", "name": "Niğde", "link": "https://www.haberler.com/nigde/"},
            {"id": "ordu_h", "name": "Ordu", "link": "https://www.haberler.com/ordu/"},
            {"id": "osmaniye_h", "name": "Osmaniye", "link": "https://www.haberler.com/osmaniye/"},
            {"id": "rize_h", "name": "Rize", "link": "https://www.haberler.com/rize/"},
            {"id": "sakarya_h", "name": "Sakarya", "link": "https://www.haberler.com/sakarya/"},
            {"id": "samsun_h", "name": "Samsun", "link": "https://www.haberler.com/samsun/"},
            {"id": "sanliurfa_h", "name": "Şanlıurfa", "link": "https://www.haberler.com/sanliurfa/"},
            {"id": "siirt_h", "name": "Siirt", "link": "https://www.haberler.com/siirt/"},
            {"id": "sinop_h", "name": "Sinop", "link": "https://www.haberler.com/sinop/"},
            {"id": "sirnak_h", "name": "Şırnak", "link": "https://www.haberler.com/sirnak/"},
            {"id": "sivas_h", "name": "Sivas", "link": "https://www.haberler.com/sivas/"},
            {"id": "tekirdag_h", "name": "Tekirdağ", "link": "https://www.haberler.com/tekirdag/"},
            {"id": "tokat_h", "name": "Tokat", "link": "https://www.haberler.com/tokat/"},
            {"id": "trabzon_h", "name": "Trabzon", "link": "https://www.haberler.com/trabzon/"},
            {"id": "tunceli_h", "name": "Tunceli", "link": "https://www.haberler.com/tunceli/"},
            {"id": "usak_h", "name": "Uşak", "link": "https://www.haberler.com/usak/"},
            {"id": "van_h", "name": "Van", "link": "https://www.haberler.com/van/"},
            {"id": "yalova_h", "name": "Yalova", "link": "https://www.haberler.com/yalova/"},
            {"id": "yozgat_h", "name": "Yozgat", "link": "https://www.haberler.com/yozgat/"},
            {"id": "zonguldak_h", "name": "Zonguldak", "link": "https://www.haberler.com/zonguldak/"}
        ]
    }
    return jsonify(config), 200

# --- 6. TARAFTAR TAKIMLARI KONFİGÜRASYONU ---
@app.route('/config/takimlar', methods=['GET'])
def get_takimlar_config():
    config = {
        "takimlar": [
            {"id": "besiktas", "name": "Beşiktaş", "slug": "besiktas", "link": "https://www.fanatik.com.tr/takim/besiktas/futbol/", "lig": 1},
            {"id": "fenerbahce", "name": "Fenerbahçe", "slug": "fenerbahce", "link": "https://www.fanatik.com.tr/takim/fenerbahce/futbol/", "lig": 1},
            {"id": "galatasaray", "name": "Galatasaray", "slug": "galatasaray", "link": "https://www.fanatik.com.tr/takim/galatasaray/futbol/", "lig": 1},
            {"id": "trabzonspor", "name": "Trabzonspor", "slug": "trabzonspor", "link": "https://www.fanatik.com.tr/takim/trabzonspor/futbol/", "lig": 1},
            {"id": "adana_demirspor", "name": "Adana Demirspor", "slug": "adana-demirspor", "link": "https://www.fanatik.com.tr/takim/adana-demirspor/futbol/", "lig": 2},
            {"id": "alanyaspor", "name": "Alanyaspor", "slug": "alanyaspor", "link": "https://www.fanatik.com.tr/takim/alanyaspor/futbol/", "lig": 1},
            {"id": "amed", "name": "Amed SFK", "slug": "amed-sportif-faaliyetler", "link": "https://www.fanatik.com.tr/takim/amed-sportif-faaliyetler/futbol/", "lig": 2},
            {"id": "antalyaspor", "name": "Antalyaspor", "slug": "antalyaspor", "link": "https://www.fanatik.com.tr/takim/antalyaspor/futbol/", "lig": 1},
            {"id": "bandirmaspor", "name": "Bandırmaspor", "slug": "bandirmaspor", "link": "https://www.fanatik.com.tr/takim/bandirmaspor/futbol/", "lig": 2},
            {"id": "basaksehir", "name": "Başakşehir", "slug": "basaksehir", "link": "https://www.fanatik.com.tr/takim/basaksehir/futbol/", "lig": 1},
            {"id": "bodrumspor", "name": "Bodrumspor", "slug": "bodrumspor", "link": "https://www.fanatik.com.tr/takim/bodrumspor/futbol/", "lig": 2},
            {"id": "boluspor", "name": "Boluspor", "slug": "boluspor", "link": "https://www.fanatik.com.tr/takim/boluspor/futbol/", "lig": 2},
            {"id": "corum_fk", "name": "Çorum FK", "slug": "corum-belediyespor", "link": "https://www.fanatik.com.tr/takim/corum-belediyespor/futbol/", "lig": 2},
            {"id": "erokspor", "name": "Erokspor", "slug": "esenler-erokspor", "link": "https://www.fanatik.com.tr/takim/esenler-erokspor/futbol/", "lig": 2},
            {"id": "erzurumspor", "name": "Erzurumspor", "slug": "bsb-erzurumspor", "link": "https://www.fanatik.com.tr/takim/bsb-erzurumspor/futbol/", "lig": 2},
            {"id": "eyupspor", "name": "Eyüpspor", "slug": "eyupspor", "link": "https://www.fanatik.com.tr/takim/eyupspor/futbol/", "lig": 1},
            {"id": "gaziantep_fk", "name": "Gaziantep FK", "slug": "gaziantep-fk", "link": "https://www.fanatik.com.tr/takim/gaziantep-fk/futbol/", "lig": 1},
            {"id": "genclerbirligi", "name": "Gençlerbirliği", "slug": "genclerbirligi", "link": "https://www.fanatik.com.tr/takim/genclerbirligi/futbol/", "lig": 1},
            {"id": "goztepe", "name": "Göztepe", "slug": "goztepe", "link": "https://www.fanatik.com.tr/takim/goztepe/futbol/", "lig": 1},
            {"id": "hatayspor", "name": "Hatayspor", "slug": "hatayspor", "link": "https://www.fanatik.com.tr/takim/hatayspor/futbol/", "lig": 2},
            {"id": "igdir_fk", "name": "Iğdır FK", "slug": "igdir-fk", "link": "https://www.fanatik.com.tr/takim/igdir-fk/futbol/", "lig": 2},
            {"id": "istanbulspor", "name": "İstanbulspor", "slug": "istanbulspor", "link": "https://www.fanatik.com.tr/takim/istanbulspor/futbol/", "lig": 2},
            {"id": "karagumruk", "name": "Karagümrük", "slug": "fatih-karagumruk", "link": "https://www.fanatik.com.tr/takim/fatih-karagumruk/futbol/", "lig": 1},
            {"id": "kasimpasa", "name": "Kasımpaşa", "slug": "kasimpasa", "link": "https://www.fanatik.com.tr/takim/kasimpasa/futbol/", "lig": 1},
            {"id": "kayserispor", "name": "Kayserispor", "slug": "kayserispor", "link": "https://www.fanatik.com.tr/takim/kayserispor/futbol/", "lig": 1},
            {"id": "keciorengucu", "name": "Keçiörengücü", "slug": "ankara-keciorengucu", "link": "https://www.fanatik.com.tr/takim/ankara-keciorengucu/futbol/", "lig": 2},
            {"id": "kocaelispor", "name": "Kocaelispor", "slug": "kocaelispor", "link": "https://www.fanatik.com.tr/takim/kocaelispor/futbol/", "lig": 1},
            {"id": "konyaspor", "name": "Konyaspor", "slug": "konyaspor", "link": "https://www.fanatik.com.tr/takim/konyaspor/futbol/", "lig": 1},
            {"id": "manisa_fk", "name": "Manisa FK", "slug": "manisa-fk", "link": "https://www.fanatik.com.tr/takim/manisa-fk/futbol/", "lig": 2},
            {"id": "pendikspor", "name": "Pendikspor", "slug": "pendikspor", "link": "https://www.fanatik.com.tr/takim/pendikspor/futbol/", "lig": 2},
            {"id": "rizespor", "name": "Rizespor", "slug": "caykur-rizespor", "link": "https://www.fanatik.com.tr/takim/caykur-rizespor/futbol/", "lig": 1},
            {"id": "sakaryaspor", "name": "Sakaryaspor", "slug": "sakaryaspor", "link": "https://www.fanatik.com.tr/takim/sakaryaspor/futbol/", "lig": 2},
            {"id": "samsunspor", "name": "Samsunspor", "slug": "samsunspor", "link": "https://www.fanatik.com.tr/takim/samsunspor/futbol/", "lig": 1},
            {"id": "sariyer", "name": "Sarıyer", "slug": "sariyer", "link": "https://www.fanatik.com.tr/takim/sariyer/futbol/", "lig": 2},
            {"id": "serikspor", "name": "Serikspor", "slug": "serik-belediyespor", "link": "https://www.fanatik.com.tr/takim/serik-belediyespor/futbol/", "lig": 2},
            {"id": "sivasspor", "name": "Sivasspor", "slug": "sivasspor", "link": "https://www.fanatik.com.tr/takim/sivasspor/futbol/", "lig": 2},
            {"id": "umraniyespor", "name": "Ümraniyespor", "slug": "umraniyespor", "link": "https://www.fanatik.com.tr/takim/umraniyespor/futbol/", "lig": 2},
            {"id": "vanspor", "name": "Vanspor", "slug": "vanspor", "link": "https://www.fanatik.com.tr/takim/vanspor/futbol/", "lig": 2}
        ]
    }
    return jsonify(config), 200

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=5000)