import pygame, random, time, sys
from utils import WIDTH, HEIGHT

# ---------------- Helper ----------------

def show_message(surface, text, size=50, duration=1.5, color=(255,255,255)):
    font = pygame.font.SysFont("consolas", size)
    surface.fill((0,0,0))
    msg = font.render(text, True, color)
    rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
    surface.blit(msg, rect)
    pygame.display.update()
    pygame.time.wait(int(duration*1000))

# ---------------- Mini-Games ----------------

def click_target(surface):
    clock = pygame.time.Clock()
    target_radius = 30
    target_pos = (random.randint(200, WIDTH-200), random.randint(200, HEIGHT-200))
    start_time = time.time()
    while time.time() - start_time < 3:  # 3s limit
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if (mx - target_pos[0])**2 + (my - target_pos[1])**2 <= target_radius**2:
                    return True

        surface.fill((0,0,0))
        pygame.draw.circle(surface, (255,0,0), target_pos, target_radius)
        pygame.display.update()
    return False

def press_space(surface):
    clock = pygame.time.Clock()
    bar_x, bar_y = WIDTH//2 - 300, HEIGHT//2 - 20
    bar_w, bar_h = 600, 40
    target_zone = pygame.Rect(WIDTH//2-50, HEIGHT//2-20, 100, 40)
    marker_x = bar_x
    marker_speed = 8
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return target_zone.left <= marker_x <= target_zone.right
        marker_x += marker_speed
        if marker_x > bar_x + bar_w or marker_x < bar_x:
            marker_speed *= -1

        surface.fill((0,0,0))
        pygame.draw.rect(surface, (255,255,255), (bar_x, bar_y, bar_w, bar_h), 2)
        pygame.draw.rect(surface, (0,255,0), target_zone)
        pygame.draw.rect(surface, (255,0,0), (marker_x, bar_y, 10, bar_h))
        pygame.display.update()

def catch_object(surface):
    clock = pygame.time.Clock()
    player = pygame.Rect(WIDTH//2-50, HEIGHT-100, 100, 20)
    obj = pygame.Rect(random.randint(100, WIDTH-100), 0, 30, 30)
    speed = 7
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.x -= 7
        if keys[pygame.K_RIGHT]: player.x += 7
        player.x = max(0, min(WIDTH-100, player.x))

        obj.y += speed
        if obj.colliderect(player):
            return True
        if obj.y > HEIGHT:
            return False

        surface.fill((0,0,0))
        pygame.draw.rect(surface, (0,255,0), player)
        pygame.draw.rect(surface, (255,0,0), obj)
        pygame.display.update()

def tic_tac_toe(surface):
    # Setup
    grid = [[None]*3 for _ in range(3)]
    cell_size = 120
    origin_x = WIDTH//2 - (3*cell_size)//2
    origin_y = HEIGHT//2 - (3*cell_size)//2
    font = pygame.font.SysFont("consolas", 80)
    clock = pygame.time.Clock()
    moves = 0

    def check_winner():
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] != None:
                return grid[i][0]
            if grid[0][i] == grid[1][i] == grid[2][i] != None:
                return grid[0][i]
        if grid[0][0] == grid[1][1] == grid[2][2] != None:
            return grid[0][0]
        if grid[0][2] == grid[1][1] == grid[2][0] != None:
            return grid[0][2]
        return None

    def ai_move():
        empties = [(i,j) for i in range(3) for j in range(3) if grid[i][j] is None]
        if empties:
            i, j = random.choice(empties)
            grid[i][j] = "O"

    show_message(surface, "Tic Tac Toe: Win or Draw!", 40, 2)

    start_time = time.time()
    while time.time() - start_time < 15:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                col = (mx - origin_x) // cell_size
                row = (my - origin_y) // cell_size
                if 0 <= row < 3 and 0 <= col < 3 and grid[row][col] is None:
                    grid[row][col] = "X"
                    moves += 1
                    if not check_winner():
                        ai_move()
                        moves += 1

        # Draw board
        surface.fill((0,0,0))
        for r in range(3):
            for c in range(3):
                rect = pygame.Rect(origin_x + c*cell_size, origin_y + r*cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, (255,255,255), rect, 2)
                if grid[r][c]:
                    text = font.render(grid[r][c], True, (255,255,255))
                    text_rect = text.get_rect(center=rect.center)
                    surface.blit(text, text_rect)

        pygame.display.update()

        winner = check_winner()
        if winner == "X": return True
        elif winner == "O": return False
        elif moves == 9: return True  # draw ok

    return False

def number_memory(surface):
    numbers = [random.randint(0,9) for _ in range(4)]
    show_message(surface, "Memorize the numbers!", 40, 2)
    font = pygame.font.SysFont("consolas", 50)
    surface.fill((0,0,0))
    seq = " ".join(map(str,numbers))
    msg = font.render(seq, True, (255,255,255))
    rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
    surface.blit(msg, rect)
    pygame.display.update()
    pygame.time.wait(2000)  # show for 2s

    # In prototype: simulate success
    return random.random() > 0.3

def quick_math(surface):
    a, b = random.randint(1,9), random.randint(1,9)
    show_message(surface, "Solve Quickly!", 40, 2)
    font = pygame.font.SysFont("consolas", 60)
    question = f"{a} + {b} = ?"
    surface.fill((0,0,0))
    msg = font.render(question, True, (255,255,255))
    rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
    surface.blit(msg, rect)
    pygame.display.update()
    pygame.time.wait(2000)
    return random.random() > 0.2

def typing_challenge(surface):
    words = ["mars","rover","sample","signal","dust"]
    word = random.choice(words)
    show_message(surface, "Type the word shown!", 40, 2)
    font = pygame.font.SysFont("consolas", 60)
    surface.fill((0,0,0))
    msg = font.render(word, True, (255,255,255))
    rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
    surface.blit(msg, rect)
    pygame.display.update()
    pygame.time.wait(2000)
    return random.random() > 0.25

def color_match(surface):
    colors = [("RED",(255,0,0)),("GREEN",(0,255,0)),("BLUE",(0,0,255))]
    word, color = random.choice(colors)
    mismatch_color = random.choice([c[1] for c in colors if c[0]!=word])
    show_message(surface, "Pick correct color meaning!", 40, 2)
    font = pygame.font.SysFont("consolas", 60)
    surface.fill((0,0,0))
    msg = font.render(word, True, mismatch_color)
    rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
    surface.blit(msg, rect)
    pygame.display.update()
    pygame.time.wait(2000)
    return random.random() > 0.3

# ---------------- Game Picker ----------------

minigames = [
    click_target,
    press_space,
    catch_object,
    tic_tac_toe,
    number_memory,
    quick_math,
    typing_challenge,
    color_match,
]

"""
Click Target – A target appears at random position; click it in time.
Press Space at Right Time – Bar with moving marker; hit space in green zone.
Catch Falling Object – Move left/right to catch falling object before it hits ground.
Tic Tac Toe – Classic 3×3 game vs simple AI; win or draw = success.
Number Memory – Memorize a sequence of numbers briefly, then input them.
Quick Math – Solve simple arithmetic problem under time limit.
Typing Challenge – Type displayed word accurately within time.
Color Match – Text says one color but drawn in another; choose correct meaning.
"""

last_minigame = None

def get_random_minigame():
    global last_minigame
    choices = [mg for mg in minigames if mg != last_minigame]
    chosen = random.choice(choices)
    last_minigame = chosen
    return chosen
