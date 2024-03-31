import scipy.stats as stats

class PlayerStatsGenerator:
    def __init__(self, config):
        self.config = config

    def generate_stats(self, player_position, player_class):
        total_points = self.config['total_points'][player_class]
        main_stats_ratio = self.config['main_stats_ratio'][player_class]
        secondary_stats_range = self.config['secondary_stats_range'][player_class]
        max_stat_value = self.config['max_stat_value']

        main_stats = self._get_main_stats(player_position)
        secondary_stats = [stat for stat in self.config['stats'] if stat not in main_stats]

        # Распределение очков между основными и второстепенными характеристиками
        main_stats_points = int(total_points * main_stats_ratio)
        secondary_stats_points = total_points - main_stats_points

        # Распределение очков для основных характеристик
        points_per_main_stat = main_stats_points // len(main_stats)
        if player_class == 1:
            points_per_main_stat = stats.randint(points_per_main_stat - 5, points_per_main_stat + 10).rvs()  # Небольшой разброс для класса 1

        # Распределение очков для второстепенных характеристик
        points_per_secondary_stat = []
        for stat in secondary_stats:
            if stat in self._get_unnecessary_stats(player_position):
                lower_bound, upper_bound = secondary_stats_range
                points = stats.randint(lower_bound, upper_bound + 1).rvs()  # Генерация в указанном диапазоне
            else:
                lower_bound, upper_bound = secondary_stats_range
                points = stats.randint(lower_bound, upper_bound + 1).rvs()  # Генерация в указанном диапазоне
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
        key_stat_multipliers = self.config.get('key_stat_multipliers', {})
        for position, multipliers in key_stat_multipliers.items():
            if player_position == position:
                for stat, multiplier in multipliers.items():
                    player_stats[stat] = round(player_stats[stat] * multiplier)

        # Ограничение диапазона значений
        for stat, value in player_stats.items():
            player_stats[stat] = min(value, max_stat_value)

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
        unnecessary_stats = []
        if position == 'Center Forward':
            unnecessary_stats.extend(['tackling', 'marking', 'crossing'])
        elif position == 'Center Back':
            unnecessary_stats.append('crossing')
        elif position == 'Central Midfielder':
            unnecessary_stats.append('crossing')
        elif position == 'Defensive Midfielder':
            unnecessary_stats.append('crossing')
        return unnecessary_stats

