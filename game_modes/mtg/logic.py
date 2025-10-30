import threading

class MTGLifeController:
    def __init__(self, gui):
        self.gui = gui

    def change_life(self, player_num, value):
        """Adjust LP and update display."""
        player = self.gui.game.player1 if player_num == 1 else self.gui.game.player2
        old_value = player.life
        player.adjust_life(value)
        new_value = player.life
        self.gui.animate_life_change(player_num, old_value, new_value)


    def reset_life(self):
        self.gui.game.reset()
        self.gui.update_display()
