# utils/summarize.py
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor
from utils.sentiment import analyze_sentiment

def summarize_and_analyze(article):
    try:
        url = article.get('url')
        if not url:
            return None

        art = Article(url)
        art.download()
        art.parse()
        art.nlp()

        text = art.text.strip()
        summary = art.summary.strip()

        if not text or not summary:
            print(f"⏭️ Skipping URL: {url}\n⚠️ Reason: Article text too short or empty")
            return None

        article['summary'] = summary
        article['sentiment'] = analyze_sentiment(text)
        return article

    except Exception as e:
        print(f"❌ Error summarizing {article.get('url')}: {e}")
        return None

def process_news_articles(articles, search=None):
    # 🔍 Filter articles if a search query is given
    if search:
        search_lower = search.lower()
        articles = [a for a in articles if search_lower in a['title'].lower()]

    # 🧵 Use ThreadPoolExecutor to summarize and analyze in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(summarize_and_analyze, articles))

    final_articles = [r for r in results if r]
    print(f"✅ Total final articles: {len(final_articles)}")
    return final_articles

