#Player Class

class Player: #Individual players object
    def __init__(self, name, starting_lp):
        self.name = name #player name
        self.lp = starting_lp #starting lifepoint value
    
    def damage(self, value): #reduce life point value by given value
        self.lp = max(0, self.lp - value)
    
    def heal(self, value): #heal life point value by given value
        self.lp += value

    def halve_lp(self): #halve the life point value
        self.lp //= 2

    def reset_lp(self, default_lp): #reset life points to the starting value
        self.lp = default_lp
    
    def __str__(self):
        return  f"{self.name}: {self.lp}"