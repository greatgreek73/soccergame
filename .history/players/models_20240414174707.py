from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    stadium_name = models.CharField(max_length=100, default='Stadium')
    stadium_capacity = models.IntegerField(default=10000)

    def __str__(self):
        return self.name

class Player(models.Model):
    POSITIONS = [
        ('Goalkeeper', 'Goalkeeper'),
        ('Right Back', 'Right Back'),
        ('Left Back', 'Left Back'),
        ('Center Back', 'Center Back'),
        ('Right Midfielder', 'Right Midfielder'),
        ('Central Midfielder', 'Central Midfielder'),
        ('Left Midfielder', 'Left Midfielder'),
        ('Attacking Midfielder', 'Attacking Midfielder'),
        ('Center Forward', 'Center Forward'),
    ]

    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=17)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    nationality = models.CharField(max_length=50, default="Unknown")
    position = models.CharField(max_length=50, choices=POSITIONS, default='Unknown')
    player_class = models.PositiveSmallIntegerField(null=True, blank=True)

    # Характеристики для всех игроков
    strength = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)
    pace = models.IntegerField(null=True, blank=True)
    marking = models.IntegerField(null=True, blank=True)
    tackling = models.IntegerField(null=True, blank=True)
    work_rate = models.IntegerField(null=True, blank=True)
    positioning = models.IntegerField(null=True, blank=True)
    passing = models.IntegerField(null=True, blank=True)
    crossing = models.IntegerField(null=True, blank=True)
    dribbling = models.IntegerField(null=True, blank=True)
    ball_control = models.IntegerField(null=True, blank=True)
    heading = models.IntegerField(null=True, blank=True)
    finishing = models.IntegerField(null=True, blank=True)
    long_range = models.IntegerField(null=True, blank=True)
    vision = models.IntegerField(null=True, blank=True)

    # Характеристики для вратарей
    handling = models.IntegerField(null=True, blank=True)
    reflexes = models.IntegerField(null=True, blank=True)
    aerial = models.IntegerField(null=True, blank=True)
    jumping = models.IntegerField(null=True, blank=True)
    command = models.IntegerField(null=True, blank=True)
    throwing = models.IntegerField(null=True, blank=True)
    kicking = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Lineup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Другие поля, связанные с составом (например, матч)
    name = models.CharField(max_length=100)  # Добавьте это поле, если его еще нет
    date = models.DateField()                # Добавьте это поле, если его еще нет

    def __str__(self):
        return f"{self.name} ({self.date}) - {self.user.username}"

class LineupPlayer(models.Model):
    lineup = models.ForeignKey(Lineup, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    position = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} - {self.position}"