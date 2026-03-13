# data/haber_kaynaklari.py

# 🌟 fast-xml-parser (JSON Dönüşüm) Kuralları
RULE_ITEM_RSS = "item"
RULE_ITEM_ATOM = "entry"

RULE_TITLE_STD = "title"
RULE_LINK_STD = "link"

RULE_IMAGE_ENCLOSURE = "enclosure"
RULE_IMAGE_MEDIA = "media:content"

RULE_DATE_PUBDATE = "pubDate"
RULE_DATE_PUBLISHED = "published"

# Tarih Formatı Sabitleri
DATE_FORMAT_STD = "ddd, DD MMM YYYY HH:mm:ss ZZ"
DATE_FORMAT_GMT = "ddd, DD MMM YYYY HH:mm:ss [GMT]"

NEWS_SOURCES = [
    {
        "id": "fenerbahce",
        "name": "Fenerbahçe",
        "rss": "https://www.fotomac.com.tr/rss/fenerbahce.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "cnnturk",
        "name": "CNN Türk",
        "rss": "https://www.cnnturk.com/feed/rss/all/news",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": "image", # CNN Türk özel JSON node'u
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_GMT
        }
    },
    {
        "id": "besiktas",
        "name": "Beşiktaş",
        "rss": "https://www.fotomac.com.tr/rss/besiktas.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "galatasaray",
        "name": "Galatasaray",
        "rss": "https://www.fotomac.com.tr/rss/galatasaray.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "trabzonspor",
        "name": "Trabzonspor",
        "rss": "https://www.fotomac.com.tr/rss/trabzonspor.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "hurriyet",
        "name": "Hürriyet",
        "rss": "https://www.hurriyet.com.tr/rss/anasayfa",
        "maxItems": 16,
        "excludeCategories": ["Resmi İlanlar", "Advertorial","Lezizz","Kelebek","Spor Arena","Aile"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_GMT
        }
    },
    {
        "id": "sozcu",
        "name": "Sözcü",
        "rss": "https://www.sozcu.com.tr/feeds-son-dakika",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "sabah",
        "name": "Sabah",
        "rss": "https://www.sabah.com.tr/rss/gundem.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial","Yaşam"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "milliyet",
        "name": "Milliyet",
        "rss": "https://www.milliyet.com.tr/rss/rssnew/sondakikarss.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": "atom:link",
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": "ddd, DD MMM YYYY HH:mm:ss  Z" 
        }
    },
    {
        "id": "haberturk",
        "name": "Habertürk",
        "rss": "https://www.haberturk.com/rss/manset.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_GMT
        }
    },
    {
        "id": "ensonhaber",
        "name": "En Son Haber",
        "rss": "https://www.ensonhaber.com/rss/gundem.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial","3. Sayfa","Magazin","Otomobil","Yaşam","Futbol","Medya"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "mynet",
        "name": "Mynet",
        "rss": "https://www.mynet.com/haber/rss/sondakika",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": "img640x360", # Mynet'e özel JSON etiketi
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": "ddd, DD MMM YY HH:mm:ss ZZ" 
        }
    },
    {
        "id": "sondakika",
        "name": "Son Dakika",
        "rss": "https://rss.sondakika.com/rss_standart.asp",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_MEDIA,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "ntvspor",
        "name": "NTV Spor",
        "rss": "https://www.ntvspor.net/rss/anasayfa",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_ATOM, # Atom feed yapısı
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBLISHED, 
            "dateFormat": "YYYY-MM-DDTHH:mm:ssZ" 
        }
    },
    {
        "id": "fotomac",
        "name": "Fotomaç",
        "rss": "https://www.fotomac.com.tr/rss/son24saat.xml",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    },
    {
        "id": "ekonomim",
        "name": "Ekonomim",
        "rss": "https://www.ekonomim.com/rss",
        "maxItems": 15,
        "excludeCategories": ["Resmi İlanlar", "Advertorial"],
        "rules": {
            "item": RULE_ITEM_RSS,
            "title": RULE_TITLE_STD,
            "link": RULE_LINK_STD,
            "image": RULE_IMAGE_ENCLOSURE,
            "dateTag": RULE_DATE_PUBDATE,
            "dateFormat": DATE_FORMAT_STD
        }
    }
]