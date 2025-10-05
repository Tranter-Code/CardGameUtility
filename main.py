import os
import tkinter as tk
from tkinter import ttk, messagebox

class Player:
    def __init__(self, name, starting_lp):
        self.name = name
        self.lp = starting_lp
    
    def damage(self, value):
        self.lp = max(0, self.lp - value)
        clear_console()
    
    def heal(self, value):
        self.lp += value
        clear_console()

    def halve_lp(self):
        self.lp //= 2
        clear_console()

    def reset_lp(self, starting_lp=8000):
        self.lp = starting_lp
        clear_console()
    
    def __str__(self):
        return  f"{self.name}: {self.lp}"
    
class Game:
    def __init__(self):
        self.player1 = Player("Player 1", 8000)
        self.player2 = Player("Player 2", 8000)

    def get_player(self, number):
        if number == 1:
            return self.player1
        elif number == 2:
            return self.player2
        else:
            return None

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

class LifePointAppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Life Point Tracker")
        self.geometry("500x300")
        self.resizable(False, False)

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

    def create_settings_tab(self):
        ttk.Label(self.settings_tab, text="Settings Coming Soon!", font=("Arial", 14)).pack(pady=20)

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
    
    def show_main_screen(self):
        self.clear_game_tab()

        top_frame = ttk.Frame(self.game_tab)
        top_frame.pack(pady=(10, 5))
        ttk.Button(top_frame, text="Reset", command=self.reset_all_lp).pack()

        ttk.Label(self.game_tab, text="Player 1", font=("Arial", 14, "bold")).pack(pady=(10, 0))
        ttk.Label(self.game_tab, textvariable=self.lp1_var, font=("Arial", 20)).pack()
        p1_frame = ttk.Frame(self.game_tab)
        p1_frame.pack(pady=5)

        ttk.Button(p1_frame, text="Damage -", command=lambda: self.show_calc_screen(1, "damage")).pack(side="left", padx=2)
        ttk.Button(p1_frame, text="Heal +", command=lambda: self.show_calc_screen(1, "heal")).pack(side="left", padx=2)
        ttk.Button(p1_frame, text="Halve", command=lambda: self.halve_lp(1)).pack(side="left", padx=2)

        ttk.Label(self.game_tab, text="Player 2", font=("Arial", 14, "bold")).pack(pady=(15, 0))
        ttk.Label(self.game_tab, textvariable=self.lp2_var, font=("Arial", 20)).pack()
        p2_frame = ttk.Frame(self.game_tab)
        p2_frame.pack(pady=5)

        ttk.Button(p2_frame, text="Damage -", command=lambda: self.show_calc_screen(2, "damage")).pack(side="left", padx=2)
        ttk.Button(p2_frame, text="Heal +", command=lambda: self.show_calc_screen(2, "heal")).pack(side="left", padx=2)
        ttk.Button(p2_frame, text="Halve", command=lambda: self.halve_lp(2)).pack(side="left", padx=2)


    def change_lp(self, player_num, delta):
        player = self.game.player1 if player_num == 1 else self.game.player2
        if delta < 0:
            player.damage(abs(delta))
        else:
            player.heal(delta)
        self.update_display()

    def halve_lp(self, player_num):
        player = self.game.player1 if player_num == 1 else self.game.player2
        player.halve_lp()
        self.update_display()

    def reset_all_lp(self):
        confirm = messagebox.askyesno("Confirm Reset", "Reset both players' Life Points to 8000?")
        if confirm:
            self.game.player1.reset_lp()
            self.game.player2.reset_lp()
            self.update_display()

    def update_display(self):
        self.lp1_var.set(str(self.game.player1.lp))
        self.lp2_var.set(str(self.game.player2.lp))
        
        

def main():
    # For now, just test in console
    game = Game()
    while True:
        print("\n--- Life Point Tracker ---")
        game.show_state()
        print("\nChoose an action:")
        print("1. Damage")
        print("2. Heal")
        print("3. Halve LP")
        print("4. Reset LP")
        print("5. Show State")
        print("0. Quit")

        choice = input("Action: ")
        if choice == "0":
            break
        elif choice in ["1", "2", "3", "4"]:
            player_num = int(input("Which player? (1 or 2): "))
            player = game.get_player(player_num)
            if not player:
                print("Invalid player.")
                continue
            
            if choice == "1":  # Damage
                value = int(input("Damage value: "))
                player.damage(value)
            elif choice == "2":  # Heal
                value = int(input("Heal value: "))
                player.heal(value)
            elif choice == "3":  # Halve
                player.halve_lp()
            elif choice == "4":  # Reset
                player.reset_lp()
        
        
        elif choice == "5":
            game.show_state()
        else:
            print("Invalid choice. Try again.")
    


if __name__ == "__main__":
    app = LifePointAppGUI()
    app.mainloop()