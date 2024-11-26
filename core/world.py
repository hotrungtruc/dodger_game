import pygame
from core.player import Player
from core.enemy import Enemy
from config import *

class World:
    def __init__(self):
        self.reset()
        self.background = pygame.image.load('assets/images/background.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WiDTH, SCREEN_HEIGHT))
    
    def reset(self):
        self.player=Player()
        self.enemies=[]
        self.gameOver=False
        self.score=0
        self.enemy_counter=0
        self.moveUp=False
        self.moveDown=False
        self.moveLeft=False
        self.moveRight=False
        self.using_mouse = True

    def is_game_over(self):
        return self.gameOver
    
    def update(self):
        self.score += 1

        # Kiểm tra di chuyển bằng phím
        if self.moveUp or self.moveDown or self.moveLeft or self.moveRight:
            self.using_mouse = False  # Tắt chuột khi dùng phím
            if self.moveUp:
                self.player.move(0, -PLAYER_SPEED)
            if self.moveDown:
                self.player.move(0, PLAYER_SPEED)
            if self.moveLeft:
                self.player.move(-PLAYER_SPEED, 0)
            if self.moveRight:
                self.player.move(PLAYER_SPEED, 0)

        # Di chuyển bằng chuột (nếu không sử dụng bàn phím)
        elif self.using_mouse:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_x = max(0, min(mouse_x - PLAYER_SIZE / 2, SCREEN_WiDTH - PLAYER_SIZE))
            player_y = max(PLAYER_MAX_UP, min(mouse_y - PLAYER_SIZE / 2, SCREEN_HEIGHT - PLAYER_SIZE))
            self.player.position = (player_x, player_y)

        # Xử lý kẻ thù
        for e in self.enemies:
            e.move()
            if self.player.did_hit(e.get_rect()):
                self.gameOver = True
            if e.is_off_screen():
                self.enemies.remove(e)

        self.enemy_counter += 1
        if self.enemy_counter > ENEMY_SPAWN_RATE:
            self.enemy_counter = 0
            self.enemies.append(Enemy())


    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        self.player.draw(surface)
        for e in self.enemies:
            e.draw(surface)

    def handle_keys(self, event):
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
