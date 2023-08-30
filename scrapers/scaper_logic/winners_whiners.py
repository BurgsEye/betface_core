import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from datetime import datetime
import json
import re
import pytz

# from app.helpers import write_scraper_results_to_csv

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }


source = 'Winners & Whiners'
baseurl = 'https://winnersandwhiners.com'


def is_number(s):
    try:
        float(s)  # for integers and floats
        return True
    except ValueError:
        return False


def get_links():
    url = 'https://winnersandwhiners.com/games/mlb/'



    page = requests.get(url,headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    article_buttons = soup.find_all('div', class_='game-index-article-buttons')

    link_urls = []

    for article_button in article_buttons:
        links = article_button.find_all('a')
        for link in links:
            link_text = link.get_text().strip()
            link_url = link.get('href')
            if link_text == 'Prediction':   
                link_url = link.get('href')
                link_urls.append(link_url)

    return link_urls


url = 'https://winnersandwhiners.com/games/mlb/8-30-2023/tampa-bay-rays-vs-miami-marlins-prediction-301/'


def scrape_page(url):

    url = baseurl + url
    page = requests.get(url,headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")


    article = soup.find('div', class_='article-image')

    team_names = article.find_all('span', class_='team-name')

    away_team = team_names[0].get_text()
    home_team = team_names[1].get_text()

    game_date = article.find('span', class_='team-game-start')
    text_parts = []
    current_text = ""

    # Iterating through span's children
    for child in game_date.children:
        if isinstance(child, NavigableString):
            current_text += child.strip() + " "
        elif isinstance(child, Tag):
            if child.name == 'br':
                text_parts.append(current_text.strip())
                current_text = ""

    text_parts.append(current_text.strip())  # Append the last text part

    game_date = text_parts[0]
    author = text_parts[1]


    # Parse the date, time, and timezone abbreviation
    date_time, _, tz_abbreviation = game_date.rpartition(' ')
    date_time = datetime.strptime(date_time, "%A, %B %d, %Y at %I:%M%p")

    # Convert the timezone abbreviation to a pytz timezone object
    tz_dict = {
        'EST': 'US/Eastern',
        'EDT': 'US/Eastern', # EDT and EST both map to US/Eastern; you would need to account for daylight saving time manually
        'CST': 'US/Central',
        'CDT': 'US/Central',
        'MST': 'US/Mountain',
        'MDT': 'US/Mountain',
        'PST': 'US/Pacific',
        'PDT': 'US/Pacific',
        'AKST': 'US/Alaska',
        'AKDT': 'US/Alaska',
        'HAST': 'US/Hawaii',
        'HADT': 'US/Hawaii',  # Rare, Hawaii usually doesn't observe daylight saving time
        'GMT': 'GMT',
        'UTC': 'UTC',
        'CET': 'Europe/Berlin',
        'CEST': 'Europe/Berlin',
        'EET': 'Europe/Helsinki',
        'EEST': 'Europe/Helsinki',
        'AEST': 'Australia/Sydney',
        'AEDT': 'Australia/Sydney',
        'AWST': 'Australia/Perth',
        'AWDT': 'Australia/Perth', # Rare, as Western Australia typically doesn't use daylight saving time
        'ACST': 'Australia/Adelaide',
        'ACDT': 'Australia/Adelaide',
        'IST': 'Asia/Kolkata',  # Indian Standard Time
        'JST': 'Asia/Tokyo',    # Japan Standard Time
        'NZST': 'Pacific/Auckland',
        'NZDT': 'Pacific/Auckland',
        'WET': 'Europe/Lisbon',
        'WEST': 'Europe/Lisbon',
        'CAT': 'Africa/Harare',
        'SAST': 'Africa/Johannesburg',
        'AST': 'America/Puerto_Rico',
        'ADT': 'America/Puerto_Rico',
        'ART': 'America/Argentina/Buenos_Aires',  # Argentina Time
    }

    if tz_abbreviation in tz_dict:
        timezone = pytz.timezone(tz_dict[tz_abbreviation])
        date_time = timezone.localize(date_time)
    else:
        raise ValueError(f"Unsupported timezone abbreviation: {tz_abbreviation}")



    game = {
        "sport": "mlb",
        "home_team": home_team,
        "away_team": away_team,
        "game_date": date_time.date().strftime("%Y-%m-%d"),
    }

    author = author.replace("Written by ", "")



    tipster = {
        "name": author,
        "source": source
    }


    picks = soup.find_all('div', class_='pick')

    tips = []

    for pick in picks:
        try:
            prediction = pick.get_text().replace("Prediction:", "").strip().replace("(", "").replace(")", "")
            prediction = " ".join([item for item in prediction.split(" ") if not is_number(item)])
            tip = { "game": game, "tipster": tipster }

            if prediction == "Over" or prediction == "Under":
                over_under = prediction
                bet_type= "OverUnder"
                tip["over_under"] = over_under
                tip["bet_type"] = bet_type
            elif prediction.split(' ')[-1] == "ML":
                bet_type = "MoneyLine"
                prediction = " ".join(prediction.split(' ')[:-1])
                tip["selected_team"] = prediction
                tip["bet_type"] = bet_type

            elif prediction.split(' ')[-1] == "Even":
                bet_type = "MoneyLine"
                prediction = " ".join(prediction.split(' ')[:-1])
                tip["selected_team"] = prediction
                tip["bet_type"] = bet_type
            else:
                bet_type = "MoneyLine"
                tip["selected_team"] = prediction
                tip["bet_type"] = bet_type
                pass

            tips.append(tip)
        except Exception as e:
            print(e)
            pass

    return tips


def scrape_winners_whiners():
    urls = get_links()
    tips_list = []
    for url in urls:
        tips = scrape_page(url)
        tips_list.extend(tips)

    return tips_list