import pygame
from core.player import Player
from core.enemy import Enemy
from config import *
from utils.helpers import HighScoreManager

class World:
    """Represents the game world, managing the player, enemies, score, and input."""

    def __init__(self):
        """Initialize the game world with background, player, enemies, and score management."""
        self.reset()
        self.background = pygame.image.load('assets/images/background.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WiDTH, SCREEN_HEIGHT))
        self.high_score_manager = HighScoreManager()

    def reset(self):
        """Reset the game state, preparing for a new game."""
        self.player = Player()
        self.enemies = []
        self.gameOver = False
        self.score = 0
        self.enemy_counter = 0
        self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False
        self.using_mouse = True

    def is_game_over(self):
        """Check if the game is over."""
        return self.gameOver

    def update(self):
        """Update game state, including player movement, enemy management, and score."""
        self.score += 1

        # Handle keyboard movement
        if self.moveUp or self.moveDown or self.moveLeft or self.moveRight:
            self.using_mouse = False
            if self.moveUp:
                self.player.move(0, -PLAYER_SPEED)
            if self.moveDown:
                self.player.move(0, PLAYER_SPEED)
            if self.moveLeft:
                self.player.move(-PLAYER_SPEED, 0)
            if self.moveRight:
                self.player.move(PLAYER_SPEED, 0)

        # Handle mouse movement if keyboard input is inactive
        elif self.using_mouse:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_x = max(0, min(mouse_x - PLAYER_SIZE / 2, SCREEN_WiDTH - PLAYER_SIZE))
            player_y = max(PLAYER_MAX_UP, min(mouse_y - PLAYER_SIZE / 2, SCREEN_HEIGHT - PLAYER_SIZE))
            self.player.position = (player_x, player_y)

        # Update enemies
        for e in self.enemies:
            e.move()
            if self.player.did_hit(e.get_rect()):  # Check collision with player
                self.gameOver = True
            if e.is_off_screen():  # Remove off-screen enemies
                self.enemies.remove(e)

        # Spawn new enemies
        self.enemy_counter += 1
        if self.enemy_counter > ENEMY_SPAWN_RATE:
            self.enemy_counter = 0
            self.enemies.append(Enemy())

        # Save high score if the game ends
        if self.gameOver:
            self.high_score_manager.save_high_score(self.score)

    def draw(self, surface):
        """Render the game world, including background, player, and enemies."""
        surface.blit(self.background, (0, 0))
        self.player.draw(surface)
        for e in self.enemies:
            e.draw(surface)

    def handle_keys(self, event):
        """Handle keyboard and mouse input for player movement."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.moveUp = True
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.moveDown = True
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.moveLeft = True
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.moveRight = True

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.moveUp = False
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.moveDown = False
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.moveLeft = False
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.moveRight = False

        if event.type == pygame.MOUSEMOTION:
            self.using_mouse = True
