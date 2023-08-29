from django.db import models

# Create your models here.


class ScraperLog(models.Model):
    scraper_name = models.CharField(max_length=255)
    scraper_start_time = models.DateTimeField()
    error_level = models.CharField(max_length=255, blank=True, null=True)
    scraper_message = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.scraper_name} - {self.scraper_start_time} - {self.error_level} - {self.scraper_message}"