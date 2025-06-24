import feedparser
from newspaper import Article
from utils.sentiment import analyze_sentiment
import threading

# 📰 RSS feed sources
FEED_SOURCES = [
    ("http://feeds.bbci.co.uk/news/rss.xml", "BBC"),
    ("https://www.thehindu.com/feeder/default.rss", "The Hindu"),
    ("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "NYT"),
    ("http://rss.cnn.com/rss/edition.rss", "CNN"),
    ("https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "TOI"),
]

# 🚫 Skip collection pages, live updates, etc.
BLOCKED_KEYWORDS = ['live-news', 'webview', '/collections/', '/videos/', '/live/']

# ✅ Check if article URL is valid
def is_valid_article(url):
    return url and not any(block in url for block in BLOCKED_KEYWORDS)

# 🔄 Fetch and clean articles from RSS feed
def fetch_feed(url, source):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        if hasattr(entry, 'title') and hasattr(entry, 'link') and is_valid_article(entry.link):
            articles.append({
                "title": entry.title,
                "url": entry.link.split('?')[0],  # Clean URL
                "source": source
            })
    return articles

# 🧠 Add summary & sentiment
def enrich_article(article):
    try:
        news = Article(article['url'])
        news.download()
        news.parse()

        article['text'] = news.text
        article['summary'] = news.title if news.title else "No summary available"
        article['sentiment'] = analyze_sentiment(news.text)
        return article
    except Exception as e:
        print(f"❌ Error processing article: {article['url']}\n{e}")
        return None

# ⚡ Multi-threaded processing for speed
def process_articles_multithreaded(articles):
    final_articles = []

    def worker(article):
        enriched = enrich_article(article)
        if enriched:
            final_articles.append(enriched)

    threads = []
    for article in articles:
        t = threading.Thread(target=worker, args=(article,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return final_articles

# 🔗 Main entry point
def get_all_news():
    all_articles = []
    for url, source in FEED_SOURCES:
        articles = fetch_feed(url, source)
        print(f"✅ {source} articles fetched: {len(articles)}")
        all_articles.extend(articles)

    return all_articles
