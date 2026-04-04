import json
import hashlib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.haber_kaynaklari import NEWS_SOURCES
from data.takimlar import TAKIMLAR
from data.kesfet import KESFET_CONFIG
from data.diger_ayarlar import PIYASA_CONFIG, MANSETLER_CONFIG, ADS_CONFIG, APP_GENERAL_CONFIG

def build_static_files():
    data = {
        "haber_kaynaklari": NEWS_SOURCES,
        "piyasa": PIYASA_CONFIG,
        "mansetler": MANSETLER_CONFIG,
        "kesfet": KESFET_CONFIG,
        "takimlar": TAKIMLAR,
        "ads": ADS_CONFIG,
        "appGeneralConfig": APP_GENERAL_CONFIG
    }
    
    # 🔥 BEST PRACTICE: MD5 yerine SHA-256
    config_str = json.dumps(data, sort_keys=True)
    version_hash = hashlib.sha256(config_str.encode()).hexdigest()[:32] # MD5 gibi 32 karakter
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cdn_data')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        
    with open(os.path.join(output_dir, 'version.json'), 'w', encoding='utf-8') as f:
        json.dump({"version": version_hash}, f, ensure_ascii=False)
        
    print(f"✅ Başarılı! cdn_data klasörüne dosyalar yazıldı. Versiyon: {version_hash}")

if __name__ == '__main__':
    build_static_files()