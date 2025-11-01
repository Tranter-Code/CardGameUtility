import customtkinter as ctk
from utils.helpers import load_settings, get_theme, build_fonts
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
        self.colour_theme = get_theme(self.config_data)
        self.fonts = build_fonts(self.colour_theme)
        ctk.set_appearance_mode(self.config_data["selected_theme"])
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

    def previous_screen(self, function):
        self.clear_window()
        function()


    # -------------------------------
    # Frame Switching
    # -------------------------------
    def switch_to(self, FrameClass, config_data):
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
        for widget in self.winfo_children():
            widget.destroy()