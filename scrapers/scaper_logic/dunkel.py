import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import os
# from app.helpers import write_scraper_results_to_csv


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }


source = 'dunkel'


def scrape_links():
    
    url = 'https://www.dunkelindex.com/picks/mlb'


    
    page = requests.get(url,headers=headers)




    soup = BeautifulSoup(page.content, "html.parser")


    games = soup.find_all('li', class_='game')



    tips = []

    for game in games:

        try:
            date_element = game.find('p', class_='time')
            # print(date_element)
            date = date_element['datetime'].split(' ')[0]

            #get attributed's value called datetime from date_element
            # date = date_element.get('datetime')

        
            dunkel_pick= ''

            team_1 = game.find('div', class_='team-1')
            team_1_li = team_1.find_all('li')
            team_1 = team_1.find('p').get_text()
            
            predicted_winner = None

            if(len(team_1_li) == 3):
                dunkel_pick =f'{team_1} - {team_1_li[2].find("span").get_text().split(" ")[-1]}'
                predicted_winner = team_1
                over_under = team_1_li[2].find("span").get_text().split(" ")[-1]

            team_2 = game.find('div', class_='team-2')
            team_2_li = team_2.find_all('li')
            team_2 = team_2.find('p').get_text()
            

            if(len(team_2_li) == 3):
                dunkel_pick =f'{team_2} - {team_2_li[2].find("span").get_text().split(" ")[-1]}'
                predicted_winner = team_2
                over_under = team_2_li[2].find("span").get_text().split(" ")[-1]

            dunkel = game.find('div', class_='dunkel')

            dunkel_p = dunkel.find_all('p')

            dunkel_predicted_winner = dunkel_p[0].get_text()
            dunkel_pridicted_score = dunkel_p[2].get_text()

            vegas_pridicted_score = dunkel_p[3].get_text()
            vegas_predicted_score = dunkel_p[5].get_text()



            tip = {
        
                'source': 'dunkel',
                'tipster': 'dunkel',
                'selected_team': predicted_winner,
                "bet_type":"OverUnder",
                "over_under": over_under,
                "game": {
                    "game_date" : date,
                    "away_team":team_1,
                    "home_team":team_2,
                    "sport": "mlb"
                    }

            }

            tip2 = {
        
                'source': 'dunkel',
                'tipster': 'dunkel',
                'selected_team': predicted_winner,
                "bet_type":"MoneyLine",
                "game": {
                    "game_date" : date,
                    "away_team":team_1,
                    "home_team":team_2,
                    "sport": "mlb"
                    }

            }

            # "team_a_percentage":  team_a_per,
            # "team_b_percentage":  team_b_per,
            
            



            tips.append(tip)
            tips.append(tip2)

        except:
            date = None

    return tips




    # print(json.dumps(tips, indent=4))    




def scrape_dunkel():
    tips = scrape_links()
    return tips


def main():
    tips = scrape_links()
    # csv = convert_to_csv_string(tips)
        # save the json to a file
    current_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    file_path = os.path.join(current_directory, 'dunkel.json')
    with open(file_path, 'w') as outfile:
        json.dump(tips, outfile, indent=4)

    print(tips)
    return tips


if __name__ == '__main__':
    main()