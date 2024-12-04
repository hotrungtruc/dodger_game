import pygame
from utils.menu import Menu
from utils.helpers import HighScoreManager
from core import World
from config import *

TEXT_COLOR = pygame.Color("white")

def run():
    """
    Main function to run the game. Manages the menu, game loop, and high score display.
    """
    pygame.init()

    # Initialize mixer for sound and music
    pygame.mixer.init()

    # Load game sounds and music
    pygame.mixer.music.load("assets/musics_and_sounds/backgound.MP3")
    pygame.mixer.music.set_volume(0.2)
    
    gameover_sound = pygame.mixer.Sound("assets/musics_and_sounds/gameover.WAV")
    gameover_sound.set_volume(0.9) 

    button_sound = pygame.mixer.Sound("assets/musics_and_sounds/button_sound.MP3")
    button_sound.set_volume(1) 

    menu_music = pygame.mixer.Sound("assets/musics_and_sounds/menu.MP3")
    menu_music.set_volume(0.05) 

    # Setup display and clock
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WiDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DODGER PYGAME")
    
    # Initialize menu
    menu = Menu(screen)
    in_menu = True
    high_score_manager = HighScoreManager()

    # Menu loop
    while in_menu:
        menu.draw()
        menu_music.play(-1)  # Play menu music in a loop
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            action = menu.handle_event(event)
            if action == "start":
                button_sound.play()
                menu_music.stop()
                pygame.mixer.music.play(-1)  # Start background music
                in_menu = False  
            elif action == "high_score":
                button_sound.play()
                menu.show_high_scores()  # Show high scores screen
            elif action == "quit":
                button_sound.play()
                pygame.quit()
                return

    # Game initialization
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    world = World()
    font = pygame.font.SysFont("bold", 42)

    pygame.mouse.set_visible(False)

    running = True
    music_playing = True  

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == ord("r"):
                world.reset()
                pygame.mixer.music.play(-1)  # Restart background music
                music_playing = True  
            else:
                world.handle_keys(event)

        clock.tick(FPS)

        if not world.is_game_over():
            world.update()
            pygame.display.update()
        else:
            if music_playing:  
                pygame.mixer.music.stop()
                gameover_sound.play()
                music_playing = False  

        # Draw game world
        world.draw(surface)

        screen.blit(surface, (0, 0))

        # Display score and high score
        text = font.render("Score: {0}".format(world.score), 1, TEXT_COLOR)
        screen.blit(text, (5, 10))
        top_score = high_score_manager.load_high_score()
        top_score_text = font.render("Top Score: {0}".format(top_score), 1, TEXT_COLOR)
        screen.blit(top_score_text, (5, 60))  

        # Display game over text if applicable
        if world.is_game_over():
            game_over = font.render("Game Over", 1, TEXT_COLOR)
            screen.blit(game_over, (SCREEN_WiDTH / 3, SCREEN_HEIGHT / 2))
            hit_r = font.render("Hit R to Reset", 1, TEXT_COLOR)
            screen.blit(hit_r, (SCREEN_WiDTH / 3, SCREEN_HEIGHT / 2 + 70))

        pygame.display.update()

if __name__ == '__main__':
    run()
    pygame.quit()
