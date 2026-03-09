NEWS_SOURCES = [
    {
        "id": "fenerbahce",
        "name": "Fenerbahçe",
        "rss": "https://www.fotomac.com.tr/rss/fenerbahce.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "cnnturk",
        "name": "CNN Türk",
        "rss": "https://www.cnnturk.com/feed/rss/all/news",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<image>([\\s\\S]*?)<\\/image>",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "besiktas",
        "name": "Beşiktaş",
        "rss": "https://www.fotomac.com.tr/rss/besiktas.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "galatasaray",
        "name": "Galatasaray",
        "rss": "https://www.fotomac.com.tr/rss/galatasaray.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "trabzonspor",
        "name": "Trabzonspor",
        "rss": "https://www.fotomac.com.tr/rss/trabzonspor.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "hurriyet",
        "name": "Hürriyet",
        "rss": "https://www.hurriyet.com.tr/rss/anasayfa",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "sozcu",
        "name": "Sözcü",
        "rss": "https://www.sozcu.com.tr/feeds-son-dakika",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<media:content[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "sabah",
        "name": "Sabah",
        "rss": "https://www.sabah.com.tr/rss/anasayfa.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "milliyet",
        "name": "Milliyet",
        "rss": "https://www.milliyet.com.tr/rss/rssnew/sondakikarss.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "url=[\"'](https?:\\/\\/.*?\\.(?:jpg|jpeg|png|webp|gif|bmp).*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "haberturk",
        "name": "Habertürk",
        "rss": "https://www.haberturk.com/rss/manset.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "ensonhaber",
        "name": "En Son Haber",
        "rss": "https://www.ensonhaber.com/rss/ensonhaber.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<media:content[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "mynet",
        "name": "Mynet",
        "rss": "https://www.mynet.com/haber/rss/sondakika",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<img640x360>(.*?)<\\/img640x360>",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "sondakika",
        "name": "Son Dakika",
        "rss": "https://rss.sondakika.com/rss_standart.asp",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<media:content[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "ntvspor",
        "name": "NTV Spor",
        "rss": "https://www.ntvspor.net/rss/anasayfa",
        "rules": {
            "item": "<entry[\\s\\S]*?>([\\s\\S]*?)<\\/entry>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<(?:atom:)?link[^>]+href=[\"'](.*?)[\"']",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<published[^>]*>([\\s\\S]*?)<\\/published>"
        }
    },
    {
        "id": "fotomac",
        "name": "Fotomaç",
        "rss": "https://www.fotomac.com.tr/rss/son24saat.xml",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    },
    {
        "id": "ekonomim",
        "name": "Ekonomim",
        "rss": "https://www.ekonomim.com/rss",
        "rules": {
            "item": "<item[\\s\\S]*?>([\\s\\S]*?)<\\/item>",
            "title": "<title[\\s\\S]*?>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/title>",
            "link": "<link>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/link>",
            "image": "<enclosure[^>]+url=[\"'](.*?)[\"']",
            "date": "<pubDate[^>]*>([\\s\\S]*?)<\\/pubDate>"
        }
    }
]