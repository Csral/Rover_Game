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
    pygame.time.wait(int(duration*1000))\
    
def get_user_input(surface, prompt="", font_size=50, max_time=7):
    """
    Displays a prompt and collects keyboard input with Enter.
    Returns typed string or None on timeout.
    """
    font = pygame.font.SysFont("consolas", font_size)
    clock = pygame.time.Clock()
    input_str = ""
    start_time = time.time()

    while True:
        # Timeout
        if time.time() - start_time > max_time:
            return None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_str
                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]
                elif event.key <= 127:  # printable chars
                    input_str += event.unicode

        # Draw prompt and typed text
        surface.fill((0,0,0))
        if prompt:
            prompt_text = font.render(prompt, True, (255,255,255))
            surface.blit(prompt_text, prompt_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        typed_text = font.render(input_str, True, (0,255,0))
        surface.blit(typed_text, typed_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.update()
        clock.tick(30)

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
    seq = "".join(map(str, numbers))

    show_message(surface, "Memorize the numbers!", 40, 2)
    font = pygame.font.SysFont("consolas", 50)

    # Show numbers
    surface.fill((0,0,0))
    msg = font.render(" ".join(seq), True, (255,255,255))
    surface.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.update()
    pygame.time.wait(2000)

    # Get input
    ans = get_user_input(surface, "Enter the numbers:")

    return ans == seq

def quick_math(surface):
    a, b = random.randint(1,9), random.randint(1,9)
    correct_answer = str(a + b)

    show_message(surface, "Solve Quickly!", 40, 2)
    font = pygame.font.SysFont("consolas", 60)

    # Show question
    surface.fill((0,0,0))
    msg = font.render(f"{a} + {b} = ?", True, (255,255,255))
    surface.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.update()

    # Get input
    ans = get_user_input(surface, "Your answer:")

    return ans == correct_answer

def typing_challenge(surface):
    words = ["mars","rover","sample","signal","dust"]
    word = random.choice(words)

    show_message(surface, "Type the word shown!", 40, 2)
    font = pygame.font.SysFont("consolas", 60)

    # Show word
    surface.fill((0,0,0))
    msg = font.render(word, True, (255,255,255))
    surface.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.update()

    # Get input
    ans = get_user_input(surface, "Type it exactly:")

    return ans == word

def color_match(surface):
    colors = [("RED",(255,0,0)),("GREEN",(0,255,0)),("BLUE",(0,0,255))]
    word, _ = random.choice(colors)
    mismatch_color = random.choice([c[1] for c in colors])  # may or may not mismatch

    show_message(surface, "Press R/G/B for WORD (not color)", 30, 2)
    font = pygame.font.SysFont("consolas", 60)

    # Show color word
    surface.fill((0,0,0))
    msg = font.render(word, True, mismatch_color)
    surface.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.update()

    # Wait for keypress
    start_time = time.time()
    while True:
        if time.time() - start_time > 5:  # timeout
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and word == "RED":
                    return True
                if event.key == pygame.K_g and word == "GREEN":
                    return True
                if event.key == pygame.K_b and word == "BLUE":
                    return True
                else:
                    return False

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
