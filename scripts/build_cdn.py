import json
import time
import os
import sys
import boto3
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.haber_kaynaklari import NEWS_SOURCES
from data.takimlar import TAKIMLAR
from data.kesfet import KESFET_CONFIG
from data.diger_ayarlar import PIYASA_CONFIG, MANSETLER_CONFIG, ADS_CONFIG, APP_GENERAL_CONFIG

def build_static_files():
    # Derleme anındaki eşsiz zaman damgası (Unix Timestamp)
    current_version = str(int(time.time()))

    # appGeneralConfig içine config_version değerini güvenli bir şekilde ekle
    app_general = APP_GENERAL_CONFIG.copy() if APP_GENERAL_CONFIG else {}
    app_general["config_version"] = current_version

    data = {
        "haber_kaynaklari": NEWS_SOURCES,
        "piyasa": PIYASA_CONFIG,
        "mansetler": MANSETLER_CONFIG,
        "kesfet": KESFET_CONFIG,
        "takimlar": TAKIMLAR,
        "ads": ADS_CONFIG,
        "appGeneralConfig": app_general
    }
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cdn_data')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        
    with open(os.path.join(output_dir, 'version.json'), 'w', encoding='utf-8') as f:
        json.dump({"version": current_version}, f, ensure_ascii=False)
        
    print(f"✅ Başarılı! cdn_data klasörüne dosyalar yazıldı. Versiyon: {current_version}")
   
    def upload_and_purge():
     s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )
    bucket = os.environ["R2_BUCKET"]

    s3.upload_file("cdn_data/version.json", bucket, "cdn_data/version.json",
        ExtraArgs={"CacheControl": "no-cache, must-revalidate", "ContentType": "application/json"})
    s3.upload_file("cdn_data/config.json", bucket, "cdn_data/config.json",
        ExtraArgs={"CacheControl": "public, max-age=3600", "ContentType": "application/json"})

    requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{os.environ['CF_ZONE_ID']}/purge_cache",
        headers={"Authorization": f"Bearer {os.environ['CF_API_TOKEN']}", "Content-Type": "application/json"},
        json={"files": [
            "https://api.gezoist.com/cdn_data/version.json",
            "https://api.gezoist.com/cdn_data/config.json",
        ]},
    )
    upload_and_purge()
if __name__ == '__main__':
    build_static_files()