from Player import *

class Game: #Game object for two player objects that are playing together, with a starting lifepoint value for both players defaulted to 8000.
    def __init__(self, starting_lp):
        self.starting_lp = starting_lp
        self.player1 = Player("Player 1", starting_lp) #create player 1 object
        self.player2 = Player("Player 2", starting_lp) #create player 2 object

    def get_player(self, number): #return either player 1 or 2 object depending on given number
        if number == 1:
            return self.player1
        elif number == 2:
            return self.player2
        else:
            return None