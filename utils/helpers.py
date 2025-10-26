import os, json, sys

def resource_path(relative_path):
    """Get absolute path to resource (works for dev and for PyInstaller)."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
        "starting_lp": 20,
        "theme": "Default",
        "sound_paths": {}
    }
}

def load_settings():
    """Load settings safely with defaults for each game mode."""
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

    # 2️⃣ Ensure all game sections exist (yugioh, mtg, etc.)
    for game, defaults in DEFAULT_CONFIG.items():
        if game not in data:
            data[game] = defaults.copy()
        else:
            # 3️⃣ Fill in any missing keys inside each section
            for key, default_value in defaults.items():
                if key not in data[game]:
                    data[game][key] = default_value

    return data

def save_settings(new_data: dict):
    """
    Save only the specified game section (e.g., 'yugioh' or 'mtg') 
    without overwriting the entire config file.
    """
    config_path = get_config_path()
    current_data = {}

    # Load current config if it exists
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                current_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading settings file before saving: {e}")
            current_data = {}

    # Merge new data
    for key, value in new_data.items():
        current_data[key] = value  # e.g. "yugioh": {...}

    # Save merged config
    try:
        with open(config_path, "w") as f:
            json.dump(current_data, f, indent=4)
        print(f"✅ Settings updated successfully in {config_path}")
    except Exception as e:
        print(f"⚠️ Error saving settings: {e}")
