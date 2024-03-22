from django.db import models
from faker import Faker
from django.contrib.auth.models import User
import random

fake = Faker()

class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

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

    name = models.CharField(max_length=100, default=fake.name())
    age = models.IntegerField(default=17)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    nationality = models.CharField(max_length=50, default="Unknown")
    position = models.CharField(max_length=50, choices=POSITIONS, default='Unknown')

    # Характеристики для полевых игроков
    strength = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    stamina = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    pace = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    marking = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    tackling = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    work_rate = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    positioning = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    passing = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    crossing = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    dribbling = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    ball_control = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    heading = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    finishing = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    long_range = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)
    vision = models.IntegerField(default=random.randint(1, 20), null=True, blank=True)

    # Характеристики для вратарей
    handling = models.IntegerField(null=True, blank=True)
    reflexes = models.IntegerField(null=True, blank=True)
    aerial = models.IntegerField(null=True, blank=True)
    jumping = models.IntegerField(null=True, blank=True)
    command = models.IntegerField(null=True, blank=True)
    throwing = models.IntegerField(null=True, blank=True)
    kicking = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name