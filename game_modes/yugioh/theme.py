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
        self.load_theme(settings["theme"])

    def load_sound_effect(self, file_name: str, folder_name: str):
        """Load a single .wav file and return a pygame sound object."""
        path = resource_path(os.path.join('assets', 'sounds', 'yugioh', folder_name, file_name))
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(0.5)
            return sound
        except Exception as e:
            print(f"⚠️ Error loading sound '{file_name}' from '{folder_name}': {e}")
            return None

    def load_theme(self, theme_name: str):
        """Load all sounds for a given theme, or custom paths from settings."""
        if theme_name == "Custom":
            sound_paths = self.settings.get("sound_paths", {})
            self.lp_count = self.load_sound_effect("LP_counting.wav", sound_paths.get("LP_counting", "basic"))
            self.lp_updated = self.load_sound_effect("LP_updated.wav", sound_paths.get("LP_updated", "basic"))
            self.lp_empty = self.load_sound_effect("LP_empty.wav", sound_paths.get("LP_empty", "basic"))
            self.refresh = self.load_sound_effect("Refresh.wav", sound_paths.get("Refresh", "basic"))
        else:
            folder = self.theme_map.get(theme_name, theme_name.lower())
            self.lp_count = self.load_sound_effect("LP_counting.wav", folder)
            self.lp_updated = self.load_sound_effect("LP_updated.wav", folder)
            self.lp_empty = self.load_sound_effect("LP_empty.wav", folder)
            self.refresh = self.load_sound_effect("Refresh.wav", folder)

    def play_sound(self, sound_name):
        """Play a previously loaded sound."""
        snd = getattr(self, sound_name, None)
        sound.play_sound(snd)