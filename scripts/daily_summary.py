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
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

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
            count = 0
            for entry in feed.entries:
                pub_date = date_parser.parse(entry.get('published', entry.get('pubDate', '')))
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)

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
    news_text = "\n".join([f"- [{n['source']}] {n['title']}" for n in news_data])
    prompt = f"""
    Sen Gezo Gündem uygulamasının baş editörüsün. Aşağıda sana Türkiye'nin en büyük 6 kaynağından gelen son 24 saatin haber başlıklarını sunuyorum:
    
    {news_text}
    
    GÖREVİN:
    1. Bu haberleri analiz et. Eski, etkisini yitirmiş veya dünden kalan önemsiz haberleri tamamen ELE.
    2. Sadece BUGÜNÜN gündemine damga vuran, hala güncelliğini ve sıcaklığını koruyan en hayati 6 maddeyi seç. Aynı konudaki haberleri tek maddede birleştir.
    3. Şeffaflık gereği, bu özeti hazırlarken yararlandığın TÜM kaynakların adını metnin en sonunda belirt.
    4. Yanıtı SADECE aşağıdaki JSON formatında ver, başka açıklama yazma:
    {{
        "push_title": "📅 Günün Özeti: Neler Oldu?",
        "push_body": "En önemli 3 maddeyi buraya kısa (max 120 karakter) yaz...",
        "detailed_summary": ["Madde 1", "Madde 2", "Madde 3", "Madde 4", "Madde 5", "Madde 6"],
        "sources_used": "Kaynak 1 • Kaynak 2 • Kaynak 3"
    }}
    """  
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        raise EnvironmentError("GEMINI_API_KEY eksik!")
    
    client = genai.Client(api_key=gemini_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini geçersiz JSON döndürdü: {e}\nYanıt: {response.text[:200]}")

def send_to_firebase(summary_data):
    doc_id = datetime.now().strftime("%Y-%m-%d")

    message = messaging.Message(
        notification=messaging.Notification(
            title=summary_data['push_title'],
            body=summary_data['push_body']
        ),
        data={
            "type": "daily_summary",
            "date": doc_id
        },
        topic="daily_summary" # BUG DÜZELTİLDİ: all_users yerine daily_summary
    )
    messaging.send(message)
    print("🚀 Bildirim başarıyla fırlatıldı!")

    db.collection("daily_summaries").document(doc_id).set({
        "items": summary_data['detailed_summary'],
        "sources": summary_data['sources_used'],
        "created_at": firestore.SERVER_TIMESTAMP
    })
    print("💾 Uygulama içi özet Firestore'a kaydedildi!")

if __name__ == "__main__":
    raw_news = get_todays_news()
    if len(raw_news) > 5:
        max_deneme = 4
        
        for deneme in range(max_deneme):
            try:
                summary = generate_ai_summary(raw_news)
                send_to_firebase(summary)
                print("✅ TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI!")
                break
                
            except Exception as e:
                hata_mesaji = str(e)
                if "503" in hata_mesaji or "429" in hata_mesaji or "UNAVAILABLE" in hata_mesaji:
                    bekleme_suresi = 15 * (deneme + 1)
                    print(f"⚠️ Gemini API şu an yoğun (Deneme {deneme + 1}/{max_deneme}). {bekleme_suresi} saniye bekleniyor...")
                    time.sleep(bekleme_suresi)
                else:
                    print(f"❌ Yapay Zeka veya Firebase aşamasında kritik hata: {e}")
                    break
        else:
            print("❌ Sunucular ısrarla yanıt vermedi, maksimum deneme sınırına ulaşıldı.")
            
    else:
        print("⚠️ Yeterli yeni haber bulunamadı, işlem iptal edildi.")