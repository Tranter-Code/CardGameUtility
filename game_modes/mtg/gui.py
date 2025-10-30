import customtkinter as ctk
from game_modes.mtg.game import Game
from game_modes.mtg.logic import MTGLifeController

class MTGFrame(ctk.CTkFrame):
    def __init__(self, master, config_data):
        super().__init__(master)
        self.master = master
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
        """Draw the main MTG layout."""
        title = ctk.CTkLabel(self, text="Magic: The Gathering", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill="both", padx=20, pady=10)

        # Player 1 frame
        self.p1_frame = ctk.CTkFrame(container, fg_color="transparent", border_width=2)
        self.p1_frame.pack(side="left", expand=True, fill="both", padx=10)
        self.p1_frame.bind("<Button-1>", lambda e: self.select_player(1))
        ctk.CTkLabel(self.p1_frame, text=self.game.player1.name, font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(self.p1_frame, textvariable=self.p1_life, font=("Arial", 24)).pack()

        # Player 2 frame
        self.p2_frame = ctk.CTkFrame(container, fg_color="transparent", border_width=2)
        self.p2_frame.pack(side="right", expand=True, fill="both", padx=10)
        self.p2_frame.bind("<Button-1>", lambda e: self.select_player(2))
        ctk.CTkLabel(self.p2_frame, text=self.game.player2.name, font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(self.p2_frame, textvariable=self.p2_life, font=("Arial", 24)).pack()

        # Control area
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10)

        self.value_var = ctk.IntVar(value=0)
        ctk.CTkLabel(control_frame, text="Change:").pack(side="left", padx=5)
        self.value_label = ctk.CTkLabel(control_frame, textvariable=self.value_var, font=("Arial", 16, "bold"))
        self.value_label.pack(side="left", padx=5)

        ctk.CTkButton(control_frame, text="+", width=40, command=self.increment).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="-", width=40, command=self.decrement).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Confirm", width=100, command=self.confirm_change).pack(side="left", padx=10)
        ctk.CTkButton(control_frame, text="Reset", width=100, command=self.controller.reset_life).pack(side="left", padx=10)
        ctk.CTkButton(control_frame, text="Back", width=100, command=self.master.show_game_selector).pack(side="left", padx=10)

    # ----------------------------
    # Core actions
    # ----------------------------
    def select_player(self, player_num):
        """Highlight selected player."""
        self.selected_player = player_num
        self.p1_frame.configure(border_color="red" if player_num == 1 else "gray")
        self.p2_frame.configure(border_color="red" if player_num == 2 else "gray")

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
        """Simple smooth number change animation."""
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
