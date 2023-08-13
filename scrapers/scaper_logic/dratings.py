import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


# from app.helpers import write_scraper_results_to_csv


source = 'dratings'

def scrape_listings():
    url = 'https://www.dratings.com/predictor/mlb-baseball-predictions/'
    page = requests.get(url)


    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("tbody", class_="table-body")

    rows = table.find_all('tr') # type: ignore



    tips = []

    for row in rows:
        try:
            data = row.find_all("td")

            date = data[0].find('span').get_text()

            # Convert from DD/MM/YYYY to YYYY-MM-DD
            date_object = datetime.strptime(date , "%m/%d/%Y")
            formatted_date = date_object.strftime("%Y-%m-%d")

            
            teams = data[1].find_all('a')
            team_a = teams[0].get_text()
            team_b = teams[1].get_text()

            percentages = data[3].find_all('span')

            team_a_per = percentages[0].get_text()
            team_b_per = percentages[1].get_text()

            team_a_per = float(team_a_per.replace('%',""))/100
            team_b_per = float(team_b_per.replace('%',""))/100

            if team_a_per < team_b_per:
                predicted_winner = team_b
            else:
                predicted_winner = team_a

            tip = {
                "selected_team":predicted_winner,
                "source":"drating",
                "tipster":"drating",
                "bet_type":"MoneyLine",
                "game": {
                "game_date" : formatted_date,
                "away_team":team_a,
                "home_team":team_b,
                "sport": "mlb"
                }
                # "team_a_percentage":  team_a_per,
                # "team_b_percentage":  team_b_per,
                
            }
            tips.append(tip)
        except:
            continue



        
    return tips




def post_to_database(tips):
    for tip in tips:
        try:

            url= 'http://127.0.0.1:5000/team/team_name/'

            response = requests.get(url+tip['team_a'])
            if response.status_code == 404:
                raise ValueError (f'Cannot find team: {tip["team_a"]}') 

            tip['team_a_name'] = tip['team_a']
            tip['team_a'] = int(response.text)

            response = requests.get(url+tip['team_b'])
            

            if response.status_code == 404:
                raise ValueError (f'Cannot find team: {tip["team_b"]}')  
            tip['team_b_name'] = tip['team_b']
            tip['team_b'] = int(response.text)

            response = requests.get(url+tip['predicted_winner'])
            tip['predicted_winner_name'] = tip['predicted_winner'] 
            tip['predicted_winner'] = int(response.text)

            # tip['date'] = datetime.strptime(tip['date'], "%m/%d/%Y").date()

            
            try:
                date_object = datetime.strptime(tip['date'] , "%m/%d/%Y")
                formatted_date = date_object.strftime("%Y-%m-%d")
                
            except:
                raise ValueError('Date format incorrect')

            tip['date'] = formatted_date
            # tip['date'] = tip['date'].strptime('%Y-%m-%d')
            # print(tip['date'])

            url= 'http://127.0.0.1:5000/game/get_or_create_game'

            payload = {
                "team_a": tip['team_a'],
                "team_b": tip['team_b'],
                "date": tip['date']

            }
            response = requests.post(url, json=payload)
            tip['game_id'] = int(response.text)

            if response.status_code == 400 or response.status_code == 500:
                raise ValueError ('Failed to create game')

            
            url = 'http://127.0.0.1:5000/tips/upsert_tip'
            
            response = requests.post(url, json=tip)

            if response.status_code == 200:
                print(response.text)
            else:
                raise ValueError('Failed to create tip')
        

        # except Exception as e:

        #     #TODO Log this shit
        #     print(tip, e)
        
        except ValueError as ve:
            print(ve)
            continue


def convert_to_csv_string(tips):
    csv_string = 'date,source,team_a,team_b,team_a_percent,team_b_percent,predicted_winner\n'
    for tip in tips:
        csv_string += f'{tip["date"]},{source},{tip["team_a"]},{tip["team_b"]},{tip["team_a_percentage"]},{tip["team_b_percentage"]},{tip["predicted_winner"]}\n'
    return csv_string
    


def scrape_dratings():
    tips = scrape_listings()
    return tips



# def main():
#     tips = scrape_listings()
#     csv = convert_to_csv_string(tips)
#     write_scraper_results_to_csv(csv, source)
#     return csv
#     # print(tips)



# if __name__ == "__main__":
#     tips = main()

#     csv = convert_to_csv_string(tips)

#     tips_string = json.dumps(tips, indent=4, sort_keys=True)
#     # now write output to a file
#     file = open("drating.csv", "w")
#     # magic happens here to make it pretty-printed
#     file.write(csv)
#     file.close()

   
