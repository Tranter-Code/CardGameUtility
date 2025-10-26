# --------------------
# Player Class
# --------------------

class Player: #Individual players object
    def __init__(self, name, life_total):
        self.name = name #player name
        self.life = life_total #starting lifepoint value
    
    def damage(self, value): #reduce life point value by given value
        self.life = max(0, self.life - value)
    
    def heal(self, value): #heal life point value by given value
        self.life += value

    def reset_lp(self, starting_life): #reset life points to the starting value
        self.life = starting_life
    

# --------------------
# Game Class
# --------------------
class Game: 
    def __init__(self, life_total):
        self.life_total = life_total
        self.player1 = Player("Player 1", life_total) #create player 1 object
        self.player2 = Player("Player 2", life_total) #create player 2 object

    def get_player(self, number): #return either player 1 or 2 object depending on given number
        if number == 1:
            return self.player1
        elif number == 2:
            return self.player2
        else:
            return None