import tkinter as tk
from tkinter import ttk
from utils.helpers import load_settings, save_settings
from game_modes.yugioh.gui import YuGiOhFrame

class CardGameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Card Game Life Points Tracker")
        self.geometry("500x400")
        self.config_data = load_settings()
        self.current_frame = None

        self.show_game_selector()

    def show_game_selector(self):
        """Initial screen to choose which game to play."""
        self.clear_window()
        frame = ttk.Frame(self)
        frame.pack(expand=True)

        ttk.Label(frame, text="Select Your Game", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Button(frame, text="Yu-Gi-Oh!", width=25, command=self.start_yugioh).pack(pady=10)

    def start_yugioh(self):
        self.switch_to(YuGiOhFrame, self.config_data)

    def switch_to(self, FrameClass, config_data):
        """Replace current frame with a new one (same window)."""
        self.clear_window()
        self.current_frame = FrameClass(self, config_data)
        self.current_frame.pack(fill="both", expand=True)

    def clear_window(self):
        """Destroy any existing widgets in the window."""
        for widget in self.winfo_children():
            widget.destroy()