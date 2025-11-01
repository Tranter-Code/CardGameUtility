import customtkinter as ctk
import threading
from utils.helpers import build_fonts
from game_modes.mtg.game import Game
from game_modes.mtg.logic import MTGLifeController

class MTGFrame(ctk.CTkFrame):
    def __init__(self, master, config_data):
        super().__init__(master)
        self.master = master
        self.config_data = config_data
        self.settings = config_data["mtg"]
        self.selected_player = None

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

        back_button = ctk.CTkButton(
            top_bar,
            text="←",
            text_color=self.master.colour_theme["text_primary"],
            fg_color="transparent",
            font=("Ariel", 16),
            width=40,
            height=40,
            corner_radius=8,
            command=self.master.back_to_main_menu
        )
        back_button.pack(side="left", padx=5, anchor="w")

        title_label = ctk.CTkLabel(
            top_bar,
            text="Magic: The Gathering",
            font=self.master.fonts["heading"],
            fg_color="transparent",
            pady=6
        )
        title_label.pack(side="left", expand=True, pady=(0, 5))

        settings_button = ctk.CTkButton(
            top_bar,
            text="⚙",
            text_color=self.master.colour_theme["text_primary"],
            fg_color="transparent",
            font=("Ariel", 20),
            width=40,
            height=40,
            corner_radius=8,
            command=lambda: print("Settings clicked")  # Placeholder
        )
        settings_button.pack(side="right", padx=5, anchor="e")

        # ----------------------------
        # Reset Button
        # ----------------------------
        reset_button = ctk.CTkButton(
            self,
            text="Reset",
            font=("Arial", 12),
            width=70,
            height=20,
            corner_radius=20,
            command=self.controller.reset_life
        )
        reset_button.pack(side="top", expand=True)

        # ----------------------------
        # Main Area
        # ----------------------------
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=20, pady=(10, 15))
        player_box_size = 250

        # Player 1 frame
        self.p1_frame = ctk.CTkFrame(
            container,
            fg_color="#373737",
            corner_radius=12,
            width=player_box_size,
            height=player_box_size,
            border_color="red"
        )
        self.p1_frame.pack(side="left", expand=True, padx=5, pady=5)
        self.p1_frame.pack_propagate(False)
        self.p1_frame.bind("<Button-1>", lambda e: self.select_player(1))

        ctk.CTkLabel(self.p1_frame, text=self.game.player1.name, font=("Arial", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self.p1_frame, textvariable=self.p1_life, font=("Arial", 36)).pack()

        # Player 2 frame
        self.p2_frame = ctk.CTkFrame(
            container,
            fg_color="#373737",
            corner_radius=12,
            width=player_box_size,
            height=player_box_size,
            border_color="red"
        )
        self.p2_frame.pack(side="right", expand=True, padx=5, pady=5)
        self.p2_frame.pack_propagate(False)
        self.p2_frame.bind("<Button-1>", lambda e: self.select_player(2))

        ctk.CTkLabel(self.p2_frame, text=self.game.player2.name, font=("Arial", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self.p2_frame, textvariable=self.p2_life, font=("Arial", 36)).pack()

        # Control area
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=10)

        self.value_var = ctk.IntVar(value=0)
        ctk.CTkLabel(control_frame, text="Change:").pack(side="left", padx=5)
        self.value_label = ctk.CTkLabel(control_frame, textvariable=self.value_var, font=("Arial", 16, "bold"))
        self.value_label.pack(side="left", padx=5)

        
        ctk.CTkButton(control_frame, text="-", width=40, command=self.decrement).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Confirm", width=100, command=self.confirm_change).pack(side="left", padx=10)
        ctk.CTkButton(control_frame, text="+", width=40, command=self.increment).pack(side="left", padx=5)
        
    # ----------------------------
    # Core actions
    # ----------------------------
    def select_player(self, player_num):
        """Highlight selected player."""
        self.selected_player = player_num
        self.p1_frame.configure(border_width=2 if player_num == 1 else 0)
        self.p2_frame.configure(border_width=2 if player_num == 2 else 0)

    def increment(self):
        self.value_var.set(self.value_var.get() + 1)

    def decrement(self):
        self.value_var.set(self.value_var.get() - 1)

    def confirm_change(self):
        """Apply the current value to the selected player."""
        if not self.selected_player:
            return  # No player selected
        value = self.value_var.get()
        self.controller.change_life(self.selected_player, value)
        self.value_var.set(0)

    # ----------------------------
    # Helpers
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
            flashes = 6  # number of flickers (even number)
            visible_color = "white"
            invisible_color = self.cget("fg_color")  # blend into background
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
                    self.after(100, flicker)
                else:
                    # Final state — show new value
                    label_widget.configure(text_color=visible_color, text=str(new))

            flicker()

        # -----------------------------
        # HEALING: Pulse font size
        # -----------------------------
        elif is_heal:
            base_font = ("Arial", 36)
            pulse_up = 45  # larger size
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
