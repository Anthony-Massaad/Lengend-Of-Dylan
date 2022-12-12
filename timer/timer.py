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

        self.switch_util = True
        self.is_mana_regen = True
        self.action_performed = False

    def trigger_active(self) -> bool:
        """set the timer to active or inactive

        Returns:
            bool: True if False, otherwise False
        """
        return not self.active

    def start_timer(self) -> None:
        """Start the timer my activating it and getting the 
        relative start time in pygame
        """
        self.active = self.trigger_active()
        self.start_time = pygame.time.get_ticks()

    def stop_timer(self) -> None:
        """when Timer is done, resets its configurations
        """
        self.active = self.trigger_active()
        self.start_time = 0

    def change_util(self, direction):
        if not self.active:
            return

        if self.function and self.switch_util:
            self.function(direction)
            self.switch_util = False

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.stop_timer()
            self.switch_util = True

    def trigger_action(self) -> None:
        """update the Timer, checking if it passed the duration given
        If so, stop the timer and launch the method if given
        """
        if not self.active:
            return

        if not self.action_performed and self.function:
            self.function()
            self.action_performed = True

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.stop_timer()
            self.action_performed = False

    def mana_regeneration(self):
        if not self.active:
            return

        if self.function and self.is_mana_regen:
            self.function()
            self.is_mana_regen = False

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.stop_timer()
            self.is_mana_regen = True
