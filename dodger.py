import pygame, random, sys
from pygame.locals import *
from background_effects import background_with_stars

WINDOWWIDTH = 1200
WINDOWHEIGHT = 800
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 20
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 30
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 3
ADDNEWBADDIERATE = 5
PLAYERMOVERATE = 5
GRAVITY_FACTOR = 0.0005 # Điều chỉnh mức độ hút


def terminate():
    """
    Thoát khỏi trò chơi.
    Gọi hàm pygame.quit() để tắt pygame và sys.exit() để dừng chương trình.
    """
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    """
    Chờ người chơi nhấn phím để tiếp tục.
    Lắng nghe các sự kiện từ bàn phím hoặc thoát trò chơi nếu cần.
    Nếu phím Escape được nhấn, trò chơi kết thúc.
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    """
    Kiểm tra xem người chơi có va chạm với baddies không.
    Duyệt qua danh sách baddies và kiểm tra nếu hình chữ nhật của người chơi
    giao nhau với hình chữ nhật của bất kỳ baddie nào.
    Trả về True nếu có va chạm, ngược lại trả về False.
    
    Args:
        playerRect (pygame.Rect): Hình chữ nhật đại diện cho người chơi.
        baddies (list): Danh sách các đối tượng "baddie", mỗi đối tượng chứa hình chữ nhật 'rect'.
    """
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    """
    Vẽ văn bản lên bề mặt màn hình tại vị trí chỉ định.
    Sử dụng font và màu văn bản được cấu hình trước.

    Args:
        text (str): Chuỗi văn bản cần hiển thị.
        font (pygame.font.Font): Font chữ dùng để hiển thị văn bản.
        surface (pygame.Surface): Bề mặt màn hình để vẽ văn bản.
        x (int): Tọa độ x của góc trên cùng bên trái của văn bản.
        y (int): Tọa độ y của góc trên cùng bên trái của văn bản.
    """
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.WAV')
pygame.mixer.music.load('background.WAV')

# set up images
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')
backgroundImage = pygame.image.load('background.png')

# resize the background to fit the window size
backgroundImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))

# Hiển thị hiệu ứng nền và menu bắt đầu
background_with_stars(windowSurface, num_stars=100)

# Hiển thị văn bản "Dodger" và hướng dẫn
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()

# Chờ người chơi nhấn phím
waitForPlayerToPressKey()

#Set up chuột tàn hình
pygame.mouse.set_visible(False)


topScore = 0
while True:
    # set up the start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # the game loop runs while the game part is playing
        score += 1  # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)

            # Random góc xuất hiện
            startCorner = random.choice(['top_left', 'top_right', 'bottom_left', 'bottom_right'])

            if startCorner == 'top_left':
                startX, startY = 0, 0
                speedX, speedY = random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
            elif startCorner == 'top_right':
                startX, startY = WINDOWWIDTH, 0
                speedX, speedY = -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
            elif startCorner == 'bottom_left':
                startX, startY = 0, WINDOWHEIGHT
                speedX, speedY = random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
            elif startCorner == 'bottom_right':
                startX, startY = WINDOWWIDTH, WINDOWHEIGHT
                speedX, speedY = -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)

            # Tạo baddie mới
            newBaddie = {
                'rect': pygame.Rect(startX, startY, baddieSize, baddieSize),
                'speedX': speedX,
                'speedY': speedY,
                'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
            }
            baddies.append(newBaddie)

        # Cập nhật vị trí baddies với lực hút
        for b in baddies:
            # Tính toán lực hút hướng về player
            if not reverseCheat and not slowCheat:
                dx = playerRect.centerx - b['rect'].centerx  # Khoảng cách x đến player
                dy = playerRect.centery - b['rect'].centery  # Khoảng cách y đến player

                # Điều chỉnh tốc độ theo hướng player
                b['speedX'] += dx * GRAVITY_FACTOR
                b['speedY'] += dy * GRAVITY_FACTOR

                # Di chuyển baddie
                b['rect'].move_ip(b['speedX'], b['speedY'])

            elif reverseCheat:
                b['rect'].move_ip(-b['speedX'], -b['speedY'])

            elif slowCheat:
                b['rect'].move_ip(b['speedX'] * 0.5, b['speedY'] * 0.5)


        # Xóa các baddie nếu ra ngoài cửa sổ
        for b in baddies[:]:
            if (b['rect'].top > WINDOWHEIGHT or b['rect'].bottom < 0 or
                b['rect'].left > WINDOWWIDTH or b['rect'].right < 0):
                baddies.remove(b)


        # Draw the game world on the window.
        windowSurface.blit(backgroundImage, (0, 0))  # Sử dụng ảnh nền

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score  # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
