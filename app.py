import customtkinter as ctk
from utils.helpers import load_settings, resource_path
from game_modes.yugioh.gui import YuGiOhFrame
# (future) from game_modes.mtg.gui import MTGFrame

class CardGameApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 🧠 App setup
        self.title("Card Game Life Points Tracker")
        self.geometry("500x400")



        # 🔧 Load global configuration
        self.config_data = load_settings()
        self.current_frame = None

        # Show the first screen
        self.show_game_selector()

    # -------------------------------
    # Main Menu
    # -------------------------------
    def show_game_selector(self):
        """Initial screen to choose which game to play."""
        self.clear_window()

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both")

        ctk.CTkLabel(frame, text="Select Your Game", font=("Arial", 18, "bold")).pack(pady=20)

        # ✅ Larger, modern CTk buttons
        ctk.CTkButton(frame, text="Yu-Gi-Oh!", width=200, height=40, command=self.start_yugioh).pack(pady=10)

        # (future-proofing) MTG placeholder
        # ctk.CTkButton(frame, text="Magic: The Gathering", width=200, height=40, command=self.start_mtg).pack(pady=10)

    # -------------------------------
    # Game Loaders
    # -------------------------------
    def start_yugioh(self):
        """Switch to the Yu-Gi-Oh! interface."""
        self.switch_to(YuGiOhFrame, self.config_data)

    # def start_mtg(self):
    #     """Switch to the MTG interface (future)."""
    #     self.switch_to(MTGFrame, self.config_data)

    # -------------------------------
    # Frame Switching
    # -------------------------------
    def switch_to(self, FrameClass, config_data):
        """Replace current frame with a new one (same window)."""
        self.clear_window()
        self.current_frame = FrameClass(self, config_data)
        self.current_frame.pack(fill="both", expand=True)

    def clear_window(self):
        """Destroy any existing widgets in the window."""
        for widget in self.winfo_children():
            widget.destroy()