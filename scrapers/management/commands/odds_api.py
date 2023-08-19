from django.core.management.base import BaseCommand
from scrapers.odds_api.schedule import get_odds

from api.games.serializers import GameSerializer

class Command(BaseCommand):
    help = "Run the odds-api endpoints"

    def handle(self, *args, **options):
        games = get_odds()
        for game in games:
            serializer = GameSerializer(data=game)
            try:
                if serializer.is_valid():
                    serializer.save()
                    print(f"Game saved {game['home_team']} vs {game['away_team']}")
                else:
                    print(serializer.errors)
            except Exception as e:
                print(e)
                print(serializer.errors)
                print(game)
                print('Error saving game')
                continue

