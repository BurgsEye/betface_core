from django.db import models
from games.models import Game, Team

class TipsterType(models.TextChoices):
    HUMAN = 'Human', 'Human'
    COMPUTER = 'Computer', 'Computer'

class Tipster(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255,null=True, blank=True)
    type = models.CharField(max_length=10, choices=TipsterType.choices,null=True, blank=True)
   

    def __str__(self):
        return f"{self.name}"


class BetType(models.TextChoices):
    MONEYLINE = 'MoneyLine', 'Money Line'
    SPREAD = 'Spread', 'Spread'
    OVER_UNDER = 'OverUnder', 'Over / Under'



class OverUnder(models.TextChoices):
    OVER = 'Over', 'Over'
    UNDER = 'Under', 'Under'



class Tip(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tipster = models.ForeignKey(Tipster, on_delete=models.CASCADE)
    bet_type = models.CharField(max_length=20, choices=BetType.choices)

    # For MoneyLine
    selected_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    
    # For Spread
    spread_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    over_under = models.CharField(max_length=5, choices=OverUnder.choices, null=True, blank=True)
    # For Over/Under
    over_under_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)



    # Common attributes
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Implement custom validation based on bet_type.
        # For example, make sure only one of the betting types' fields is filled.
        pass

    def __str__(self):
        return f"Tip for {self.tipster} -  {self.game} - {self.bet_type}"