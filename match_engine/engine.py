from .models import Team
import random

def simulate_match(team1_players, team2_players, club1, club2):
    team1 = Team(team1_players, club1)
    team2 = Team(team2_players, club2)

    team1_stats = team1.calculate_stats()
    team2_stats = team2.calculate_stats()

    stats_difference = abs(team1_stats - team2_stats)
    random_factor = random.randint(0, stats_difference // 2)

    if team1_stats + random_factor >= team2_stats:
        winner = team1
        loser = team2
    else:
        winner = team2
        loser = team1

    return winner, loser

def select_players(players):
    goalkeeper = random.choice([p for p in players if p.position == 'Goalkeeper'])
    center_back = random.choice([p for p in players if p.position == 'Center Back'])
    central_midfielder = random.choice([p for p in players if p.position == 'Central Midfielder'])
    center_forward = random.choice([p for p in players if p.position == 'Center Forward'])

    return [goalkeeper, center_back, central_midfielder, center_forward]