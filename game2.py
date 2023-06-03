import pygame
import string
import random
import time
import math

# 게임 설정
WIDTH = 500
HEIGHT = 500
FPS = 60
BOUNDARY_PADDING = 20  # 최대 경계로부터의 패딩

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 알파벳 설정
alphabet = list(string.ascii_lowercase)

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 게임 변수 초기화
start_time = 0
elapsed_time = 0
letters = {}  # 알파벳 객체를 담을 딕셔너리
success = False

def create_letters():
    positions = get_unique_positions(len(alphabet))
    for i, letter in enumerate(alphabet):
        x, y = positions[i]
        letters[letter] = pygame.Rect(x-15, y-15, 30, 30)

def get_unique_positions(num_positions):
    positions = []
    total_positions = WIDTH * HEIGHT
    
    if num_positions > total_positions:
        raise ValueError("The number of positions exceeds the total available positions.")
    
    while len(positions) < num_positions:
        position = random.randint(0, total_positions - 1)
        x = position % WIDTH
        y = position // WIDTH
        if (
            x > BOUNDARY_PADDING
            and x < WIDTH - BOUNDARY_PADDING
            and y > BOUNDARY_PADDING
            and y < HEIGHT - BOUNDARY_PADDING
            and not any(math.hypot(x - px, y - py) < 50 for px, py in positions)
        ):
            positions.append((x, y))
    
    return positions

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x,y))
    screen.blit(text_surface, text_rect)


running = True
correct_idx = 0
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if correct_idx == 0:
                start_time = time.time()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:     
            pos = pygame.mouse.get_pos()
            clicked_letter = next((letter for letter, rect in letters.items() if rect.collidepoint(pos)), None)
            if clicked_letter and clicked_letter == alphabet[correct_idx]:
                del letters[clicked_letter]
                correct_idx += 1

    if start_time == 0:
        draw_text("Press Enter to Start!", pygame.font.Font(None, 50), BLACK, WIDTH/2, HEIGHT/2)
    else:
        if not success:
            elapsed_time = time.time() - start_time
            draw_text("Elapsed Time: {:.2f} seconds".format(elapsed_time), pygame.font.Font(None, 20), BLACK, 100, 20)

        if correct_idx == len(alphabet):
            if not success:
                success_time = elapsed_time
                success = True
            draw_text("Success!", pygame.font.Font(None, 50), BLACK, WIDTH/2, HEIGHT/2)
            draw_text("Elapsed Time: {:.2f} seconds".format(success_time), pygame.font.Font(None, 30), BLACK, WIDTH/2, HEIGHT/2 + 50)
        
        else: #화면 갱신될 떄 마다 표시되는 것들 (이 과정에서 삭제가 진행되기 때문에 없어지 객체를 제외하고 다시 그림)
            for letter,rect in letters.items(): 
                pygame.draw.rect(screen, WHITE, rect)
                draw_text(letter.upper(), pygame.font.Font(None, 30), BLACK, rect.centerx, rect.centery)

        if correct_idx < len(alphabet) and len(letters) == 0: # 처음에 그릴 때 
            create_letters()

    pygame.display.flip() # 현재 화면의 모든 내용을 실제 화면에 업데이트, 게임 루프 마지막에 호출해서 게임 상태 업데이트 및 새로운 프레임이 화면에 표시. 부드러운 애니메이션 및 그래픽

pygame.quit()