"""
Yazar Bildirim Sistemi
GitHub Actions ile her sabah 07:00'de çalışır.
Favori yazarların yeni makalelerini kontrol eder ve FCM ile bildirim gönderir.
"""

import os
import json
import hashlib
import logging
from datetime import datetime, timezone
from typing import Optional

import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore, messaging

# ─────────────────────────────────────────────
# 1. LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# 2. YAZAR LİSTESİ
#    rss   → RSS feed URL'si
#    scrape → scrape edilecek URL
#    match → RSS'te yazar adı eşleşmesi (RSS için)
# ─────────────────────────────────────────────
AUTHORS = [
    # ── Sözcü (RSS) ──────────────────────────
    {
        "id": "yilmaz_ozdil",
        "name": "Yılmaz Özdil",
        "source": "rss",
        "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar",
        "match": "Yılmaz Özdil",
    },
    {
        "id": "emin_colasan",
        "name": "Emin Çölaşan",
        "source": "rss",
        "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar",
        "match": "Emin Çölaşan",
    },
    {
        "id": "soner_yalcin",
        "name": "Soner Yalçın",
        "source": "rss",
        "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar",
        "match": "Soner Yalçın",
    },
    {
        "id": "ismail_saymaz",
        "name": "İsmail Saymaz",
        "source": "rss",
        "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar",
        "match": "İsmail Saymaz",
    },
    {
        "id": "erman_toroglu",
        "name": "Erman Toroğlu",
        "source": "rss",
        "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar",
        "match": "Erman Toroğlu",
    },
    # ── Habertürk (RSS) ───────────────────────
    {
        "id": "murat_bardakci",
        "name": "Murat Bardakçı",
        "source": "rss",
        "rss": "https://www.haberturk.com/rss/kategori/yazarlar.xml",
        "match": "Murat Bardakçı",
    },
    # ── Hürriyet (Scrape) ─────────────────────
    {
        "id": "ahmet_hakan",
        "name": "Ahmet Hakan",
        "source": "scrape_hurriyet",
        "scrape_url": "https://www.hurriyet.com.tr/yazarlar/",
    },
    {
        "id": "abdulkadir_selvi",
        "name": "Abdülkadir Selvi",
        "source": "scrape_hurriyet",
        "scrape_url": "https://www.hurriyet.com.tr/yazarlar/",
    },
    {
        "id": "osman_muftuoglu",
        "name": "Osman Müftüoğlu",
        "source": "scrape_hurriyet",
        "scrape_url": "https://www.hurriyet.com.tr/yazarlar/",
    },
    # ── Sabah (Scrape) ────────────────────────
    {
        "id": "ahmet_cakar",
        "name": "Ahmet Çakar",
        "source": "scrape_sabah",
        "scrape_url": "https://m.sabah.com.tr/yazarlar",
    },
    # ── Fatih Altaylı (Scrape) ────────────────
    {
        "id": "fatih_altayli",
        "name": "Fatih Altaylı",
        "source": "scrape_altayli",
        "scrape_url": "https://fatihaltayli.com.tr/yazilar/fatih-altayli/kose-yazilari",
    },
    # ── 10haber (Scrape) ──────────────────────
    {
        "id": "ertugrul_ozkok",
        "name": "Ertuğrul Özkök",
        "source": "scrape_10haber",
        "scrape_url": "https://10haber.net/yazarlar/ertugrul-ozkok/",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; K) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Mobile Safari/537.36"
    )
}

# ─────────────────────────────────────────────
# 3. FETCH YARDIMCILARI
# ─────────────────────────────────────────────

def fetch(url: str, timeout: int = 10) -> Optional[requests.Response]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception as e:
        log.warning(f"Fetch hatası [{url}]: {e}")
        return None


def url_hash(url: str) -> str:
    """URL'yi Firestore doc ID'si olarak kullanmak için hash'le."""
    return hashlib.md5(url.encode()).hexdigest()


# ─────────────────────────────────────────────
# 4. MAKALE BULUCULARI
# ─────────────────────────────────────────────

def find_from_rss(author: dict) -> Optional[dict]:
    """RSS feed'den yazara ait bugünkü makaleyi bul."""
    r = fetch(author["rss"])
    if not r:
        return None

    soup = BeautifulSoup(r.content, "xml")
    today = datetime.now(timezone.utc).date()

    for item in soup.find_all("item"):
        title_tag = item.find("title")
        if not title_tag:
            continue

        # Sözcü RSS: <title> = yazar adı
        if author["match"].lower() not in title_tag.text.lower():
            continue

        link_tag = item.find("link")
        pub_tag = item.find("pubDate")

        if not link_tag:
            continue

        # Tarih kontrolü — bugünkü makale mi?
        if pub_tag:
            try:
                from email.utils import parsedate_to_datetime
                pub_date = parsedate_to_datetime(pub_tag.text).date()
                if pub_date != today:
                    continue
            except Exception:
                pass  # Tarih parse edilemezse yine de gönder

        article_title_tag = item.find("description") or title_tag
        return {
            "url": link_tag.text.strip(),
            "title": article_title_tag.text.strip()[:100],
        }

    return None


def find_from_hurriyet(author: dict) -> Optional[dict]:
    """Hürriyet yazarlar sayfasından yazarın bugünkü makalesini bul."""
    r = fetch(author["scrape_url"])
    if not r:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    for box in soup.select("a.author-box"):
        name_tag = box.select_one("span.name")
        if not name_tag:
            continue
        if author["name"].lower() not in name_tag.text.lower():
            continue

        title_tag = box.select_one("span.title")
        href = box.get("href", "")
        if not href:
            continue

        url = href if href.startswith("http") else f"https://www.hurriyet.com.tr{href}"
        return {
            "url": url,
            "title": title_tag.text.strip() if title_tag else author["name"],
        }

    return None


def find_from_sabah(author: dict) -> Optional[dict]:
    """Sabah yazarlar sayfasından yazarın bugünkü makalesini bul."""
    r = fetch(author["scrape_url"])
    if not r:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    for li in soup.select("div.manset.writer ul li"):
        name_tag = li.select_one("strong:not(.sub)")
        if not name_tag:
            continue
        if author["name"].lower() not in name_tag.text.lower():
            continue

        a_tag = li.find("a")
        title_tag = li.select_one("strong.sub")
        if not a_tag:
            continue

        href = a_tag.get("href", "")
        url = href if href.startswith("http") else f"https://www.sabah.com.tr{href}"
        return {
            "url": url,
            "title": title_tag.text.strip() if title_tag else author["name"],
        }

    return None


def find_from_altayli(author: dict) -> Optional[dict]:
    """fatihaltayli.com.tr'den en son köşe yazısını bul."""
    r = fetch(author["scrape_url"])
    if not r:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()

    for a in soup.select("a.blog-item"):
        href = a.get("href", "")
        if not href:
            continue

        # URL'de bugünün tarihi var mı kontrol et (örn: /2026-03-30/)
        today_str = today.strftime("%Y-%m-%d")
        if today_str not in href:
            continue

        url = href if href.startswith("http") else f"https://fatihaltayli.com.tr{href}"
        title = a.get("title") or a.get_text(strip=True)[:100]
        return {"url": url, "title": title}

    return None


def find_from_10haber(author: dict) -> Optional[dict]:
    """10haber.net'ten en son makaleyi bul."""
    r = fetch(author["scrape_url"])
    if not r:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # İlk makale linki
    a = soup.select_one("article a, .post a, h2 a")
    if not a:
        return None

    href = a.get("href", "")
    url = href if href.startswith("http") else f"https://10haber.net{href}"
    title = a.get_text(strip=True)[:100]
    return {"url": url, "title": title}


FINDERS = {
    "rss": find_from_rss,
    "scrape_hurriyet": find_from_hurriyet,
    "scrape_sabah": find_from_sabah,
    "scrape_altayli": find_from_altayli,
    "scrape_10haber": find_from_10haber,
}


# ─────────────────────────────────────────────
# 5. ANA MANTIĞI
# ─────────────────────────────────────────────

def main():
    # Firebase Admin SDK başlat
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    if not cred_json:
        raise EnvironmentError("FIREBASE_CREDENTIALS environment variable eksik!")

    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    sent_ref = db.collection("sentArticles")
    favorites_ref = db.collection("userFavorites")

    for author in AUTHORS:
        log.info(f"Kontrol ediliyor: {author['name']}")

        try:
            finder = FINDERS.get(author["source"])
            if not finder:
                log.warning(f"Finder bulunamadı: {author['source']}")
                continue

            article = finder(author)
            if not article:
                log.info(f"  → Bugün yeni makale yok: {author['name']}")
                continue

            log.info(f"  → Makale bulundu: {article['url']}")

            # Daha önce gönderildi mi?
            article_id = url_hash(article["url"])
            sent_doc = sent_ref.document(article_id).get()
            if sent_doc.exists:
                log.info(f"  → Zaten gönderildi, atlanıyor.")
                continue

            # Bu yazarı favorileyen kullanıcıların token'larını bul
            users = favorites_ref.where(
                "favoriteAuthorIds", "array_contains", author["id"]
            ).stream()

            tokens = [doc.id for doc in users]  # doc.id = FCM token

            if not tokens:
                log.info(f"  → Favorileyen kullanıcı yok: {author['name']}")
                # Yine de gönderildi olarak işaretle
                sent_ref.document(article_id).set({
                    "url": article["url"],
                    "authorId": author["id"],
                    "sentAt": firestore.SERVER_TIMESTAMP,
                })
                continue

            log.info(f"  → {len(tokens)} kullanıcıya gönderiliyor...")

            # FCM multicast — max 500 token per batch
            batch_size = 500
            success_count = 0

            for i in range(0, len(tokens), batch_size):
                batch_tokens = tokens[i:i + batch_size]
                message = messaging.MulticastMessage(
                    tokens=batch_tokens,
                    notification=messaging.Notification(
                        title=author["name"],
                        body=article["title"],
                    ),
                    data={"url": article["url"]},
                    android=messaging.AndroidConfig(
                        priority="high",
                        notification=messaging.AndroidNotification(
                            sound="default",
                        ),
                    ),
                    apns=messaging.APNSConfig(
                        payload=messaging.APNSPayload(
                            aps=messaging.Aps(sound="default"),
                        ),
                    ),
                )

                response = messaging.send_each_for_multicast(message)
                success_count += response.success_count

                # Bozuk token'ları Firestore'dan sil
                for idx, resp in enumerate(response.responses):
                    if not resp.success:
                        error_code = resp.exception.code if resp.exception else ""
                        if error_code in (
                            "messaging/registration-token-not-registered",
                            "messaging/invalid-registration-token",
                        ):
                            bad_token = batch_tokens[idx]
                            favorites_ref.document(bad_token).delete()
                            log.info(f"  → Bozuk token silindi: {bad_token[:20]}...")

            log.info(f"  → Gönderildi: {success_count}/{len(tokens)} başarılı")

            # Gönderildi olarak işaretle
            sent_ref.document(article_id).set({
                "url": article["url"],
                "authorId": author["id"],
                "authorName": author["name"],
                "sentAt": firestore.SERVER_TIMESTAMP,
            })

        except Exception as e:
            log.error(f"❌ {author['name']} işlenirken beklenmeyen hata oluştu: {e}")
            continue

    log.info("✅ Tüm yazarlar kontrol edildi.")


if __name__ == "__main__":
    main()
