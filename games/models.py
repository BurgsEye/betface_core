from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import JSONField

# Sport Model
class Sport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, unique=True,  null=True, blank=True) 
    number_of_teams = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.name

# Team Model
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=255,  null=True, blank=True)
    sport = models.ForeignKey(Sport, related_name='teams', on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='teams/logos/', blank=True, null=True)
    
    def __str__(self):
        return self.name

# TeamAlias Model
class TeamAlias(models.Model):
    team = models.ForeignKey(Team, related_name='aliases', on_delete=models.CASCADE)
    alias = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.alias} ({self.team.name})"

class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    favourite = models.ForeignKey(Team, related_name='favourite_games', on_delete=models.CASCADE, null=True, blank=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    game_date = models.DateField()
    game_time = models.TimeField(blank=True, null=True)
    scores = JSONField(default=dict, blank=True, null=True)  # e.g., {"home": 2, "away": 1}

    class Meta:
        unique_together = ('game_date', 'home_team', 'away_team')

    def clean(self):
        # Ensure that home_team and away_team are from the same sport
        if self.home_team.sport != self.away_team.sport:
            raise ValidationError("Home and Away teams must be from the same sport.")
        
    def save(self, *args, **kwargs):
        self.clean()
        super(Game, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} on {self.game_date}"

