# --------------------
# Player Class
# --------------------

class Player:
    def __init__(self, name: str, starting_life: int = 20):
        self.name = name
        self.life = starting_life

    def adjust_life(self, amount: int):
        """Increase or decrease life points."""
        self.life += amount



# --------------------
# Game Class
# --------------------

class Game:
    def __init__(self, starting_life=20, player1_name="Player 1", player2_name="Player 2"):
        self.player1 = Player(player1_name, starting_life)
        self.player2 = Player(player2_name, starting_life)
        self.starting_life = starting_life

    def reset(self):
        """Reset both players to starting life points."""
        self.player1.life = self.starting_life
        self.player2.life = self.starting_life