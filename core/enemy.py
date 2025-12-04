import pygame
import random
from config import *

class Enemy:
    """Represents an enemy with size, speed, position, and an image."""

    def __init__(self):
        """Initialize the enemy with random size, speed, spawn position, and direction."""
        self.size = random.randint(ENEMY_MIN_SIZE, ENEMY_MAX_SIZE)
        self.speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.image = pygame.image.load('dodger_game\\assets\\images\\enemy.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))
        
        # Randomly choose a spawn corner
        spawn_corner = random.choice(["top_left", "top_right", "bottom_left", "bottom_right"])
        
        if spawn_corner == "top_left":
            self.position = (0, 0)
            self.direction = (random.uniform(0.5, 1), random.uniform(0.5, 1))  # Diagonal down-right
        elif spawn_corner == "top_right":
            self.position = (SCREEN_WiDTH - self.size, 0)
            self.direction = (random.uniform(-1, -0.5), random.uniform(0.5, 1))  # Diagonal down-left
        elif spawn_corner == "bottom_left":
            self.position = (0, SCREEN_HEIGHT - self.size)
            self.direction = (random.uniform(0.5, 1), random.uniform(-1, -0.5))  # Diagonal up-right
        elif spawn_corner == "bottom_right":
            self.position = (SCREEN_WiDTH - self.size, SCREEN_HEIGHT - self.size)
            self.direction = (random.uniform(-1, -0.5), random.uniform(-1, -0.5))  # Diagonal up-left

        # Normalize direction vector to ensure consistent speed
        magnitude = (self.direction[0]**2 + self.direction[1]**2)**0.5
        self.direction = (self.direction[0] / magnitude, self.direction[1] / magnitude)

    def draw(self, surface):
        """Draw the enemy on the game surface."""
        surface.blit(self.image, self.position)

    def move(self):
        """Move the enemy based on its speed and direction."""
        self.position = (self.position[0] + self.direction[0] * self.speed,
                         self.position[1] + self.direction[1] * self.speed)

    def is_off_screen(self):
        """Check if the enemy is off the screen."""
        return (self.position[0] < -self.size or self.position[0] > SCREEN_WiDTH or
                self.position[1] < -self.size or self.position[1] > SCREEN_HEIGHT)

    def get_rect(self):
        """Get the rectangle for collision detection."""
        return pygame.Rect(self.position, (self.size, self.size))
