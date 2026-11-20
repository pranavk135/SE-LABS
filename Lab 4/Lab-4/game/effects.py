import random
import pygame


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2.5, 2.5)
        self.vy = random.uniform(-3.0, -0.5)
        self.max_life = self.life = random.randint(18, 32)
        self.size = random.randint(3, 6)

    @property
    def alive(self):
        return self.life > 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15
        self.life -= 1

    def render(self, surface):
        radius = max(1, int(self.size * self.life / self.max_life))
        pygame.draw.circle(surface, (190, 180, 160), (int(self.x), int(self.y)), radius)
