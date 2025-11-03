import customtkinter as ctk
from tkinter import messagebox
from utils.helpers import save_settings
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
        self.sfx = SoundThemeManager(config_data, self.theme_map)
        self.lp_controller = LifePointController(self)

        # StringVars for UI
        self.lp1_var = ctk.StringVar(value=str(self.game.player1.lp))
        self.lp2_var = ctk.StringVar(value=str(self.game.player2.lp))

        # Build main screen
        self.show_main_screen()
        self.sfx.play_sound("Refresh")


    # ----------------------------
    # Main game screen
    # ----------------------------
    def show_main_screen(self):
        # ----------------------------
        # Top Bar
        # ----------------------------
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", side="top", pady=(10, 0), padx=5)
        top_bar.grid_columnconfigure(0, weight=1)  # left spacer
        top_bar.grid_columnconfigure(1, weight=3)  # title area
        top_bar.grid_columnconfigure(2, weight=1)  # right spacer

        back_button = ctk.CTkButton(
            top_bar,
            text="",
            image=self.master.icons["back"],
            text_color=self.master.colour_theme["text_primary"],
            fg_color="transparent",
            hover_color=self.master.colour_theme["button_hover"],
            font=("Ariel", 16),
            width=40,
            height=40,
            corner_radius=8,
            command=self.master.back_to_main_menu
        )
        back_button.grid(row=0, column=0, sticky="w", padx=5)

        title_label = ctk.CTkLabel(
            top_bar,
            text="Yu-Gi-Oh!",
            font=self.master.fonts["heading"],
            pady = 6
        )
        title_label.grid(row=0, column=1, padx=5)

        settings_button = ctk.CTkButton(
            top_bar,
            text="",
            image=self.master.icons["settings"],
            text_color=self.master.colour_theme["text_primary"],
            fg_color="transparent",
            hover_color=self.master.colour_theme["button_hover"],
            font=("Arial", 20),
            width=40,
            height=40,
            corner_radius=8,
            command=lambda: self.change_screen(self.show_settings_screen)
        )
        settings_button.grid(row=0, column=2, sticky="e", padx=5)

        # Player 1
        ctk.CTkLabel(self, text=self.game.player1.name, font=("Arial", 14, "bold"), pady=6).pack(pady=(10, 0))
        ctk.CTkLabel(self, textvariable=self.lp1_var, font=("Arial", 20)).pack()
        p1_frame = ctk.CTkFrame(self)
        p1_frame.pack(pady=5)
        ctk.CTkButton(p1_frame, text="Damage -",
                      command=lambda: self.change_screen(lambda: self.show_calc_screen(1, "damage"))).pack(side="left", padx=2)
        ctk.CTkButton(p1_frame, text="Heal +",
                      command=lambda: self.change_screen(lambda: self.show_calc_screen(1, "heal"))).pack(side="left", padx=2)
        ctk.CTkButton(p1_frame, text="Halve",
                      command=lambda: self.lp_controller.halve_lp(1)).pack(side="left", padx=2)

        # Player 2
        ctk.CTkLabel(self, text=self.game.player2.name, font=("Arial", 14, "bold"), pady=6).pack(pady=(15, 0))
        ctk.CTkLabel(self, textvariable=self.lp2_var, font=("Arial", 20)).pack()
        p2_frame = ctk.CTkFrame(self)
        p2_frame.pack(pady=5)
        ctk.CTkButton(p2_frame, text="Damage -",
                      command=lambda: self.change_screen(lambda: self.show_calc_screen(2, "damage"))).pack(side="left", padx=2)
        ctk.CTkButton(p2_frame, text="Heal +",
                      command=lambda: self.change_screen(lambda: self.show_calc_screen(2, "heal"))).pack(side="left", padx=2)
        ctk.CTkButton(p2_frame, text="Halve",
                      command=lambda: self.lp_controller.halve_lp(2)).pack(side="left", padx=2)

    # ----------------------------
    # Settings screen 
    # ----------------------------
    def show_settings_screen(self):
        # ----------------------------
        # Top Bar
        # ----------------------------
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", side="top", pady=(10, 0), padx=5)
        top_bar.grid_columnconfigure(0, weight=1)  # left spacer
        top_bar.grid_columnconfigure(1, weight=3)  # title area
        top_bar.grid_columnconfigure(2, weight=1)  # right spacer

        # ← Back Button
        back_button = ctk.CTkButton(
            top_bar,
            text="",
            image=self.master.icons["back"],
            text_color=self.master.colour_theme["text_primary"],
            fg_color="transparent",
            hover_color=self.master.colour_theme["button_hover"],
            font=("Ariel", 16),
            width=40,
            height=40,
            corner_radius=8,
            command=lambda: self.change_screen(self.show_main_screen)
        )
        back_button.grid(row=0, column=0, sticky="w", padx=5)

        # 🏷️ Title Label
        title_label = ctk.CTkLabel(
            top_bar,
            text="Settings",
            font=self.master.fonts["heading"],
            pady=6
        )
        title_label.grid(row=0, column=1, padx=5)

        # Right Placeholder (non-interactive)
        placeholder = ctk.CTkLabel(top_bar, text="", width=40)
        placeholder.grid(row=0, column=2, sticky="e", padx=5)

        # ----------------------------
        # Settings Content (rows)
        # ----------------------------
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=20, pady=12)

        def add_row(label_text, widget_factory, stretch_right=False):
            """Adds a new row (label + widget) using pack layout."""
            row = ctk.CTkFrame(content, fg_color="transparent")
            row.pack(fill="x", pady=6, padx=20)

            label = ctk.CTkLabel(row, text=label_text, font=self.master.fonts["body"], pady=6)
            label.pack(side="left")

            widget = widget_factory(row)
            if stretch_right:
                widget.pack(side="right", fill="x", expand=True)
            else:
                widget.pack(side="right")

        def add_separator(text):
            sep = ctk.CTkLabel(
                content,
                text=text,
                font=self.master.fonts["body"],
                text_color=self.master.colour_theme["text_primary"],
                pady=6
            )
            sep.pack(fill="x", pady=(25, 5))
        
        # --- Appearance (Dark / Light)
        def make_theme_switch(parent):
            switch = ctk.CTkSwitch(parent, text="")

            def on_toggle():
                # toggle app theme using your existing API
                self.master.toggle_theme(switch, lambda: self.change_screen(self.show_settings_screen))

            switch.configure(command=on_toggle)

            if self.master.config_data["global"]["selected_theme"] == "dark":
                switch.select()
            return switch

        add_row("Appearance (Dark Mode)", make_theme_switch)

        # --- Volume Slider
        def make_volume_slider(parent):
            slider = ctk.CTkSlider(
                parent,
                from_=0,
                to=1,
                number_of_steps=100,
            )
            slider.set(self.master.config_data["global"].get("volume", 1.0))

            # Save current value on release
            def on_release(event):
                value = round(slider.get(), 2)
                self.master.set_volume(value)  # save to config + update global volume
                if hasattr(self, "sfx") and hasattr(self.sfx, "sounds"):
                    # Apply new volume to all loaded sounds
                    for sound in self.sfx.sounds.values():
                        sound.set_volume(value)

            # Bind left mouse release to commit
            slider.bind("<ButtonRelease-1>", on_release)

            return slider

        add_row("Sound Volume", make_volume_slider, stretch_right=True)

        add_separator("---------------------------------------- Yu-Gi-Oh ----------------------------------------")

        # --- Player Names
        add_row("Player Names",
                lambda parent: ctk.CTkButton(parent, text="Edit", width=90, command=self.open_name_editor))

        # --- Starting LP
        add_row("Starting Life Points",
                lambda parent: ctk.CTkButton(parent, text="Edit", width=90, command=self.open_starting_lp_editor))

        # --- Sound Theme (dropdown + customize button in same row)
        def make_sound_theme_row(parent):
            inner = ctk.CTkFrame(parent, fg_color="transparent")

            self.theme_var = ctk.StringVar(value=self.current_theme)

            theme_selector = ctk.CTkOptionMenu(
                inner,
                values=list(self.theme_map.keys()),
                variable=self.theme_var,
                command=self.on_theme_change,
                width=160
            )
            theme_selector.pack(side="left", padx=(0, 8))

            btn_custom = ctk.CTkButton(
                inner,
                text="Customize…",
                width=90,
                command=self.open_custom_theme_editor
            )
            btn_custom.pack(side="left")

            return inner

        add_row("Sound Theme", make_sound_theme_row)

    # ----------------------------
    # Settings handlers
    # ----------------------------
    def on_theme_change(self, selected):
        self.sfx.sounds = self.sfx.load_theme(selected)
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
        self.sfx.play_sound("Refresh")


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
        p1_entry = ctk.CTkEntry(popup, width=200, justify="center")
        p1_entry.insert(0, self.game.player1.name)
        p1_entry.pack(pady=5)

        # Player 2
        ctk.CTkLabel(popup, text="Player 2 Name:").pack()
        p2_entry = ctk.CTkEntry(popup, width=200, justify="center")  
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

        lp_entry = ctk.CTkEntry(popup, width=200, justify="center")
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
            self.sfx.sounds = self.sfx.load_theme("Custom")

            self.master.title("Yu-Gi-Oh! Life Points — Theme: Custom")
            if hasattr(self, 'theme_var'):
                self.theme_var.set("Custom")

            self.sfx.play_sound("Refresh")
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
        player = self.game.player1 if player_num == 1 else self.game.player2

        ctk.CTkLabel(
            self,
            text=f"{player.name} - {action.capitalize()}",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(self, text=f"Current LP: {player.lp}", font=("Arial", 12)).pack(pady=(0, 10))
        ctk.CTkLabel(self, text=f"Enter value to {action}:").pack(pady=5)

        entry = ctk.CTkEntry(self)
        entry.pack()
        entry.focus_set()

        # ----------------------------
        # Button actions
        # ----------------------------
        def confirm(event=None):
            try:
                value = int(entry.get())
                if action == "damage":
                    self.lp_controller.change_lp(player_num, -value)
                elif action == "heal":
                    self.lp_controller.change_lp(player_num, value)
                self.change_screen(self.show_main_screen)
            except ValueError:
                entry.delete(0, ctk.END)
                entry.insert(0, "Invalid")
            return "break"

        def cancel(event=None):
            self.change_screen(self.show_main_screen)

        # ----------------------------
        # Buttons
        # ----------------------------
        ctk.CTkButton(self, text="Confirm", command=confirm).pack(pady=10)
        ctk.CTkButton(self, text="Cancel", command=cancel).pack()

        # ----------------------------
        # Key bindings
        # ----------------------------
        # Allow Enter to confirm while typing in the entry box
        entry.bind("<Return>", confirm)
        entry.bind("<Escape>", cancel)   # ✅ also bind to entry
        self.bind("<Escape>", cancel)    # ✅ frame-level backup


    # ----------------------------
    # Helpers
    # ----------------------------
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def change_screen(self, function):
        self.clear_screen()
        function()

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
        self.sfx.play_sound("LP_counting")

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
                    self.sfx.play_sound("LP_empty")
                else:
                    self.sfx.play_sound("LP_updated")

        # Start animation
        self.after(100, update_step)
    
    def update_display(self):
        """Update both players' LP display."""
        self.lp1_var.set(str(self.game.player1.lp))
        self.lp2_var.set(str(self.game.player2.lp))

