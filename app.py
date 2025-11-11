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
            "back": load_icon("arrow_left", size=(17,17), mode=self.config_data["global"]["selected_theme"]),
            "settings": load_icon("settings", size=(17,17), mode=self.config_data["global"]["selected_theme"]),
            "reset": load_icon("reset", size=(17,17), mode=self.config_data["global"]["selected_theme"]),
            "plus": load_icon("plus", size=(17,17)),
            "minus": load_icon("minus", size=(17,17))
        }
        ctk.set_appearance_mode(self.config_data["global"]["selected_theme"])
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
            self.geometry("550x415")
        elif FrameClass.__name__ == "YuGiOhFrame":
            self.geometry("500x360")
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
        top_bar.pack(fill="x", side="top", pady=(5, 0), padx=5)
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=3)
        top_bar.grid_columnconfigure(2, weight=1)

        # ← Back Button
        back_button = ctk.CTkButton(
            top_bar,
            text="",
            image=self.icons["back"],
            fg_color="transparent",
            hover_color=self.colour_theme["button_hover"],
            width=40,
            height=40,
            command=self.draw_main_menu
        )
        back_button.grid(row=0, column=0, sticky="w", padx=5)

        # Title
        title_label = ctk.CTkLabel(top_bar,
                                   text="Settings",
                                   font=self.fonts["heading"],
                                   pady=6)
        title_label.grid(row=0, column=1)

        # Left placeholder (for balance)
        placeholder = ctk.CTkLabel(top_bar, text="", width=40)
        placeholder.grid(row=0, column=2, sticky="w", padx=5)

        # ⚙️ Content
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(expand=True, pady=5)

        # Theme row (label + switch side by side)
        theme_row = ctk.CTkFrame(content, fg_color="transparent")
        theme_row.pack(fill="x", padx=30, pady=(5, 10))

        theme_label = ctk.CTkLabel(
            theme_row,
            text="Dark Mode",
            font=self.fonts["body"]
        )
        theme_label.pack(side="left", anchor="w")

        theme_switch = ctk.CTkSwitch(
            theme_row,
            text="",  # no label text, since we have our own label
            command=lambda: self.toggle_theme(theme_switch, self.show_settings_menu)
        )
        theme_switch.pack(side="right", anchor="e")

        if self.config_data["global"]["selected_theme"] == "dark":
            theme_switch.select()

        # Volume row (label + slider side by side)
        volume_row = ctk.CTkFrame(content, fg_color="transparent")
        volume_row.pack(fill="x", padx=30, pady=(10, 10))

        volume_label = ctk.CTkLabel(volume_row, text="Volume", font=self.fonts["body"])
        volume_label.pack(side="left", anchor="w")

        # --- Volume Slider
        def make_volume_slider(parent):
            slider = ctk.CTkSlider(
                parent,
                from_=0,
                to=1,
                number_of_steps=100,
            )
            slider.set(self.config_data["global"].get("volume", 1.0))

            # Save current value on release
            def on_release(event):
                value = round(slider.get(), 2)
                self.set_volume(value)  # save to config + update global volume

            # Bind left mouse release to commit
            slider.bind("<ButtonRelease-1>", on_release)

            return slider

        volume_slider = make_volume_slider(volume_row)
        volume_slider.set(self.config_data["global"].get("volume", 0.5))
        volume_slider.pack(side="right", fill="x", expand=True)

    # -------------------------------
    # Handlers
    # -------------------------------
    def toggle_theme(self, switch, function):
        theme = "dark" if switch.get() else "light"
        self.config_data["global"]["selected_theme"] = theme
        save_settings({"global": {"selected_theme": theme}})
        ctk.set_appearance_mode(theme)
        self.icons = {
            "back": load_icon("arrow_left", size=(20,20), mode=theme),
            "settings": load_icon("settings", size=(20,20), mode=theme),
            "reset": load_icon("reset", size=(17,17), mode=theme),
            "plus": load_icon("plus", size=(17,17)),
            "minus": load_icon("minus", size=(17,17))
        }
        self.colour_theme = get_theme(self.config_data)
        function()

    def set_volume(self, value):
        self.config_data["global"]["volume"] = round(float(value), 2)
        save_settings({"global": {"volume": self.config_data["global"]["volume"]}})
