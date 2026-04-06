"""
Yazar Bildirim Sistemi v5.0 (Gerçek Thread-Safe & LXML Edition)
- thundering herd problemi Event'ler ile çözüldü.
- lxml entegrasyonu ile CPU darboğazı giderildi.
"""

import os
import json
import hashlib
import logging
import smtplib
import threading
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta, date as date_type
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore, messaging
from firebase_admin.exceptions import AlreadyExistsError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

TR_TZ = timezone(timedelta(hours=3))
TARGET_EMAIL = "fargac@gmail.com"

# 🔥 GERÇEK THREAD-SAFE CACHE YÖNETİMİ
FETCH_EVENTS: dict = {}
FETCH_RESULTS: dict = {}
_cache_lock = threading.Lock()

KEY_ID, KEY_NAME, KEY_SOURCE, KEY_SCRAPE_URL, KEY_URL, KEY_TITLE = "id", "name", "source", "scrape_url", "url", "title"

AUTHORS = [
    # ── Sözcü (RSS) ──────────────────────────────────────────────────────────
    {KEY_ID: "yilmaz_ozdil",   KEY_NAME: "Yılmaz Özdil",   KEY_SOURCE: "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Yılmaz Özdil"},
    {KEY_ID: "emin_colasan",   KEY_NAME: "Emin Çölaşan",   KEY_SOURCE: "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Emin Çölaşan"},
    {KEY_ID: "soner_yalcin",   KEY_NAME: "Soner Yalçın",   KEY_SOURCE: "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Soner Yalçın"},
    {KEY_ID: "ismail_saymaz",  KEY_NAME: "İsmail Saymaz",  KEY_SOURCE: "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "İsmail Saymaz"},
    {KEY_ID: "erman_toroglu",  KEY_NAME: "Erman Toroğlu",  KEY_SOURCE: "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Erman Toroğlu"},
    {KEY_ID: "rahmi_turan",    KEY_NAME: "Rahmi Turan",    KEY_SOURCE: "rss", "rss": "https://www.sozcu.com.tr/feeds-rss-category-yazar", "match": "Rahmi Turan"},

    # ── Habertürk (RSS) ──────────────────────────────────────────────────────
    {KEY_ID: "murat_bardakci", KEY_NAME: "Murat Bardakçı", KEY_SOURCE: "rss", "rss": "https://www.haberturk.com/rss/kategori/yazarlar.xml", "match": "Murat Bardakçı"},

    # ── Diğer Siteler (Scrape) ───────────────────────────────────────────────
    {KEY_ID: "ahmet_hakan",      KEY_NAME: "Ahmet Hakan",      KEY_SOURCE: "scrape_hurriyet", KEY_SCRAPE_URL: "https://www.hurriyet.com.tr/yazarlar/"},
    {KEY_ID: "abdulkadir_selvi", KEY_NAME: "Abdülkadir Selvi", KEY_SOURCE: "scrape_hurriyet", KEY_SCRAPE_URL: "https://www.hurriyet.com.tr/yazarlar/"},
    {KEY_ID: "osman_muftuoglu",  KEY_NAME: "Osman Müftüoğlu",  KEY_SOURCE: "scrape_hurriyet", KEY_SCRAPE_URL: "https://www.hurriyet.com.tr/yazarlar/"},
    {KEY_ID: "fatih_cekirge",    KEY_NAME: "Fatih Çekirge",    KEY_SOURCE: "scrape_hurriyet", KEY_SCRAPE_URL: "https://www.hurriyet.com.tr/yazarlar/"},
    {KEY_ID: "nedim_sener",      KEY_NAME: "Nedim Şener",      KEY_SOURCE: "scrape_hurriyet", KEY_SCRAPE_URL: "https://www.hurriyet.com.tr/yazarlar/"},
    {KEY_ID: "ahmet_cakar",      KEY_NAME: "Ahmet Çakar",      KEY_SOURCE: "scrape_sabah", KEY_SCRAPE_URL: "https://m.sabah.com.tr/yazarlar"},
    {KEY_ID: "gurcan_bilgic",    KEY_NAME: "Gürcan Bilgiç",    KEY_SOURCE: "scrape_sabah", KEY_SCRAPE_URL: "https://m.sabah.com.tr/yazarlar"},
    {KEY_ID: "levent_tuzemen",   KEY_NAME: "Levent Tüzemen",   KEY_SOURCE: "scrape_sabah", KEY_SCRAPE_URL: "https://m.sabah.com.tr/yazarlar"},
    {KEY_ID: "salih_tuna",       KEY_NAME: "Salih Tuna",       KEY_SOURCE: "scrape_sabah", KEY_SCRAPE_URL: "https://m.sabah.com.tr/yazarlar"},
    {KEY_ID: "fatih_altayli",    KEY_NAME: "Fatih Altaylı",    KEY_SOURCE: "scrape_altayli", KEY_SCRAPE_URL: "https://fatihaltayli.com.tr/yazilar/fatih-altayli/kose-yazilari"},
    {KEY_ID: "ertugrul_ozkok",   KEY_NAME: "Ertuğrul Özkök",   KEY_SOURCE: "scrape_10haber", KEY_SCRAPE_URL: "https://10haber.net/yazarlar/ertugrul-ozkok/"},
    {KEY_ID: "ali_bayramoglu",   KEY_NAME: "Ali Bayramoğlu",   KEY_SOURCE: "scrape_karar", KEY_SCRAPE_URL: "https://www.karar.com/yazarlar/ali-bayramoglu"},
    {KEY_ID: "taha_akyol",       KEY_NAME: "Taha Akyol",       KEY_SOURCE: "scrape_karar", KEY_SCRAPE_URL: "https://www.karar.com/yazarlar/taha-akyol"},
    {KEY_ID: "cigdem_toker",     KEY_NAME: "Çiğdem Toker",     KEY_SOURCE: "scrape_t24", KEY_SCRAPE_URL: "https://t24.com.tr/yazarlar/cigdem-toker"},
    {KEY_ID: "emre_kongar",      KEY_NAME: "Emre Kongar",      KEY_SOURCE: "scrape_cumhuriyet", KEY_SCRAPE_URL: "https://www.cumhuriyet.com.tr/yazarlar/emre-kongar"},
    {KEY_ID: "mahfi_egilmez",    KEY_NAME: "Mahfi Eğilmez",    KEY_SOURCE: "scrape_mahfi", KEY_SCRAPE_URL: "https://www.mahfiegilmez.com/"},
    {KEY_ID: "zeki_uzundurukan", KEY_NAME: "Zeki Uzundurukan", KEY_SOURCE: "scrape_fotomac", KEY_SCRAPE_URL: "https://www.fotomac.com.tr/yazarlar/zeki_uzundurukan/arsiv"},
    {KEY_ID: "turgay_demir",     KEY_NAME: "Turgay Demir",     KEY_SOURCE: "scrape_fotomac", KEY_SCRAPE_URL: "https://www.fotomac.com.tr/yazarlar/turgay_demir/arsiv"},
    {KEY_ID: "huseyin_gulerce",  KEY_NAME: "Hüseyin Gülerce",  KEY_SOURCE: "scrape_star", KEY_SCRAPE_URL: "https://m.star.com.tr/yazarlar/huseyin-gulerce/"},
    {KEY_ID: "deniz_zeyrek",     KEY_NAME: "Deniz Zeyrek",     KEY_SOURCE: "scrape_nefes", KEY_SCRAPE_URL: "https://nefes.com.tr/yazarlar/deniz-zeyrek"},
    {KEY_ID: "abdurrahman_dilipak", KEY_NAME: "Abdurrahman Dilipak", KEY_SOURCE: "scrape_habervakti", KEY_SCRAPE_URL: "https://www.habervakti.com/abdurrahman-dilipak"},
    {KEY_ID: "nihal_bengisu_karaca", KEY_NAME: "N. Bengisu Karaca", KEY_SOURCE: "scrape_nihal", KEY_SCRAPE_URL: "https://www.haberturk.com/ozel-icerikler/nihal-bengisu-karaca"},
    {KEY_ID: "ali_karahasanoglu", KEY_NAME: "Ali Karahasanoğlu", KEY_SOURCE: "scrape_yeniakit", KEY_SCRAPE_URL: "https://m.yeniakit.com.tr/yazarlar/ali-karahasanoglu"},
    {KEY_ID: "ali_eyuboglu",     KEY_NAME: "Ali Eyüboğlu",     KEY_SOURCE: "scrape_milliyet", KEY_SCRAPE_URL: "https://www.milliyet.com.tr/yazarlar/ali-eyuboglu/"},
]

# --- AĞ VE OTURUM YAPILANDIRMASI ---
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"}

secure_session = requests.Session()
secure_session.headers.update(HEADERS)
retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["HEAD", "GET"])
secure_session.mount("http://", HTTPAdapter(max_retries=retry_strategy, pool_connections=15, pool_maxsize=15))
secure_session.mount("https://", HTTPAdapter(max_retries=retry_strategy, pool_connections=15, pool_maxsize=15))

# ─────────────────────────────────────────────────────────────────────────────
# YARDIMCI (HELPER) FONKSİYONLAR
# ─────────────────────────────────────────────────────────────────────────────

def get_soup(url: str, is_xml: bool = False) -> BeautifulSoup:
    """
    URL'yi çeker ve parse edilmiş Soup objesini döner.
    Event/Kilit mekanizması ile tam Thread-Safe (Kurumsal Seviye).
    """
    with _cache_lock:
        # Eğer sonuç zaten varsa dön
        if url in FETCH_RESULTS:
            return FETCH_RESULTS[url]

        # Sonuç yoksa ve kimse şu an çekmiyorsa, Event oluştur ve görevi sen al
        if url not in FETCH_EVENTS:
            FETCH_EVENTS[url] = threading.Event()
            needs_fetch = True
        else:
            needs_fetch = False

    if needs_fetch:
        try:
            r = secure_session.get(url, timeout=15)
            r.raise_for_status()
            
            # 🔥 PERFORMANS: lxml parser, html.parser'a göre 5-10 kat daha hızlıdır
            parser_type = "xml" if is_xml else "lxml"
            soup = BeautifulSoup(r.content if is_xml else r.text, parser_type)
            
            with _cache_lock:
                FETCH_RESULTS[url] = soup
        finally:
            # İşlem bittiğinde (başarılı/hata) bekleyen diğer thread'leri serbest bırak
            with _cache_lock:
                FETCH_EVENTS[url].set()
    else:
        # Başka bir thread çekiyor, onun bitirmesini bekle
        FETCH_EVENTS[url].wait()

    return FETCH_RESULTS.get(url)


def build_url(href: str, base_domain: str) -> str:
    """Bağıl (relative) linkleri tam (absolute) linke çevirir."""
    if not href:
        return ""
    return href if href.startswith("http") else f"{base_domain.rstrip('/')}/{href.lstrip('/')}"


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]


def send_error_email(author_name: str, error_message: str):
    msg_user, msg_pass = os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS")
    if not msg_user or not msg_pass:
        return

    msg = MIMEText(f"Sistem {author_name} için veri çekerken hata aldı.\n\nDetay:\n{error_message}", "plain", "utf-8")
    msg['Subject'], msg['From'], msg['To'] = f"⚠️ Yazar Sistemi Hatası: {author_name}", msg_user, TARGET_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(msg_user, msg_pass)
            server.sendmail(msg_user, TARGET_EMAIL, msg.as_string())
    except smtplib.SMTPException as e:
        log.error(f"❌ E-posta gönderme başarısız: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# ÖZEL SCRAPER FONKSİYONLARI
# ─────────────────────────────────────────────────────────────────────────────

def find_from_rss(author: dict) -> Optional[dict]:
    soup = get_soup(author["rss"], is_xml=True)
    if not soup: return None
    today = datetime.now(TR_TZ).date()

    for item in soup.find_all("item"):
        title_tag = item.find("title")
        if not title_tag or author["match"].lower() not in title_tag.text.lower():
            continue

        link_tag = item.find("link")
        if not link_tag:
            continue

        pub_tag = item.find("pubDate")
        if pub_tag:
            try:
                from email.utils import parsedate_to_datetime
                if parsedate_to_datetime(pub_tag.text).astimezone(TR_TZ).date() != today:
                    continue
            except (ValueError, TypeError):
                continue

        desc = item.find("description") or title_tag
        return {KEY_URL: link_tag.text.strip(), KEY_TITLE: desc.text.strip()[:100]}
    return None


def find_from_hurriyet(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    for box in soup.select("a.author-box"):
        name_tag = box.select_one("span.name")
        if not name_tag or author[KEY_NAME].lower() not in name_tag.text.lower():
            continue

        href = box.get("href", "")
        if not href:
            continue

        title_tag = box.select_one("span.title")
        return {KEY_URL: build_url(href, "https://www.hurriyet.com.tr"), KEY_TITLE: title_tag.text.strip() if title_tag else author[KEY_NAME]}
    return None


def find_from_sabah(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    for li in soup.select("div.manset.writer ul li"):
        name_tag = li.select_one("strong:not(.sub)")
        if not name_tag or author[KEY_NAME].lower() not in name_tag.text.lower():
            continue

        a_tag = li.find("a")
        if not a_tag:
            continue

        title_tag = li.select_one("strong.sub")
        return {KEY_URL: build_url(a_tag.get("href", ""), "https://www.sabah.com.tr"), KEY_TITLE: title_tag.text.strip() if title_tag else author[KEY_NAME]}
    return None


def find_from_altayli(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_str = datetime.now(TR_TZ).date().strftime("%Y-%m-%d")

    for a in soup.select("a.blog-item"):
        href = a.get("href", "")
        if today_str not in href:
            continue
        return {KEY_URL: build_url(href, "https://fatihaltayli.com.tr"), KEY_TITLE: (a.get("title") or a.get_text(strip=True))[:100]}
    return None


def find_from_10haber(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    a = soup.select_one("article a, .post a, h2 a")
    if not a:
        return None
    return {KEY_URL: build_url(a.get("href", ""), "https://10haber.net"), KEY_TITLE: a.get_text(strip=True)[:100]}


def find_from_karar(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_str = str(datetime.now(TR_TZ).date())

    for article in soup.select("section.author-article article.item, article.item.box-shadow"):
        time_tag = article.find("time")
        if time_tag and time_tag.get("datetime", "")[:10] != today_str:
            continue

        a_tag = article.find("a")
        if not a_tag:
            continue

        h3 = article.find("h3")
        return {KEY_URL: build_url(a_tag.get("href", ""), "https://www.karar.com"), KEY_TITLE: h3.text.strip()[:100] if h3 else author[KEY_NAME]}
    return None


def find_from_t24(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_day_str = str(datetime.now(TR_TZ).date().day)

    for a in soup.select("section.aramakartalanimobil a[href]"):
        date_tag = a.select_one("div.aramakartalanimobilcardtarih")
        if date_tag and today_day_str not in date_tag.text:
            continue

        h4 = a.select_one("h4, div.aramakartalanimobilcardbaslik")
        return {KEY_URL: build_url(a.get("href", ""), "https://t24.com.tr"), KEY_TITLE: h4.text.strip()[:100] if h4 else author[KEY_NAME]}
    return None


def find_from_cumhuriyet(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today = datetime.now(TR_TZ).date()
    today_str, today_day_str = str(today), str(today.day)

    for a in soup.select("div#articles-container a[href]"):
        title_div = a.select_one("div.font-semibold, div.line-clamp-2")
        if not title_div:
            continue

        time_tag = a.find("time") or a.select_one("div.text-xs")
        if time_tag:
            date_text = time_tag.get("datetime", "") or time_tag.text
            if today_str not in date_text and today_day_str not in date_text:
                continue

        return {KEY_URL: build_url(a.get("href", ""), "https://www.cumhuriyet.com.tr"), KEY_TITLE: title_div.text.strip()[:100]}
    return None


def find_from_mahfi(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_year_str = str(datetime.now(TR_TZ).date().year)

    for article in soup.select("article.post"):
        date_tag = article.select_one("time, .post-date, abbr.published")
        if date_tag and today_year_str not in (date_tag.get("datetime", "") or date_tag.get("title", "") or date_tag.text):
            continue

        a = article.select_one("h3.post-title a")
        if not a:
            continue

        return {KEY_URL: build_url(a.get("href", ""), "https://www.mahfiegilmez.com"), KEY_TITLE: a.text.strip()[:100]}
    return None


def find_from_fotomac(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_day_str = str(datetime.now(TR_TZ).date().day)

    for item in soup.select("div.archive-item"):
        date_tag = item.select_one("span.text-date, span.date")
        if date_tag and today_day_str not in date_tag.text:
            continue

        a, h3 = item.find("a"), (item.find("h3", id="article-title") or item.find("h3"))
        if not a:
            continue

        return {KEY_URL: build_url(a.get("href", ""), "https://www.fotomac.com.tr"), KEY_TITLE: h3.text.strip()[:100] if h3 else author[KEY_NAME]}
    return None


def find_from_star(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_day_str = str(datetime.now(TR_TZ).date().day)

    for li in soup.select("ul.main li"):
        date_div = li.select_one("div.date")
        if date_div and today_day_str not in date_div.text:
            continue

        a, title_div = li.find("a"), li.select_one("div.font-size-20")
        if not a:
            continue

        return {KEY_URL: build_url(a.get("href", ""), "https://m.star.com.tr"), KEY_TITLE: title_div.text.strip()[:100] if title_div else author[KEY_NAME]}
    return None


def find_from_nefes(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_day_str = str(datetime.now(TR_TZ).date().day)

    for article in soup.select("section.author-posts article.article-card"):
        time_tag = article.find("time")
        if time_tag and today_day_str not in time_tag.text:
            continue

        a, title_span = article.find("a"), article.select_one("span:not(.article-icon)")
        if not a:
            continue

        return {KEY_URL: build_url(a.get("href", ""), "https://nefes.com.tr"), KEY_TITLE: title_span.text.strip()[:100] if title_span else author[KEY_NAME]}
    return None


def find_from_habervakti(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_day_str = str(datetime.now(TR_TZ).date().day)

    for card in soup.select("div.card"):
        date_div = card.select_one("div.small.text-secondary")
        if date_div and "Bugün" not in date_div.text and today_day_str not in date_div.text:
            continue

        a = card.select_one("h4.lead a")
        if not a:
            continue

        return {KEY_URL: build_url(a.get("href", ""), "https://www.habervakti.com"), KEY_TITLE: a.text.strip()[:100]}
    return None


def find_from_nihal(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today = datetime.now(TR_TZ).date()
    today_str, today_day_str = str(today), str(today.day)

    for li in soup.select("div#infinite-data li, ul.articles-list li"):
        date_p = li.select_one("p, span, div.date")
        if date_p and today_str not in date_p.text and today_day_str not in date_p.text:
            continue

        a = li.select_one("h3 a, h2 a")
        if not a:
            continue

        return {KEY_URL: build_url(a.get("href", ""), "https://www.haberturk.com"), KEY_TITLE: a.text.strip()[:100]}
    return None


def find_from_yeniakit(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today_str = str(datetime.now(TR_TZ).date())

    for section in soup.select("section.article"):
        time_tag = section.select_one("time[datetime]")
        if time_tag and time_tag.get("datetime", "")[:10] != today_str:
            continue

        a, h1 = section.find("a"), section.select_one("h1.title")
        if not a:
            continue

        return {KEY_URL: build_url(a.get("href", ""), "https://m.yeniakit.com.tr"), KEY_TITLE: h1.text.strip()[:100] if h1 else author[KEY_NAME]}
    return None


def find_from_milliyet(author: dict) -> Optional[dict]:
    soup = get_soup(author[KEY_SCRAPE_URL])
    if not soup: return None
    today = datetime.now(TR_TZ).date()
    TR_MONTHS = {"Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4, "Mayıs": 5, "Haziran": 6, "Temmuz": 7, "Ağustos": 8, "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12}

    for box in soup.select("div.box-preview"):
        date_span = box.select_one("span.box-preview__date")
        if date_span:
            try:
                parts = date_span.text.strip().split()
                if len(parts) == 3:
                    if date_type(int(parts[2]), TR_MONTHS.get(parts[1], 0), int(parts[0])) != today:
                        continue
            except (ValueError, TypeError, IndexError):
                pass

        a = box.select_one("h2.box-preview__title a, a.box-preview__link")
        if not a:
            continue

        return {KEY_URL: build_url(a.get("href", ""), "https://www.milliyet.com.tr"), KEY_TITLE: a.text.strip()[:100]}
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

# ─────────────────────────────────────────────────────────────────────────────
# ANA İŞLEYİŞ
# ─────────────────────────────────────────────────────────────────────────────

def process_author(author: dict, sent_ref):
    log.info(f"🔍 Kontrol ediliyor: {author[KEY_NAME]}")
    try:
        finder = FINDERS.get(author[KEY_SOURCE])
        if not finder:
            return log.warning(f"  → Finder yok: {author[KEY_SOURCE]}")

        article = finder(author)
        if not article:
            return log.info(f"  → {author[KEY_NAME]}: Bugün makale yok.")

        article_id = url_hash(article[KEY_URL])
        doc_ref = sent_ref.document(article_id)

        if doc_ref.get().exists:
            return log.info(f"  → {author[KEY_NAME]}: Zaten gönderildi.")

        topic_name = f"yazar_{author[KEY_ID]}"
        log.info(f"  → {author[KEY_NAME]}: '{topic_name}' konusuna mesaj atılıyor...")

        msg = messaging.Message(
            notification=messaging.Notification(title=author[KEY_NAME], body=article[KEY_TITLE]),
            data={"url": article[KEY_URL]},
            topic=topic_name,
            android=messaging.AndroidConfig(priority="high", notification=messaging.AndroidNotification(sound="default")),
            apns=messaging.APNSConfig(payload=messaging.APNSPayload(aps=messaging.Aps(sound="default"))),
        )

        resp = messaging.send(msg)
        log.info(f"  → Başarılı (Message ID): {resp}")

        try:
            doc_ref.create({
                "url": article[KEY_URL],
                "authorId": author[KEY_ID],
                "authorName": author[KEY_NAME],
                "sentAt": firestore.SERVER_TIMESTAMP
            })
        except AlreadyExistsError:
            pass

    except requests.exceptions.RequestException as ce:
        log.error(f"❌ {author[KEY_NAME]} Ağ Hatası: {ce}")
        send_error_email(author[KEY_NAME], f"Ağ/Timeout Hatası: {str(ce)}")
    except Exception as e:
        log.error(f"❌ {author[KEY_NAME]} Parse/Beklenmeyen Hata: {e}")
        send_error_email(author[KEY_NAME], f"Sistem/Parse Hatası: {str(e)}")


def main():
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    if not cred_json:
        raise EnvironmentError("FIREBASE_CREDENTIALS environment variable eksik!")

    firebase_admin.initialize_app(credentials.Certificate(json.loads(cred_json)))
    sent_ref = firestore.client().collection("sentArticles")

    log.info("🚀 Enterprise Tarama başlatılıyor... (max_workers=10)")

    # Threading işlemi bittikten sonra açık portları temizlemek için 
    # session işlemlerini sarmalıyoruz.
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_author, author, sent_ref) for author in AUTHORS]
        for f in futures:
            try:
                f.result()
            except Exception as e:
                log.error(f"Kritik Thread Hatası: {e}")
                
    # Memory Leak Önlemi: Dangling (Askıda kalmış) socketleri temizle
    secure_session.close()

    log.info("✅ Tüm işlemler güvenle tamamlandı.")


if __name__ == "__main__":
    main()