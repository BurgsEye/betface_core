from rest_framework import serializers
from tips.models import Tip, Tipster, BetType, OverUnder

from games.models import Game, Team, Sport

from api.games.serializers import GameSerializer, TeamSerializer

from shared.utils import get_team_by_name_or_alias, get_game_by_teams_and_date


# class TipSerializer(serializers.ModelSerializer):
#     game = GameSerializer()
#     selected_team = serializers.CharField(source="selected_team.name", required=False)
#     tipster = serializers.CharField(source="tipster.name")
#     source = serializers.CharField(source="tipster.source")
#     bet_type = serializers.CharField()

#     class Meta:
#         model = Tip
#         fields = "__all__"

#     def validate_over_under(self, value):
#         over_under_choices = [choice[0] for choice in OverUnder.choices]
#         if value not in over_under_choices:
#             raise serializers.ValidationError(
#                 f"Invalid over_under. Available over_under options are: {', '.join(over_under_choices)}"
#             )

#         return value

#     def validate_bet_type(self, value):
#         """
#         Validate the bet_type against available bet_types in the database.
#         """
#         bet_type_choices = [choice[0] for choice in BetType.choices]

#         if value not in bet_type_choices:
#             raise serializers.ValidationError(
#                 f"Invalid bet_type. Available bet_types are: {', '.join(bet_type_choices)}"
#             )

#         return value

#     def _create_or_update_game(self, game_data):
#         game_serializer = GameSerializer(data=game_data)

#         # Create the game if it doesn't exist
#         if game_serializer.is_valid():
#             game = game_serializer.create(game_serializer.validated_data)
#             return game

#         else:
#             raise serializers.ValidationError(
#                 f"Invalid game data: {game_serializer.errors}"
#             )

        

#     def _create_or_update_tipster(self, tipster_name, source_name):
#         tipster , _  = Tipster.objects.get_or_create(name=tipster_name, source=source_name)
#         return tipster



#     def create(self, validated_data):
#         # Extract and process game data
#         game_data = validated_data.pop("game", None)
#         if not game_data:
#             raise serializers.ValidationError("Game data is missing.")

#         # validated_data["game"] = self._create_or_update_game(game_data)

#         # find game based on home_team, away_team, and date
#         game = get_game_by_teams_and_date(
#             game_data['home_team'],
#             game_data['away_team'],
#             game_data['game_date'],
#         )

#         if game:
#             validated_data["game"] = game
#         else:
#             raise serializers.ValidationError(
#                 f"Game not found for {validated_data['game']['home_team']} vs {validated_data['game']['away_team']} on {validated_data['game']['date']}"
#             )


#         try:
#             if validated_data["selected_team"]["name"]:
#                 # Extract and process selected team data
#                 validated_data["selected_team"] = get_team_by_name_or_alias(
#                     validated_data["selected_team"]["name"]
#                 )
#         except KeyError:
#             pass

#         # CHECK IF TIPSTER EXISTS
#         # IF NOT, CREATE IT
#         # IF YES, GET IT
        
#         validated_data["tipster"] = self._create_or_update_tipster(validated_data["tipster"]["name"], validated_data["tipster"]["source"])
        
        

#         # CHECK IF TIP EXISTS
#         # IF NOT, CREATE IT
#         # IF YES, UPDATE IT
#         lookup_params = {
#             "game": validated_data["game"],
#             "tipster": validated_data["tipster"],
#             "bet_type": validated_data["bet_type"],
#         }

#         for key in lookup_params:
#             validated_data.pop(key, None)

#         tip, created = Tip.objects.update_or_create(
#             defaults=validated_data, **lookup_params
#         )

#         return tip

#     def to_representation(self, instance):
#         """
#         Overriding this method to customize the serialized output.
#         """
#         # Use the original representation
#         rep = super().to_representation(instance)

#         # Replace IDs with the full serialized data for home_team, away_team, and sport
#         rep["tipster"] = TipsterSerializer(instance.tipster).data
#         rep["selected_team"] = TeamSerializer(instance.selected_team).data

#         return rep

class TipsterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipster
        fields = "__all__"


class TipSerializer(serializers.ModelSerializer):

    selected_team = serializers.CharField(required=False)
    tipster = TipsterSerializer()
    # source = serializers.CharField()
    # home_team = serializers(source="game.home_team")
    # away_team = serializers.CharField(source="game.away_team")
    # game_date = serializers.DateField(source="game.game_date")
    # sport = serializers.CharField(source="game.sport")

    game = GameSerializer()

    def validate_selected_team(self, value):
        try:
            get_team_by_name_or_alias(value)
        except serializers.ValidationError as e:
            raise e
        return value
    
    def validate_game(self, value):
        try:
            get_game_by_teams_and_date(value['home_team'], value['away_team'], value['game_date'])
        except serializers.ValidationError as e:
            raise e
        return value

    class Meta:
        model = Tip
        fields = "__all__"

    def create(self, validated_data):
        # Extract and process game data

        
        validated_data["game"] = get_game_by_teams_and_date(
            validated_data['game']['home_team'],
            validated_data['game']['away_team'],
            validated_data['game']['game_date'],
        )

        if 'selected_team' in validated_data:
            validated_data["selected_team"] = get_team_by_name_or_alias(
                validated_data["selected_team"]
            )

        tipster = validated_data.pop("tipster")
        validated_data["tipster"], created = Tipster.objects.update_or_create(
            name=tipster["name"],
            source=tipster["source"],
        )


        lookup_params = {
                "game": validated_data["game"],
                "tipster": validated_data["tipster"],
                "bet_type": validated_data["bet_type"],
            }

        tip, created = Tip.objects.update_or_create(
            defaults=validated_data, **lookup_params
        )

        # print(tip)

        return tip
    
    # def to_representation(self, instance):
    #     """
    #     Overriding this method to customize the serialized output.
    #     """
    #     # Use the original representation
    #     rep = super().to_representation(instance)
    #     print('Game Serializer')
    #     print(rep)
        
        
    #     return rep



