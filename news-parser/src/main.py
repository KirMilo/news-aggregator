# from celery import Celery
# from celery.schedules import crontab
#
# from src.constants import PARSING_INTERVAL_MINUTES
# from src.news_parser import NewsParser
#
# app = Celery("main")
#
# app.conf.beat_schedule = {
#     "parsing": {
#         "task": "tasks.main",
#         "schedule": crontab(minute=f"*/{PARSING_INTERVAL_MINUTES}"),
#     }
# }
#
#
# def start_parsing_news():
#     news_parser = NewsParser()
#     news_parser.parse()
#     news_parser.create_news()
#
#
# @app.task
# def main():
#     start_parsing_news()


if __name__ == "__main__":
    from src.news_parser import NewsParser

    news_parser = NewsParser()
    news_parser.parse()
    news_parser.create_news()
