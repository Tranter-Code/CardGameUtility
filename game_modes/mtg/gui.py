import customtkinter as ctk
from game_modes.mtg.game import Game
from game_modes.mtg.logic import MTGLifeController

class MTGFrame(ctk.CTkFrame):
    def __init__(self, master, config_data):
        super().__init__(master)
        self.master = master
        self.config_data = config_data
        self.settings = config_data["mtg"]
        self.selected_player = None  # 1 or 2

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
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=50)
        top_bar.pack(fill="x", side="top", pady=(5, 10), padx=10)

        back_button = ctk.CTkButton(
            top_bar,
            text="←",
            width=40,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#3C3C3C",
            text_color="white",
            command=self.master.back_to_main_menu
        )
        back_button.pack(side="left", padx=5, anchor="w")

        title_label = ctk.CTkLabel(
            top_bar,
            text="Magic: The Gathering",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        title_label.pack(side="left", expand=True, pady=5)

        settings_button = ctk.CTkButton(
            top_bar,
            text="⚙",
            width=40,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#3C3C3C",
            text_color="white",
            command=lambda: print("Settings clicked")  # Placeholder
        )
        settings_button.pack(side="right", padx=5, anchor="e")

        # ----------------------------
        # Reset Button
        # ----------------------------
        reset_button = ctk.CTkButton(
            self, text="Reset",
            width=70,
            height=20,
            corner_radius=8,
            text_color="white",
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
            fg_color="#222222",
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
            fg_color="#222222",
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

        ctk.CTkButton(control_frame, text="+", width=40, command=self.increment).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="-", width=40, command=self.decrement).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Confirm", width=100, command=self.confirm_change).pack(side="left", padx=10)
        
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
        steps = 20
        value = (new - old) / steps
        current = old

        def step():
            nonlocal current
            if abs(current - new) > abs(value):
                current += value
                val = int(round(current))
                if player_num == 1:
                    self.p1_life.set(val)
                else:
                    self.p2_life.set(val)
                self.after(30, step)
            else:
                if player_num == 1:
                    self.p1_life.set(new)
                else:
                    self.p2_life.set(new)

        step()

    def update_display(self):
        self.p1_life.set(self.game.player1.life)
        self.p2_life.set(self.game.player2.life)
