import requests
from decouple import config
# from app.models import Game, Team
import json
from datetime import datetime
import pprint
import os
# from app import db

# from app.helpers.email import send_email_generic


from ..scaper_logic.utils import write_json



api_key = config("ODDS_API_KEY")


base_url = 'https://api.the-odds-api.com'
oods_url = base_url + f'/v4/sports/baseball_mlb/odds?apiKey={api_key}&regions=uk&markets=h2h&oddsFormat=american'



class GameResponse:
    def __init__(self, home_team, away_team,favourite, game_date, game_time):
        self.home_team = home_team
        self.away_team = away_team
        self.game_date = game_date
        self.game_time = game_time
        self.favourite = favourite
        self.sport = "mlb"

    def to_json(self):
        return {
            'home_team': self.home_team,
            'away_team': self.away_team,
            'game_date': self.game_date,
            'game_time': self.game_time,
            'favourite': self.favourite,
            'sport': self.sport
        }

def fetch_game_responses(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('Error with request')
        return None
    return response.json()


def process_game_responses(game_responses):
    games = []
    for game_response in game_responses:
        try:
            home_team = game_response['home_team']
            away_team = game_response['away_team']
            date = game_response['commence_time'].split('T')[0]
            # game_date = datetime.strptime(date, '%Y-%m-%d').date()
            game_date = game_response['commence_time'].split('T')[0]
            game_time = game_response['commence_time'].split('T')[1][:-1]
            game_odds = process_game_odds(home_team, away_team, game_response['bookmakers'])
            favourite = calculate_favourite(home_team, away_team, game_odds)


            game =  GameResponse ( home_team, away_team,favourite, game_date, game_time)

            if not game:

                raise Exception('Error creating game')

            games.append(game)
        except Exception as e:
            print(e)  # TODO: log error
            continue
    return games


def process_game_odds(home_team, away_team,bookmakers):
    game_odds = []
    for bookmaker in bookmakers:
        for market in bookmaker['markets']:
            if market['key'] == 'h2h':
                for outcome in market['outcomes']:
                    home_odds = None
                    away_odds = None
                    if outcome['name'] == home_team:
                        home_odds = outcome['price']
                    elif outcome['name'] == away_team:
                        away_odds = outcome['price']
                    game_odds.append({
                        'bookmaker': bookmaker['title'],
                        'home_odds': home_odds,
                        'away_odds': away_odds
                    })
    return game_odds


def calculate_favourite(home_team, away_team, game_odds):
    home_odds_sum = 0
    away_odds_sum = 0
    for odds in game_odds:
        if odds['home_odds']:
            home_odds_sum += odds['home_odds']
        elif odds['away_odds']:
            away_odds_sum += odds['away_odds']
    return home_team if home_odds_sum < away_odds_sum else away_team



def get_odds():
    response = requests.get(oods_url)
    if response.status_code != 200:
        print('Error with request')
        return
    game_responses = response.json()

    # save the json to a file
    current_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    file_path = os.path.join(current_directory, 'odds_api_schedule.json')
    with open(file_path, 'w') as outfile:
        json.dump(game_responses, outfile)


    games = process_game_responses(game_responses)

    game_array = []


    for game in games:
        game_array.append(game.to_json())


    write_json(game_array, 'odds_api_schedule_formatted.json')

    # send_email_generic('Scheduled Game Import', f'Upserted {len(games)} games')
    return game_array


if __name__ == '__main__':
    get_odds()