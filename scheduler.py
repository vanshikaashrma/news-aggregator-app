from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scraper

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scraper.get_all_news, 'interval', hours=1)
    scheduler.start()
