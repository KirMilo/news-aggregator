from datetime import timezone, timedelta

UTC_PLUS_3 = timezone(timedelta(hours=3))
PARSING_INTERVAL_MINUTES = 10
DB_SERVICE_URL = "http://localhost:8000"
RESOURCES_ENDPOINT_GET = "/api/v1/news/sources/"
CREATE_NEWS_ENDPOINT_POST = "/api/v1/news/create/"
