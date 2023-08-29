from django.contrib import admin
from .models import ScraperLog
# Register your models here.


class ScraperLogAdmin(admin.ModelAdmin):
    list_display = ('scraper_name', 'scraper_start_time', 'error_level', 'scraper_message')
    list_filter = ('scraper_name', 'scraper_start_time', 'error_level')
    search_fields = ('scraper_name', 'scraper_start_time', 'error_level')

admin.site.register(ScraperLog, ScraperLogAdmin)