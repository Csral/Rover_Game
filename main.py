import pygame, sys, random, time
from utils import WHITE, BLACK, RED, GREEN, ORANGE, PRIORITY_COLORS, get_font, get_contrast_color, Button
from events import generate_random_event
from minigames import get_random_minigame
from logs import generate_log

#* Init
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rover Event Control")

MISSION_TIME = 300  # 5 min
MAX_ACTIVE_EVENTS = 5

# state config
event_id_counter = 1
incoming_events = []
active_events = []
queued_events = []
selected_event = None
selected_list = None
health = 100
score = 0
start_time = time.time()

# Logs
logs = []
last_log_time = 0

# Healing mini-game trigger
next_heal_trigger = random.randint(20, 40)

font = get_font(22)

# Buttons
buttons = []
button_labels = [
    ("Honor [H]", lambda: honor_event()),
    ("Reject [R]", lambda: reject_event()),
    ("Queue [Q]", lambda: queue_event()),
    ("Execute [S]", lambda: execute_from_queue()),
    ("Terminate [T]", lambda: terminate_event()),
    ("Priority++ [M]", lambda: modify_priority()),
    ("Priority-- [N]", lambda: modify_priority_down()),
]

def center_buttons():
    btn_width, btn_height, spacing = 180, 40, 20
    total_width = len(button_labels) * (btn_width + spacing) - spacing
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT - 80
    buttons.clear()
    for i, (label, action) in enumerate(button_labels):
        rect = (start_x + i * (btn_width + spacing), y, btn_width, btn_height)
        buttons.append(Button(rect, label, action))

center_buttons()

#* Game functions
def honor_event():
    global selected_event, selected_list, health, score
    if selected_event and selected_list == "incoming" and len(active_events) < MAX_ACTIVE_EVENTS:
        if selected_event in incoming_events:
            incoming_events.remove(selected_event)
            active_events.append(selected_event)
            logs.append(f"Honored: {selected_event.hint_text()} (P{selected_event.priority})")
            selected_event = None
            # Mini-game
            if random.random() < 0.3:
                if not trigger_minigame():
                    health -= 10
                else:
                    score += 10

def reject_event():
    global selected_event, selected_list, health
    if selected_event and selected_list == "incoming":
        if selected_event in incoming_events:
            incoming_events.remove(selected_event)
            health -= 5
            logs.append(f"Rejected: {selected_event.hint_text()} (P{selected_event.priority})")
        selected_event = None

def queue_event():
    global selected_event, selected_list
    if selected_event and selected_list == "incoming":
        if selected_event in incoming_events:
            incoming_events.remove(selected_event)
            queued_events.append(selected_event)
            logs.append(f"Queued: {selected_event.hint_text()} (P{selected_event.priority})")
            selected_event = None

def execute_from_queue():
    global selected_event, selected_list
    if selected_event and selected_list == "queue" and len(active_events) < MAX_ACTIVE_EVENTS:
        if selected_event in queued_events:
            queued_events.remove(selected_event)
            active_events.append(selected_event)
            logs.append(f"Executed: {selected_event.hint_text()} (P{selected_event.priority})")
            selected_event = None

def terminate_event():
    global selected_event, selected_list, health
    if selected_event:
        if selected_list == "active" and selected_event in active_events:
            fraction_completed = 1 - (selected_event.duration / selected_event.total_duration)
            damage = 10 * (1 - fraction_completed) + 3 * fraction_completed
            health -= int(damage)
            active_events.remove(selected_event)
            logs.append(f"Terminated: {selected_event.hint_text()} (-{int(damage)} HP)")
        elif selected_list == "queue" and selected_event in queued_events:
            queued_events.remove(selected_event)
            logs.append(f"Removed from Queue: {selected_event.hint_text()}")
        selected_event = None

def modify_priority():
    global selected_event, selected_list
    if selected_event and selected_list == "queue":
        selected_event.modify_priority(1)

def modify_priority_down():
    global selected_event, selected_list
    if selected_event and selected_list == "queue":
        selected_event.modify_priority(-1)

def trigger_minigame():
    mg = get_random_minigame()
    return mg(WIN)

#* UI
incoming_rects, active_rects, queue_rects = [], [], []

def draw_event_list(events, title, x, y, list_name, rect_store, show_timer=False):
    WIN.blit(font.render(title, True, ORANGE), (x, y))
    rect_store.clear()

    box_width = 400
    max_width = box_width - 10  # padding inside box
    base_font = font

    vertical_spacing = 42  # spacing between entries
    box_height = 32        # height of each event box

    for i, ev in enumerate(events[:8]):
        rect_y = y + 30 + i * vertical_spacing
        rect = pygame.Rect(x, rect_y, box_width, box_height)
        rect_store.append((rect, ev))

        # Priority color
        priority_color = PRIORITY_COLORS.get(ev.priority, (70,70,70))
        if ev == selected_event:
            priority_color = tuple(min(255, c + 50) for c in priority_color)
        pygame.draw.rect(WIN, priority_color, rect)

        # Build event text
        text = f"{ev.name} [{ev.hint_text()}] P{ev.priority}"
        if show_timer:
            text += f" [{ev.duration:.1f}s]"
        else:
            text += f" [{ev.expire_time:.1f}s]"

        text_color = get_contrast_color(priority_color)

        # Word wrapping by pixel width
        words = text.split(" ")
        lines = [""]
        for word in words:
            test_line = lines[-1] + word + " "
            if base_font.size(test_line)[0] <= max_width:
                lines[-1] = test_line
            else:
                lines.append(word + " ")

        # Shrink font if >2 lines
        if len(lines) > 2:
            small_font = get_font(18)
            lines = [" ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])]
            for j, line in enumerate(lines[:2]):
                WIN.blit(small_font.render(line.strip(), True, text_color),
                         (x+5, rect_y + j*14))
        else:
            for j, line in enumerate(lines):
                WIN.blit(base_font.render(line.strip(), True, text_color),
                         (x+5, rect_y + j*14))
        
def draw_ui():
    WIN.fill((30, 30, 30))

    # Health bar
    pygame.draw.rect(WIN, RED, (WIDTH//2 - 200, 20, 400, 25))
    pygame.draw.rect(WIN, GREEN, (WIDTH//2 - 200, 20, 4*health, 25))

    # Score
    WIN.blit(font.render(f"Score: {score}", True, WHITE), (WIDTH//2 - 50, 55))

    # Timer
    elapsed = int(time.time() - start_time)
    remaining = max(0, MISSION_TIME - elapsed)
    WIN.blit(font.render(f"Time: {remaining}s", True, WHITE), (WIDTH//2 - 50, 80))

    # Event lists
    margin_top = 120
    spacing_x = 20
    panel_width = 400
    total_width = 3 * panel_width + 2 * spacing_x
    start_x = (WIDTH - total_width) // 2

    draw_event_list(incoming_events, "Incoming Events", start_x, margin_top, "incoming", incoming_rects)
    draw_event_list(active_events, "Active Events", start_x + panel_width + spacing_x, margin_top, "active", active_rects, show_timer=True)
    draw_event_list(queued_events, "Queued Events", start_x + 2*(panel_width + spacing_x), margin_top, "queue", queue_rects)

    # Logs
    WIN.blit(font.render("System Logs", True, ORANGE), (WIDTH//2 - 100, 400))
    log_area = pygame.Rect(WIDTH//2 - 480, 430, 960, 200)
    pygame.draw.rect(WIN, (40, 40, 40), log_area)
    pygame.draw.rect(WIN, WHITE, log_area, 1)
    for i, entry in enumerate(logs[-7:]):
        if isinstance(entry, tuple):
            log, color = entry
        else:
            log, color = entry, WHITE  # fallback for old string logs
        WIN.blit(font.render(log, True, color), (log_area.x + 10, log_area.y + 5 + i*22))

    # Buttons
    for btn in buttons:
        btn.draw(WIN, font)

    pygame.display.update()

# Input processor
def handle_click(pos):
    global selected_event, selected_list
    for rect, ev in incoming_rects:
        if rect.collidepoint(pos):
            selected_event, selected_list = ev, "incoming"
            return
    for rect, ev in active_rects:
        if rect.collidepoint(pos):
            selected_event, selected_list = ev, "active"
            return
    for rect, ev in queue_rects:
        if rect.collidepoint(pos):
            selected_event, selected_list = ev, "queue"
            return
    for btn in buttons:
        if btn.rect.collidepoint(pos):
            btn.action()

#* GAME LOOP
clock = pygame.time.Clock()
spawn_timer = 0

running = True
while running:
    clock.tick(60)
    spawn_timer += 1
    elapsed = int(time.time() - start_time)

    # Spawn new event every 3s
    if spawn_timer >= 180:
        incoming_events.append(generate_random_event(event_id_counter))
        event_id_counter += 1
        spawn_timer = 0

    # Expire incoming events
    for ev in incoming_events[:]:
        ev.expire_time -= 1/60
        if ev.expire_time <= 0:
            incoming_events.remove(ev)
            health -= ev.impact
            logs.append(f"Missed: {ev.hint_text()} (-{ev.impact} HP)")

    # Decrement active events timer
    for ev in active_events[:]:
        ev.duration -= 1/60
        if ev.duration <= 0:
            active_events.remove(ev)
            score += ev.benefit
            logs.append(f"Completed: {ev.hint_text()} (+{ev.benefit} pts)")

    # Generate logs every 0.5s
    if time.time() - last_log_time >= 0.5:
        logs.append(generate_log())
        if len(logs) > 30:
            logs.pop(0)
        last_log_time = time.time()

    # Random healing mini-game
    if elapsed >= next_heal_trigger:
        if trigger_minigame():
            health = min(100, health + 15)
            logs.append("Healing mini-game success! +15 HP")
        next_heal_trigger = elapsed + (random.randint(10,20) if health < 30 else random.randint(20,40))

    # Check fail/win
    if health <= 0 or elapsed >= MISSION_TIME:
        WIN.fill(BLACK)
        msg = "MISSION SUCCESS!" if health > 0 else "ROVER FAILURE!"
        WIN.blit(font.render(f"{msg} Final Health: {health}, Score: {score}", True, WHITE), (WIDTH//2 - 200, HEIGHT//2))
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)
        if event.type == pygame.MOUSEMOTION:
            for btn in buttons:
                btn.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h: honor_event()
            elif event.key == pygame.K_r: reject_event()
            elif event.key == pygame.K_q: queue_event()
            elif event.key == pygame.K_s: execute_from_queue()
            elif event.key == pygame.K_t: terminate_event()
            elif event.key == pygame.K_m: modify_priority()
            elif event.key == pygame.K_n: modify_priority_down()

    draw_ui()