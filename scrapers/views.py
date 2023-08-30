from django.shortcuts import render
from django.views.generic.list import ListView
from .models import ScraperLog
# Create your views here.


class LatestLogs(ListView):
    model = ScraperLog
    template_name = 'scrapers/latest_logs.html'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self):
        # Get the most recent scraper_start_time
        latest_time = ScraperLog.objects.latest('scraper_start_time').scraper_start_time

        # Get all logs with that start time
        logs_with_latest_time = ScraperLog.objects.filter(scraper_start_time=latest_time)

        # Print each log
        for log in logs_with_latest_time:
            print(log)

        return ScraperLog.objects.all().order_by('-scraper_start_time')
    
    def get_logs():
        # Get the most recent scraper_start_time
        latest_time = ScraperLog.objects.latest('scraper_start_time').scraper_start_time

        # Get all logs with that start time
        logs_with_latest_time = ScraperLog.objects.filter(scraper_start_time=latest_time)

        logs_by_scraper = {}
        for log in logs_with_latest_time:
            if log.scraper_name not in logs_by_scraper:
                logs_by_scraper[log.scraper_name] = []
            if log.error_level == "ERROR" or log.error_level == "WARNING":
                # print(log.scraper_message)
                logs_by_scraper[log.scraper_name].append(log.scraper_message)
            
    

        return logs_by_scraper
    



