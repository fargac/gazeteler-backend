# Ortak Regex Kuralları (SonarQube S1192 Best Practice Çözümü - Raw Strings)
RULE_ITEM_STD = r"<item[\s\S]*?>([\s\S]*?)<\/item>"
RULE_TITLE_STD = r"<title[\s\S]*?>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/title>"
RULE_LINK_STD = r"<link>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/link>"
RULE_DATE_STD = r"<pubDate[^>]*>([\s\S]*?)<\/pubDate>"

RULE_IMAGE_ENCLOSURE = r"<enclosure[^>]+url=[\"'](.*?)[\"']"
RULE_IMAGE_MEDIA = r"<media:content[^>]+url=[\"'](.*?)[\"']"

NEWS_SOURCES = [
    {
        "id": "fenerbahce",
        "name": "Fenerbahçe",
        "rss": "https://www.fotomac.com.tr/rss/fenerbahce.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "cnnturk",
        "name": "CNN Türk",
        "rss": "https://www.cnnturk.com/feed/rss/all/news",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": r"<image>([\s\S]*?)<\/image>", # Sadece CNN Türk'e özel
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "besiktas",
        "name": "Beşiktaş",
        "rss": "https://www.fotomac.com.tr/rss/besiktas.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "galatasaray",
        "name": "Galatasaray",
        "rss": "https://www.fotomac.com.tr/rss/galatasaray.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "trabzonspor",
        "name": "Trabzonspor",
        "rss": "https://www.fotomac.com.tr/rss/trabzonspor.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "hurriyet",
        "name": "Hürriyet",
        "rss": "https://www.hurriyet.com.tr/rss/anasayfa",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "sozcu",
        "name": "Sözcü",
        "rss": "https://www.sozcu.com.tr/feeds-son-dakika",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "sabah",
        "name": "Sabah",
        "rss": "https://www.sabah.com.tr/rss/anasayfa.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "milliyet",
        "name": "Milliyet",
        "rss": "https://www.milliyet.com.tr/rss/rssnew/sondakikarss.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": r"url=[\"'](https?:\/\/.*?\.(?:jpg|jpeg|png|webp|gif|bmp).*?)[\"']", # Sadece Milliyet'e özel
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "haberturk",
        "name": "Habertürk",
        "rss": "https://www.haberturk.com/rss/manset.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "ensonhaber",
        "name": "En Son Haber",
        "rss": "https://www.ensonhaber.com/rss/ensonhaber.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "mynet",
        "name": "Mynet",
        "rss": "https://www.mynet.com/haber/rss/sondakika",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": r"<img640x360>(.*?)<\/img640x360>", # Sadece Mynet'e özel
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "sondakika",
        "name": "Son Dakika",
        "rss": "https://rss.sondakika.com/rss_standart.asp",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "ntvspor",
        "name": "NTV Spor",
        "rss": "https://www.ntvspor.net/rss/anasayfa",
        "rules": {
            "item": r"<entry[\s\S]*?>([\s\S]*?)<\/entry>", # Sadece NTV Spor'a özel
            "title": RULE_TITLE_STD,
            "link": r"<(?:atom:)?link[^>]+href=[\"'](.*?)[\"']", # Sadece NTV Spor'a özel
            "image": RULE_IMAGE_ENCLOSURE,
            "date": r"<published[^>]*>([\s\S]*?)<\/published>" # Sadece NTV Spor'a özel
        }
    },
    {
        "id": "fotomac",
        "name": "Fotomaç",
        "rss": "https://www.fotomac.com.tr/rss/son24saat.xml",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    },
    {
        "id": "ekonomim",
        "name": "Ekonomim",
        "rss": "https://www.ekonomim.com/rss",
        "rules": {
            "item": RULE_ITEM_STD,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "date": RULE_DATE_STD
        }
    }
]