import pygame
from config import *
from utils.helpers import HighScoreManager

class Menu:
    """Handles the main menu interface, including navigation and high score display."""

    def __init__(self, screen):
        """
        Initialize the menu with the game screen, background, font, and buttons.

        Args:
            screen (pygame.Surface): The main screen surface to render the menu on.
        """
        self.high_score_manager = HighScoreManager()
        self.screen = screen
        self.font = pygame.font.SysFont("bold", 60)  # Main font for menu text
        self.background = pygame.Surface((SCREEN_WiDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load("dodger_game\\assets\\images\\menu_bg.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WiDTH, SCREEN_HEIGHT))
        self.buttons = [
            {"label": "Start Game", "action": "start", "rect": pygame.Rect(0, 0, 0, 0)},
            {"label": "High Score", "action": "high_score", "rect": pygame.Rect(0, 0, 0, 0)},
            {"label": "Quit Game", "action": "quit", "rect": pygame.Rect(0, 0, 0, 0)},
        ]

    def draw(self):
        """Render the menu background, buttons, and highlights."""
        self.screen.blit(self.background, (0, 0))
        for i, button in enumerate(self.buttons):
            label = self.font.render(button["label"], True, (255, 255, 255))  # Button text
            x = SCREEN_WiDTH // 2 - label.get_width() // 2
            y = SCREEN_HEIGHT // 3 + i * 100

            button_width = label.get_width() + 40
            button_height = label.get_height() + 20

            button["rect"] = pygame.Rect(x, y, button_width, button_height)  # Update button rect

            # Highlight button on hover
            if button["rect"].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (102, 204, 255), button["rect"])
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 3)

            # Render button text
            self.screen.blit(label, (x + 20, y + 10))

    def handle_event(self, event):
        """
        Handle user input events like mouse clicks.

        Args:
            event (pygame.Event): The input event to process.

        Returns:
            str or None: The action associated with the clicked button, or None if no action.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(pos):
                    return button["action"]
        return None

    def draw_text(self, text, x, y):
        """
        Draw text at the specified screen coordinates.

        Args:
            text (str): The text to render.
            x (int): X-coordinate.
            y (int): Y-coordinate.
        """
        text_obj = self.font.render(text, True, (255, 255, 255))
        text_rect = text_obj.get_rect(topleft=(x, y))
        self.screen.blit(text_obj, text_rect)

    def show_high_scores(self):
        """Display the high scores in a loop until the user presses ESC."""
        high_score = self.high_score_manager.load_high_score()
        while True:
            self.screen.fill((0, 0, 0))  # Clear the screen with black
            self.draw_text("High Scores", SCREEN_WiDTH // 2 - 100, 150)
            self.draw_text(f"Highest Score: {high_score}", SCREEN_WiDTH // 2 - 150, 300)
            self.draw_text("Press ESC to return", SCREEN_WiDTH // 2 - 150, 400)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
