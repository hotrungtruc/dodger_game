import pygame
import random
from config import *

class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.image = pygame.image.load('assets/images/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.position = (SCREEN_WiDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 10)

    def draw(self, surface):
        # Vẽ player mà không có hiệu ứng blur
        surface.blit(self.image, self.position)

        # Vẽ lửa
        self.draw_fire(surface)

    def draw_fire(self, surface):
        player_x, player_y = self.position

        # Đặt tọa độ hai bên dưới player
        left_fire_x = player_x + self.size // 5
        right_fire_x = player_x + self.size - self.size // 3 + 4
        fire_y = player_y + self.size + 17

        # Vẽ hai ngọn lửa
        for fire_x in (left_fire_x, right_fire_x):
            self.draw_flame(surface, fire_x, fire_y)

    def draw_flame(self, surface, fire_x, fire_y):
        # Tạo các vòng lửa gradient từ cam đến vàng với kích thước nhỏ hơn
        for i in range(4):  # Số vòng lửa
            width = random.randint(4, 8) * (4 - i)  # Giảm dần kích thước (giảm tối thiểu)
            height = random.randint(6, 10) * (4 - i)  # Giảm chiều cao
            alpha = max(0, 150 - i * 40)  # Giảm độ trong suốt một cách mượt mà
            flame_color = (255, 100 + i * 30, 0, alpha)  # Màu từ cam đến vàng nhạt
            flame_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Hỗ trợ alpha
            pygame.draw.ellipse(flame_surface, flame_color, (0, 0, width, height))
            surface.blit(flame_surface, (fire_x - width // 2, fire_y - height // 2))

    def move(self, x, y):
        # Cập nhật vị trí
        new_x = self.position[0] + x
        new_y = self.position[1] + y
        if new_x < 0 or new_x > SCREEN_WiDTH - self.size:
            new_x = self.position[0]
        if new_y < PLAYER_MAX_UP or new_y > SCREEN_HEIGHT - self.size:
            new_y = self.position[1]

        # Cập nhật vị trí player
        self.position = (new_x, new_y)

    def get_rect(self):
        return pygame.Rect(self.position, (self.size, self.size))

    def did_hit(self, rect):
        r = self.get_rect()
        return r.colliderect(rect)

