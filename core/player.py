import pygame
import random
from config import *

class Player:
    """Represents the player with size, speed, position, and firing capabilities."""

    def __init__(self):
        """Initialize the player with default size, speed, position, and load assets."""
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.image = pygame.image.load('dodger_game\\assets\\images\\player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.position = (SCREEN_WiDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 10)
        self.lasers = []  # Placeholder for future laser functionality

    def draw(self, surface):
        """Draw the player and its fire effect on the game surface."""
        surface.blit(self.image, self.position)
        self.draw_fire(surface)

    def draw_fire(self, surface):
        """Draw fire effects beneath the player's position."""
        player_x, player_y = self.position
        left_fire_x = player_x + self.size // 5
        right_fire_x = player_x + self.size - self.size // 3 + 4
        fire_y = player_y + self.size + 17

        for fire_x in (left_fire_x, right_fire_x):
            self.draw_flame(surface, fire_x, fire_y)

    def draw_flame(self, surface, fire_x, fire_y):
        """Render dynamic flame effects at the specified position."""
        for i in range(4):
            base_width = random.randint(3, 6) * (4 - i)
            base_height = random.randint(5, 8) * (4 - i)
            width = max(1, base_width - i * 2)
            height = max(1, base_height)
            alpha = max(0, 150 - i * 40)  # Reduce transparency over layers
            flame_color = (255, 100 + i * 30, 0, alpha)
            flame_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.ellipse(flame_surface, flame_color, (0, 0, width, height))
            surface.blit(flame_surface, (fire_x - width // 2, fire_y - height // 2 + i - 7))

    def move(self, x, y):
        """Update the player's position, ensuring it stays within screen bounds."""
        new_x = self.position[0] + x
        new_y = self.position[1] + y

        # Keep the player within horizontal bounds
        if new_x < 0 or new_x > SCREEN_WiDTH - self.size:
            new_x = self.position[0]

        # Keep the player within vertical bounds
        if new_y < 0 or new_y > SCREEN_HEIGHT - self.size:
            new_y = self.position[1]

        self.position = (new_x, new_y)

    def get_rect(self):
        """Return the player's rectangular area for collision detection."""
        return pygame.Rect(self.position, (self.size, self.size))

    def did_hit(self, rect):
        """Check if the player collides with the given rectangle."""
        return self.get_rect().colliderect(rect)
