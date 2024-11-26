import pygame
import random
from config import *

class Enemy:
    def __init__(self):
        self.size=random.randint(ENEMY_MIN_SIZE, ENEMY_MAX_SIZE)
        self.speed=random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.image = pygame.image.load('assets/images/enemy.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))
        self.position=(random.randint(0,SCREEN_WiDTH-self.size),0-self.size)

    def draw(self, surface):
        surface.blit(self.image, self.position)
    
    def move(self):
        self.position=(self.position[0], self.position[1]+self.speed)

    def is_off_screen(self):
        return self.position[1]>SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.position, (self.size, self.size))