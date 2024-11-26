import pygame
from config import *

class Menu:
    def __init__(self, screen):
        """
        Hàm khởi tạo Menu. Nhận đối tượng màn hình và khởi tạo các thuộc tính menu như phông chữ, hình nền, và các nút.
        """
        self.screen = screen
        self.font = pygame.font.SysFont("bold", 60) 
        self.background = pygame.Surface((SCREEN_WiDTH, SCREEN_HEIGHT))  
        self.background = pygame.image.load("assets/images/menu_bg.jpg") 
        self.background = pygame.transform.scale(self.background, (SCREEN_WiDTH, SCREEN_HEIGHT))  

        # Danh sách các nút trong menu, mỗi nút có nhãn (label), hành động (action) và kích thước (rect)
        self.buttons = [
            {"label": "Start Game", "action": "start", "rect": pygame.Rect(0, 0, 0, 0)},
            {"label": "Quit Game", "action": "quit", "rect": pygame.Rect(0, 0, 0, 0)},
        ]

    def draw(self):
        """
        Hàm vẽ menu lên màn hình, bao gồm hình nền và các nút.
        Các nút có hiệu ứng hover (di chuột qua) để thay đổi màu sắc.
        """
        self.screen.blit(self.background, (0, 0))  

        # Duyệt qua tất cả các nút và vẽ chúng lên màn hình
        for i, button in enumerate(self.buttons):
            # Tạo nhãn cho nút (label) với màu trắng
            label = self.font.render(button["label"], True, (255, 255, 255))  
            x = SCREEN_WiDTH // 2 - label.get_width() // 2  
            y = SCREEN_HEIGHT // 3 + i * 100  

            # Tính kích thước khung nút lớn hơn một chút để tạo khoảng cách xung quanh văn bản
            button_width = label.get_width() + 40  
            button_height = label.get_height() + 20 

            # Tạo hình chữ nhật (rect) cho nút
            button["rect"] = pygame.Rect(x, y, button_width, button_height)

            # Kiểm tra xem chuột có di qua nút không (hover effect)
            if button["rect"].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (102, 204, 255), button["rect"])  
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 3)  # Khung màu trắng với độ dày 3

            self.screen.blit(label, (x + 20, y + 10))  # Căn giữa chữ, thêm khoảng cách xung quanh

    def handle_event(self, event):
        """
        Xử lý sự kiện chuột. Kiểm tra nếu người dùng nhấn vào một nút.
        Nếu nhấn vào nút, trả về hành động tương ứng (start hoặc quit).
        """
        if event.type == pygame.MOUSEBUTTONDOWN:  
            pos = pygame.mouse.get_pos()  
            for button in self.buttons:
                if button["rect"].collidepoint(pos):  
                    return button["action"]  
        return None  
