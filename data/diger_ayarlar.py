# Ortak Sabitler (SonarQube S1192 Çözümü)
KEY_SATIS = "Satış"
FORMAT_TR_CURRENCY = "tr_currency"

PIYASA_CONFIG = {
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
    "weather_api_base": "https://api.open-meteo.com/v1/forecast"
}

ADS_CONFIG = {
    "ad_frequency": 15,
    "app_open_cooldown": 3
}

base = "https://i13.haber7.net/haber7/gazete"
MANSETLER_CONFIG = [
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
    {"id": "manset_fotomac", "name": "Fotomaç", "pattern": f"{base}/fotomac"}
]