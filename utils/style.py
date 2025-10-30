import customtkinter as ctk

def setup_style(mode="dark", theme="blue"):
    """Configure CustomTkinter global appearance."""
    ctk.set_appearance_mode(mode)  # "dark", "light", or "system"
    ctk.set_default_color_theme(theme)  # "blue", "green", "dark-blue"