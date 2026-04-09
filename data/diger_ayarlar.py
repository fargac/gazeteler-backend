# diger_ayarlar.py

# Ortak Sabitler (SonarQube S1192 Çözümü)
KEY_SATIS = "Satış"
FORMAT_TR_CURRENCY = "tr_currency"

APP_GENERAL_CONFIG = {
    "webview_agents": {
        "android": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",
        "ios": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1"
    },
    # 🔥 YENİ: Dinamik Paylaşım Ayarları eklendi
    "shareText": "📱 Uygulamayı İndir:",
    "shareUrlAndroid": "https://play.google.com/store/apps/details?id=com.denizbatu.gazeteler.activity",
    "shareUrlIos": "" ,
    "mansetProvider": "haber7.com"
}

PIYASA_CONFIG = {
    "show_weather": True,
    "market_api": "https://finans.truncgil.com/today.json",
    "market_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    "market_rules": {
        "usd": {"key": "USD", "subKey": KEY_SATIS, "format": FORMAT_TR_CURRENCY},
        "eur": {"key": "EUR", "subKey": KEY_SATIS, "format": FORMAT_TR_CURRENCY},
        "gold": {"key": "gram-altin", "subKey": KEY_SATIS, "format": FORMAT_TR_CURRENCY},
        "ceyrek": {"key": "ceyrek-altin", "subKey": KEY_SATIS, "format": FORMAT_TR_CURRENCY}
    },
    "weather_api_base": "https://api.open-meteo.com/v1/forecast",
    
    # 🔥 YENİ: Konum bulma API'si artık backend'den gönderiliyor
    "geocode_api_base": "https://api.bigdatacloud.net/data/reverse-geocode-client"
}

ADS_CONFIG = {
   "interstitial_frequency": 5,    # Kaç tıklamada bir geçiş reklamı çıkacak
    "interstitial_cooldown": 60,    # İki geçiş reklamı arası minimum saniye
    "app_open_cooldown": 30,        # Açılış reklamı arası minimum dakika
    "native_ad_interval": 6         # Akışta kaç haberde bir reklam çıkacak
}

base = "https://i13.haber7.net/haber7/gazete"

MANSETLER_CONFIG = [
    {"id": "manset_hurriyet", "name": "Hürriyet", "pattern": f"{base}/hurriyet", "link": "https://www.hurriyet.com.tr"},
    {"id": "manset_sabah", "name": "Sabah", "pattern": f"{base}/sabah", "link": "https://www.sabah.com.tr"},
    {"id": "manset_milliyet", "name": "Milliyet", "pattern": f"{base}/milliyet", "link": "https://www.milliyet.com.tr"},
    {"id": "manset_turkiye", "name": "Türkiye", "pattern": f"{base}/turkiye", "link": "https://www.turkiyegazetesi.com.tr"},
    {"id": "manset_aksam", "name": "Akşam", "pattern": f"{base}/aksam", "link": "https://www.aksam.com.tr"},
    {"id": "manset_yeni_safak", "name": "Yeni Şafak", "pattern": f"{base}/yeni-safak", "link": "https://www.yenisafak.com"},
    {"id": "manset_yeni_akit", "name": "Yeni Akit", "pattern": f"{base}/yeni-akit", "link": "https://www.yeniakit.com.tr"},
    {"id": "manset_dirilis_postasi", "name": "Diriliş P.", "pattern": f"{base}/dirilis-postasi", "link": "https://www.dirilispostasi.com"},
    {"id": "manset_milat", "name": "Milat", "pattern": f"{base}/milat", "link": "https://www.milatgazetesi.com"},
    {"id": "manset_turkgun", "name": "Türkgün", "pattern": f"{base}/turkgun", "link": "https://www.turkgun.com"},
    {"id": "manset_yeni_birlik", "name": "Yeni Birlik", "pattern": f"{base}/yeni-birlik", "link": "https://www.gazetebirlik.com"},
    {"id": "manset_milli_gazete", "name": "Milli Gazete", "pattern": f"{base}/milli-gazete", "link": "https://www.milligazete.com.tr"},
    {"id": "manset_dunya", "name": "Dünya", "pattern": f"{base}/dunya", "link": "https://www.dunya.com"},
    {"id": "manset_yeni_cag", "name": "Yeniçağ", "pattern": f"{base}/yenicag", "link": "https://www.yenicaggazetesi.com.tr"},
    {"id": "manset_yeni_soz", "name": "Yenisöz", "pattern": f"{base}/yenisoz", "link": "https://www.yenisoz.com.tr"},
    {"id": "manset_aydinlik", "name": "Aydınlık", "pattern": f"{base}/aydinlik", "link": "https://www.aydinlik.com.tr"},
    {"id": "manset_dogru-haber", "name": "Doğru Haber", "pattern": f"{base}/dogru-haber", "link": "https://dogruhaber.com.tr"},
    {"id": "manset_takvim", "name": "Takvim", "pattern": f"{base}/takvim-gazetesi", "link": "https://www.takvim.com.tr"},
    {"id": "manset_fanatik", "name": "Fanatik", "pattern": f"{base}/fanatik", "link": "https://www.fanatik.com.tr"},
    {"id": "manset_fotomac", "name": "Fotomaç", "pattern": f"{base}/fotomac", "link": "https://www.fotomac.com.tr"}
]