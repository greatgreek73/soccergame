class Team:
    def __init__(self, players, club):
        self.players = players
        self.club = club

    def calculate_stats(self):
        total_stats = 0
        for player in self.players:
            if player.position == 'Goalkeeper':
                total_stats += player.reflexes + player.aerial + player.jumping + player.command + player.throwing + player.kicking
            else:
                total_stats += player.strength + player.stamina + player.pace + player.marking + player.tackling + player.work_rate + player.positioning + player.passing + player.crossing + player.dribbling + player.ball_control + player.heading + player.finishing + player.long_range + player.vision
        return total_stats