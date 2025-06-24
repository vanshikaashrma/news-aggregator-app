# app.py
from flask import Flask, render_template, request
from scraper.scraper import get_all_news
from utils.summarize import process_news_articles
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_all_news, 'interval', hours=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

start_scheduler()

@app.route('/')
def index():
    query = request.args.get('q', '')
    try:
        articles = get_all_news()
        articles = process_news_articles(articles, search=query)
    except Exception as e:
        print(f"❌ Error processing articles: {e}")
        articles = []
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
