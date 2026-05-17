# scripts/db_cleanup.py
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone, timedelta

# Firestore batch işlemi başına maksimum 500 döküman silinebilir.
FIRESTORE_BATCH_LIMIT = 500


# scripts/db_cleanup.py içindeki batch_delete fonksiyonunu BUNUNLA DEĞİŞTİR:

def batch_delete(db, query):
    """
    🔥 GERÇEK PAGINATION & BATCH MİMARİSİ
    Sadece FIRESTORE_BATCH_LIMIT (500) kadar dökümanı RAM'e alır.
    Silme bitince bir sonraki 500'ü çeker. Sunucu RAM'i asla şişmez.
    """
    deleted_total = 0

    while True:
        # Sadece 500 tanesini RAM'e al (Sihirli kelime: .limit() )
        docs = list(query.limit(FIRESTORE_BATCH_LIMIT).stream())
        
        if not docs:
            break # Silinecek döküman kalmadı, döngüyü bitir
            
        batch = db.batch()
        for doc in docs:
            batch.delete(doc.reference)
        
        batch.commit()
        deleted_total += len(docs)
        print(f"🧹 {len(docs)} döküman silindi. Toplam: {deleted_total}")
        
    return deleted_total


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
        query = db.collection("sentArticles").where("sentAt", "<", ninety_days_ago)
        count = batch_delete(db, query)
        print(f"✅ sentArticles: {count} adet eski kayıt başarıyla silindi.")
    except Exception as e:
        print(f"❌ sentArticles temizlenirken hata: {e}")

    # 2. GÜNÜN ÖZETİ GEÇMİŞİ (daily_summaries)
    try:
        query = db.collection("daily_summaries").where("created_at", "<", ninety_days_ago)
        count = batch_delete(db, query)
        print(f"✅ daily_summaries: {count} adet eski özet başarıyla silindi.")
    except Exception as e:
        print(f"❌ daily_summaries temizlenirken hata: {e}")

    print("🏁 [GEZO CLEANUP] Temizlik operasyonu sorunsuz tamamlandı.")


if __name__ == "__main__":
    clean_old_records()
