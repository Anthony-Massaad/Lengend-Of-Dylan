import pygame
from logger.log import Log

class Timer:

    def __init__(self, duration: int, function=None) -> None:
        """Timer class initalization for character/player action in the game

        Args:
            duration (int): the duration of the timer
            function (method, optional): the function Timer calls when passed duration. Defaults to None.
        """
        self.duration = duration
        self.function = function
        self.start_time = 0
        self.active = False

    def get_pygame_time(self) -> int:
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
        """check the Timer status 

        Returns:
            bool: True if active, otherwise False
        """
        return self.active

    def start_timer(self) -> None:
        """Start the timer my activating it and getting the 
        relative start time in pygame
        """
        self.active = self.trigger_active()
        self.start_time = self.get_pygame_time()
    
    def stop_timer(self) -> None:
        """when Timer is done, resets its configurations
        """
        self.active = self.trigger_active()
        self.start_time = 0

    def update(self, hit_frame, current_frame) -> None: 
        """update the Timer, checking if it passed the duration given
        If so, stop the timer and launch the method if given
        """
        if not self.active: return

        if hit_frame == current_frame:
            Log.info(f"Hitting at frame {hit_frame} with {current_frame}")
            if self.function:
                self.function()

        current_time = self.get_pygame_time()
        if current_time - self.start_time >= self.duration:
            self.stop_timer()
            Log.info(f"Timer stopped")
                
            