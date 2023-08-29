from django.core.management.base import BaseCommand
from scrapers.scaper_logic.dratings import scrape_dratings
from scrapers.scaper_logic.dunkel import scrape_dunkel
from scrapers.scaper_logic.betfirm import scrape_betfirm
from scrapers.scaper_logic.wunderdog import scrape_wunderdog
from scrapers.scaper_logic.pickwise import scrape_pickwise
from scrapers.scaper_logic.covers import scrape_covers

from api.tips.serializers import TipSerializer


class Command(BaseCommand):
    help = "Run the scrapers"

    def run_scraper(self, scraper_func, scraper_name):
        print(f"Scraping {scraper_name} tips...")
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
            except Exception as e:
                print(f"{scraper_name} tip not valid", end=' ')
                print(e, tip)

    def handle(self, *args, **options):

        self.run_scraper(scrape_dratings, "Dratings")
        self.run_scraper(scrape_dunkel, "Dunkel")
        self.run_scraper(scrape_betfirm, "Betfirm")
        
        self.run_scraper(scrape_pickwise, "Pickwise")
        self.run_scraper(scrape_wunderdog, "Wunderdog")
        self.run_scraper(scrape_covers, "Covers")
