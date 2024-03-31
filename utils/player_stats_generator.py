import scipy.stats as stats

class PlayerStatsGenerator:
    def __init__(self, config):
        self.config = config

    def generate_stats(self, player_position, player_class):
        total_points = self.config['total_points'][player_class]
        main_stats_ratio = self.config['main_stats_ratio'][player_class]
        max_stat_value = self.config['max_stat_value']

        main_stats = self._get_main_stats(player_position)
        secondary_stats = [stat for stat in self.config['stats'] if stat not in main_stats]

        # Распределение очков между основными и второстепенными характеристиками
        main_stats_points = int(total_points * main_stats_ratio)
        secondary_stats_points = total_points - main_stats_points

        # Распределение очков для основных характеристик
        main_stat_points = []
        for i in range(len(main_stats)):
            lower_bound = main_stats_points // len(main_stats) - 10
            upper_bound = main_stats_points // len(main_stats) + 10
            points = stats.randint(max(lower_bound, 5), upper_bound).rvs()
            main_stat_points.append(points)

        # Распределение очков для второстепенных характеристик
        points_per_secondary_stat = []
        unnecessary_stats = self._get_unnecessary_stats(player_position)
        for stat in secondary_stats:
            if stat in unnecessary_stats:
                lower_bound, upper_bound = (1, 30)  # Диапазон для ненужных характеристик
                points = stats.randint(lower_bound, upper_bound + 1).rvs()
            else:
                lower_bound, upper_bound = (5, 50)  # Диапазон для остальных второстепенных характеристик
                points = stats.randint(lower_bound, upper_bound + 1).rvs()
            points_per_secondary_stat.append(points)

        player_stats = {}
        for i, stat in enumerate(self.config['stats']):
            if stat in main_stats:
                index = main_stats.index(stat)
                player_stats[stat] = main_stat_points[index]
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
        if position == 'Center Forward':
            return ['marking', 'tackling', 'crossing']
        return []