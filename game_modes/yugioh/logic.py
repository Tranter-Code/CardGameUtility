import threading

class LifePointController:
    """Handles all LP changes, animations, and related sound effects."""

    def __init__(self, gui):
        self.gui = gui  # reference to YuGiOhFrame
        self.sfx = gui.sfx
        self.game = gui.game

    def change_lp(self, player_num, value):
        """Increase or decrease LP for a player and animate the change."""
        game = self.gui.game 
        player = self.game.player1 if player_num == 1 else self.game.player2
        old_value = player.lp
        if value < 0:
            player.damage(abs(value))
        else:
            player.heal(value)

        new_value = player.lp
        self.gui.animate_lp_change(player_num, old_value, new_value)

    def halve_lp(self, player_num):
        player = self.game.player1 if player_num == 1 else self.game.player2
        old_value = player.lp
        player.halve_lp()
        self.gui.animate_lp_change(player_num, old_value, player.lp)

    def reset_all_lp(self):
        confirm = self.gui.messagebox.askyesno(
            "Confirm Reset",
            f"Reset both players' Life Points to {self.game.starting_lp}?"
        )
        if confirm:
            self.game.player1.reset_lp(self.game.starting_lp)
            self.game.player2.reset_lp(self.game.starting_lp)
            self.gui.update_display()
            self.sfx.play_sound("Refresh")

    def get_player(self, player_num):
        return self.gui.game.player1 if player_num == 1 else self.gui.game.player2