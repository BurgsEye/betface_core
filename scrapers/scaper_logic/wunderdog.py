import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

# from app.helpers import write_scraper_results_to_csv

source = 'wunderdog'


# Converts verbose date into YYYY-MM-DD
def convert_date(string_date):
    converted_date = datetime.strptime(string_date, '%a %b %d, %Y')
    converted_date = converted_date.strftime('%Y-%m-%d')
    return converted_date



# Converts the string format into teams
def get_teams(string_teams):
    teams = string_teams.split('@')
    team_a = teams[0].strip()
    team_b = teams[1].strip()
    return team_a, team_b





def scrape_listings(url):

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find('div', class_='tab-pane')

    rows = table.find_all('div')

    current_date = datetime.now()

    links = []

    for row in rows:
        class_name = row.get('class')
        if 'p-comppicks-table-head' in row["class"]:
            # print('Header found')
            date = row.find('span').get_text()
            date_object = datetime.strptime(date, "%a %b %d, %Y")
            # Calculate the time difference
            time_difference = current_date - date_object

            # Define a timedelta representing 2 days
            two_days_timedelta = timedelta(days=2)
            # Compare the time difference with the timedelta
            if time_difference > two_days_timedelta:
                # print('Date is more than 2 days old')
                break

            continue
        elif 'p-comppicks-table-line'in row["class"]:
            # print('Line found')
            link = row.find('a').get('href')
            links.append(link)
            continue
        else:
            # print('Unknown class')
            # print(class_name)
            continue

    # print('Fin found')  

    # print(links)

    

    return links

def scrape_page(link):
    # page_url = 'https://www.wunderdog.com/mlb-baseball/picks/houston-astros-at-los-angeles-dodgers-picks-predictions-odds-june-25-2023-1'
    base_url = 'https://www.wunderdog.com'
    page_url = base_url + link
    page = requests.get(page_url)

    soup = BeautifulSoup(page.content, "html.parser")

    teams = soup.find_all('div', class_='p-picks-teams-item-name')

    tips=[]

    away_team = teams[0].get_text()
    home_team = teams[1].get_text()

    game_date = soup.find('div', class_='p-picks-teams-item-date').get_text()
    
    game_date = " ".join(game_date.split()[:-3])

    game_date = datetime.strptime(game_date, "%B %d, %Y").date().strftime("%Y-%m-%d")
   
    # game_date = datetime.strptime(game_date, "%B %d, %Y %I:%M %p %Z").date()

    tipster = {"name": "uunderdog", "source": "wunderdog"}
    game = {"game_date": game_date, "away_team": away_team, "home_team": home_team, "sport": "mlb"}

    target_div = soup.find("div", class_="p-picks-table-label", text="Computer Predictions")

    results_table = target_div.find_next("div", class_="p-picks-table-lines")
    # results_table = soup.find_all('div', class_='p-picks-table-lines')[1]

    result_rows = results_table.find_all('div', class_='p-picks-table-line')

    runline_row = result_rows[2]
    runline_winner = runline_row.find('div', class_='p-picks-table-check').parent
    if 'col2' in runline_winner["class"]:
        runline_winner = home_team
    else:
        runline_winner = away_team
    
    tips.append({"tipster": tipster, "game": game, "bet_type": "Spread", "selected_team": runline_winner})

    moneyline_row = result_rows[3]
    moneyline_winner = moneyline_row.find('div', class_='p-picks-table-check').parent
    if 'col2' in moneyline_winner["class"]:
        moneyline_winner = home_team
    else:
        moneyline_winner = away_team

    tips.append({"tipster": tipster, "game": game, "bet_type": "MoneyLine", "selected_team": moneyline_winner})

    over_under_row = result_rows[4]
    over_under_winner = over_under_row.find_all('div', class_='p-picks-table-text')[1].get_text()
    over_under_winner = "".join(over_under_winner.split("\n")).strip().title()
    over_under= over_under_winner.split(' ')[0]
    over_under_value = over_under_winner.split(' ')[1]

    tips.append({"tipster": tipster, "game": game, "bet_type": "OverUnder", "over_under": over_under, "over_under_value": over_under_value })





    return tips



# main script

# tips = scrape_listings(url)

# print(len(tips))


# for tip in tips:
#     tip = scrape_page(tip)






def main():

    url = 'https://www.wunderdog.com/mlb-baseball/matchups-2023'
    links = scrape_listings(url)
    counter = 0
    tips = []
    for link in links:
        counter += 1
        # print(f'Processing tip {counter} of {len(tips)}')
        tips.extend( scrape_page(link))
    # post_to_database(tips)
    
    # with open('wunderdog.json', 'w') as outfile:
    #     json.dump(tips, outfile)

    return tips


def scrape_wunderdog():
    return main()


if __name__ == "__main__":
    tips = main()
    # csv = convert_to_csv_string(tips)


#     # tips_string = json.dumps(tips, indent=4, sort_keys=True)
#     # # now write output to a file
#     # file = open("wunderdog.json", "w")
#     # # magic happens here to make it pretty-printed
#     # file.write(tips_string)
#     # file.close()
#     print(tips)

