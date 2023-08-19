from rest_framework import serializers
from games.models import Game, Sport, Team, TeamAlias

from shared.utils import get_team_by_name_or_alias

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'



class TeamAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamAlias
        fields = '__all__'


class TeamListSerializer(serializers.ListSerializer):
    def create(self, validated_data_list):
        # Create an empty list to store teams
        teams = []

        # Loop over each set of validated data in the list
        for validated_data in validated_data_list:
            # Corrected super call
            team = super(TeamListSerializer, self).create([validated_data])
            teams.append(team[0])  # since create returns a list, extract the first item

        return teams

class TeamSerializer(serializers.ModelSerializer):
    # aliases = TeamAliasSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = '__all__'
        list_serializer_class = TeamListSerializer


# class GameListSerializer(serializers.ListSerializer):
#     def create(self, validated_data_list):
#         # Create an empty list to store games
#         games = []

#         # Loop over each set of validated data in the list
#         for validated_data in validated_data_list:
#             # Corrected super call
#             game = super(GameListSerializer, self).create([validated_data])
#             games.append(game[0])  # since create returns a list, extract the first item

#         return games

class GameSerializer(serializers.ModelSerializer):
    home_team = serializers.CharField()
    away_team = serializers.CharField()
    favourite = serializers.CharField(required=False)
    sport = serializers.CharField()

    class Meta:
        model = Game
        fields = '__all__'
        # list_serializer_class = GameListSerializer 

    def validate_home_team(self, value):
        try:
            get_team_by_name_or_alias(value)
        except serializers.ValidationError as e:
            raise e
        return value
    
    def validate_away_team(self, value):
        try:
            get_team_by_name_or_alias(value)
        except serializers.ValidationError as e:
            raise e
        return value
    
    def validate_favourite(self, value):
        try:
            get_team_by_name_or_alias(value)
        except serializers.ValidationError as e:
            raise e
        return value
    
    def validate_sport(self, value):
        try:
            Sport.objects.get(name=value)
        except Sport.DoesNotExist:
            raise serializers.ValidationError(f"Invalid sport: {value}")
        return value
    

    def create(self, validated_data):
       
        
        home_team = get_team_by_name_or_alias(validated_data.pop('home_team'))
        away_team = get_team_by_name_or_alias(validated_data.pop('away_team'))

        if 'favourite' in validated_data:
            validated_data['favourite']  = get_team_by_name_or_alias(validated_data.pop('favourite'))
        
        validated_data['sport'] = Sport.objects.get(name=validated_data['sport'])

        game_date = validated_data.pop('game_date')
        
        try:
            
            instance, created = Game.objects.update_or_create(
                home_team=home_team,
                away_team=away_team,
                game_date=game_date,
                
                defaults= validated_data
            )
        except serializers.ValidationError as e:
            raise e
            
        return instance


    # def to_representation(self, instance):
    #     """
    #     Overriding this method to customize the serialized output.
    #     """
    #     # Use the original representation
    #     rep = super().to_representation(instance)
    #     # Replace IDs with the full serialized data for home_team, away_team, and sport
    #     rep['home_team'] = TeamSerializer(instance.home_team).data
    #     rep['away_team'] = TeamSerializer(instance.away_team).data
    #     rep['favourite'] = TeamSerializer(instance.favourite).data
    #     rep['sport'] = SportSerializer(instance.sport).data
        
    #     return rep
    


class GamesBySportSerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True, read_only=True, source='game_set')  # using the default reverse relation name

    class Meta:
        model = Sport
        fields = ('name', 'games')
