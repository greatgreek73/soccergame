from .models import Team
import random

def simulate_match(team1_players, team2_players):
    # Выбираем игроков для матча
    team1_players_selected = select_players(team1_players)
    team2_players_selected = select_players(team2_players)

    # Создаем команды из выбранных игроков
    team1 = Team(team1_players_selected)
    team2 = Team(team2_players_selected)

    team1_stats = team1.calculate_stats()
    team2_stats = team2.calculate_stats()

    stats_difference = abs(team1_stats - team2_stats)
    random_factor = random.randint(0, stats_difference // 2)  # Случайный фактор в диапазоне от 0 до половины разницы характеристик

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