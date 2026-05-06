class GameManager:
    def __init__(self):
        self.current_game = None
        self.level = 1
        self.score = 0
        self.lives = 3
        self.is_game_over = False

    def start_game(self, game_name):
        self.current_game = game_name
        self.level = 1
        self.score = 0
        self.lives = 3
        self.is_game_over = False

    def next_level(self):
        if not self.is_game_over:
            self.level += 1

    def add_score(self, points):
        if not self.is_game_over and points > 0:
            self.score += points

    def lose_life(self):
        if self.is_game_over:
            return

        self.lives -= 1

        if self.lives <= 0:
            self.lives = 0
            self.game_over()

    def game_over(self):
        self.is_game_over = True
        print("GAME OVER!")

    def reset(self):
        self.start_game(self.current_game)