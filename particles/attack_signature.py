import pygame

from support_functions.support_functions import SupportFunctions

class AttackAnimation:

    def __init__(self):
        self.frames = {
            'slash': SupportFunctions.import_folder('graphics/particles/slash')
        }

    def create_attack_animation(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        AttackSignature(groups, pos, animation_frames)

class AttackSignature(pygame.sprite.Sprite):

    def __init__(self, groups: pygame.sprite.Group, pos, animation_frames):
        super().__init__(groups)
        self.sprite_type = "attack_signature"
        self.frame_index = 0
        self.animation = animation_frames
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect

    def animate(self, delta_time):
        self.frame_index += 12 * delta_time
        if self.frame_index >= len(self.animation):
            self.kill()
        else:
            self.image = self.animation[int(self.frame_index)]

    def update(self, delta_time):
        self.animate(delta_time)
