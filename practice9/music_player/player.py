import pygame
import os

class MusicPlayer:
    def __init__(self, tracks):
        self.tracks = tracks
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False

    def get_current_track(self):
        return os.path.basename(self.tracks[self.current_index])

    def play(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.load(self.tracks[self.current_index])
            pygame.mixer.music.play()

        self.is_playing = True
        self.is_paused = False

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        self.is_paused = True

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.tracks)
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False

    def previous_track(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False