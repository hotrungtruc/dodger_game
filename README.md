
# Dodger Game 🎮

**Dodger Game** là một trò chơi đơn giản được phát triển bằng Python với thư viện **Pygame**. Nhiệm vụ của người chơi là điều khiển nhân vật (player) để tránh các vật cản (enemy) rơi từ trên xuống. Điểm số sẽ tăng dần khi bạn sống sót lâu hơn!

---

## 🚀 Tính năng
- **Điều khiển nhân vật**: Bằng bàn phím (W/A/S/D hoặc phím mũi tên) hoặc chuột.
- **Hiệu ứng đồ họa**: Nhân vật được trang bị hiệu ứng lửa động.
- **Nhạc nền và âm thanh**:
  - Nhạc nền thư giãn.
  - Hiệu ứng âm thanh khi thua.
- **Tính điểm**: Điểm số tăng theo thời gian.

---

## 📁 Cấu trúc dự án
```plaintext
project/
├── assets/                    # Chứa các tài nguyên
│   ├── images/                # Hình ảnh
│   │   ├── player.png
│   │   ├── enemy.png
│   │   ├── background.png
│   ├── musics_and_sounds/     # Âm thanh
│       ├── background.mp3
│       ├── gameover.WAV
├── config.py                  # Cấu hình (biến cố định)
├── main.py                    # Tệp chính để chạy game
├── core/                      # Các thành phần chính của game
│   ├── __init__.py            # Để đánh dấu thư mục là một module
│   ├── player.py              # Lớp Player
│   ├── enemy.py               # Lớp Enemy
│   ├── world.py               # Lớp World
├── utils/                     # Các tiện ích, hàm hỗ trợ
│   ├── __init__.py
│   ├── helpers.py             # Các hàm phụ trợ chung
└── README.md                  # Hướng dẫn, mô tả dự án
```

---

## 🛠️ Cài đặt

### 1. Yêu cầu
- Python >= 3.8
- Thư viện `pygame` 

Cài đặt `pygame` bằng lệnh:
```bash
pip install pygame
```

### 2. Chạy trò chơi
- Clone dự án về:
```bash
git clone <repository-url>
```

- Di chuyển đến thư mục dự án:
```bash
cd project
```

- Chạy tệp `main.py`:
```bash
python main.py
```

---

## 🎮 Cách chơi
1. Sử dụng bàn phím:
   - **W hoặc Mũi tên Lên**: Di chuyển lên.
   - **S hoặc Mũi tên Xuống**: Di chuyển xuống.
   - **A hoặc Mũi tên Trái**: Di chuyển sang trái.
   - **D hoặc Mũi tên Phải**: Di chuyển sang phải.
2. Hoặc điều khiển bằng chuột.
3. Tránh va chạm với các vật cản.
4. Nếu thua, nhấn **R** để chơi lại.

---

## 📖 Thông tin thêm
- **Ngôn ngữ lập trình**: Python
- **Thư viện sử dụng**: Pygame
- **Hiệu ứng âm thanh**: [Nguồn miễn phí](https://freesound.org)

---

## 📜 Giấy phép
Dự án này sử dụng giấy phép [MIT](LICENSE). Bạn có thể tự do sao chép, chỉnh sửa và phân phối.

---

## 🛠️ Đóng góp
Nếu bạn muốn đóng góp:
1. Fork dự án.
2. Tạo nhánh mới:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit thay đổi:
   ```bash
   git commit -m "Add my feature"
   ```
4. Tạo Pull Request.

Cảm ơn bạn đã quan tâm đến dự án này! 🎉
