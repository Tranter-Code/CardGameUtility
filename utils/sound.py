import pygame, os
from utils.helpers import resource_path

pygame.mixer.init()

def load_sound(file_name, folder_name):
    path = resource_path(os.path.join("assets", "sounds", folder_name, file_name))
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.5)
        return sound
    except Exception as e:
        print(f"⚠️ Could not load sound: {path} ({e})")
        return None

def play_sound(sound):
    """Play a previously loaded sound."""
    if sound:
        sound.play()

def stop_all_sounds():
    """Stop all currently playing sounds."""
    pygame.mixer.stop()