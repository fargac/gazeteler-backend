# scripts/db_cleanup.py
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone, timedelta

def clean_old_records():
    print("🧹 [GEZO CLEANUP] Veritabanı temizlik botu başlatıldı...")
    
    # Firebase Bağlantısı
    if not firebase_admin._apps:
        cred_json = os.environ.get("FIREBASE_CREDENTIALS")
        if not cred_json:
            raise EnvironmentError("FIREBASE_CREDENTIALS eksik!")
        cred_dict = json.loads(cred_json)
        firebase_admin.initialize_app(credentials.Certificate(cred_dict))

    db = firestore.client()
    
    # 90 gün öncesinin sınır tarihini belirle
    ninety_days_ago = datetime.now(timezone.utc) - timedelta(days=90)
    print(f"📅 Sınır Tarih: {ninety_days_ago.strftime('%d.%m.%Y')} (Bu tarihten eskiler silinecek)")

    # 1. YAZAR BİLDİRİM GEÇMİŞİ (sentArticles)
    try:
        sent_ref = db.collection("sentArticles")
        # 90 günden eski olanları getir
        old_articles = sent_ref.where("sentAt", "<", ninety_days_ago).stream()
        count_articles = 0
        for doc in old_articles:
            doc.reference.delete()
            count_articles += 1
        print(f"✅ sentArticles: {count_articles} adet eski kayıt başarıyla silindi.")
    except Exception as e:
        print(f"❌ sentArticles temizlenirken hata: {e}")

    # 2. GÜNÜN ÖZETİ GEÇMİŞİ (daily_summaries)
    try:
        summary_ref = db.collection("daily_summaries")
        old_summaries = summary_ref.where("created_at", "<", ninety_days_ago).stream()
        count_summaries = 0
        for doc in old_summaries:
            doc.reference.delete()
            count_summaries += 1
        print(f"✅ daily_summaries: {count_summaries} adet eski özet başarıyla silindi.")
    except Exception as e:
        print(f"❌ daily_summaries temizlenirken hata: {e}")

    print("🏁 [GEZO CLEANUP] Temizlik operasyonu sorunsuz tamamlandı.")

if __name__ == "__main__":
    clean_old_records()
