import json
from config import *

class HighScoreManager:
    def __init__(self, file_name='high_score.json'):
        self.file_name = file_name
    
    def load_high_score(self):
        """
        Hàm tải điểm cao nhất từ file.
        Nếu file không tồn tại hoặc bị lỗi, trả về 0.
        """
        try:
            with open(self.file_name, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_high_score(self, score):
        """
        Hàm lưu điểm cao nhất vào file.
        """
        try:
            high_score = self.load_high_score()
            if score > high_score:
                with open(self.file_name, 'w') as f:
                    json.dump({'high_score': score}, f)
        except Exception as e:
            print(f"Error saving high score: {e}")