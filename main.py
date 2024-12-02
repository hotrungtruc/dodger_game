import pygame
from utils import Menu, HighScoreManager
from core import World
from config import *

TEXT_COLOR = pygame.Color("white")

def run():
    pygame.init()

    # Khởi tạo âm thanh
    pygame.mixer.init()

    # Tải nhạc nền
    pygame.mixer.music.load("assets/musics_and_sounds/background.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Phát nhạc lặp lại
    
    # Tải âm thanh khi thua
    gameover_sound = pygame.mixer.Sound("assets/musics_and_sounds/gameover.WAV")
    gameover_sound.set_volume(0.7) 

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WiDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DODGER PYGAME")
    
    menu = Menu(screen)
    in_menu = True
    high_score_manager = HighScoreManager()
    # Hiển thị menu
    while in_menu:
        menu.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            action = menu.handle_event(event)
            if action == "start":
                in_menu = False  # Bắt đầu game
            elif action == "high_score":
                menu.show_high_scores()  # Hiển thị bảng điểm cao
            elif action == "quit":
                pygame.quit()
                return

    # Bắt đầu game chính
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    world = World()
    font = pygame.font.SysFont("bold", 42)

    pygame.mouse.set_visible(False)

    running = True
    music_playing = True  # Biến để kiểm tra trạng thái nhạc nền

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == ord("r"):
                # Reset game và phát lại nhạc nền
                world.reset()
                pygame.mixer.music.play(-1)  # Phát lại nhạc nền
                music_playing = True  # Đặt trạng thái nhạc là đang phát
            else:
                world.handle_keys(event)

        clock.tick(FPS)

        if not world.is_game_over():
            world.update()
              # Hiển thị điểm cao trong lúc chơi
            pygame.display.update()
        else:
            # Dừng nhạc nền và phát âm thanh khi thua
            if music_playing:  
                pygame.mixer.music.stop()
                gameover_sound.play()
                music_playing = False  

        world.draw(surface)

        screen.blit(surface, (0, 0))

        text = font.render("Score: {0}".format(world.score), 1, TEXT_COLOR)
        screen.blit(text, (5, 10))
        top_score = high_score_manager.load_high_score()
        top_score_text = font.render("Top Score: {0}".format(top_score), 1, TEXT_COLOR)
        screen.blit(top_score_text, (5, 60))
        if world.is_game_over():
            game_over = font.render("Game Over", 1, TEXT_COLOR)
            screen.blit(game_over, (SCREEN_WiDTH / 3, SCREEN_HEIGHT / 2))
            hit_r = font.render("Hit R to Reset", 1, TEXT_COLOR)
            screen.blit(hit_r, (SCREEN_WiDTH / 3, SCREEN_HEIGHT / 2 + 70))

        pygame.display.update()

if __name__ == '__main__':
    run()
    pygame.quit()