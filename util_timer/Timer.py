import pygame

class Timer:

    def __init__(self, duration, function=None) -> None:
        self.duration = duration
        self.function = function
        self.start_time = 0
        self.active = False

    def get_pygame_time(self):
        """get relative time of game in milliseconds

        Returns:
            int: the current duration of the game
        """
        return pygame.time.get_ticks()

    def trigger_active(self) -> bool:
        """set the timer to active or inactive

        Returns:
            bool: True if False, otherwise False
        """
        return not self.active
    
    def check_active(self) -> bool:
        return self.active

    def start_timer(self) -> None:
        """Start the timer my activating it and getting the 
        relative start time in pygame
        """
        self.active = self.trigger_active()
        self.start_time = self.get_pygame_time()
    
    def stop_timer(self) -> None:
        self.active = self.trigger_active()
        self.start_time = 0

    def update(self) -> None: 
        if not self.active: return
        current_time = self.get_pygame_time()
        if current_time - self.start_time >= self.duration:
            self.stop_timer()
            if self.function:
                self.function()
            