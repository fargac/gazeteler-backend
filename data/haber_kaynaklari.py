# data/haber_kaynaklari.py

# Ortak Regex Kuralları
RULE_ITEM_STD = r"<item[\s\S]*?>([\s\S]*?)<\/item>"
RULE_TITLE_STD = r"<title[\s\S]*?>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/title>"
RULE_LINK_STD = r"<link>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/link>"

RULE_IMAGE_ENCLOSURE = r"<enclosure[^>]+url=[\"'](.*?)[\"']"
RULE_IMAGE_MEDIA = r"<media:content[^>]+url=[\"'](.*?)[\"']"

# 🌟 SonarQube S1192 Çözümü: Tarih Formatı Sabitleri
DATE_FORMAT_STD = "ddd, DD MMM YYYY HH:mm:ss ZZ"
DATE_FORMAT_GMT = "ddd, DD MMM YYYY HH:mm:ss [GMT]"

NEWS_SOURCES = [
    {
        "id": "fenerbahce",
        "name": "Fenerbahçe",
        "rss": "https://www.fotomac.com.tr/rss/fenerbahce.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "cnnturk",
        "name": "CNN Türk",
        "rss": "https://www.cnnturk.com/feed/rss/all/news",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": r"<image>([\s\S]*?)<\/image>",
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_GMT
        }
    },
    {
        "id": "besiktas",
        "name": "Beşiktaş",
        "rss": "https://www.fotomac.com.tr/rss/besiktas.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "galatasaray",
        "name": "Galatasaray",
        "rss": "https://www.fotomac.com.tr/rss/galatasaray.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "trabzonspor",
        "name": "Trabzonspor",
        "rss": "https://www.fotomac.com.tr/rss/trabzonspor.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "hurriyet",
        "name": "Hürriyet",
        "rss": "https://www.hurriyet.com.tr/rss/anasayfa",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_GMT
        }
    },
    {
        "id": "sozcu",
        "name": "Sözcü",
        "rss": "https://www.sozcu.com.tr/feeds-son-dakika",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "sabah",
        "name": "Sabah",
        "rss": "https://www.sabah.com.tr/rss/anasayfa.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "milliyet",
        "name": "Milliyet",
        "rss": "https://www.milliyet.com.tr/rss/rssnew/sondakikarss.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": r"url=[\"'](https?:\/\/.*?\.(?:jpg|jpeg|png|webp|gif|bmp).*?)[\"']",
            "dateTag": "pubDate",
            "dateFormat": "ddd, DD MMM YYYY HH:mm:ss  Z" # Kendine has olduğu için sabitlenmedi
        }
    },
    {
        "id": "haberturk",
        "name": "Habertürk",
        "rss": "https://www.haberturk.com/rss/manset.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_GMT
        }
    },
    {
        "id": "ensonhaber",
        "name": "En Son Haber",
        "rss": "https://www.ensonhaber.com/rss/ensonhaber.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "mynet",
        "name": "Mynet",
        "rss": "https://www.mynet.com/haber/rss/sondakika",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": r"<img640x360>(.*?)<\/img640x360>",
            "dateTag": "pubDate",
            "dateFormat": "ddd, DD MMM YY HH:mm:ss ZZ" # Kendine has olduğu için sabitlenmedi
        }
    },
    {
        "id": "sondakika",
        "name": "Son Dakika",
        "rss": "https://rss.sondakika.com/rss_standart.asp",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "ntvspor",
        "name": "NTV Spor",
        "rss": "https://www.ntvspor.net/rss/anasayfa",
        "maxItems": 15,
        "rules": {
            "item": r"<entry[\s\S]*?>([\s\S]*?)<\/entry>",
            "title": RULE_TITLE_STD,
            "link": r"<(?:atom:)?link[^>]+href=[\"'](.*?)[\"']",
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "published",
            "dateFormat": "YYYY-MM-DDTHH:mm:ssZ" # Kendine has olduğu için sabitlenmedi
        }
    },
    {
        "id": "fotomac",
        "name": "Fotomaç",
        "rss": "https://www.fotomac.com.tr/rss/son24saat.xml",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "ekonomim",
        "name": "Ekonomim",
        "rss": "https://www.ekonomim.com/rss",
        "maxItems": 15,
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": "pubDate",
            "dateFormat": DATE_FORMAT_STD
        }
    }
]