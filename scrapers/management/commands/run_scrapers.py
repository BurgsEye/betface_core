from django.core.management.base import BaseCommand
from scrapers.scaper_logic.dratings import scrape_dratings
from scrapers.scaper_logic.dunkel import scrape_dunkel
from scrapers.scaper_logic.betfirm import scrape_betfirm
from scrapers.scaper_logic.wunderdog import scrape_wunderdog
from scrapers.scaper_logic.pickwise import scrape_pickwise
from scrapers.scaper_logic.covers import scrape_covers
from scrapers.models import ScraperLog
from datetime import datetime

from shared.utils import ModelDoesNotExistError

from api.tips.serializers import TipSerializer


class Command(BaseCommand):
    help = "Run the scrapers"

    def run_scraper(self, scraper_func, scraper_name, scraper_time):
        
        print(f"Scraping {scraper_name} tips...")
        ScraperLog.objects.create(scraper_name=scraper_name, scraper_start_time =scraper_time, error_level="INFO", scraper_message="Start scraping tips...")
        try:
            tips = scraper_func()
        except Exception as e:
            print(f"{scraper_name} scraper failed")
            print(e)
            return
        
        for tip in tips:
            try:
                serializer = TipSerializer(data=tip)
                if serializer.is_valid():
                    serializer.save()
                    print(f"Saved {scraper_name} tip: {tip['game']}")
                else:
                    print(serializer.errors)
            except ModelDoesNotExistError as e:
                if e.model_name == "Game":
                    ScraperLog.objects.create(scraper_name=scraper_name, scraper_start_time =scraper_time, error_level="ERROR", scraper_message=str(e))

                elif e.model_name == "Team":
                    ScraperLog.objects.create(scraper_name=scraper_name, scraper_start_time =scraper_time, error_level="WARNING", scraper_message=str(e))
                else:
                    ScraperLog.objects.create(scraper_name=scraper_name, scraper_start_time =scraper_time, error_level="ERROR", scraper_message=str(e)) 
            except Exception as e:
                ScraperLog.objects.create(scraper_name=scraper_name, scraper_start_time =scraper_time, error_level="ERROR", scraper_message=str(e))
                print(f"{scraper_name} tip not valid", end=' ')
                print(e, tip)
        
        ScraperLog.objects.create(scraper_name=scraper_name, scraper_start_time =scraper_time, error_level="INFO", scraper_message="Finished scraping tips...") 

    def handle(self, *args, **options):
        scraper_time = datetime.now()
        self.run_scraper(scrape_covers, "Covers",scraper_time)
        self.run_scraper(scrape_dratings, "Dratings",scraper_time)
        self.run_scraper(scrape_dunkel, "Dunkel",scraper_time)
        self.run_scraper(scrape_betfirm, "Betfirm",scraper_time)
        
        self.run_scraper(scrape_pickwise, "Pickwise",scraper_time)
        self.run_scraper(scrape_wunderdog, "Wunderdog",scraper_time)
        
