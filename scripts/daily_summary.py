import os
import json
import feedparser
import firebase_admin
from firebase_admin import credentials, messaging, firestore
from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser

# YENİ NESİL GEMINI KÜTÜPHANESİ
from google import genai

# 1. AYARLAR VE KAYNAKLAR
SOURCES = [
    {"name": "Habertürk", "url": "https://www.haberturk.com/rss/manset.xml"},
    {"name": "Sözcü", "url": "https://www.sozcu.com.tr/feeds-son-dakika"},
    {"name": "Hürriyet", "url": "https://www.hurriyet.com.tr/rss/anasayfa"},
    {"name": "Ekonomim", "url": "https://www.ekonomim.com/rss"},
    {"name": "NTV Spor", "url": "https://www.ntvspor.net/rss/anasayfa"},
    {"name": "Son Dakika", "url": "https://rss.sondakika.com/rss_standart.asp"}
]

# 2. FIREBASE BAĞLANTISI (Environment variables ile)
if not firebase_admin._apps:
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_todays_news():
    today_news_list = []
    # Türkiye saatiyle (UTC+3) bugünün başlangıcını bul
    tr_tz = timezone(timedelta(hours=3))
    now_tr = datetime.now(tr_tz)
    today_start = now_tr.replace(hour=0, minute=0, second=0, microsecond=0)

    print(f"🔎 {now_tr.strftime('%d.%m.%Y')} tarihli haberler taranıyor...")

    for source in SOURCES:
        try:
            feed = feedparser.parse(source['url'])
            count = 0
            for entry in feed.entries:
                # Haber tarihini çöz
                pub_date = date_parser.parse(entry.get('published', entry.get('pubDate', '')))
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)

                # Sadece bugünün haberleri
                if pub_date >= today_start:
                    today_news_list.append({
                        "source": source['name'],
                        "title": entry.title
                    })
                    count += 1
            print(f"✅ {source['name']}: {count} yeni haber alındı.")
        except Exception as e:
            print(f"❌ {source['name']} okunurken hata: {e}")
    
    return today_news_list

def generate_ai_summary(news_data):
    # Gemini'ye gidecek metni hazırla
    news_text = "\n".join([f"- [{n['source']}] {n['title']}" for n in news_data])
    
    prompt = f"""
    Sen Gezo Gündem uygulamasının baş editörüsün. Aşağıda sana Türkiye'nin en büyük 6 kaynağından gelen bugünün haber başlıklarını sunuyorum:
    
    {news_text}
    
    GÖREVİN:
    1. Bu haberleri analiz et, aynı konudaki haberleri tek bir maddede birleştir.
    2. Türkiye gündemi için en hayati 6 maddeyi seç.
    3. Şeffaflık gereği, bu özeti hazırlarken yararlandığın TÜM kaynakların adını metnin en sonunda belirt.
    4. Yanıtı SADECE aşağıdaki JSON formatında ver, başka açıklama yazma:
    {{
        "push_title": "📅 Günün Özeti: Neler Oldu?",
        "push_body": "En önemli 3 maddeyi buraya kısa (max 120 karakter) yaz...",
        "detailed_summary": ["Madde 1", "Madde 2", "Madde 3", "Madde 4", "Madde 5", "Madde 6"],
        "sources_used": "Kaynak 1 • Kaynak 2 • Kaynak 3"
    }}
    """
    
    # YEPYENİ SDK KULLANIMI VE GEMINI 2.0 FLASH
    # API key'i GitHub Actions'dan garantili şekilde alıyoruz
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY")) 
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    
    # JSON temizleme (Markdown taglarını kaldırır)
    clean_response = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_response)

def send_to_firebase(summary_data):
    doc_id = datetime.now().strftime("%Y-%m-%d")

    # 1. ADIM: Bildirimi Fırlat (Data payload'ı eklendi)
    message = messaging.Message(
        notification=messaging.Notification(
            title=summary_data['push_title'],
            body=summary_data['push_body']
        ),
        data={
            "type": "daily_summary",
            "date": doc_id
        },
        topic="all_users"
    )
    messaging.send(message)
    print("🚀 Bildirim başarıyla fırlatıldı!")

    # 2. ADIM: Uygulama İçi Vitrin İçin Firestore'a Kaydet
    db.collection("daily_summaries").document(doc_id).set({
        "items": summary_data['detailed_summary'],
        "sources": summary_data['sources_used'],
        "created_at": firestore.SERVER_TIMESTAMP
    })
    print("💾 Uygulama içi özet Firestore'a kaydedildi!")

# ANA ÇALIŞTIRICI
if __name__ == "__main__":
    raw_news = get_todays_news()
    if len(raw_news) > 5:
        try:
            summary = generate_ai_summary(raw_news)
            send_to_firebase(summary)
            print("✅ TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI!")
        except Exception as e:
            print(f"❌ Yapay Zeka veya Firebase aşamasında kritik hata: {e}")
    else:
        print("⚠️ Yeterli yeni haber bulunamadı, işlem iptal edildi.")