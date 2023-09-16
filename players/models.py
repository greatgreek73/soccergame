from django.db import models
from faker import Faker
from django.contrib.auth.models import User

fake = Faker()

class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100, default=fake.name())
    age = models.IntegerField(default=17)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    nationality = models.CharField(max_length=50, default="Unknown")

    def __str__(self):
        return self.name
