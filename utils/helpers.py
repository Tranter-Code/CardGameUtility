import os, json, sys
from PIL import Image, ImageOps
import customtkinter as ctk

def resource_path(relative_path: str):
    try:
        # Running in packaged .exe
        base_path = sys._MEIPASS  
    except Exception:
        # Running in development → go to project root
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

def get_config_path(filename="config.json"):
    """Return the config path outside of the packaged app bundle."""
    if hasattr(sys, "_MEIPASS"):
        # When packaged, store config in user's appdata/home folder
        base = os.path.expanduser("~/.card_game_utility")
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, filename)
    else:
        return os.path.join(os.path.abspath("."), filename)


CONFIG_FILE = resource_path("config.json")

DEFAULT_CONFIG = {
    "global": {
        "selected_theme": "dark",
        "volume": 0.5
    },
    "yugioh": {
        "player1_name": "Player 1",
        "player2_name": "Player 2",
        "starting_lp": 8000,
        "theme": "Basic",
        "sound_paths": {
            "LP_counting": "basic",
            "LP_updated": "basic",
            "LP_empty": "basic",
            "Refresh": "basic"
        }
    },
    "mtg": {
        "player1_name": "Player 1",
        "player2_name": "Player 2",
        "starting_life": 20,
        "theme": "Default",
        "sound_paths": {}
    },
    "themes": {
        "dark": {
            "background": "#1e1e1e",
            "frame_bg": "#2a2a2a",
            "text_primary": "white",
            "text_secondary": "black",
            "container_bg": "#3a3a3a",
            "button_bg": "#2c2c2c",
            "button_hover": "#3a3a3a",
            "button_text": "#ffffff",
            "accent": "#00b4d8",
            "warning": "#ff4b4b",
            "fonts": {
                "heading": {
                    "family": "Arial",
                    "size": 20,
                    "weight": "bold"
                },
                "subheading": {
                    "family": "Arial",
                    "size": 16,
                    "weight": "bold"
                },
                "body": {
                    "family": "Arial",
                    "size": 14
                },
                "lp_counter": {
                    "family": "Arial",
                    "size": 36,
                    "weight": "bold"
                }
            }
        },
        "light": {
            "background": "#f4f4f4",
            "frame_bg": "#ffffff",
            "text_primary": "black",
            "text_secondary": "white",
            "container_bg": "#e0e0e0",
            "button_bg": "#e0e0e0",
            "button_hover": "#d0d0d0",
            "button_text": "#000000",
            "accent": "#0077b6",
            "warning": "#d90429",
            "fonts": {
                "heading": {
                    "family": "Arial",
                    "size": 20,
                    "weight": "bold"
                },
                "subheading": {
                    "family": "Arial",
                    "size": 16,
                    "weight": "bold"
                },
                "body": {
                    "family": "Arial",
                    "size": 14
                },
                "lp_counter": {
                    "family": "Arial",
                    "size": 36,
                    "weight": "bold"
                }
            }
        }
    }
}

def load_settings():
    config_path = get_config_path()
    data = {}

    # 1️⃣ Load existing config file (if available)
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading settings file: {e}")
            data = {}
    else:
        print("ℹ️ No config file found, creating new one with defaults.")
        data = DEFAULT_CONFIG.copy()
        save_settings(data)

    # 2️⃣ Ensure all sections exist and safely merge dict sections
    for section, defaults in DEFAULT_CONFIG.items():
        if section not in data:
            # Safe shallow copy for dicts, direct assignment for primitives
            data[section] = defaults.copy() if isinstance(defaults, dict) else defaults
        elif isinstance(defaults, dict) and isinstance(data[section], dict):
            # Merge missing keys inside dict sections
            for key, default_value in defaults.items():
                if key not in data[section]:
                    data[section][key] = default_value

    # ✅ Ensure critical global defaults (in case missing)
    if "global" not in data:
        data["global"] = DEFAULT_CONFIG["global"].copy()
    if "selected_theme" not in data["global"]:
        data["global"]["selected_theme"] = "dark"
    if "volume" not in data["global"]:
        data["global"]["volume"] = 1.0

    return data


def save_settings(new_data: dict):
    config_path = get_config_path()
    current_data = {}

    # Load current config
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                current_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading settings file before saving: {e}")
            current_data = {}

    # Deep merge helper
    def merge_dicts(target, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and isinstance(target.get(key), dict):
                merge_dicts(target[key], value)
            else:
                target[key] = value

    # Merge the new data safely
    merge_dicts(current_data, new_data)

    # Save updated config
    try:
        with open(config_path, "w") as f:
            json.dump(current_data, f, indent=4)
    except Exception as e:
        print(f"⚠️ Error saving settings: {e}")


def get_theme(config_data: dict):
    theme = {}
    if config_data["global"]["selected_theme"] == "dark":
        theme = config_data["themes"]["dark"]
        return theme
    else:
        theme = config_data["themes"]["light"]
        return theme

def build_fonts(selected_theme:dict):
    font_defs = selected_theme.get("fonts", {})
    fonts = {}

    for key, props in font_defs.items():
        fonts[key] = ctk.CTkFont(
            family=props.get("family", "Arial"),
            size=props.get("size", 12),
            weight=props.get("weight", "normal")
        )
    return fonts

def load_icon(name: str, size=(24, 24), mode="dark"):

    path = resource_path(os.path.join("assets", "icons", f"{name}.png"))
    if not os.path.exists(path):
        raise FileNotFoundError(f"Icon not found: {path}")

    img = Image.open(path).convert("RGBA")

    # --- Extract alpha channel ---
    alpha = img.getchannel("A")

    # --- Convert color ---
    if mode == "dark":
        # White icon
        recolored = Image.new("RGBA", img.size, (255, 255, 255, 255))
    else:
        # Black icon
        recolored = Image.new("RGBA", img.size, (0, 0, 0, 255))

    # --- Reapply alpha to keep transparency ---
    recolored.putalpha(alpha)

    return ctk.CTkImage(light_image=recolored, dark_image=recolored, size=size)
