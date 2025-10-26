import os, sys, threading
import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import resource_path, load_settings, save_settings
from game_modes.yugioh.game import Game
from game_modes.yugioh.logic import LifePointController
from game_modes.yugioh.theme import SoundThemeManager


class YuGiOhFrame(ttk.Frame):
    def __init__(self, master, config_data):
        super().__init__(master)
        self.master = master
        self.settings = config_data["yugioh"]
        self.current_overrides = self.settings.get("sound_paths", {})
        self.current_theme = self.settings["theme"]
        self.messagebox = messagebox

        # Window setup
        icon_path = resource_path("assets/icons/icon.png")
        master.iconphoto(False, tk.PhotoImage(file=icon_path))
        master.title(f"Yu-Gi-Oh! Life Points — Theme: {self.current_theme}")

        # Theme map (for sound folders)
        self.theme_map = {
            "Basic": "basic",
            "Duel Monsters": "dm",
            "GX": "gx",
            "5DS": "5ds",
            "Zexal": "zexal",
            "Arc-V": "arcv",
            "Vrains": "vrains",
        }

        # Game setup
        self.game = Game(starting_lp=self.settings["starting_lp"])
        self.game.player1.name = self.settings["player1_name"]
        self.game.player2.name = self.settings["player2_name"]

        # Sound + LP controller
        self.sfx = SoundThemeManager(self.settings, self.theme_map)
        self.lp_controller = LifePointController(self)

        # StringVars for UI
        self.lp1_var = tk.StringVar(value=str(self.game.player1.lp))
        self.lp2_var = tk.StringVar(value=str(self.game.player2.lp))

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.game_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.game_tab, text="Game")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.pack(expand=True, fill="both")
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Draw interface
        self.show_main_screen()
        self.create_settings_tab()

    # ----------------------------
    # Event handlers
    # ----------------------------
    def on_tab_change(self, event):
        """Handle tab switching."""
        self.update_idletasks()
        selected_tab = event.widget.tab(event.widget.index("current"))["text"]
        if selected_tab == "Game":
            self.show_main_screen()
            self.sfx.play_sound("refresh")

    # ----------------------------
    # Game screen
    # ----------------------------
    def show_main_screen(self):
        self.clear_game_tab()

        top_frame = ttk.Frame(self.game_tab)
        top_frame.pack(pady=(10, 5))
        ttk.Button(top_frame, text="Reset", command=self.lp_controller.reset_all_lp).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Back to Menu", command=self.master.show_game_selector).pack(side="left", padx=5)

        # Player 1
        ttk.Label(self.game_tab, text=self.game.player1.name, font=("Arial", 14, "bold")).pack(pady=(10, 0))
        ttk.Label(self.game_tab, textvariable=self.lp1_var, font=("Arial", 20)).pack()
        p1_frame = ttk.Frame(self.game_tab)
        p1_frame.pack(pady=5)
        ttk.Button(p1_frame, text="Damage -", command=lambda: self.show_calc_screen(1, "damage")).pack(side="left", padx=2)
        ttk.Button(p1_frame, text="Heal +", command=lambda: self.show_calc_screen(1, "heal")).pack(side="left", padx=2)
        ttk.Button(p1_frame, text="Halve", command=lambda: self.lp_controller.halve_lp(1)).pack(side="left", padx=2)

        # Player 2
        ttk.Label(self.game_tab, text=self.game.player2.name, font=("Arial", 14, "bold")).pack(pady=(15, 0))
        ttk.Label(self.game_tab, textvariable=self.lp2_var, font=("Arial", 20)).pack()
        p2_frame = ttk.Frame(self.game_tab)
        p2_frame.pack(pady=5)
        ttk.Button(p2_frame, text="Damage -", command=lambda: self.show_calc_screen(2, "damage")).pack(side="left", padx=2)
        ttk.Button(p2_frame, text="Heal +", command=lambda: self.show_calc_screen(2, "heal")).pack(side="left", padx=2)
        ttk.Button(p2_frame, text="Halve", command=lambda: self.lp_controller.halve_lp(2)).pack(side="left", padx=2)

    # ----------------------------
    # Settings tab
    # ----------------------------
    def create_settings_tab(self):
        for widget in self.settings_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.settings_tab, text="Settings", font=("Arial", 16, "bold")).pack(pady=(10, 15))

        ttk.Button(self.settings_tab, text="Change Player Names", command=self.open_name_editor).pack(pady=10)
        ttk.Button(self.settings_tab, text="Change Starting Life Points", command=self.open_starting_lp_editor).pack(pady=5)

        ttk.Label(self.settings_tab, text="Select Sound Theme:").pack(pady=(20, 5))
        frame = ttk.Frame(self.settings_tab)
        frame.pack(pady=5)

        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_selector = ttk.Combobox(
            frame,
            textvariable=self.theme_var,
            values=list(self.theme_map.keys()),
            state="readonly",
            width=20,
        )
        theme_selector.pack(side="left", padx=(0, 10))
        ttk.Button(frame, text="Customize...", command=self.open_custom_theme_editor).pack(side="left")

        def on_theme_change(event=None):
            selected = self.theme_var.get()
            self.sfx.load_theme(selected)
            self.current_theme = selected
            self.settings["theme"] = selected
            if selected != "Custom":
                self.settings["sound_paths"] = {
                    "LP_counting": self.theme_map[selected],
                    "LP_updated": self.theme_map[selected],
                    "LP_empty": self.theme_map[selected],
                    "Refresh": self.theme_map[selected]
                }
            save_settings({"yugioh": self.settings})
            self.master.title(f"Yu-Gi-Oh! Life Points — Theme: {selected}")
            self.sfx.play_sound("refresh")

        theme_selector.bind("<<ComboboxSelected>>", on_theme_change)

    # ----------------------------
    # Player editing popups
    # ----------------------------
    def open_name_editor(self):
        popup = tk.Toplevel(self)
        popup.title("Edit Player Names")
        popup.geometry("300x210")
        popup.resizable(False, False)
        popup.grab_set()

        ttk.Label(popup, text="Edit Player Names", font=("Arial", 14, "bold")).pack(pady=10)

        # Player 1
        ttk.Label(popup, text="Player 1 Name:").pack()
        p1_entry = ttk.Entry(popup, width=25)
        p1_entry.insert(0, self.game.player1.name)
        p1_entry.pack(pady=5)

        # Player 2
        ttk.Label(popup, text="Player 2 Name:").pack()
        p2_entry = ttk.Entry(popup, width=25)
        p2_entry.insert(0, self.game.player2.name)
        p2_entry.pack(pady=5)

        def save_names():
            # Read input or fall back to defaults
            name1 = p1_entry.get().strip() or "Player 1"
            name2 = p2_entry.get().strip() or "Player 2"

            # Update objects
            self.game.player1.name = name1
            self.game.player2.name = name2
            self.settings["player1_name"] = name1
            self.settings["player2_name"] = name2

            # Persist to config
            save_settings({"yugioh": self.settings})

            # Refresh GUI
            self.show_main_screen()
            self.sfx.play_sound("refresh")
            popup.destroy()

        ttk.Button(popup, text="Save", command=save_names).pack(pady=15)
        popup.bind("<Return>", lambda e: save_names())


    def open_starting_lp_editor(self):
        popup = tk.Toplevel(self)
        popup.title("Edit Starting Life Points")
        popup.geometry("300x180")
        popup.resizable(False, False)
        popup.grab_set()

        ttk.Label(popup, text="Change Starting LP", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(popup, text="Starting Life Points:").pack()

        lp_entry = ttk.Entry(popup, width=20)
        lp_entry.insert(0, str(self.game.starting_lp))
        lp_entry.pack(pady=5)

        def save_lp():
            try:
                new_lp = int(lp_entry.get())
                if new_lp <= 0:
                    raise ValueError

                # Update logic + settings
                self.game.starting_lp = new_lp
                self.game.player1.reset_lp(new_lp)
                self.game.player2.reset_lp(new_lp)
                self.settings["starting_lp"] = new_lp

                # Persist and refresh
                save_settings({"yugioh": self.settings})
                self.lp1_var.set(str(new_lp))
                self.lp2_var.set(str(new_lp))
                self.sfx.play_sound("refresh")

                popup.destroy()
            except ValueError:
                lp_entry.delete(0, tk.END)
                lp_entry.insert(0, "Invalid")

        ttk.Button(popup, text="Save", command=save_lp).pack(pady=15)
        popup.bind("<Return>", lambda e: save_lp())

    def open_custom_theme_editor(self):
        """Popup for customizing the Yu-Gi-Oh sound theme."""
        popup = tk.Toplevel(self)
        popup.title("Customize Sound Theme")
        popup.geometry("400x270")
        popup.resizable(False, False)
        popup.grab_set()

        ttk.Label(popup, text="Customize Sound Theme", font=("Arial", 14, "bold")).pack(pady=10)

        # Get sound paths and theme mapping
        sound_paths = self.settings.get("sound_paths", {})
        reverse_theme_map = {v: k for k, v in self.theme_map.items()}

        sound_keys = ["LP_counting", "LP_updated", "LP_empty", "Refresh"]
        available_themes = list(self.theme_map.keys())  # No "Custom"

        selections = {}

        for key in sound_keys:
            frame = ttk.Frame(popup)
            frame.pack(pady=5)
            ttk.Label(frame, text=key.replace("_", " ").title() + ":").pack(side="left", padx=5)

            folder_value = sound_paths.get(key, "basic")
            current_theme = reverse_theme_map.get(folder_value, "Basic")
            var = tk.StringVar(value=current_theme)

            combo = ttk.Combobox(
                frame, textvariable=var, values=available_themes, state="readonly", width=15
            )
            combo.pack(side="left")
            selections[key] = var

        def save_custom_theme():
            """Save per-sound theme selections to settings and reload."""
            new_sound_paths = {}
            for key, var in selections.items():
                display_name = var.get()
                folder_name = self.theme_map.get(display_name, "basic")
                new_sound_paths[key] = folder_name

            # Update config.json
            self.settings["theme"] = "Custom"
            self.settings["sound_paths"] = new_sound_paths
            self.current_overrides = new_sound_paths
            self.current_theme = "Custom"

            save_settings({"yugioh": self.settings})
            self.sfx.load_theme("Custom")


            self.master.title("Yu-Gi-Oh! Life Points — Theme: Custom")
            if hasattr(self, 'theme_var'):
                self.theme_var.set("Custom")

            # Play confirmation sound
            self.sfx.play_sound("refresh")

            popup.destroy()

        ttk.Button(popup, text="Save Custom Theme", command=save_custom_theme).pack(pady=20)

    def show_calc_screen(self, player_num, action):
        self.clear_game_tab()

        player = self.game.player1 if player_num == 1 else self.game.player2
        ttk.Label(self.game_tab, text=f"{player.name} - {action.capitalize()}",
                font=("Arial", 16, "bold")).pack(pady=20)

        ttk.Label(self.game_tab, text=f"Current LP: {player.lp}", font=("Arial", 12)).pack(pady=(0, 10))
        ttk.Label(self.game_tab, text=f"Enter value to {action}:").pack(pady=5)
        entry = ttk.Entry(self.game_tab)
        entry.pack()
        entry.focus()

        def confirm(event=None):
            try:
                value = int(entry.get())
                if action == "damage":
                    self.lp_controller.change_lp(player_num, -value)
                elif action == "heal":
                    self.lp_controller.change_lp(player_num, value)
                self.show_main_screen()
            except ValueError:
                entry.delete(0, tk.END)
                entry.insert(0, "Invalid")
            return "break"

        def cancel(event=None):
            self.show_main_screen()

        # Buttons
        ttk.Button(self.game_tab, text="Confirm", command=confirm).pack(pady=10)
        ttk.Button(self.game_tab, text="Cancel", command=cancel).pack()

        # ✅ Key bindings (focus-aware)
        entry.bind("<Return>", confirm)     # Press Enter inside the entry box
        self.master.bind("<Return>", confirm)  # Fallback: global Enter
        self.master.bind("<Escape>", cancel)

    # ----------------------------
    # UI helpers
    # ----------------------------
    def clear_game_tab(self):
        for widget in self.game_tab.winfo_children():
            widget.destroy()

        # ----------------------------
    # LP Animation
    # ----------------------------
    def animate_lp_change(self, player_num: int, old_value: int, new_value: int, duration: int = 1200):
        """Smoothly animate LP change with sound."""
        steps = 60
        delay = duration // steps
        delta = (new_value - old_value) / steps
        current = old_value
        count = 0

        # Play counting sound
        self.sfx.play_sound("lp_count")

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
                # Final update
                if player_num == 1:
                    self.lp1_var.set(str(new_value))
                else:
                    self.lp2_var.set(str(new_value))

                # Play ending sound
                if new_value == 0:
                    self.sfx.play_sound("lp_empty")
                else:
                    self.sfx.play_sound("lp_updated")

        # Start animation
        self.after(100, update_step)
    
    def update_display(self):
        """Update both players' LP display."""
        self.lp1_var.set(str(self.game.player1.lp))
        self.lp2_var.set(str(self.game.player2.lp))

