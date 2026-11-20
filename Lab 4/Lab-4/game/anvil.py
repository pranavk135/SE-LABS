import random
import pygame


class Anvil:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.width = 40
        self.height = 32
        self.x = random.randint(20, screen_width - self.width - 20)
        self.y = -self.height
        self.speed = random.uniform(4.5, 7.0)

    def update(self):
        self.y += self.speed

    def is_off_screen(self, screen_height):
        return self.y > screen_height + 10

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def _colors(self):
        if self.speed < 5.5:                      # slow: original grey
            return (120, 120, 130), (80, 80, 90)
        if self.speed < 6.25:                     # medium: orange
            return (255, 170, 60), (200, 110, 20)
        return (255, 80, 60), (170, 30, 25)       # fast: red

    def render(self, surface):
        top_color, base_color = self._colors()
        top_rect = pygame.Rect(int(self.x) + 4, int(self.y), self.width - 8, 14)
        pygame.draw.rect(surface, top_color, top_rect, border_radius=2)

        base_rect = pygame.Rect(int(self.x), int(self.y) + 14, self.width, 18)
        pygame.draw.rect(surface, base_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, (200, 200, 210), base_rect, width=1, border_radius=3)
