import customtkinter as ctk
from tkinter import messagebox
from utils.helpers import save_settings
from game_modes.mtg.game import Game
from game_modes.mtg.logic import MTGLifeController

class MTGFrame(ctk.CTkFrame):
    def __init__(self, master, config_data):
        super().__init__(master)
        self.master = master
        self.config_data = config_data
        self.settings = config_data["mtg"]
        self.selected_player = None
        self.temp_value = ctk.IntVar(value=0)

        # Game setup
        self.game = Game(
            starting_life=self.settings["starting_life"],
            player1_name=self.settings["player1_name"],
            player2_name=self.settings["player2_name"]
        )

        # Controller
        self.controller = MTGLifeController(self)

        # StringVars for UI
        self.p1_life = ctk.StringVar(value=str(self.game.player1.life))
        self.p2_life = ctk.StringVar(value=str(self.game.player2.life))

        self.build_ui()

        # Key bindings for keyboard control
        self.master.bind("<Up>", lambda e: self.increment())
        self.master.bind("<Down>", lambda e: self.decrement())
        self.master.bind("<Return>", lambda e: self.confirm_change())

    # ----------------------------
    # UI Setup
    # ----------------------------
    def build_ui(self):
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
            text="Magic: The Gathering",
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

        # ----------------------------
        # Reset Button
        # ----------------------------
        reset_button = ctk.CTkButton(
            self,
            text="",
            image=self.master.icons["reset"],
            fg_color="transparent",
            hover_color=self.master.colour_theme["button_hover"],
            font=("Arial", 12),
            width=40,
            height=40,
            corner_radius=8,
            command=self.confirm_reset
        )
        reset_button.pack(side="top", expand=True)

        # ----------------------------
        # Main Area (Players)
        # ----------------------------
        main_area = ctk.CTkFrame(self, fg_color="transparent")
        main_area.pack(expand=True, fill="both", padx=20, pady=(10, 5))

        player_box_size = 230

        # --- Player 1 frame ---
        self.p1_frame = ctk.CTkFrame(
            main_area,
            fg_color=self.master.colour_theme["container_bg"],
            corner_radius=12,
            width=player_box_size,
            height=player_box_size,
            border_color="red"
        )
        self.p1_frame.pack(side="left", expand=True, padx=10, pady=5)
        self.p1_frame.pack_propagate(False)
        self.p1_frame.bind("<Button-1>", lambda e: self.select_player(1))

        ctk.CTkLabel(self.p1_frame,
            text=self.game.player1.name,
            font=("Arial", 14, "bold"),
            text_color=self.master.colour_theme["text_primary"],
            pady=6).pack(pady=(10, 5))
        ctk.CTkLabel(self.p1_frame,
            textvariable=self.p1_life,
            font=("Arial", 36),
            text_color=self.master.colour_theme["text_primary"]).pack()
        self.p1_pending_label = ctk.CTkLabel(
            self.p1_frame,
            text="",
            font=("Arial", 20, "bold"),
            text_color="red"
        )
        self.p1_pending_label.pack(pady=(5, 0))  # directly below life total

        # --- Player 2 frame ---
        self.p2_frame = ctk.CTkFrame(
            main_area,
            fg_color=self.master.colour_theme["container_bg"],
            corner_radius=12,
            width=player_box_size,
            height=player_box_size,
            border_color="red"
        )
        self.p2_frame.pack(side="left", expand=True, padx=10, pady=5)
        self.p2_frame.pack_propagate(False)
        self.p2_frame.bind("<Button-1>", lambda e: self.select_player(2))

        ctk.CTkLabel(self.p2_frame,
            text=self.game.player2.name,
            font=("Arial", 14, "bold"),
            text_color=self.master.colour_theme["text_primary"],
            pady=6).pack(pady=(10, 5))
        ctk.CTkLabel(self.p2_frame,
            textvariable=self.p2_life,
            font=("Arial", 36),
            text_color=self.master.colour_theme["text_primary"]).pack()
        self.p2_pending_label = ctk.CTkLabel(self.p2_frame,
            text="",
            font=("Arial", 20, "bold"),
            text_color="red"
        )
        self.p2_pending_label.pack(pady=(5, 0))

        # ----------------------------
        # Control Bar
        # ----------------------------
        control_bar = ctk.CTkFrame(self, fg_color="transparent")
        control_bar.pack(pady=(10, 10))

        # Inner centered layout
        center_group = ctk.CTkFrame(control_bar, fg_color="transparent")
        center_group.pack(anchor="center")

        ctk.CTkButton(center_group, text="", image=self.master.icons["minus"],
                    width=50, height=40, command=self.decrement).grid(row=0, column=0, padx=10)

        ctk.CTkButton(center_group, text="Confirm",
                    width=100, height=40, font=("Arial", 14, "bold"),
                    command=self.confirm_change).grid(row=0, column=1, padx=10)

        ctk.CTkButton(center_group, text="", image=self.master.icons["plus"],
                    width=50, height=40, command=self.increment).grid(row=0, column=2, padx=10)
        
    # ----------------------------
    # Core actions
    # ----------------------------
    def select_player(self, player_num):
        if self.selected_player == player_num:
            return
    
        self.selected_player = player_num

        # Update borders
        self.p1_frame.configure(border_width=2 if player_num == 1 else 0)
        self.p2_frame.configure(border_width=2 if player_num == 2 else 0)

        # Reset both pending labels
        self.p1_pending_label.configure(text="")
        self.p2_pending_label.configure(text="")

        # Start pending value
        self.temp_value.set(-1)

        # Default to red (since -1 is the starting value)
        default_color = "red"

        # Display it under the correct player
        if player_num == 1:
            self.p1_pending_label.configure(text="-1", text_color=default_color)
        elif player_num == 2:
            self.p2_pending_label.configure(text="-1", text_color=default_color)

    def increment(self):
        if not self.selected_player:
            return

        current = self.temp_value.get()
        new_val = current + 1

        # Skip 0 → jump from -1 to +1
        if current == -1:
            new_val = 1

        # Clamp to reasonable range (optional)
        if new_val > 99:
            new_val = 99

        self.temp_value.set(new_val)
        self.update_pending_label()

    def decrement(self):
        if not self.selected_player:
            return

        current = self.temp_value.get()
        new_val = current - 1

        # Skip 0 → jump from +1 to -1
        if current == 1:
            new_val = -1

        if new_val < -99:
            new_val = -99

        self.temp_value.set(new_val)
        self.update_pending_label()
    
    def update_pending_label(self):
        value = self.temp_value.get()

        # Choose colour
        if value < 0:
            color = "red"
        elif value > 0:
            color = "green"
        else:
            color = self.master.colour_theme["text_primary"]  # neutral or hidden

        # Update the correct label
        if self.selected_player == 1:
            self.p1_pending_label.configure(text=str(value), text_color=color)
            self.p2_pending_label.configure(text="")
        elif self.selected_player == 2:
            self.p2_pending_label.configure(text=str(value), text_color=color)
            self.p1_pending_label.configure(text="")

    def confirm_change(self):
        if not self.selected_player:
            return

        value = self.temp_value.get()
        self.controller.change_life(self.selected_player, value)
        self.temp_value.set(0)

        # Clear pending indicators
        self.p1_pending_label.configure(text="")
        self.p2_pending_label.configure(text="")

        # Remove highlight from both players
        self.p1_frame.configure(border_width=0)
        self.p2_frame.configure(border_width=0)

        # Clear selection
        self.selected_player = None

    # ----------------------------
    # Animation
    # ----------------------------
    def animate_life_change(self, player_num, old, new):
        # Identify target player
        if player_num == 1:
            label_widget = self.p1_frame.winfo_children()[1]
            life_var = self.p1_life
        else:
            label_widget = self.p2_frame.winfo_children()[1]
            life_var = self.p2_life

        # Detect change type
        is_damage = new < old
        is_heal = new > old
        animation_duration = 150

        # -----------------------------
        # DAMAGE: Flash text visibility
        # -----------------------------
        if is_damage:
            flashes = 10  # number of flickers (even number)
            visible_color = self.master.colour_theme["text_primary"]
            invisible_color = self.master.colour_theme["container_bg"]  # blend into background
            count = 0
            total_duration = flashes // 2 * animation_duration

            self.after(total_duration // 2 + 100, lambda: life_var.set(str(new)))

            def flicker():
                nonlocal count
                if count < flashes:
                    # Alternate between visible and invisible
                    color = visible_color if count % 2 == 0 else invisible_color
                    label_widget.configure(text_color=color)
                    count += 1
                    self.after(70, flicker)
                else:
                    # Final state — show new value
                    label_widget.configure(text_color=visible_color, text=str(new))

            flicker()

        # -----------------------------
        # HEALING: Pulse font size
        # -----------------------------
        elif is_heal:
            base_font = ("Arial", 36)
            pulse_up = 42  # larger size
            pulse_down = 36  # normal size
            pulses = 3
            count = 0

            total_duration = pulses * 2 * animation_duration

            self.after(total_duration // 2, lambda: life_var.set(str(new)))

            def pulse():
                nonlocal count
                if count < pulses * 2:
                    new_size = pulse_up if count % 2 == 0 else pulse_down
                    label_widget.configure(font=("Arial", new_size))
                    count += 1
                    self.after(120, pulse)
                else:
                    # Final update with new number at normal size
                    label_widget.configure(font=base_font, text=str(new))

            pulse()

        # -----------------------------
        # No change or neutral update
        # -----------------------------
        else:
            label_widget.configure(text=str(new))
    

    def update_display(self):
        self.p1_life.set(self.game.player1.life)
        self.p2_life.set(self.game.player2.life)

    # ----------------------------
    # Helpers
    # ----------------------------
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def change_screen(self, function):
        self.clear_screen()
        function()

    def clear_selection(self):
        self.selected_player = None
        self.p1_frame.configure(border_width=0)
        self.p2_frame.configure(border_width=0)
        self.p1_pending_label.configure(text="")
        self.p2_pending_label.configure(text="")
        self.temp_value = ctk.IntVar(value=0)

    def show_settings_screen(self):
        # ----------------------------
        # Top Bar
        # ----------------------------
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", side="top", pady=(10, 0), padx=5)
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=3)
        top_bar.grid_columnconfigure(2, weight=1)

        # ← Back Button
        back_button = ctk.CTkButton(
            top_bar,
            text="",
            image=self.master.icons["back"],
            text_color=self.master.colour_theme["text_primary"],
            fg_color="transparent",
            hover_color=self.master.colour_theme["button_hover"],
            width=40,
            height=40,
            corner_radius=8,
            command=lambda: self.change_screen(self.build_ui)
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

        # Right Placeholder (non-interactive, keeps title centered)
        placeholder = ctk.CTkLabel(top_bar, text="", width=40)
        placeholder.grid(row=0, column=2, sticky="e", padx=5)

        # ----------------------------
        # Settings Content 
        # ----------------------------
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=20, pady=12)

        def add_row(label_text, widget_factory, stretch_right=False):
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

        # ----------------------------
        # 🔹 Global Settings
        # ----------------------------

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

        # ----------------------------
        # 🔹 Magic: The Gathering Settings
        # ----------------------------
        add_separator("------------------------------------------ Magic: The Gathering ------------------------------------------")

        # --- Player Names ---
        add_row("Player Names", lambda parent: ctk.CTkButton(
            parent,
            text="Edit",
            width=90,
            command= self.open_name_editor
        ))

        # --- Starting Life Total ---
        add_row("Starting Life", lambda parent: ctk.CTkButton(
            parent,
            text="Edit",
            width=90,
            command= self.open_starting_life_editor
        ))
    
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
            save_settings({"mtg": self.settings})
            popup.destroy()

        ctk.CTkButton(popup, text="Save", command=save_names).pack(pady=15)
        popup.bind("<Return>", lambda e: save_names())

    def open_starting_life_editor(self):
        """Popup for changing the starting life total in Magic: The Gathering."""
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Starting Life Total")
        popup.geometry("300x180")
        popup.resizable(False, False)
        popup.grab_set()

        # --- Title ---
        ctk.CTkLabel(
            popup,
            text="Change Starting Life",
            font=self.master.fonts["heading"]
        ).pack(pady=10)

        ctk.CTkLabel(popup, text="Starting Total Life:").pack()

        # --- Entry Field ---
        life_entry = ctk.CTkEntry(popup, width=200, justify="center")
        life_entry.insert(0, str(self.game.starting_life))
        life_entry.pack(pady=5)

        # --- Save Handler ---
        def save_life_value():
            try:
                new_life = int(life_entry.get())
                if new_life <= 0:
                    raise ValueError

                # Update game state
                self.game.starting_life = new_life
                self.game.reset()

                # Update display variables (labels)
                self.p1_life.set(str(self.game.player1.life))
                self.p2_life.set(str(self.game.player2.life))

                # Save to config under "mtg"
                self.settings["starting_life"] = new_life
                from utils.helpers import save_settings
                save_settings({"mtg": self.settings})

                # Optional: play refresh sound if available
                if hasattr(self, "sfx"):
                    self.sfx.play_sound("Refresh")
                popup.destroy()

            except ValueError:
                # Simple input validation
                life_entry.delete(0, ctk.END)
                life_entry.insert(0, "Invalid")

        # --- Buttons ---
        ctk.CTkButton(popup, text="Save", command=save_life_value).pack(pady=15)
        popup.bind("<Return>", lambda e: save_life_value())


    def confirm_reset(self):
        """Ask the user for confirmation before resetting the game."""
        answer = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the game?")
        
        if answer:
            # Perform reset
            self.controller.reset_life()
            self.clear_selection()
            self.p1_pending_label.configure(text="")
            self.p2_pending_label.configure(text="")