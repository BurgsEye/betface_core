from django.core.management.base import BaseCommand
from scrapers.scaper_logic.dratings import scrape_dratings
from scrapers.scaper_logic.dunkel import scrape_dunkel
from scrapers.scaper_logic.betfirm import scrape_betfirm
from scrapers.scaper_logic.wunderdog import scrape_wunderdog
from scrapers.scaper_logic.pickwise import scrape_pickwise

from api.tips.serializers import TipSerializer


class Command(BaseCommand):
    help = "Run the scrapers"

    def run_scraper(self, scraper_func, scraper_name):
        print(f"Scraping {scraper_name} tips...")
        tips = scraper_func()
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

        # print("Scraping Drating tips...")
        # tips = scrape_dratings()
        # for tip in tips:
        #     serializer = TipSerializer(data=tip)
        #     if serializer.is_valid():
        #         serializer.save()
        #         print("Saved Drating tip: {}".format(tip['game']))
        #     else:
        #         print(serializer.errors)

        # print("Scraping Dunkel tips...")
        # tips = scrape_dunkel()
        # for tip in tips:
        #     serializer = TipSerializer(data=tip)
        #     if serializer.is_valid():
        #         serializer.save()
        #         print("Saved Dunkel tip: {}".format(tip['game']))
        #     else:
        #         print(serializer.errors)

        # print("Scraping Betfirm tips...")
        # tips = scrape_betfirm()
        # for tip in tips:
        #     serializer = TipSerializer(data=tip)
        #     try:
        #         if serializer.is_valid():
        #             serializer.save()
        #             print("Saved Betfirm tip: {}".format(tip['game']))
        #         else:
        #             print('Betfirm tip not valid', end=' ')
        #             print(serializer.errors)
        #     except Exception as e:
        #         print('Betfirm tip not valid', end=' ')
        #         print(e, tip)

