"""
Yazar Bildirim Sistemi
GitHub Actions ile her sabah 07:00'de çalışır.
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

AUTHORS = [
    # ── Sözcü (RSS) ──────────────────────────────────────────────────────────
    {"id": "yilmaz_ozdil",   "name": "Yılmaz Özdil",   "source": "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Yılmaz Özdil"},
    {"id": "emin_colasan",   "name": "Emin Çölaşan",   "source": "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Emin Çölaşan"},
    {"id": "soner_yalcin",   "name": "Soner Yalçın",   "source": "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Soner Yalçın"},
    {"id": "ismail_saymaz",  "name": "İsmail Saymaz",  "source": "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "İsmail Saymaz"},
    {"id": "erman_toroglu",  "name": "Erman Toroğlu",  "source": "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Erman Toroğlu"},
    {"id": "rahmi_turan",    "name": "Rahmi Turan",    "source": "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Rahmi Turan"},

    # ── Habertürk (RSS) ──────────────────────────────────────────────────────
    {"id": "murat_bardakci", "name": "Murat Bardakçı", "source": "rss", "rss": "https://www.haberturk.com/rss/kategori/yazarlar.xml", "match": "Murat Bardakçı"},

    # ── Hürriyet (Scrape) ────────────────────────────────────────────────────
    {"id": "ahmet_hakan",      "name": "Ahmet Hakan",      "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "abdulkadir_selvi", "name": "Abdülkadir Selvi", "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "osman_muftuoglu",  "name": "Osman Müftüoğlu",  "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "fatih_cekirge",    "name": "Fatih Çekirge",    "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "nedim_sener",      "name": "Nedim Şener",      "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},

    # ── Sabah (Scrape) ───────────────────────────────────────────────────────
    {"id": "ahmet_cakar",    "name": "Ahmet Çakar",    "source": "scrape_sabah", "scrape_url": "https://m.sabah.com.tr/yazarlar"},
    {"id": "gurcan_bilgic",  "name": "Gürcan Bilgiç",  "source": "scrape_sabah", "scrape_url": "https://m.sabah.com.tr/yazarlar"},
    {"id": "levent_tuzemen", "name": "Levent Tüzemen", "source": "scrape_sabah", "scrape_url": "https://m.sabah.com.tr/yazarlar"},
    {"id": "salih_tuna",     "name": "Salih Tuna",     "source": "scrape_sabah", "scrape_url": "https://m.sabah.com.tr/yazarlar"},

    # ── Fatih Altaylı ────────────────────────────────────────────────────────
    {"id": "fatih_altayli", "name": "Fatih Altaylı", "source": "scrape_altayli", "scrape_url": "https://fatihaltayli.com.tr/yazilar/fatih-altayli/kose-yazilari"},

    # ── 10haber ──────────────────────────────────────────────────────────────
    {"id": "ertugrul_ozkok", "name": "Ertuğrul Özkök", "source": "scrape_10haber", "scrape_url": "https://10haber.net/yazarlar/ertugrul-ozkok/"},

    # ── Karar ────────────────────────────────────────────────────────────────
    {"id": "ali_bayramoglu", "name": "Ali Bayramoğlu", "source": "scrape_karar", "scrape_url": "https://www.karar.com/yazarlar/ali-bayramoglu"},
    {"id": "taha_akyol",     "name": "Taha Akyol",     "source": "scrape_karar", "scrape_url": "https://www.karar.com/yazarlar/taha-akyol"},

    # ── T24 ──────────────────────────────────────────────────────────────────
    {"id": "cigdem_toker", "name": "Çiğdem Toker", "source": "scrape_t24", "scrape_url": "https://t24.com.tr/yazarlar/cigdem-toker"},

    # ── Cumhuriyet ───────────────────────────────────────────────────────────
    {"id": "emre_kongar", "name": "Emre Kongar", "source": "scrape_cumhuriyet", "scrape_url": "https://www.cumhuriyet.com.tr/yazarlar/emre-kongar"},

    # ── Mahfi Eğilmez ────────────────────────────────────────────────────────
    {"id": "mahfi_egilmez", "name": "Mahfi Eğilmez", "source": "scrape_mahfi", "scrape_url": "https://www.mahfiegilmez.com/"},

    # ── Fotomaç ──────────────────────────────────────────────────────────────
    {"id": "zeki_uzundurukan", "name": "Zeki Uzundurukan", "source": "scrape_fotomac", "scrape_url": "https://www.fotomac.com.tr/yazarlar/zeki_uzundurukan/arsiv"},
    {"id": "turgay_demir",     "name": "Turgay Demir",     "source": "scrape_fotomac", "scrape_url": "https://www.fotomac.com.tr/yazarlar/turgay_demir/arsiv"},

    # ── Star ─────────────────────────────────────────────────────────────────
    {"id": "huseyin_gulerce", "name": "Hüseyin Gülerce", "source": "scrape_star", "scrape_url": "https://m.star.com.tr/yazarlar/huseyin-gulerce/"},

    # ── Nefes ────────────────────────────────────────────────────────────────
    {"id": "deniz_zeyrek", "name": "Deniz Zeyrek", "source": "scrape_nefes", "scrape_url": "https://nefes.com.tr/yazarlar/deniz-zeyrek"},

    # ── HaberVakti ───────────────────────────────────────────────────────────
    {"id": "abdurrahman_dilipak", "name": "Abdurrahman Dilipak", "source": "scrape_habervakti", "scrape_url": "https://www.habervakti.com/abdurrahman-dilipak"},

    # ── Nihal Bengisu Karaca (Habertürk özel içerik sayfası) ─────────────────
    {"id": "nihal_bengisu_karaca", "name": "N. Bengisu Karaca", "source": "scrape_nihal", "scrape_url": "https://www.haberturk.com/ozel-icerikler/nihal-bengisu-karaca"},

    # ── Ali Karahasanoğlu (Yeni Akit) ────────────────────────────────────────
    {"id": "ali_karahasanoglu", "name": "Ali Karahasanoğlu", "source": "scrape_yeniakit", "scrape_url": "https://m.yeniakit.com.tr/yazarlar/ali-karahasanoglu"},

    # ── Milliyet ─────────────────────────────────────────────────────────────
    {"id": "ali_eyuboglu", "name": "Ali Eyüboğlu", "source": "scrape_milliyet", "scrape_url": "https://www.milliyet.com.tr/yazarlar/ali-eyuboglu/"},
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; K) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Mobile Safari/537.36"
    )
}


def fetch(url: str, timeout: int = 10) -> Optional[requests.Response]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception as e:
        log.warning(f"Fetch hatası [{url}]: {e}")
        return None


def url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def find_from_rss(author: dict) -> Optional[dict]:
    r = fetch(author["rss"])
    if not r:
        return None
    soup = BeautifulSoup(r.content, "xml")
    today = datetime.now(timezone.utc).date()
    for item in soup.find_all("item"):
        title_tag = item.find("title")
        if not title_tag or author["match"].lower() not in title_tag.text.lower():
            continue
        link_tag = item.find("link")
        pub_tag = item.find("pubDate")
        if not link_tag:
            continue
        if pub_tag:
            try:
                from email.utils import parsedate_to_datetime
                if parsedate_to_datetime(pub_tag.text).date() != today:
                    continue
            except Exception:
                pass
        desc = item.find("description") or title_tag
        return {"url": link_tag.text.strip(), "title": desc.text.strip()[:100]}
    return None


def find_from_hurriyet(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    for box in soup.select("a.author-box"):
        name_tag = box.select_one("span.name")
        if not name_tag or author["name"].lower() not in name_tag.text.lower():
            continue
        href = box.get("href", "")
        if not href:
            continue
        title_tag = box.select_one("span.title")
        url = href if href.startswith("http") else f"https://www.hurriyet.com.tr{href}"
        return {"url": url, "title": title_tag.text.strip() if title_tag else author["name"]}
    return None


def find_from_sabah(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    for li in soup.select("div.manset.writer ul li"):
        name_tag = li.select_one("strong:not(.sub)")
        if not name_tag or author["name"].lower() not in name_tag.text.lower():
            continue
        a_tag = li.find("a")
        if not a_tag:
            continue
        href = a_tag.get("href", "")
        url = href if href.startswith("http") else f"https://www.sabah.com.tr{href}"
        title_tag = li.select_one("strong.sub")
        return {"url": url, "title": title_tag.text.strip() if title_tag else author["name"]}
    return None


def find_from_altayli(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today_str = datetime.now(timezone.utc).date().strftime("%Y-%m-%d")
    for a in soup.select("a.blog-item"):
        href = a.get("href", "")
        if today_str not in href:
            continue
        url = href if href.startswith("http") else f"https://fatihaltayli.com.tr{href}"
        return {"url": url, "title": (a.get("title") or a.get_text(strip=True))[:100]}
    return None


def find_from_10haber(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    a = soup.select_one("article a, .post a, h2 a")
    if not a:
        return None
    href = a.get("href", "")
    url = href if href.startswith("http") else f"https://10haber.net{href}"
    return {"url": url, "title": a.get_text(strip=True)[:100]}


def find_from_karar(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    for article in soup.select("section.author-article article.item, article.item.box-shadow"):
        time_tag = article.find("time")
        if time_tag:
            dt_str = time_tag.get("datetime", "")
            if dt_str and dt_str[:10] != str(today):
                continue
        a_tag = article.find("a")
        h3 = article.find("h3")
        if not a_tag:
            continue
        href = a_tag.get("href", "")
        url = href if href.startswith("http") else f"https://www.karar.com{href}"
        return {"url": url, "title": h3.text.strip()[:100] if h3 else author["name"]}
    return None


def find_from_t24(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    for a in soup.select("section.aramakartalanimobil a[href]"):
        date_tag = a.select_one("div.aramakartalanimobilcardtarih")
        if date_tag and str(today.day) not in date_tag.text:
            continue
        h4 = a.select_one("h4, div.aramakartalanimobilcardbaslik")
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://t24.com.tr{href}"
        return {"url": url, "title": h4.text.strip()[:100] if h4 else author["name"]}
    return None


def find_from_cumhuriyet(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    container = soup.select_one("div#articles-container")
    if not container:
        return None
    for a in container.select("a[href]"):
        title_div = a.select_one("div.font-semibold, div.line-clamp-2")
        if not title_div:
            continue
        time_tag = a.find("time") or a.select_one("div.text-xs")
        if time_tag:
            date_text = time_tag.get("datetime", "") or time_tag.text
            if str(today) not in date_text and str(today.day) not in date_text:
                continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.cumhuriyet.com.tr{href}"
        return {"url": url, "title": title_div.text.strip()[:100]}
    return None


def find_from_mahfi(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    for article in soup.select("article.post"):
        date_tag = article.select_one("time, .post-date, abbr.published")
        if date_tag:
            date_text = date_tag.get("datetime", "") or date_tag.get("title", "") or date_tag.text
            if str(today.year) not in date_text:
                continue
        a = article.select_one("h3.post-title a")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.mahfiegilmez.com{href}"
        return {"url": url, "title": a.text.strip()[:100]}
    return None


def find_from_fotomac(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    for item in soup.select("div.archive-item"):
        date_tag = item.select_one("span.text-date, span.date")
        if date_tag and str(today.day) not in date_tag.text:
            continue
        a = item.find("a")
        h3 = item.find("h3", id="article-title") or item.find("h3")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.fotomac.com.tr{href}"
        return {"url": url, "title": h3.text.strip()[:100] if h3 else author["name"]}
    return None


def find_from_star(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    for li in soup.select("ul.main li"):
        date_div = li.select_one("div.date")
        if date_div and str(today.day) not in date_div.text:
            continue
        a = li.find("a")
        title_div = li.select_one("div.font-size-20")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://m.star.com.tr{href}"
        return {"url": url, "title": title_div.text.strip()[:100] if title_div else author["name"]}
    return None


def find_from_nefes(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    for article in soup.select("section.author-posts article.article-card"):
        time_tag = article.find("time")
        if time_tag and str(today.day) not in time_tag.text:
            continue
        a = article.find("a")
        title_span = article.select_one("span:not(.article-icon)")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://nefes.com.tr{href}"
        return {"url": url, "title": title_span.text.strip()[:100] if title_span else author["name"]}
    return None


def find_from_habervakti(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    for card in soup.select("div.card"):
        date_div = card.select_one("div.small.text-secondary")
        if date_div and "Bugün" not in date_div.text and str(today.day) not in date_div.text:
            continue
        a = card.select_one("h4.lead a")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.habervakti.com{href}"
        return {"url": url, "title": a.text.strip()[:100]}
    return None


def find_from_nihal(author: dict) -> Optional[dict]:
    """Habertürk özel içerik sayfası: div#infinite-data ul li h3 a[href]"""
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    container = soup.select_one("div#infinite-data, ul.articles-list")
    if not container:
        return None
    for li in container.select("li"):
        # Tarih: "Giriş: 2026-03-31" formatı
        date_p = li.select_one("p, span, div.date")
        if date_p and str(today) not in date_p.text and str(today.day) not in date_p.text:
            continue
        a = li.select_one("h3 a, h2 a")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.haberturk.com{href}"
        return {"url": url, "title": a.text.strip()[:100]}
    return None


def find_from_yeniakit(author: dict) -> Optional[dict]:
    """Yeni Akit: section.article a[href] + time[datetime]"""
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    for section in soup.select("section.article"):
        time_tag = section.select_one("time[datetime]")
        if time_tag:
            dt = time_tag.get("datetime", "")
            if dt[:10] != str(today):
                continue
        a = section.find("a")
        h1 = section.select_one("h1.title")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://m.yeniakit.com.tr{href}"
        return {"url": url, "title": h1.text.strip()[:100] if h1 else author["name"]}
    return None


def find_from_milliyet(author: dict) -> Optional[dict]:
    """Milliyet: div.box-preview h2.box-preview__title a + span.box-preview__date"""
    r = fetch(author["scrape_url"])
    if not r:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(timezone.utc).date()
    # Türkçe ay adları
    TR_MONTHS = {
        "Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4,
        "Mayıs": 5, "Haziran": 6, "Temmuz": 7, "Ağustos": 8,
        "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12
    }
    for box in soup.select("div.box-preview"):
        date_span = box.select_one("span.box-preview__date")
        if date_span:
            try:
                parts = date_span.text.strip().split()  # ["31", "Mart", "2026"]
                if len(parts) == 3:
                    day, month_tr, year = int(parts[0]), parts[1], int(parts[2])
                    month = TR_MONTHS.get(month_tr, 0)
                    from datetime import date as date_type
                    if date_type(year, month, day) != today:
                        continue
            except Exception:
                pass
        a = box.select_one("h2.box-preview__title a, a.box-preview__link")
        if not a:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.milliyet.com.tr{href}"
        return {"url": url, "title": a.text.strip()[:100]}
    return None


FINDERS = {
    "rss":               find_from_rss,
    "scrape_hurriyet":   find_from_hurriyet,
    "scrape_sabah":      find_from_sabah,
    "scrape_altayli":    find_from_altayli,
    "scrape_10haber":    find_from_10haber,
    "scrape_karar":      find_from_karar,
    "scrape_t24":        find_from_t24,
    "scrape_cumhuriyet": find_from_cumhuriyet,
    "scrape_mahfi":      find_from_mahfi,
    "scrape_fotomac":    find_from_fotomac,
    "scrape_star":       find_from_star,
    "scrape_nefes":      find_from_nefes,
    "scrape_habervakti": find_from_habervakti,
    "scrape_nihal":      find_from_nihal,
    "scrape_yeniakit":   find_from_yeniakit,
    "scrape_milliyet":   find_from_milliyet,
}


def main():
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    if not cred_json:
        raise EnvironmentError("FIREBASE_CREDENTIALS environment variable eksik!")

    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    sent_ref = db.collection("sentArticles")
    favorites_ref = db.collection("userFavorites")

    for author in AUTHORS:
        log.info(f"Kontrol ediliyor: {author['name']}")
        try:
            finder = FINDERS.get(author["source"])
            if not finder:
                log.warning(f"  → Finder yok: {author['source']}")
                continue

            article = finder(author)
            if not article:
                log.info(f"  → Bugün makale yok.")
                continue

            log.info(f"  → Makale bulundu: {article['url']}")

            article_id = url_hash(article["url"])
            if sent_ref.document(article_id).get().exists:
                log.info(f"  → Zaten gönderildi.")
                continue

            users = favorites_ref.where("favoriteAuthorIds", "array_contains", author["id"]).stream()
            tokens = [doc.id for doc in users]

            if not tokens:
                log.info(f"  → Favorileyen kullanıcı yok.")
                sent_ref.document(article_id).set({
                    "url": article["url"],
                    "authorId": author["id"],
                    "sentAt": firestore.SERVER_TIMESTAMP,
                })
                continue

            log.info(f"  → {len(tokens)} kullanıcıya gönderiliyor...")
            success_count = 0

            for i in range(0, len(tokens), 500):
                batch = tokens[i:i + 500]
                msg = messaging.MulticastMessage(
                    tokens=batch,
                    notification=messaging.Notification(title=author["name"], body=article["title"]),
                    data={"url": article["url"]},
                    android=messaging.AndroidConfig(
                        priority="high",
                        notification=messaging.AndroidNotification(sound="default"),
                    ),
                    apns=messaging.APNSConfig(
                        payload=messaging.APNSPayload(aps=messaging.Aps(sound="default")),
                    ),
                )
                resp = messaging.send_each_for_multicast(msg)
                success_count += resp.success_count

                for idx, r in enumerate(resp.responses):
                    if not r.success:
                        code = r.exception.code if r.exception else ""
                        if code in (
                            "messaging/registration-token-not-registered",
                            "messaging/invalid-registration-token",
                        ):
                            favorites_ref.document(batch[idx]).delete()
                            log.info(f"  → Bozuk token silindi.")

            log.info(f"  → Başarılı: {success_count}/{len(tokens)}")
            sent_ref.document(article_id).set({
                "url": article["url"],
                "authorId": author["id"],
                "authorName": author["name"],
                "sentAt": firestore.SERVER_TIMESTAMP,
            })

        except Exception as e:
            log.error(f"❌ {author['name']} hatası: {e}")
            continue

    log.info("✅ Tamamlandı.")


if __name__ == "__main__":
    main()