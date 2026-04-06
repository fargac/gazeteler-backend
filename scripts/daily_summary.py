import os
import json
import feedparser
import time
import firebase_admin
from firebase_admin import credentials, messaging, firestore
from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser
from google import genai

SOURCES = [
    {"name": "Habertürk", "url": "https://www.haberturk.com/rss/manset.xml"},
    {"name": "Sözcü", "url": "https://www.sozcu.com.tr/feeds-son-dakika"},
    {"name": "Hürriyet", "url": "https://www.hurriyet.com.tr/rss/anasayfa"},
    {"name": "Ekonomim", "url": "https://www.ekonomim.com/rss"},
    {"name": "NTV Spor", "url": "https://www.ntvspor.net/rss/anasayfa"},
    {"name": "Son Dakika", "url": "https://rss.sondakika.com/rss_standart.asp"}
]

if not firebase_admin._apps:
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    cred_dict = json.loads(cred_json)
    firebase_admin.initialize_app(credentials.Certificate(cred_dict))

db = firestore.client()

def get_todays_news():
    today_news_list = []
    tr_tz = timezone(timedelta(hours=3))
    now_tr = datetime.now(tr_tz)
    today_start = now_tr - timedelta(hours=24)

    print(f"🔎 {now_tr.strftime('%d.%m.%Y')} tarihli haberler taranıyor...")

    for source in SOURCES:
        try:
            feed = feedparser.parse(source['url'])
            for entry in feed.entries:
                pub_date = date_parser.parse(entry.get('published', entry.get('pubDate', '')))
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)

                if pub_date >= today_start:
                    today_news_list.append({"source": source['name'], "title": entry.title})
        except Exception as e:
            print(f"❌ {source['name']} okunurken hata: {e}")
    
    return today_news_list

def generate_ai_summary(news_data):
    news_text = "\n".join([f"- [{n['source']}] {n['title']}" for n in news_data])
    prompt = f"""
    Sen Gezo Gündem uygulamasının baş editörüsün. Türkiye'nin en büyük 6 kaynağından son 24 saatin haberleri:
    {news_text}
    GÖREVİN: BUGÜNÜN gündemine damga vuran en hayati 6 maddeyi seç. Yanıtı SADECE aşağıdaki JSON formatında ver:
    {{
        "push_title": "📅 Günün Özeti: Neler Oldu?",
        "push_body": "Kısa özet...",
        "detailed_summary": [
            {{"title": "Madde 1 Kısa Başlık", "desc": "Detay"}},
            {{"title": "Madde 2 Kısa Başlık", "desc": "Detay"}}
        ],
        "sources_used": "Kaynak 1 • Kaynak 2"
    }}
    """  
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt,
        config=genai.types.GenerateContentConfig(response_mime_type="application/json")
    )
    return json.loads(response.text)

def save_to_cdn(summary_data, doc_id):
    # 🔥 YENİ: Veriyi CDN için JSON dosyası olarak diske yazıyoruz
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cdn_data', 'summaries')
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, f"{doc_id}.json")
    
    cdn_payload = {
        "date": doc_id,
        "items": summary_data['detailed_summary'],
        "sources": summary_data['sources_used']
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(cdn_payload, f, ensure_ascii=False, separators=(',', ':'))
        
    print(f"📦 CDN dosyası oluşturuldu: {file_path}")

def send_to_firebase(summary_data, doc_id):
    message = messaging.Message(
        notification=messaging.Notification(title=summary_data['push_title'], body=summary_data['push_body']),
        data={"type": "daily_summary", "date": doc_id},
        topic="daily_summary" 
    )
    messaging.send(message)
    print("🚀 Bildirim başarıyla fırlatıldı!")

    db.collection("daily_summaries").document(doc_id).set({
        "items": summary_data['detailed_summary'],
        "sources": summary_data['sources_used'],
        "created_at": firestore.SERVER_TIMESTAMP
    })
    print("💾 Yedek olarak Firestore'a kaydedildi!")

if __name__ == "__main__":
    raw_news = get_todays_news()
    if len(raw_news) > 5:
        tr_tz = timezone(timedelta(hours=3))
        doc_id = datetime.now(tr_tz).strftime("%Y-%m-%d")
        
        for deneme in range(4):
            try:
                summary = generate_ai_summary(raw_news)
                save_to_cdn(summary, doc_id) # Önce diske yaz
                send_to_firebase(summary, doc_id) # Sonra bildirimi at
                print("✅ TÜM İŞLEMLER BAŞARILI!")
                break
            except Exception as e:
                time.sleep(15 * (deneme + 1))