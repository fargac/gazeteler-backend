"""
Yazar Bildirim Sistemi v3.0 (Hybrid Enterprise Edition - Full Scrapers)
GitHub Actions ile her sabah 07:00'de çalışır.
"""

import os
import json
import hashlib
import logging
import smtplib
import time
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore, messaging
from firebase_admin.exceptions import AlreadyExistsError

# Log ayarları
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Türkiye Saat Dilimi (UTC+3) - Timezone Bug'ı çözümü
TR_TZ = timezone(timedelta(hours=3))

TARGET_EMAIL = "fargac@gmail.com"

# RSS ve URL İstekleri için Global Cache
FETCH_CACHE = {}

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

    # ── Diğer Siteler (Scrape) ───────────────────────────────────────────────
    {"id": "ahmet_hakan",      "name": "Ahmet Hakan",      "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "abdulkadir_selvi", "name": "Abdülkadir Selvi", "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "osman_muftuoglu",  "name": "Osman Müftüoğlu",  "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "fatih_cekirge",    "name": "Fatih Çekirge",    "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "nedim_sener",      "name": "Nedim Şener",      "source": "scrape_hurriyet", "scrape_url": "https://www.hurriyet.com.tr/yazarlar/"},
    {"id": "ahmet_cakar",      "name": "Ahmet Çakar",      "source": "scrape_sabah", "scrape_url": "https://m.sabah.com.tr/yazarlar"},
    {"id": "gurcan_bilgic",    "name": "Gürcan Bilgiç",    "source": "scrape_sabah", "scrape_url": "https://m.sabah.com.tr/yazarlar"},
    {"id": "levent_tuzemen",   "name": "Levent Tüzemen",   "source": "scrape_sabah", "scrape_url": "https://m.sabah.com.tr/yazarlar"},
    {"id": "salih_tuna",       "name": "Salih Tuna",       "source": "scrape_sabah", "scrape_url": "https://m.sabah.com.tr/yazarlar"},
    {"id": "fatih_altayli",    "name": "Fatih Altaylı",    "source": "scrape_altayli", "scrape_url": "https://fatihaltayli.com.tr/yazilar/fatih-altayli/kose-yazilari"},
    {"id": "ertugrul_ozkok",   "name": "Ertuğrul Özkök",   "source": "scrape_10haber", "scrape_url": "https://10haber.net/yazarlar/ertugrul-ozkok/"},
    {"id": "ali_bayramoglu",   "name": "Ali Bayramoğlu",   "source": "scrape_karar", "scrape_url": "https://www.karar.com/yazarlar/ali-bayramoglu"},
    {"id": "taha_akyol",       "name": "Taha Akyol",       "source": "scrape_karar", "scrape_url": "https://www.karar.com/yazarlar/taha-akyol"},
    {"id": "cigdem_toker",     "name": "Çiğdem Toker",     "source": "scrape_t24", "scrape_url": "https://t24.com.tr/yazarlar/cigdem-toker"},
    {"id": "emre_kongar",      "name": "Emre Kongar",      "source": "scrape_cumhuriyet", "scrape_url": "https://www.cumhuriyet.com.tr/yazarlar/emre-kongar"},
    {"id": "mahfi_egilmez",    "name": "Mahfi Eğilmez",    "source": "scrape_mahfi", "scrape_url": "https://www.mahfiegilmez.com/"},
    {"id": "zeki_uzundurukan", "name": "Zeki Uzundurukan", "source": "scrape_fotomac", "scrape_url": "https://www.fotomac.com.tr/yazarlar/zeki_uzundurukan/arsiv"},
    {"id": "turgay_demir",     "name": "Turgay Demir",     "source": "scrape_fotomac", "scrape_url": "https://www.fotomac.com.tr/yazarlar/turgay_demir/arsiv"},
    {"id": "huseyin_gulerce",  "name": "Hüseyin Gülerce",  "source": "scrape_star", "scrape_url": "https://m.star.com.tr/yazarlar/huseyin-gulerce/"},
    {"id": "deniz_zeyrek",     "name": "Deniz Zeyrek",     "source": "scrape_nefes", "scrape_url": "https://nefes.com.tr/yazarlar/deniz-zeyrek"},
    {"id": "abdurrahman_dilipak", "name": "Abdurrahman Dilipak", "source": "scrape_habervakti", "scrape_url": "https://www.habervakti.com/abdurrahman-dilipak"},
    {"id": "nihal_bengisu_karaca", "name": "N. Bengisu Karaca", "source": "scrape_nihal", "scrape_url": "https://www.haberturk.com/ozel-icerikler/nihal-bengisu-karaca"},
    {"id": "ali_karahasanoglu","name": "Ali Karahasanoğlu", "source": "scrape_yeniakit", "scrape_url": "https://m.yeniakit.com.tr/yazarlar/ali-karahasanoglu"},
    {"id": "ali_eyuboglu",     "name": "Ali Eyüboğlu",     "source": "scrape_milliyet", "scrape_url": "https://www.milliyet.com.tr/yazarlar/ali-eyuboglu/"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def send_error_email(author_name: str, error_message: str):
    msg_user = os.environ.get("EMAIL_USER")
    msg_pass = os.environ.get("EMAIL_PASS")

    if not msg_user or not msg_pass:
        log.error("E-posta yetkileri eksik (EMAIL_USER/EMAIL_PASS). Bildirim atılamadı.")
        return

    subject = f"⚠️ Yazar Sistemi Hatası: {author_name}"
    body = f"Sistem {author_name} için veri çekerken hata aldı.\n\nDetay:\n{error_message}\n\nSite yapısı değişmiş veya erişim engeli (403/Timeout) yaşanmış olabilir."
    
    msg = MIMEText(body, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = msg_user
    msg['To'] = TARGET_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(msg_user, msg_pass)
            server.sendmail(msg_user, TARGET_EMAIL, msg.as_string())
        log.info(f"📧 Hata bildirimi {TARGET_EMAIL} adresine gönderildi.")
    except Exception as e:
        log.error(f"❌ E-posta gönderme başarısız: {e}")

def fetch(url: str, timeout: int = 15, retries: int = 3) -> Optional[requests.Response]:
    if url in FETCH_CACHE:
        return FETCH_CACHE[url]

    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
            FETCH_CACHE[url] = r
            return r
        except requests.exceptions.RequestException as e:
            log.warning(f"⚠️ Retry {i+1}/{retries} [{url}] Hata: {e}")
            time.sleep(2)
            
    raise ConnectionError(f"URL'ye ulaşılamadı (Max retries aşıldı): {url}")

def url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

# ─────────────────────────────────────────────────────────────────────────────
# ÖZEL SCRAPER FONKSİYONLARI (Hepsi TR Timezone Uyumlu)
# ─────────────────────────────────────────────────────────────────────────────

def find_from_rss(author: dict) -> Optional[dict]:
    r = fetch(author["rss"])
    soup = BeautifulSoup(r.content, "xml")
    today = datetime.now(TR_TZ).date()
    for item in soup.find_all("item"):
        title_tag = item.find("title")
        if not title_tag or author["match"].lower() not in title_tag.text.lower():
            continue
        link_tag = item.find("link")
        pub_tag = item.find("pubDate")
        if not link_tag: continue
        if pub_tag:
            try:
                from email.utils import parsedate_to_datetime
                pub_date = parsedate_to_datetime(pub_tag.text).astimezone(TR_TZ).date()
                if pub_date != today: continue
            except Exception:
                pass
        desc = item.find("description") or title_tag
        return {"url": link_tag.text.strip(), "title": desc.text.strip()[:100]}
    return None

def find_from_hurriyet(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    for box in soup.select("a.author-box"):
        name_tag = box.select_one("span.name")
        if not name_tag or author["name"].lower() not in name_tag.text.lower(): continue
        href = box.get("href", "")
        if not href: continue
        title_tag = box.select_one("span.title")
        url = href if href.startswith("http") else f"https://www.hurriyet.com.tr{href}"
        return {"url": url, "title": title_tag.text.strip() if title_tag else author["name"]}
    return None

def find_from_sabah(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    for li in soup.select("div.manset.writer ul li"):
        name_tag = li.select_one("strong:not(.sub)")
        if not name_tag or author["name"].lower() not in name_tag.text.lower(): continue
        a_tag = li.find("a")
        if not a_tag: continue
        href = a_tag.get("href", "")
        url = href if href.startswith("http") else f"https://www.sabah.com.tr{href}"
        title_tag = li.select_one("strong.sub")
        return {"url": url, "title": title_tag.text.strip() if title_tag else author["name"]}
    return None

def find_from_altayli(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today_str = datetime.now(TR_TZ).date().strftime("%Y-%m-%d")
    for a in soup.select("a.blog-item"):
        href = a.get("href", "")
        if today_str not in href: continue
        url = href if href.startswith("http") else f"https://fatihaltayli.com.tr{href}"
        return {"url": url, "title": (a.get("title") or a.get_text(strip=True))[:100]}
    return None

def find_from_10haber(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    a = soup.select_one("article a, .post a, h2 a")
    if not a: return None
    href = a.get("href", "")
    url = href if href.startswith("http") else f"https://10haber.net{href}"
    return {"url": url, "title": a.get_text(strip=True)[:100]}

def find_from_karar(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    for article in soup.select("section.author-article article.item, article.item.box-shadow"):
        time_tag = article.find("time")
        if time_tag:
            dt_str = time_tag.get("datetime", "")
            if dt_str and dt_str[:10] != str(today): continue
        a_tag = article.find("a")
        h3 = article.find("h3")
        if not a_tag: continue
        href = a_tag.get("href", "")
        url = href if href.startswith("http") else f"https://www.karar.com{href}"
        return {"url": url, "title": h3.text.strip()[:100] if h3 else author["name"]}
    return None

def find_from_t24(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    for a in soup.select("section.aramakartalanimobil a[href]"):
        date_tag = a.select_one("div.aramakartalanimobilcardtarih")
        if date_tag and str(today.day) not in date_tag.text: continue
        h4 = a.select_one("h4, div.aramakartalanimobilcardbaslik")
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://t24.com.tr{href}"
        return {"url": url, "title": h4.text.strip()[:100] if h4 else author["name"]}
    return None

def find_from_cumhuriyet(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    container = soup.select_one("div#articles-container")
    if not container: return None
    for a in container.select("a[href]"):
        title_div = a.select_one("div.font-semibold, div.line-clamp-2")
        if not title_div: continue
        time_tag = a.find("time") or a.select_one("div.text-xs")
        if time_tag:
            date_text = time_tag.get("datetime", "") or time_tag.text
            if str(today) not in date_text and str(today.day) not in date_text: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.cumhuriyet.com.tr{href}"
        return {"url": url, "title": title_div.text.strip()[:100]}
    return None

def find_from_mahfi(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    for article in soup.select("article.post"):
        date_tag = article.select_one("time, .post-date, abbr.published")
        if date_tag:
            date_text = date_tag.get("datetime", "") or date_tag.get("title", "") or date_tag.text
            if str(today.year) not in date_text: continue
        a = article.select_one("h3.post-title a")
        if not a: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.mahfiegilmez.com{href}"
        return {"url": url, "title": a.text.strip()[:100]}
    return None

def find_from_fotomac(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    for item in soup.select("div.archive-item"):
        date_tag = item.select_one("span.text-date, span.date")
        if date_tag and str(today.day) not in date_tag.text: continue
        a = item.find("a")
        h3 = item.find("h3", id="article-title") or item.find("h3")
        if not a: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.fotomac.com.tr{href}"
        return {"url": url, "title": h3.text.strip()[:100] if h3 else author["name"]}
    return None

def find_from_star(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    for li in soup.select("ul.main li"):
        date_div = li.select_one("div.date")
        if date_div and str(today.day) not in date_div.text: continue
        a = li.find("a")
        title_div = li.select_one("div.font-size-20")
        if not a: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://m.star.com.tr{href}"
        return {"url": url, "title": title_div.text.strip()[:100] if title_div else author["name"]}
    return None

def find_from_nefes(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    for article in soup.select("section.author-posts article.article-card"):
        time_tag = article.find("time")
        if time_tag and str(today.day) not in time_tag.text: continue
        a = article.find("a")
        title_span = article.select_one("span:not(.article-icon)")
        if not a: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://nefes.com.tr{href}"
        return {"url": url, "title": title_span.text.strip()[:100] if title_span else author["name"]}
    return None

def find_from_habervakti(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    for card in soup.select("div.card"):
        date_div = card.select_one("div.small.text-secondary")
        if date_div and "Bugün" not in date_div.text and str(today.day) not in date_div.text: continue
        a = card.select_one("h4.lead a")
        if not a: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.habervakti.com{href}"
        return {"url": url, "title": a.text.strip()[:100]}
    return None

def find_from_nihal(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    container = soup.select_one("div#infinite-data, ul.articles-list")
    if not container: return None
    for li in container.select("li"):
        date_p = li.select_one("p, span, div.date")
        if date_p and str(today) not in date_p.text and str(today.day) not in date_p.text: continue
        a = li.select_one("h3 a, h2 a")
        if not a: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.haberturk.com{href}"
        return {"url": url, "title": a.text.strip()[:100]}
    return None

def find_from_yeniakit(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    for section in soup.select("section.article"):
        time_tag = section.select_one("time[datetime]")
        if time_tag:
            dt = time_tag.get("datetime", "")
            if dt[:10] != str(today): continue
        a = section.find("a")
        h1 = section.select_one("h1.title")
        if not a: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://m.yeniakit.com.tr{href}"
        return {"url": url, "title": h1.text.strip()[:100] if h1 else author["name"]}
    return None

def find_from_milliyet(author: dict) -> Optional[dict]:
    r = fetch(author["scrape_url"])
    soup = BeautifulSoup(r.text, "html.parser")
    today = datetime.now(TR_TZ).date()
    TR_MONTHS = {"Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4, "Mayıs": 5, "Haziran": 6, "Temmuz": 7, "Ağustos": 8, "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12}
    for box in soup.select("div.box-preview"):
        date_span = box.select_one("span.box-preview__date")
        if date_span:
            try:
                parts = date_span.text.strip().split()
                if len(parts) == 3:
                    day, month_tr, year = int(parts[0]), parts[1], int(parts[2])
                    month = TR_MONTHS.get(month_tr, 0)
                    from datetime import date as date_type
                    if date_type(year, month, day) != today: continue
            except Exception: pass
        a = box.select_one("h2.box-preview__title a, a.box-preview__link")
        if not a: continue
        href = a.get("href", "")
        url = href if href.startswith("http") else f"https://www.milliyet.com.tr{href}"
        return {"url": url, "title": a.text.strip()[:100]}
    return None

def safe_scrape(finder_func, author: dict):
    try:
        return finder_func(author)
    except Exception as e:
        raise ValueError(f"Scraper hatası veya DOM kırıldı: {str(e)}")

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

# ─────────────────────────────────────────────────────────────────────────────
# ANA İŞLEYİŞ (HİBRİT MİMARİ - SIFIR FIRESTORE READ)
# ─────────────────────────────────────────────────────────────────────────────

def process_author(author: dict, sent_ref):
    """Tek bir yazarı işleyen paralel thread fonksiyonu."""
    log.info(f"🔍 Kontrol ediliyor: {author['name']}")
    try:
        finder = FINDERS.get(author["source"])
        if not finder:
            log.warning(f"  → Finder yok: {author['source']}")
            return

        article = safe_scrape(finder, author)
        if not article:
            log.info(f"  → {author['name']}: Bugün makale yok.")
            return

        article_id = url_hash(article["url"])
        doc_ref = sent_ref.document(article_id)

        # 1. ATOMIC DUPLICATE KONTROL (Race Condition Koruması)
        if doc_ref.get().exists:
            log.info(f"  → {author['name']}: Zaten gönderildi.")
            return

        # 🚀 2. HİBRİT MİMARİ ZİRVESİ: Firestore'dan okuma YOK!
        topic_name = f"yazar_{author['id']}"
        log.info(f"  → {author['name']}: '{topic_name}' konusuna (Topic) mesaj atılıyor...")

        msg = messaging.Message(
            notification=messaging.Notification(title=author["name"], body=article["title"]),
            data={"url": article["url"]},
            topic=topic_name,
            android=messaging.AndroidConfig(priority="high", notification=messaging.AndroidNotification(sound="default")),
            apns=messaging.APNSConfig(payload=messaging.APNSPayload(aps=messaging.Aps(sound="default"))),
        )

        resp = messaging.send(msg)
        log.info(f"  → Başarılı (Message ID): {resp}")
        
        try:
            doc_ref.create({
                "url": article["url"],
                "authorId": author["id"],
                "authorName": author["name"],
                "sentAt": firestore.SERVER_TIMESTAMP,
            })
        except AlreadyExistsError:
            pass 

    except ConnectionError as ce:
        log.error(f"❌ {author['name']} Ağ Hatası: {ce}")
        send_error_email(author["name"], f"Ağ/Timeout Hatası: {str(ce)}")
        
    except ValueError as ve:
        log.error(f"❌ {author['name']} DOM/Parse Hatası: {ve}")
        send_error_email(author["name"], f"HTML Kırılması/Değişiklik: {str(ve)}")
        
    except Exception as e:
        log.error(f"❌ {author['name']} Beklenmeyen Hata: {e}")
        send_error_email(author["name"], f"Beklenmeyen Sistem Hatası: {str(e)}")

def main():
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    if not cred_json:
        raise EnvironmentError("FIREBASE_CREDENTIALS environment variable eksik!")

    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    sent_ref = db.collection("sentArticles")

    log.info("🚀 Enterprise Tarama başlatılıyor... (max_workers=10)")
    
    futures = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for author in AUTHORS:
            futures.append(executor.submit(process_author, author, sent_ref))

    for f in futures:
        try:
            f.result() 
        except Exception as e:
            log.error(f"Kritik Thread Hatası: {e}")

    log.info("✅ Tüm işlemler güvenle tamamlandı.")

if __name__ == "__main__":
    main()