import os
import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import threading

class Player:
    def __init__(self, name, starting_lp):
        self.name = name
        self.lp = starting_lp
    
    def damage(self, value):
        self.lp = max(0, self.lp - value)
    
    def heal(self, value):
        self.lp += value

    def halve_lp(self):
        self.lp //= 2

    def reset_lp(self, default_lp):
        self.lp = default_lp
    
    def __str__(self):
        return  f"{self.name}: {self.lp}"
    
class Game:
    def __init__(self, starting_lp=8000):
        self.starting_lp = starting_lp
        self.player1 = Player("Player 1", starting_lp)
        self.player2 = Player("Player 2", starting_lp)

    def get_player(self, number):
        if number == 1:
            return self.player1
        elif number == 2:
            return self.player2
        else:
            return None

class LifePointAppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Life Point Tracker")
        self.geometry("500x300")
        self.resizable(False, False)

        pygame.mixer.init()
        self.lp_count_sound = pygame.mixer.Sound("assets/sounds/LP_counting.wav")
        self.lp_end_sound = pygame.mixer.Sound("assets/sounds/LP_updated.wav")
        self.lp_count_sound.set_volume(0.3)
        self.lp_end_sound.set_volume(0.3)   

        self.game = Game()

        self.lp1_var = tk.StringVar(value=str(self.game.player1.lp))
        self.lp2_var = tk.StringVar(value=str(self.game.player2.lp))
        
        #Tabs
        notebook = ttk.Notebook(self)
        self.game_tab = ttk.Frame(notebook)
        self.settings_tab = ttk.Frame(notebook)
        notebook.add(self.game_tab, text="Game")
        notebook.add(self.settings_tab, text="Settings")
        notebook.pack(expand=True, fill='both')
        
        def on_tab_change(event):
            self.update_idletasks()
        notebook.bind("<<NotebookTabChanged>>", on_tab_change)

        self.show_main_screen()
        self.create_settings_tab()
        self.focus_force()

    def show_main_screen(self):
        self.clear_game_tab()

        top_frame = ttk.Frame(self.game_tab)
        top_frame.pack(pady=(10, 5))
        ttk.Button(top_frame, text="Reset", command=self.reset_all_lp).pack()

        ttk.Label(self.game_tab, text=self.game.player1.name, font=("Arial", 14, "bold")).pack(pady=(10, 0))
        ttk.Label(self.game_tab, textvariable=self.lp1_var, font=("Arial", 20)).pack()
        p1_frame = ttk.Frame(self.game_tab)
        p1_frame.pack(pady=5)

        ttk.Button(p1_frame, text="Damage -", command=lambda: self.show_calc_screen(1, "damage")).pack(side="left", padx=2)
        ttk.Button(p1_frame, text="Heal +", command=lambda: self.show_calc_screen(1, "heal")).pack(side="left", padx=2)
        ttk.Button(p1_frame, text="Halve", command=lambda: self.halve_lp(1)).pack(side="left", padx=2)

        ttk.Label(self.game_tab, text=self.game.player2.name, font=("Arial", 14, "bold")).pack(pady=(15, 0))
        ttk.Label(self.game_tab, textvariable=self.lp2_var, font=("Arial", 20)).pack()
        p2_frame = ttk.Frame(self.game_tab)
        p2_frame.pack(pady=5)

        ttk.Button(p2_frame, text="Damage -", command=lambda: self.show_calc_screen(2, "damage")).pack(side="left", padx=2)
        ttk.Button(p2_frame, text="Heal +", command=lambda: self.show_calc_screen(2, "heal")).pack(side="left", padx=2)
        ttk.Button(p2_frame, text="Halve", command=lambda: self.halve_lp(2)).pack(side="left", padx=2)

    def create_settings_tab(self):
        for widget in self.settings_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.settings_tab, text="Settings", font=("Arial", 16, "bold")).pack(pady=(10, 15))

        ttk.Button(self.settings_tab, text="Change Player Names", command=self.open_name_editor).pack(pady=20)

        ttk.Button(self.settings_tab, text="Change Starting Life Points", command=self.open_starting_lp_editor).pack(pady=10)

    def open_name_editor(self):
        popup = tk.Toplevel(self)
        popup.title("Edit Player Names")
        popup.geometry("300x210")
        popup.resizable(False, False)
        popup.grab_set()  # makes the window modal (focus lock)

        ttk.Label(popup, text="Edit Player Names", font=("Arial", 14, "bold")).pack(pady=10)

        # Entry for Player 1
        ttk.Label(popup, text="Player 1 Name:").pack()
        p1_entry = ttk.Entry(popup, width=25)
        p1_entry.insert(0, self.game.player1.name)  # pre-fill current name
        p1_entry.pack(pady=5)

        # Entry for Player 2
        ttk.Label(popup, text="Player 2 Name:").pack()
        p2_entry = ttk.Entry(popup, width=25)
        p2_entry.insert(0, self.game.player2.name)
        p2_entry.pack(pady=5)

        def save_names():
            name1 = p1_entry.get().strip() or "Player 1"
            name2 = p2_entry.get().strip() or "Player 2"
            self.game.player1.name = name1
            self.game.player2.name = name2
            self.show_main_screen()
            popup.destroy()

        ttk.Button(popup, text="Save", command=save_names).pack(pady=15)

        popup.bind("<Return>", lambda e: save_names())

    def open_starting_lp_editor(self):
        popup = tk.Toplevel(self)
        popup.title("Edit Starting Life Points")
        popup.geometry("300x180")
        popup.resizable(False, False)
        popup.grab_set()  # make window modal

        ttk.Label(popup, text="Change Starting LP", font=("Arial", 14, "bold")).pack(pady=10)

        # LP entry
        ttk.Label(popup, text="Starting Life Points:").pack()
        lp_entry = ttk.Entry(popup, width=20)
        lp_entry.insert(0, str(self.game.starting_lp))
        lp_entry.pack(pady=5)

        def save_lp():
            try:
                new_lp = int(lp_entry.get())
                if new_lp <= 0:
                    raise ValueError

                # Update both players and refresh UI
                self.game.starting_lp = new_lp
                self.game.player1.reset_lp(new_lp)
                self.game.player2.reset_lp(new_lp)
                self.update_display()
                popup.destroy()
            except ValueError:
                lp_entry.delete(0, tk.END)
                lp_entry.insert(0, "Invalid")

        ttk.Button(popup, text="Save", command=save_lp).pack(pady=15)

        popup.bind("<Return>", lambda e: save_lp())

    def show_calc_screen(self, player_num, action):
        self.clear_game_tab()

        player = self.game.player1 if player_num == 1 else self.game.player2
        ttk.Label(self.game_tab, text=f"{player.name} - {action.capitalize()}", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(self.game_tab, text=f"Current LP: {player.lp}", font=("Arial", 12)).pack(pady=(0, 10))

        ttk.Label(self.game_tab, text=f"Enter value to {action}:").pack(pady=5)
        entry = ttk.Entry(self.game_tab)
        entry.pack()
        entry.focus()

        def confirm(event=None):
            try:
                value = int(entry.get())
                if action == "damage":
                    self.change_lp(player_num, -value)
                elif action == "heal":
                    self.change_lp(player_num, value)
                self.show_main_screen()
            except ValueError:
                entry.delete(0, tk.END)
                entry.insert(0, "Invalid")

        def cancel():
            self.show_main_screen()

        ttk.Button(self.game_tab, text="Confirm", command=confirm).pack(pady=10)
        ttk.Button(self.game_tab, text="Cancel", command=cancel).pack()

        self.bind("<Return>", confirm)
        self.bind("<Escape>", lambda e: cancel())

    def clear_game_tab(self):
        for widget in self.game_tab.winfo_children():
            widget.destroy()

    def change_lp(self, player_num, delta):
        player = self.game.player1 if player_num == 1 else self.game.player2
        old_value = player.lp
        if delta < 0:
            player.damage(abs(delta))
        else:
            player.heal(delta)
        new_value = player.lp
        self.animate_lp_change(player_num, old_value, new_value)

    def halve_lp(self, player_num):
        player = self.game.player1 if player_num == 1 else self.game.player2
        old_value = player.lp
        player.halve_lp()
        new_value = player.lp
        self.animate_lp_change(player_num, old_value, new_value)

    def reset_all_lp(self):
        confirm = messagebox.askyesno("Confirm Reset", f"Reset both players' Life Points to {self.game.starting_lp}?")
        if confirm:
            self.game.player1.reset_lp(self.game.starting_lp)
            self.game.player2.reset_lp(self.game.starting_lp)
            self.update_display()

    def update_display(self):
        self.lp1_var.set(str(self.game.player1.lp))
        self.lp2_var.set(str(self.game.player2.lp))
    
    def animate_lp_change(self, player_num: int, old_value: int, new_value: int, duration: int = 1300):
        steps = 60  # smoothness (frames)
        delay = duration // steps
        delta = (new_value - old_value) / steps
        current = old_value
        count = 0

        threading.Thread(target=lambda: self.lp_count_sound.play()).start()

        def update_step():
            nonlocal current, count
            if count < steps:
                current += delta
                display_value = int(round(current))
                if player_num == 1:
                    self.lp1_var.set(str(display_value))
                else:
                    self.lp2_var.set(str(display_value))
                count += 1
                self.after(delay, update_step)
            else:
                if player_num == 1:
                    self.lp1_var.set(str(new_value))
                else:
                    self.lp2_var.set(str(new_value))
                threading.Thread(target=lambda: self.lp_end_sound.play()).start()

        self.after(100, update_step())

if __name__ == "__main__":
    app = LifePointAppGUI()
    app.mainloop()