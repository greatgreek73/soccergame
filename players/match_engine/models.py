class Team:
    def __init__(self, players):
        self.players = players

    def calculate_stats(self):
        total_stats = 0
        for player in self.players:
            if player.position == 'Goalkeeper':
                total_stats += player.reflexes + player.line_play + player.endurance
            else:
                total_stats += player.shooting + player.passing + player.speed
        return total_stats