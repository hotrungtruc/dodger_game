import pygame
import random
from config import *

class Enemy:
    """Represents an enemy with size, speed, position, and an image."""

    def __init__(self):
        """Initialize the enemy with random size, speed, and spawn position."""
        self.size = random.randint(ENEMY_MIN_SIZE, ENEMY_MAX_SIZE)
        self.speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.image = pygame.image.load('assets/images/enemy.png')
        self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))
        self.position = (random.randint(0, SCREEN_WiDTH - self.size), -self.size)

    def draw(self, surface):
        """Draw the enemy on the game surface."""
        surface.blit(self.image, self.position)

    def move(self):
        """Move the enemy downward based on its speed."""
        self.position = (self.position[0], self.position[1] + self.speed)

    def is_off_screen(self):
        """Check if the enemy is off the screen."""
        return self.position[1] > SCREEN_HEIGHT

    def get_rect(self):
        """Get the rectangle for collision detection."""
        return pygame.Rect(self.position, (self.size, self.size))
