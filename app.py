import customtkinter as ctk
from utils.helpers import load_settings, save_settings, get_theme, build_fonts, load_icon
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
        self.icons = {
            "back": load_icon("arrow_left", size=(20,20), mode=self.config_data["selected_theme"]),
            "settings": load_icon("settings", size=(20,20), mode=self.config_data["selected_theme"])
        }
        ctk.set_appearance_mode(self.config_data["selected_theme"])
        self.current_frame = None

        self.draw_main_menu()

    # -------------------------------
    # Main Menu
    # -------------------------------
    def draw_main_menu(self, animate=False):
        self.clear_window()

        # Root container
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both")

        # ----------------------------
        # Top Bar
        # ----------------------------
        top_bar = ctk.CTkFrame(frame, fg_color="transparent")
        top_bar.pack(fill="x", side="top", pady=(10, 0), padx=5)
        top_bar.grid_columnconfigure(0, weight=1)  # left spacer
        top_bar.grid_columnconfigure(1, weight=3)  # title area
        top_bar.grid_columnconfigure(2, weight=1)  # right spacer

        # Left placeholder (for balance)
        placeholder = ctk.CTkLabel(top_bar, text="", width=40)
        placeholder.grid(row=0, column=0, sticky="w", padx=5)

        # 🏷️ Title Label
        title_label = ctk.CTkLabel(
            top_bar,
            text="Choose your Game",
            font=self.fonts["heading"],
            pady=6
        )
        title_label.grid(row=0, column=1, padx=5)

        # ⚙️ Settings Button
        settings_button = ctk.CTkButton(
            top_bar,
            text="",
            image=self.icons["settings"],
            text_color=self.colour_theme["text_primary"],
            fg_color="transparent",
            hover=False,
            font=("Arial", 16),
            width=40,
            height=40,
            corner_radius=8,
            command=self.show_settings_menu
        )
        settings_button.grid(row=0, column=2, sticky="e", padx=5)

        # ----------------------------
        # Game Selection Buttons
        # ----------------------------
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(expand=True)

        ctk.CTkButton(button_frame,
                      text="Yu-Gi-Oh!",
                      width=200,
                      height=40,
                      command=self.start_yugioh).pack(pady=10)
        ctk.CTkButton(button_frame,
                      text="Magic: The Gathering",
                      width=200, height=40,
                      command=self.start_mtg).pack(pady=10)

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

    
    # -------------------------------
    # Settings Menu
    # -------------------------------
    def show_settings_menu(self):
        self.clear_window()
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both")

        # 🔹 Top Bar
        top_bar = ctk.CTkFrame(frame, fg_color="transparent")
        top_bar.pack(fill="x", side="top", pady=(10, 0), padx=5)
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=3)
        top_bar.grid_columnconfigure(2, weight=1)

        # ← Back Button
        back_button = ctk.CTkButton(
            top_bar, text="", image=self.icons["back"],
            fg_color="transparent", width=40, height=40,
            command=self.draw_main_menu
        )
        back_button.grid(row=0, column=0, sticky="w", padx=5)

        # Title
        title_label = ctk.CTkLabel(top_bar, text="Settings", font=self.fonts["heading"])
        title_label.grid(row=0, column=1)

        # ⚙️ Content
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(expand=True, pady=20)

        # Theme toggle
        ctk.CTkLabel(content, text="Theme:").pack(pady=(5, 0))
        theme_switch = ctk.CTkSwitch(
            content,
            text="Dark Mode",
            command=lambda: self.toggle_theme(theme_switch)
        )
        theme_switch.pack(pady=10)
        if self.config_data["selected_theme"] == "dark":
            theme_switch.select()

        # Volume slider
        ctk.CTkLabel(content, text="Volume:").pack(pady=(15, 0))
        volume_slider = ctk.CTkSlider(
            content,
            from_=0,
            to=1,
            number_of_steps=10,
            command=lambda v: self.set_volume(v)
        )
        volume_slider.set(self.config_data.get("volume", 1.0))
        volume_slider.pack(pady=10)

    # -------------------------------
    # Handlers
    # -------------------------------
    def toggle_theme(self, switch):
        theme = "dark" if switch.get() else "light"
        self.config_data["selected_theme"] = theme
        save_settings({"selected_theme": theme})
        ctk.set_appearance_mode(theme)
        self.colour_theme = get_theme(self.config_data)
        self.draw_main_menu()  # refresh UI with new theme

    def set_volume(self, value):
        self.config_data["volume"] = round(float(value), 2)
        save_settings({"volume": self.config_data["volume"]})
        print(f"🔊 Volume set to {self.config_data['volume'] * 100:.0f}%")