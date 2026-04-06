# scripts/db_cleanup.py
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone, timedelta

# Firestore batch işlemi başına maksimum 500 döküman silinebilir.
FIRESTORE_BATCH_LIMIT = 500


def batch_delete(db, query):
    """
    Verilen Firestore sorgusundaki tüm dökümanları batch'ler halinde siler.

    🔥 FIX: Eski versiyon tüm dökümanları stream() ile RAM'e yüklüyor,
    sonra tek tek delete() çağırıyordu. Bu iki probleme yol açıyordu:
      1. Çok sayıda kayıt varsa memory spike (tüm docs RAM'de)
      2. Her delete() ayrı bir network isteği (yavaş)

    Yeni versiyon: 500'lük batch'ler halinde siler.
      - Sabit bellek kullanımı (sadece 500 döküman aynı anda RAM'de)
      - Her 500 silme tek bir network isteği (Firestore batch write)
    """
    deleted_total = 0
    batch = db.batch()
    batch_count = 0

    for doc in query.stream():
        batch.delete(doc.reference)
        batch_count += 1
        deleted_total += 1

        if batch_count == FIRESTORE_BATCH_LIMIT:
            batch.commit()
            batch = db.batch()
            batch_count = 0

    # Kalan dökümanları commit et (500'ün katı olmayan son grup)
    if batch_count > 0:
        batch.commit()

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
