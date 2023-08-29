# utils/team_helpers.py

from games.models import Team, TeamAlias, Game
from rest_framework import serializers
from django.db.models import Q

from datetime import datetime, timedelta


class ModelDoesNotExistError(Exception):
    def __init__(self, model_name, *args, **kwargs):
        self.model_name = model_name
        super().__init__(*args, **kwargs)


def get_team_by_name_or_alias(team_name):
    """Retrieve a Team instance by its name or alias."""
    try:
        return Team.objects.get(name=team_name)
    except Team.DoesNotExist:
        try:
            alias = TeamAlias.objects.get(alias=team_name)
            return alias.team
        except TeamAlias.DoesNotExist:
            raise ModelDoesNotExistError("Team",f"Team '{team_name}' does not exist.")
        

def get_game_by_teams_and_date(home_team, away_team, game_date, first=True):
    """Retrieve a Game instance by its home team, away_team, and date."""
    
    # Construct Q queries for home and away teams based on name or alias
    home_team_query = Q(home_team__name=home_team) | Q(home_team__aliases__alias=home_team)
    away_team_query = Q(away_team__name=away_team) | Q(away_team__aliases__alias=away_team)

    try:
        # Fetch the game that satisfies both the home and away team conditions along with the game_date
        game = Game.objects.filter(home_team_query & away_team_query & Q(game_date=game_date)).distinct()

        # Check if a game was found
        if game.exists():
  
            return game.first()
        else:
            if first:
                # add a day and try again
                if isinstance(game_date, str):
                    game_date = datetime.strptime(game_date, '%Y-%m-%d')
                # game_object = datetime.strptime(game_date, '%Y-%m-%d')
                # print(home_team, away_team, game_date)
                game_date = game_date + timedelta(days=1)
                # print(home_team, away_team, game_date)
                return get_game_by_teams_and_date(home_team, away_team, game_date, first=False)
            raise ModelDoesNotExistError("Game",f"Game between {home_team} and {away_team} on {game_date} does not exist.")

    except Game.DoesNotExist:
        raise ModelDoesNotExistError("Game",f"Game between {home_team} and {away_team} on {game_date} does not exist.")