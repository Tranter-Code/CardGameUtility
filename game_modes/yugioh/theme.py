import os
import pygame
from utils import sound
from utils.helpers import resource_path

class SoundThemeManager:
    """Handles sound effects and theme loading for Yu-Gi-Oh."""

    def __init__(self, settings, theme_map):
        self.settings = settings
        self.theme_map = theme_map
        pygame.mixer.init()
        self.sounds = self.load_theme(settings["yugioh"]["theme"])

    def load_sound_effect(self, file_name: str, folder_name: str):
        """Load a single .wav file and return a pygame sound object."""
        path = resource_path(os.path.join('assets', 'sounds', 'yugioh', folder_name, file_name))
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.settings["global"]["volume"])
            return sound
        except Exception as e:
            print(f"⚠️ Error loading sound '{file_name}' from '{folder_name}': {e}")
            return None

    def load_theme(self, theme_name: str):
        sounds = {}

        if theme_name == "Custom":
            sound_paths = self.settings["yugioh"].get("sound_paths", {})
            sounds["LP_counting"] = self.load_sound_effect("LP_counting.wav", sound_paths.get("LP_counting", "basic"))
            sounds["LP_updated"] = self.load_sound_effect("LP_updated.wav", sound_paths.get("LP_updated", "basic"))
            sounds["LP_empty"] = self.load_sound_effect("LP_empty.wav", sound_paths.get("LP_empty", "basic"))
            sounds["Refresh"] = self.load_sound_effect("Refresh.wav", sound_paths.get("Refresh", "basic"))
        else:
            folder = self.theme_map.get(theme_name, theme_name.lower())
            sounds["LP_counting"] = self.load_sound_effect("LP_counting.wav", folder)
            sounds["LP_updated"] = self.load_sound_effect("LP_updated.wav", folder)
            sounds["LP_empty"] = self.load_sound_effect("LP_empty.wav", folder)
            sounds["Refresh"] = self.load_sound_effect("Refresh.wav", folder)

        return sounds

    def play_sound(self, sound_name: str):
        snd = self.sounds.get(sound_name)
        if snd:
            try:
                snd.play()
            except Exception as e:
                print(f"⚠️ Failed to play sound '{sound_name}': {e}")
        else:
            print(f"⚠️ Sound '{sound_name}' not found in current theme.")