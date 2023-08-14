import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

from .utils import write_json


# from app.helpers import write_scraper_results_to_csv


source = 'betfirm'

def scrape_page():

    url = 'https://www.betfirm.com/free-baseball-picks/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }


    page = requests.get(url,headers=headers)

    # print(page.content)

    soup = BeautifulSoup(page.content, "html.parser")



    divs = soup.find_all('div', class_='free-pick-col')


    tips = []

    for div in divs:
        tipser = div.find("h3").get_text()
        date = div.find("div", class_="free-pick-time").get_text()
        date = date.split(",")[0].replace("'","20")
        # Convert Jun 25 2023 to 2023-06-25
        date = datetime.strptime(date, '%b %d %Y').strftime('%Y-%m-%d')

        game = div.find("div", class_="free-pick-game").get_text()

        #split by line break
        game = game.split("\n")[2]
        game = game.replace(" | ","")

        
        game_result = div.find("div", class_="pick-result").find("b").get_text()
        game_result = game_result.split("\n")[1]
        # try:
        #     #remove characters after -
            
        #     print(head)
        #     game_result = game_result.split("-")[0]
        # except:
        #     pass
        
        # try:
        #     game_result = game_result.split(" ")[0]
        # except:
        #     pass
        

        game_result, sep, tail = game_result.partition('-')
        game_result, sep, tail = game_result.partition('+')

        prediction = game_result.strip()
        bet_type = 'MoneyLine'



        print(prediction.split(" ")[0])

        if prediction.split(" ")[0] == 'OVER' or prediction.split(" ")[0] == 'UNDER':
            bet_type = 'OverUnder'
            over_under = prediction.split(" ")[0].capitalize()
            over_under_value = prediction.split(" ")[1].replace("½", ".5")
            prediction = None

            tip = {

                "source":"betfirm",
                "tipster":tipser,
                "bet_type":bet_type,
                "over_under": over_under,
                "over_under_value": over_under_value,
                "game": {
                "game_date" : date,
                "away_team":game.split(" vs ")[0],
                "home_team":game.split(" vs ")[1],
                "sport": "mlb"
                }
                # "team_a_percentage":  team_a_per,
                # "team_b_percentage":  team_b_per,
                
            }

        else:
            tip = {
                "selected_team":prediction,
                "source":"betfirm",
                "tipster":tipser,
                "bet_type":bet_type,
                "game": {
                "game_date" : date,
                "away_team":game.split(" vs ")[0],
                "home_team":game.split(" vs ")[1],
                "sport": "mlb"
                }
                # "team_a_percentage":  team_a_per,
                # "team_b_percentage":  team_b_per,
                
            }


        tips.append(tip)

    return tips


def convert_to_csv_string(tips):
    csv = "date,source,tipser,team_a,team_b,predicted_outcome\n"
    for tip in tips:
        csv += f"{tip['date']},{source},{tip['tipsers']},{tip['team_a']},{tip['team_b']},{tip['predicted_outcome']}\n"
    return csv

  
def main():
    tips = scrape_page()
    # csv = convert_to_csv_string(tips)
    write_json(tips, 'betfirm')
    return tips


def scrape_betfirm():
    tips = scrape_page()
    return tips



if __name__ == "__main__":
    main()
