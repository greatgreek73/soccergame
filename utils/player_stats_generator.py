import scipy.stats as stats

class PlayerStatsGenerator:
    def __init__(self, config):
        self.config = config

    def generate_stats(self, player_position, player_class):
        total_points_distribution = {1: 600, 2: 500, 3: 400, 4: 350}
        total_points = total_points_distribution[player_class]

        main_stats = self._get_main_stats(player_position)
        secondary_stats = [stat for stat in self.config['stats'] if stat not in main_stats]

        # Распределение очков между основными и второстепенными характеристиками
        if player_class == 1:
            main_stats_points = int(total_points * 0.8)  # 80% очков для основных характеристик для класса 1
            secondary_stats_points = total_points - main_stats_points
        elif player_position == 'Center Forward':
            main_stats_points = int(total_points * 0.7)  # 70% очков для основных характеристик
            secondary_stats_points = total_points - main_stats_points
        else:
            main_stats_points = int(total_points * 0.6)  # 60% очков для основных характеристик
            secondary_stats_points = total_points - main_stats_points

        # Распределение очков для основных характеристик
        points_per_main_stat = main_stats_points // len(main_stats)
        if player_class == 1:
            points_per_main_stat = stats.randint(points_per_main_stat - 5, points_per_main_stat + 10).rvs()  # Небольшой разброс для класса 1

        # Распределение очков для второстепенных характеристик
        points_per_secondary_stat = []
        for stat in secondary_stats:
            if stat in self._get_unnecessary_stats(player_position):
                points = stats.randint(1, 31).rvs()  # Генерация от 1 до 30 с уменьшением вероятности больших значений
            else:
                if player_class == 1:
                    points = stats.randint(30, 61).rvs()  # Генерация от 30 до 60 для класса 1
                else:
                    points = stats.randint(1, 101).rvs()  # Генерация от 1 до 100
            points_per_secondary_stat.append(points)

        player_stats = {}
        for i, stat in enumerate(self.config['stats']):
            if stat in main_stats:
                player_stats[stat] = points_per_main_stat
            else:
                if i < len(points_per_secondary_stat):
                    player_stats[stat] = points_per_secondary_stat[i]
                else:
                    player_stats[stat] = 0  # или любое другое значение по умолчанию

        # Выделение ключевых характеристик для некоторых позиций
        if player_position == 'Goalkeeper':
            player_stats['reflexes'] = round(player_stats['reflexes'] * 1.2)
            player_stats['positioning'] = round(player_stats['positioning'] * 1.2)
            player_stats['handling'] = round(player_stats['handling'] * 1.2)
        elif player_position == 'Defensive Midfielder':
            player_stats['long_range'] = round(player_stats['long_range'] * 1.5)

        # Ограничение диапазона значений
        for stat, value in player_stats.items():
            if player_class == 1:
                player_stats[stat] = max(30, min(100, value))
            else:
                player_stats[stat] = max(10, min(80, value))

        return player_stats

    def _get_main_stats(self, position):
        if position == 'Goalkeeper':
            return ['reflexes', 'positioning', 'handling']
        elif position == 'Right Back' or position == 'Left Back':
            return ['marking', 'tackling', 'crossing']
        elif position == 'Center Back':
            return ['marking', 'tackling', 'heading']
        elif position == 'Right Midfielder' or position == 'Left Midfielder':
            return ['pace', 'crossing', 'ball_control']
        elif position == 'Central Midfielder':
            return ['passing', 'work_rate', 'vision']
        elif position == 'Attacking Midfielder':
            return ['passing', 'long_range', 'ball_control']
        elif position == 'Center Forward':
            return ['heading', 'finishing', 'long_range']
        elif position == 'Defensive Midfielder':
            return ['passing', 'tackling', 'marking']
        elif position == 'Right Defensive Midfielder' or position == 'Left Defensive Midfielder':
            return ['marking', 'tackling', 'crossing']

    def _get_unnecessary_stats(self, position):
        if position == 'Center Forward':
            return ['marking', 'tackling', 'crossing']
        return []