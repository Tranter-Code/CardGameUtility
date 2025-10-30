import customtkinter as ctk
import darkdetect
from utils.helpers import load_settings
from game_modes.yugioh.gui import YuGiOhFrame
from game_modes.mtg.gui import MTGFrame

class CardGameApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 🧠 App setup
        self.title("Card Game Life Points Tracker")
        self.geometry("300x200")
        self.resizable(False, False)

        # 🔧 Load global configuration
        self.config_data = load_settings()
        if darkdetect.isDark:
            self.colour_theme = self.config_data["themes"]["dark"]
        else:
            self.colour_theme = self.config_data["themes"]["light"]
        self.current_frame = None

        self.draw_main_menu()

    # -------------------------------
    # Main Menu
    # -------------------------------
    def draw_main_menu(self, animate=False):
        """Build the main menu (with optional fade-in animation)."""
        self.clear_window()

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both")

        ctk.CTkLabel(frame, text="Select Your Game", font=("Arial", 18, "bold")).pack(pady=20)
        ctk.CTkButton(frame, text="Yu-Gi-Oh!", width=200, height=40, command=self.start_yugioh).pack(pady=10)
        ctk.CTkButton(frame, text="Magic: The Gathering", width=200, height=40, command=self.start_mtg).pack(pady=10)

    # -------------------------------
    # Screen Loaders
    # -------------------------------
    def start_yugioh(self):
        self.switch_to(YuGiOhFrame, self.config_data)

    def start_mtg(self):
        self.switch_to(MTGFrame, self.config_data)

    def back_to_main_menu(self):
        self.clear_window()
        self.draw_main_menu()
        self.geometry("300x200")

    # -------------------------------
    # Frame Switching
    # -------------------------------
    def switch_to(self, FrameClass, config_data):
        """Replace current frame with a new one (same window) and animate appearance."""
        self.clear_window()

        self.current_frame = FrameClass(self, config_data)
        self.current_frame.pack(fill="both", expand=True)

        # Determine target window size
        if FrameClass.__name__ == "MTGFrame":
            self.geometry("600x415")
        elif FrameClass.__name__ == "YuGiOhFrame":
            self.geometry("500x400")
        else:
            self.geometry("500x400")


    def clear_window(self):
        """Destroy any existing widgets in the window."""
        for widget in self.winfo_children():
            widget.destroy()