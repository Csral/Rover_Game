import pygame

# Window dimensions
WIDTH, HEIGHT = 1440, 720

# Colors

PRIORITY_COLORS = {
    0: (100, 100, 100),   # Gray
    1: (0, 100, 255),     # Blue
    2: (0, 200, 0),       # Green
    3: (255, 255, 0),     # Yellow
    4: (255, 165, 0),     # Orange
    5: (255, 0, 0)        # Red
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
DARK_GRAY = (40, 40, 40)

def get_contrast_color(bg_color):
    # YIQ brightness formula
    r, g, b = bg_color
    brightness = (r*299 + g*587 + b*114) / 1000
    return (0,0,0) if brightness > 128 else (255,255,255)

# Fonts
def get_font(size=24):
    return pygame.font.SysFont("consolas", size)

# Button utility
class Button:
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.hover = False

    def draw(self, WIN, font):
        color = BLUE if self.hover else GRAY
        pygame.draw.rect(WIN, color, self.rect)
        pygame.draw.rect(WIN, WHITE, self.rect, 2)
        text_surf = font.render(self.text, True, WHITE)
        WIN.blit(text_surf, (self.rect.x + 10, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            self.action()