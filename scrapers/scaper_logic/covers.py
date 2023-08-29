import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import pytz


# from app.helpers import write_scraper_results_to_csv

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }


source = 'covers'





def scrape_page(url, tipser_name):

    page = requests.get(url,headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find('tbody')

    rows = table.find_all('tr')[1:]

    tips =[]

    for row in rows:
        away_team = row.find('span', class_='covers-CoversConsensus-table--teamBlock').get_text().strip()
        home_team = row.find('span', class_='covers-CoversConsensus-table--teamBlock2').get_text().strip()
    
        date_cell = row.find_all('td')[1]
        dates = [value.strip() for value in date_cell.get_text(separator='|').split('|')]
        
   

        # Extract month and day
        date_str= f'{dates[0]}  {dates[1]}'

            # Extract date and time components
        date_part = date_str.split()[1:3]
        time_part = date_str.split()[3:5]

            # Create standard date and time strings
        formatted_date_str = f"{date_part[0]} {date_part[1]} {datetime.now().year}"
        formatted_time_str = ' '.join(time_part).replace('ET', '').strip()

        # Convert to datetime objects
        date_obj = datetime.strptime(formatted_date_str, '%b %d %Y')
        time_obj = datetime.strptime(formatted_time_str, '%I:%M %p')

        # Combine date and time into a single datetime object
        combined_datetime = datetime.combine(date_obj, time_obj.time())

        # Adjust for Eastern Time
        eastern = pytz.timezone('US/Eastern')
        localized_datetime = eastern.localize(combined_datetime)


            # Convert to GMT/UTC
        utc_datetime = localized_datetime.astimezone(pytz.utc)

        # Extract just the date
        utc_date = utc_datetime.date()

        # format date as YYYY-MM-DD

        utc_date = utc_date.strftime("%Y-%m-%d")


        game = {
            'game_date': utc_date,
            'away_team': away_team,
            'home_team': home_team, 
            "sport": "mlb"
        }

        


        cells = row.find_all('td')[4]
        # Split the text using <br> and strip any whitespace
        values = [value.strip() for value in cells.get_text(separator='|').split('|')]

        # Assign to separate variables
        away_team_picks, home_team_picks = values

        if int(away_team_picks) > int(home_team_picks):
            winner = away_team
        else:
            winner = home_team

        tipser = {"name": tipser_name, "source": source}

     
        tip = {"tipster": tipser, "game": game, "bet_type": "Spread", "selected_team": winner}

        tips.append(tip)
    
    return tips

def main():

    url = 'https://contests.covers.com/consensus/topconsensus/mlb/overall'
    tipser = 'Overall Bettors'

    try:
        overall_tips = scrape_page(url, tipser)
    except Exception as e:
        print('Failed to extract overall tips')

    url = 'https://contests.covers.com/consensus/topconsensus/mlb/expert'
    tipser = 'Team Leaders'

    try:
        expert_tips = scrape_page(url, tipser)
    except Exception as e:
        print('Failed to extract expert tips')

    url = 'https://contests.covers.com/consensus/topconsensus/mlb/top10pct'
    tipser = 'Top 10%'

    try:

        top10_tips = scrape_page(url, tipser)
    except Exception as e:
        print('Failed to extract top 10% tips')

    # merge lists
    tips = overall_tips + expert_tips + top10_tips

    return tips

def scrape_covers():
    tips = main()
    return tips

if __name__ == '__main__':
    main()