import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re


# from app.helpers import write_scraper_results_to_csv

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }


source = 'pickwise'

class over_under:
    def __init__(self, over_under, over_under_value ):
        self.bet_type = 'OverUnder'
        self.over_under = over_under
        self.over_under_value = over_under_value

class moneyline:
    def __init__(self, winner):
        self.bet_type = 'MoneyLine'
        self.moneyline = winner

class spread:
    def __init__(self, winner):
        self.bet_type = 'Spread'
        self.winner = winner



    

def scrape_links():
    
    url = 'https://www.pickswise.com/mlb/predictions/'


    
    page = requests.get(url,headers=headers)




    soup = BeautifulSoup(page.content, "html.parser")

    # FInd div with class that starts with CardHeader_title


    # Find all div elements with class starting with "CardHeader_title"
    divs = soup.find_all('span', class_=lambda x: x and x.startswith('CardHeader_title'))




    # divs = soup.find_all('span', class_='CardHeader_title__z69i1')[0]

    date = divs[0].get_text()

    current_year = datetime.now().year

    date = datetime.strptime(date + " " + str(current_year), "%a %b %d %Y")
    date = date.strftime("%Y-%m-%d")





    event_divs = soup.find_all(attrs={"data-testid": "EventInfo"})


    # Extract href values from the EventInfo elements
    tips = []
    for event_info in event_divs:


        teams_divs = event_info.find('div', class_=lambda x: x and x.startswith('EventInfo_competitors')).find_all('div')  

        team_a = teams_divs[0].get_text()
        team_b = teams_divs[1].get_text()

        team_a = re.split(r'(\d+)', team_a, maxsplit=1)
        team_b = re.split(r'(\d+)', team_b, maxsplit=1)

        tip = {
            'date': date,
            'source': 'pickwise',
            'team_a': team_a[0],
            'team_b': team_b[0]
        }
    
        

    
        href = event_info['href']
        
        if href is not None:
            tip['url'] = href
            
        tips.append(tip)

    return tips





def scrape_page(tip):

    

    base_url = 'https://www.pickswise.com/'



    full_url = base_url + tip['url']


    page = requests.get(full_url,headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

   


    tips = []
    try:  
        card_divs = soup.find_all(attrs={"data-testid": "CardGrid--grid"})[0]
   
        bet_type = None

        author = soup.find('div', attrs={'data-testid': 'AuthorBio'}).find('h2').get_text()  # type: ignore

        tip_return = {
            "tipster": {"name": author, "source": "pickwise"},
            "game" : { "home_team": tip['team_b'], "away_team": tip['team_a'], "game_date": tip['date'], "sport": "mlb"},
        }
        
        for card in card_divs:
            
            
            bet_type_site = card.find_all(attrs={"data-testid": "Pill"})[0].get_text()

            prediction = card.find('div', class_=lambda x: x and x.startswith('SelectionInfo_outcome_')).get_text()

            

            if bet_type_site == 'Run Line Pick':
                bet_type = 'Spread'
                prediction_parts = prediction.split(' ')
                prediction = ' '.join(prediction_parts[:-1])
                if len(prediction.split(' ')) > 2:
                    prediction = ' '.join(prediction.split(' ')[1:])
                else:
                    prediction = prediction.split(' ')[1]
                tip_return['selected_team'] = prediction
                tip_return['bet_type'] = bet_type
               
            elif bet_type_site == 'Game Totals Pick':
                bet_type = 'OverUnder'
                over_under = prediction.split(' ')[0]
                over_under_value = prediction.split(' ')[1]
                tip_return['bet_type'] = bet_type
                tip_return['over_under'] = over_under
                tip_return['over_under_value'] = over_under_value

            elif bet_type_site == 'Money Line Pick':
                bet_type = 'MoneyLine'
                prediction_parts = prediction.split(' ')
                prediction = ' '.join(prediction_parts[:-1])
                if len(prediction.split(' ')) > 2:
                    prediction = ' '.join(prediction.split(' ')[1:])
                else:
                    prediction = prediction.split(' ')[1]
                tip_return['selected_team'] = prediction
                tip_return['bet_type'] = bet_type

            else:
                # print("Bet type not found")
                continue

            # selection = card.find('div', class_=lambda x: x and x.startswith('SelectionInfo_outcome_')).get_text()
            # # print(selection)

            # single_tip['prediction'] = selection

            # rating_div = soup.find('div', attrs={'data-testid': 'ConfidenceRating'})

            # if rating_div is not None:
            #     filled_stars = rating_div.find_all('span', class_='Icon_tertiary__138uQ')  # type: ignore
            #     empty_stars = rating_div.find_all('span', class_='Icon_empty__1uGrI')  # type: ignore
            #     rating = f"{len(filled_stars)}/{len(filled_stars) + len(empty_stars)}"
            #     tip['rating'] = rating
            # else:
            #     print("Rating not found")

            tips.append(tip_return)
        

        # author = soup.find('div', attrs={'data-testid': 'AuthorBio'}).find('h2').get_text()  # type: ignore
    
        # for tip in tips:
        #     tip['tipster'] = author



    except Exception as e:
        # print(e,"No tips found")
        pass

    return tips




def main():
    tip_links = scrape_links()

    tips = []
    for tip in tip_links:
        tip_array = scrape_page(tip)
        for tip in tip_array:

            tips.append(tip)

    

    # csv = convert_to_csv_string(tips)


    

    return tips


def scrape_pickwise():
    return main()


if __name__ == "__main__":
    main()