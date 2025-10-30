import os, sys, threading
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from utils.helpers import resource_path, load_settings, save_settings
from game_modes.yugioh.game import Game
from game_modes.yugioh.logic import LifePointController
from game_modes.yugioh.theme import SoundThemeManager


class YuGiOhFrame(ctk.CTkFrame):
    def __init__(self, master, config_data):
        super().__init__(master)
        self.master = master
        self.settings = config_data["yugioh"]
        self.current_overrides = self.settings.get("sound_paths", {})
        self.current_theme = self.settings["theme"]
        self.messagebox = messagebox

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
        self.lp1_var = ctk.StringVar(value=str(self.game.player1.lp))
        self.lp2_var = ctk.StringVar(value=str(self.game.player2.lp))

        # ✅ Tabs (single creation only)
        self.notebook = ctk.CTkTabview(self, command=self.on_tab_change)
        self.notebook.pack(expand=True, fill="both")

        # ✅ Create tabs AFTER defining notebook
        self.game_tab = self.notebook.add("Game")
        self.settings_tab = self.notebook.add("Settings")

        # Draw interface
        self.show_main_screen()
        self.create_settings_tab()
        self.sfx.play_sound("refresh")

    # ----------------------------
    # Event handlers
    # ----------------------------
    def on_tab_change(self):
        selected_tab = self.notebook.get()
        if selected_tab == "Game":
            self.show_main_screen()


    # ----------------------------
    # Game screen
    # ----------------------------
    def show_main_screen(self):
        self.clear_game_tab()

        top_frame1 = ctk.CTkFrame(self.game_tab)
        top_frame1.pack(padx=5, pady=5, anchor="nw")
        ctk.CTkButton(top_frame1, text="Back", command=self.master.back_to_main_menu).pack(side="left")

        top_frame = ctk.CTkFrame(self.game_tab)
        top_frame.pack(pady=(10, 5))
        ctk.CTkButton(top_frame, text="Reset", command=self.lp_controller.reset_all_lp).pack(side="left", padx=5)
        

        # Player 1
        ctk.CTkLabel(self.game_tab, text=self.game.player1.name, font=("Arial", 14, "bold")).pack(pady=(10, 0))
        ctk.CTkLabel(self.game_tab, textvariable=self.lp1_var, font=("Arial", 20)).pack()
        p1_frame = ctk.CTkFrame(self.game_tab)
        p1_frame.pack(pady=5)
        ctk.CTkButton(p1_frame, text="Damage -", command=lambda: self.show_calc_screen(1, "damage")).pack(side="left", padx=2)
        ctk.CTkButton(p1_frame, text="Heal +", command=lambda: self.show_calc_screen(1, "heal")).pack(side="left", padx=2)
        ctk.CTkButton(p1_frame, text="Halve", command=lambda: self.lp_controller.halve_lp(1)).pack(side="left", padx=2)

        # Player 2
        ctk.CTkLabel(self.game_tab, text=self.game.player2.name, font=("Arial", 14, "bold")).pack(pady=(15, 0))
        ctk.CTkLabel(self.game_tab, textvariable=self.lp2_var, font=("Arial", 20)).pack()
        p2_frame = ctk.CTkFrame(self.game_tab)
        p2_frame.pack(pady=5)
        ctk.CTkButton(p2_frame, text="Damage -", command=lambda: self.show_calc_screen(2, "damage")).pack(side="left", padx=2)
        ctk.CTkButton(p2_frame, text="Heal +", command=lambda: self.show_calc_screen(2, "heal")).pack(side="left", padx=2)
        ctk.CTkButton(p2_frame, text="Halve", command=lambda: self.lp_controller.halve_lp(2)).pack(side="left", padx=2)

    # ----------------------------
    # Settings tab
    # ----------------------------
    def create_settings_tab(self):
        for widget in self.settings_tab.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.settings_tab, text="Settings", font=("Arial", 16, "bold")).pack(pady=(10, 15))

        ctk.CTkButton(self.settings_tab, text="Change Player Names", command=self.open_name_editor).pack(pady=10)
        ctk.CTkButton(self.settings_tab, text="Change Starting Life Points", command=self.open_starting_lp_editor).pack(pady=5)

        ctk.CTkLabel(self.settings_tab, text="Select Sound Theme:").pack(pady=(20, 5))
        frame = ctk.CTkFrame(self.settings_tab)
        frame.pack(pady=5)

        # ✅ Corrected CTkOptionMenu
        self.theme_var = ctk.StringVar(value=self.current_theme)
        theme_selector = ctk.CTkOptionMenu(
            master=frame,
            values=list(self.theme_map.keys()),
            variable=self.theme_var,
            command=self.on_theme_change
        )
        theme_selector.pack(side="left", padx=(0, 10))

        ctk.CTkButton(frame, text="Customize...", command=self.open_custom_theme_editor).pack(side="left")


    def on_theme_change(self, selected):
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

    # ----------------------------
    # Player editing popups
    # ----------------------------
    def open_name_editor(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Player Names")
        popup.geometry("300x260")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Edit Player Names", font=("Arial", 14, "bold")).pack(pady=10)

        # Player 1
        ctk.CTkLabel(popup, text="Player 1 Name:").pack()
        p1_entry = ctk.CTkEntry(popup, width=200)  # ✅ Fixed
        p1_entry.insert(0, self.game.player1.name)
        p1_entry.pack(pady=5)

        # Player 2
        ctk.CTkLabel(popup, text="Player 2 Name:").pack()
        p2_entry = ctk.CTkEntry(popup, width=200)  # ✅ Fixed
        p2_entry.insert(0, self.game.player2.name)
        p2_entry.pack(pady=5)

        def save_names():
            name1 = p1_entry.get().strip() or "Player 1"
            name2 = p2_entry.get().strip() or "Player 2"
            self.game.player1.name = name1
            self.game.player2.name = name2
            self.settings["player1_name"] = name1
            self.settings["player2_name"] = name2

            # Save and refresh
            save_settings({"yugioh": self.settings})
            self.show_main_screen()
            popup.destroy()

        ctk.CTkButton(popup, text="Save", command=save_names).pack(pady=15)
        popup.bind("<Return>", lambda e: save_names())


    def open_starting_lp_editor(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Starting Life Points")
        popup.geometry("300x180")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Change Starting LP", font=("Arial", 14, "bold")).pack(pady=10)
        ctk.CTkLabel(popup, text="Starting Life Points:").pack()

        lp_entry = ctk.CTkEntry(popup, width=200)  # ✅ Fixed
        lp_entry.insert(0, str(self.game.starting_lp))
        lp_entry.pack(pady=5)

        def save_lp():
            try:
                new_lp = int(lp_entry.get())
                if new_lp <= 0:
                    raise ValueError

                self.game.starting_lp = new_lp
                self.game.player1.reset_lp(new_lp)
                self.game.player2.reset_lp(new_lp)
                self.settings["starting_lp"] = new_lp

                save_settings({"yugioh": self.settings})
                self.lp1_var.set(str(new_lp))
                self.lp2_var.set(str(new_lp))

                popup.destroy()
            except ValueError:
                lp_entry.delete(0, ctk.END)
                lp_entry.insert(0, "Invalid")

        ctk.CTkButton(popup, text="Save", command=save_lp).pack(pady=15)
        popup.bind("<Return>", lambda e: save_lp())

    def open_custom_theme_editor(self):
        """Popup for customizing the Yu-Gi-Oh sound theme."""
        popup = ctk.CTkToplevel(self)
        popup.title("Customize Sound Theme")
        popup.geometry("420x320")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Customize Sound Theme",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Get sound paths and theme mapping
        sound_paths = self.settings.get("sound_paths", {})
        reverse_theme_map = {v: k for k, v in self.theme_map.items()}

        sound_keys = ["LP_counting", "LP_updated", "LP_empty", "Refresh"]
        available_themes = list(self.theme_map.keys())  # No "Custom"

        selections = {}

        for key in sound_keys:
            frame = ctk.CTkFrame(popup)
            frame.pack(pady=6, padx=20, fill="x")

            # Label for sound type
            ctk.CTkLabel(
                frame,
                text=key.replace("_", " ").title() + ":",
                anchor="w"
            ).pack(side="left", padx=5)

            folder_value = sound_paths.get(key, "basic")
            current_theme = reverse_theme_map.get(folder_value, "Basic")
            var = ctk.StringVar(value=current_theme)

            # ✅ Proper CTkOptionMenu usage
            combo = ctk.CTkOptionMenu(
                master=frame,
                variable=var,
                values=available_themes,
                width=160,
                height=30,
                corner_radius=8
            )
            combo.pack(side="right", padx=10)
            selections[key] = var

        # Save button
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

            self.sfx.play_sound("refresh")
            popup.destroy()

        ctk.CTkButton(
            popup,
            text="Save Custom Theme",
            command=save_custom_theme,
            width=200,
            height=40,
            corner_radius=10
        ).pack(pady=20)

    def show_calc_screen(self, player_num, action):
        self.clear_game_tab()

        player = self.game.player1 if player_num == 1 else self.game.player2
        ctk.CTkLabel(self.game_tab, text=f"{player.name} - {action.capitalize()}",
                font=("Arial", 16, "bold")).pack(pady=20)

        ctk.CTkLabel(self.game_tab, text=f"Current LP: {player.lp}", font=("Arial", 12)).pack(pady=(0, 10))
        ctk.CTkLabel(self.game_tab, text=f"Enter value to {action}:").pack(pady=5)
        entry = ctk.CTkEntry(self.game_tab)
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
                entry.delete(0, ctk.END)
                entry.insert(0, "Invalid")
            return "break"

        def cancel(event=None):
            self.show_main_screen()

        # Buttons
        ctk.CTkButton(self.game_tab, text="Confirm", command=confirm).pack(pady=10)
        ctk.CTkButton(self.game_tab, text="Cancel", command=cancel).pack()

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

