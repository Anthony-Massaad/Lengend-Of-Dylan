import pygame
import random

from support_functions.support_functions import SupportFunctions

class Animation:

    def __init__(self):
        self.frames = {
            # magic
            'flame': SupportFunctions.import_folder('graphics/particles/flame/frames'),
            'heal': SupportFunctions.import_folder('graphics/particles/heal/frames'),

            # attacks
            'claw': SupportFunctions.import_folder('graphics/particles/claw'),
            'thunder': SupportFunctions.import_folder('graphics/particles/thunder'),

            # monster deaths
            'raccoon': SupportFunctions.import_folder('graphics/particles/raccoon'),
            'spirit': SupportFunctions.import_folder('graphics/particles/nova'),

            # leafs
            'leaf': (
                SupportFunctions.import_folder('graphics/particles/leaf1'),
                SupportFunctions.import_folder('graphics/particles/leaf2'),
                SupportFunctions.import_folder('graphics/particles/leaf3'),
                SupportFunctions.import_folder('graphics/particles/leaf4'),
                SupportFunctions.import_folder('graphics/particles/leaf5'),
                SupportFunctions.import_folder('graphics/particles/leaf6'),
                self.reflect_images(SupportFunctions.import_folder('graphics/particles/leaf1')),
                self.reflect_images(SupportFunctions.import_folder('graphics/particles/leaf2')),
                self.reflect_images(SupportFunctions.import_folder('graphics/particles/leaf3')),
                self.reflect_images(SupportFunctions.import_folder('graphics/particles/leaf4')),
                self.reflect_images(SupportFunctions.import_folder('graphics/particles/leaf5')),
                self.reflect_images(SupportFunctions.import_folder('graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        flipped_frames = []
        for frame in frames:
            flip = pygame.transform.flip(frame, True, False)
            flipped_frames.append(flip)
        return flipped_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = random.choice(self.frames['leaf'])
        Particle(groups, pos, animation_frames)


class Particle(pygame.sprite.Sprite):

    def __init__(self, groups: pygame.sprite.Group, pos, animation_frames):
        super().__init__(groups)
        self.frame_index = 0
        self.animation = animation_frames
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self, delta_time):
        self.frame_index += 12 * delta_time
        if self.frame_index >= len(self.animation):
            self.kill()
        else:
            self.image = self.animation[int(self.frame_index)]

    def update(self, delta_time):
        self.animate(delta_time)
