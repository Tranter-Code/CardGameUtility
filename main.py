import os 
import tkinter as tk 
from tkinter import ttk, messagebox 
import pygame 
import threading 

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
    
class Game: #Game object for two player objects that are playing together, with a starting lifepoint value for both players defaulted to 8000.
    def __init__(self, starting_lp=8000):
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

class LifePointAppGUI(tk.Tk): # GUI app.
    def __init__(self):
        super().__init__()
        self.title("Life Point Tracker") #set title for top of window
        self.geometry("500x300") #set dimensions of window
        self.resizable(False, False) #make window non-resizable

        # Initialize pygame mixer for sound effects
        pygame.mixer.init()
        self.lp_count_sound = pygame.mixer.Sound("assets/sounds/dm/LP_counting.wav") #load sound effect - counting lp
        self.lp_end_sound = pygame.mixer.Sound("assets/sounds/dm/LP_updated.wav") #load sound effect - updated lp
        self.lp_count_sound.set_volume(0.3) #set volume for counting sound effect
        self.lp_end_sound.set_volume(0.3)   #set volume for updated sound effect

        self.game = Game() #create game object

        self.lp1_var = tk.StringVar(value=str(self.game.player1.lp)) #stringvar for player 1 lifepoint value
        self.lp2_var = tk.StringVar(value=str(self.game.player2.lp)) #stringvar for player 2 lifepoint value
        
        #Tabs
        notebook = ttk.Notebook(self)
        self.game_tab = ttk.Frame(notebook) #create main game tab
        self.settings_tab = ttk.Frame(notebook) #create settings tab
        notebook.add(self.game_tab, text="Game") #add tabs to notebook
        notebook.add(self.settings_tab, text="Settings")
        notebook.pack(expand=True, fill='both')
        
        def on_tab_change(event): #function to handle tab change events
            self.update_idletasks()
        notebook.bind("<<NotebookTabChanged>>", on_tab_change)

        self.show_main_screen()
        self.create_settings_tab()
        self.focus_force()

    def show_main_screen(self): #draw the main screen on the window
        self.clear_game_tab()

        top_frame = ttk.Frame(self.game_tab) #create top frame
        top_frame.pack(pady=(10, 5))
        ttk.Button(top_frame, text="Reset", command=self.reset_all_lp).pack() #create reset button

        ttk.Label(self.game_tab, text=self.game.player1.name, font=("Arial", 14, "bold")).pack(pady=(10, 0)) #create player 1 label
        ttk.Label(self.game_tab, textvariable=self.lp1_var, font=("Arial", 20)).pack() #create player 1 lifepoint label
        p1_frame = ttk.Frame(self.game_tab) #create player 1 frame
        p1_frame.pack(pady=5)

        ttk.Button(p1_frame, text="Damage -", command=lambda: self.show_calc_screen(1, "damage")).pack(side="left", padx=2) #create damaeg button for player 1
        ttk.Button(p1_frame, text="Heal +", command=lambda: self.show_calc_screen(1, "heal")).pack(side="left", padx=2) #create heal button for player 1
        ttk.Button(p1_frame, text="Halve", command=lambda: self.halve_lp(1)).pack(side="left", padx=2) #create halve button for player 1

        ttk.Label(self.game_tab, text=self.game.player2.name, font=("Arial", 14, "bold")).pack(pady=(15, 0)) #create player 2 label
        ttk.Label(self.game_tab, textvariable=self.lp2_var, font=("Arial", 20)).pack() #create player 2 lifepoint label
        p2_frame = ttk.Frame(self.game_tab) #create player 2 frame
        p2_frame.pack(pady=5)

        ttk.Button(p2_frame, text="Damage -", command=lambda: self.show_calc_screen(2, "damage")).pack(side="left", padx=2) #create damage button for player 2
        ttk.Button(p2_frame, text="Heal +", command=lambda: self.show_calc_screen(2, "heal")).pack(side="left", padx=2) #create heal button for player 2
        ttk.Button(p2_frame, text="Halve", command=lambda: self.halve_lp(2)).pack(side="left", padx=2) #create halve button for player 2

    def create_settings_tab(self): #draw the settings tab on the window
        for widget in self.settings_tab.winfo_children(): 
            widget.destroy()

        ttk.Label(self.settings_tab, text="Settings", font=("Arial", 16, "bold")).pack(pady=(10, 15)) #create settings label

        ttk.Button(self.settings_tab, text="Change Player Names", command=self.open_name_editor).pack(pady=20) #create button to change player names

        ttk.Button(self.settings_tab, text="Change Starting Life Points", command=self.open_starting_lp_editor).pack(pady=10) #create button to change starting lifepoints

    def open_name_editor(self): #open popup window to edit player names
        popup = tk.Toplevel(self) #open a popup window
        popup.title("Edit Player Names") #set title for popup window
        popup.geometry("300x210") #set dimensions for popup window
        popup.resizable(False, False) #make popup window non-resizable
        popup.grab_set()  #give the popup window focus

        ttk.Label(popup, text="Edit Player Names", font=("Arial", 14, "bold")).pack(pady=10) #create label for popup window

        # Entry for Player 1
        ttk.Label(popup, text="Player 1 Name:").pack() 
        p1_entry = ttk.Entry(popup, width=25) #create entry box for player 1 name
        p1_entry.insert(0, self.game.player1.name)  # pre-fill current name
        p1_entry.pack(pady=5)

        # Entry for Player 2
        ttk.Label(popup, text="Player 2 Name:").pack()
        p2_entry = ttk.Entry(popup, width=25) #create entry box for player 2 name
        p2_entry.insert(0, self.game.player2.name) # pre-fill current name
        p2_entry.pack(pady=5)

        def save_names(): #function to save the names entered in the entry boxes
            name1 = p1_entry.get().strip() or "Player 1" #default to "Player 1" if entry is empty
            name2 = p2_entry.get().strip() or "Player 2" #default to "Player 2" if entry is empty
            self.game.player1.name = name1 #update player 1 name
            self.game.player2.name = name2 #update player 2 name
            self.show_main_screen() #refresh main screen to show updated names
            popup.destroy() #close popup window

        ttk.Button(popup, text="Save", command=save_names).pack(pady=15) #create save button
        popup.bind("<Return>", lambda e: save_names()) #make enter key save names

    def open_starting_lp_editor(self): #open popup window to edit starting lifepoints
        popup = tk.Toplevel(self) #open a popup window
        popup.title("Edit Starting Life Points") #set title for popup window
        popup.geometry("300x180") #set dimensions for popup window
        popup.resizable(False, False) #make popup window non-resizable
        popup.grab_set()  #give the popup window focus

        ttk.Label(popup, text="Change Starting LP", font=("Arial", 14, "bold")).pack(pady=10) #create label for popup window

        # LP entry
        ttk.Label(popup, text="Starting Life Points:").pack() #
        lp_entry = ttk.Entry(popup, width=20) #create entry box for starting lifepoints
        lp_entry.insert(0, str(self.game.starting_lp)) # pre-fill current starting lifepoint value
        lp_entry.pack(pady=5)

        def save_lp(): #function to save the starting lifepoint value entered in the entry box
            try: #try to convert entry to integer
                new_lp = int(lp_entry.get()) #get value from entry box
                if new_lp <= 0: 
                    raise ValueError #raise error if value is not positive

                # Update both players and refresh UI
                self.game.starting_lp = new_lp #update starting lifepoint value
                self.game.player1.reset_lp(new_lp) #reset player 1 lifepoints to new starting value
                self.game.player2.reset_lp(new_lp) #reset player 2 lifepoints to new starting value
                self.update_display() #refresh main screen to show updated lifepoint values
                popup.destroy() #close popup window
            except ValueError:
                lp_entry.delete(0, tk.END) #clear entry box
                lp_entry.insert(0, "Invalid") #insert "Invalid" into entry box if entry is not a valid integer

        ttk.Button(popup, text="Save", command=save_lp).pack(pady=15) #create save button
        popup.bind("<Return>", lambda e: save_lp()) #make enter key save lifepoint value

    def show_calc_screen(self, player_num, action): #draw the calculation screen for damage/heal input
        self.clear_game_tab() #clear the game tab

        player = self.game.player1 if player_num == 1 else self.game.player2 #get the player object based on player number
        ttk.Label(self.game_tab, text=f"{player.name} - {action.capitalize()}", font=("Arial", 16, "bold")).pack(pady=20) #create label for calculation screen
        ttk.Label(self.game_tab, text=f"Current LP: {player.lp}", font=("Arial", 12)).pack(pady=(0, 10)) #create label to show current lifepoint value

        ttk.Label(self.game_tab, text=f"Enter value to {action}:").pack(pady=5) #create label for entry box
        entry = ttk.Entry(self.game_tab) #create entry box for damage/heal value
        entry.pack() 
        entry.focus() #give focus to entry box

        def confirm(event=None): #function to confirm the damage/heal value entered in the entry box
            try: #try to convert entry to integer
                value = int(entry.get()) #get value from entry box
                if action == "damage": 
                    self.change_lp(player_num, -value) #apply damage to player if action is "damage"
                elif action == "heal":
                    self.change_lp(player_num, value) #apply heal to player if action is "heal"
                self.show_main_screen()
            except ValueError:
                entry.delete(0, tk.END) #clear entry box
                entry.insert(0, "Invalid") #insert "Invalid" into entry box if entry is not a valid integer

        def cancel(): #function to cancel the damage/heal input and return to main screen
            self.show_main_screen()

        ttk.Button(self.game_tab, text="Confirm", command=confirm).pack(pady=10) #create confirm button
        ttk.Button(self.game_tab, text="Cancel", command=cancel).pack() #create cancel button

        self.bind("<Return>", confirm) #make enter key confirm input
        self.bind("<Escape>", lambda e: cancel()) #make escape key cancel input and return to main screen

    def clear_game_tab(self): #clear all widgets from the game tab
        for widget in self.game_tab.winfo_children():
            widget.destroy()

    def change_lp(self, player_num, mode): #change the lifepoint value of the given player by the given mode (positive for heal, negative for damage)
        player = self.game.player1 if player_num == 1 else self.game.player2 #get the player object
        old_value = player.lp #store the old lifepoint value
        if mode < 0:
            player.damage(abs(mode)) #apply damage to player if mode value is negative
        else:
            player.heal(mode) #apply heal to player if mode value is positive
        new_value = player.lp #update players lifepoints to new value
        self.animate_lp_change(player_num, old_value, new_value) #animate the lifepoint change

    def halve_lp(self, player_num): #halve the lifepoint value of the given player
        player = self.game.player1 if player_num == 1 else self.game.player2 #get the player object
        old_value = player.lp #store the old lifepoint value
        player.halve_lp() #halve the players lifepoints
        new_value = player.lp #update players lifepoints to new value
        self.animate_lp_change(player_num, old_value, new_value) #animate the lifepoint change

    def reset_all_lp(self): #reset both players lifepoint values to the starting value
        confirm = messagebox.askyesno("Confirm Reset", f"Reset both players' Life Points to {self.game.starting_lp}?") #ask user to confirm reset
        if confirm: #if user confirms reset
            self.game.player1.reset_lp(self.game.starting_lp) #reset player 1 lifepoints to starting value
            self.game.player2.reset_lp(self.game.starting_lp) #reset player 2 lifepoints to starting value
            self.update_display() #refresh main screen to show updated lifepoint values

    def update_display(self): #update the lifepoint display for both players
        self.lp1_var.set(str(self.game.player1.lp)) 
        self.lp2_var.set(str(self.game.player2.lp))
    
    def animate_lp_change(self, player_num: int, old_value: int, new_value: int, duration: int = 1300): 
        steps = 60  #number of animation steps/frames
        delay = duration // steps #delay between each step in milliseconds
        delta = (new_value - old_value) / steps #change in lifepoint value per step
        current = old_value #current lifepoint value
        count = 0 

        threading.Thread(target=lambda: self.lp_count_sound.play()).start() #play counting sound effect in a separate thread

        def update_step(): #function to update the lifepoint value for each step of the animation
            nonlocal current, count #use nonlocal to modify variables from the outer scope
            if count < steps:
                current += delta #increment current lifepoint value by delta
                display_value = int(round(current)) #round current value to nearest integer for display
                #update the appropriate player's lifepoint display
                if player_num == 1: 
                    self.lp1_var.set(str(display_value))
                else:
                    self.lp2_var.set(str(display_value))
                count += 1 #increment step count
                self.after(delay, update_step)
            #final update to ensure exact new value is displayed
            else: 
                if player_num == 1: 
                    self.lp1_var.set(str(new_value))
                else:
                    self.lp2_var.set(str(new_value))
                threading.Thread(target=lambda: self.lp_end_sound.play()).start() #play updated sound effect in a separate thread

        self.after(100, update_step()) #wait specified ms delay and then start animation

    def load_sound_theme(self, theme_name: str, overrides: dict | None = None):
        """Load a sound theme, optionally mixing custom overrides."""

        base_path = os.path.join("sounds", theme_name)
        self.sounds = {}

        def load_sound(filename, folder=base_path):
            path = os.path.join(folder, filename)
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(0.5)
                return sound
            return None

        # Default sounds for the theme
        for key in ["lp_count", "lp_end", "damage", "heal", "halve"]:
            self.sounds[key] = load_sound(f"{key}.wav")

        # Apply overrides if provided (Custom theme)
        if overrides:
            for key, (override_theme, file_name) in overrides.items():
                override_path = os.path.join("sounds", override_theme, file_name)
                if os.path.exists(override_path):
                    self.sounds[key] = pygame.mixer.Sound(override_path)
                    self.sounds[key].set_volume(0.5)

        self.current_theme = theme_name
        self.current_overrides = overrides or {}
        
if __name__ == "__main__": 
    app = LifePointAppGUI() #create and run the GUI app
    app.mainloop() #start the main event loop