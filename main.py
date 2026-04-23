import pygame
import sys
import math
import random
import json
import os
from collections import deque
from enum import Enum

# ------------------------- Initial Setup -------------------------
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 850
HEADER_HEIGHT = 120
GAME_AREA_HEIGHT = SCREEN_HEIGHT - HEADER_HEIGHT
DEAD_ZONE_Y = SCREEN_HEIGHT - 150


# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    STATS = 4


# Colors with gradients
BLACK = (18, 18, 24)
DARK_BG = (25, 25, 35)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 120, 255)
GREEN = (60, 255, 100)
YELLOW = (255, 220, 50)
PURPLE = (160, 60, 255)
ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (50, 50, 60)
CYAN = (60, 255, 255)
PINK = (255, 100, 150)
LIGHT_BLUE = (100, 200, 255)
SOFT_GREEN = (100, 255, 150)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Swipe Brick Breaker")
clock = pygame.time.Clock()

# Fonts with better styling
try:
    title_font = pygame.font.Font(None, 56)
    header_font = pygame.font.Font(None, 42)
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    large_font = pygame.font.Font(None, 72)
    number_font = pygame.font.Font(None, 32)
    huge_font = pygame.font.Font(None, 96)
except:
    title_font = pygame.font.SysFont('Arial', 56, bold=True)
    header_font = pygame.font.SysFont('Arial', 42, bold=True)
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)
    large_font = pygame.font.SysFont('Arial', 72, bold=True)
    number_font = pygame.font.SysFont('Arial', 32, bold=True)
    huge_font = pygame.font.SysFont('Arial', 96, bold=True)

# Game constants
MAX_COLS = 7
MARGIN = 5
BRICK_HEIGHT = 32

# Animation variables
screen_shake = 0
transition_alpha = 0
brick_move_animation = 0
countdown_value = 3
countdown_timer = 0

# Statistics
game_stats = {
    'bricks_broken': 0,
    'total_shots': 0,
    'accuracy': 0.0,
    'powerups_collected': 0,
    'max_combo': 0,
    'play_time': 0
}

# Sound effects (placeholder - will be created if files don't exist)
try:
    shoot_sound = pygame.mixer.Sound('shoot.wav')
    break_sound = pygame.mixer.Sound('break.wav')
    powerup_sound = pygame.mixer.Sound('powerup.wav')
    game_over_sound = pygame.mixer.Sound('gameover.wav')
except:
    # Create silent sounds if files don't exist
    shoot_sound = pygame.mixer.Sound(buffer=bytes(100))
    break_sound = pygame.mixer.Sound(buffer=bytes(100))
    powerup_sound = pygame.mixer.Sound(buffer=bytes(100))
    game_over_sound = pygame.mixer.Sound(buffer=bytes(100))


# ------------------------- Save System -------------------------
class SaveSystem:
    @staticmethod
    def save_best_score(score):
        try:
            data = {'best_score': score, 'games_played': 0, 'total_bricks': 0}
            if os.path.exists('save_data.json'):
                with open('save_data.json', 'r') as f:
                    existing = json.load(f)
                    data['games_played'] = existing.get('games_played', 0)
                    data['total_bricks'] = existing.get('total_bricks', 0)
                    if score <= existing.get('best_score', 0):
                        data['best_score'] = existing['best_score']

            with open('save_data.json', 'w') as f:
                json.dump(data, f)
            return data['best_score']
        except:
            return score

    @staticmethod
    def load_best_score():
        try:
            with open('save_data.json', 'r') as f:
                data = json.load(f)
                return data.get('best_score', 0)
        except:
            return 0

    @staticmethod
    def update_stats(games_played=0, total_bricks=0):
        try:
            data = {'best_score': 0, 'games_played': 0, 'total_bricks': 0}
            if os.path.exists('save_data.json'):
                with open('save_data.json', 'r') as f:
                    data = json.load(f)

            if games_played > 0:
                data['games_played'] = data.get('games_played', 0) + games_played
            if total_bricks > 0:
                data['total_bricks'] = data.get('total_bricks', 0) + total_bricks

            with open('save_data.json', 'w') as f:
                json.dump(data, f)
        except:
            pass


# ------------------------- Particle System -------------------------
class Particle:
    def __init__(self, x, y, color, velocity_scale=1.0):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 4) * velocity_scale
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = random.randint(40, 80)
        self.max_life = self.life
        self.size = random.randint(2, 6)
        self.gravity = 0.1

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.98
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = self.life / self.max_life
            size = int(self.size * alpha)
            if size > 0:
                c = tuple(int(ch * alpha) for ch in self.color)
                pygame.draw.circle(surface, c, (int(self.x), int(self.y)), size)
                if size > 2:
                    pygame.draw.circle(surface, (255, 255, 255, int(alpha * 100)),
                                       (int(self.x), int(self.y)), size + 1, 1)


# ------------------------- Floating Text -------------------------
class FloatingText:
    def __init__(self, x, y, text, color, size=24):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 60
        self.max_life = 60
        self.size = size
        self.vy = -1.5

    def update(self):
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = self.life / self.max_life
            font = pygame.font.Font(None, self.size)
            text_surface = font.render(self.text, True, self.color)
            text_surface.set_alpha(int(255 * alpha))
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            surface.blit(text_surface, text_rect)


# ------------------------- Button Class -------------------------
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = color
        self.animation = 0
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.hovered else self.color
        if self.hovered:
            self.animation = min(10, self.animation + 1)
        else:
            self.animation = max(0, self.animation - 1)

    def draw(self, surface):
        # Button shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=12)

        # Main button
        rect = self.rect.copy()
        if self.animation > 0:
            scale = 1 + (self.animation / 100)
            rect.width *= scale
            rect.height *= scale
            rect.center = self.rect.center

        pygame.draw.rect(surface, self.current_color, rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=10)

        # Text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# ------------------------- Item Class -------------------------
class Item:
    TYPES = {
        'extra_ball': {'color': CYAN, 'symbol': '+1', 'effect': 'add_ball'},
        'fire_ball': {'color': ORANGE, 'symbol': '🔥', 'effect': 'fire'},
        'pierce': {'color': PURPLE, 'symbol': '⟋', 'effect': 'pierce'}
    }

    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.type = item_type
        self.radius = 12
        self.active = True
        self.collected = False
        self.color = self.TYPES[item_type]['color']
        self.symbol = self.TYPES[item_type]['symbol']
        self.float_offset = random.uniform(0, math.pi * 2)
        self.float_timer = 0
        self.collect_animation = 0

    def update(self):
        self.float_timer += 0.05
        self.y += math.sin(self.float_timer + self.float_offset) * 0.5

        if self.collect_animation > 0:
            self.collect_animation -= 1
            self.radius += 1

    def draw(self, surface):
        if self.active:
            pulse = 1 + math.sin(self.float_timer * 2) * 0.1
            radius = int(self.radius * pulse)

            # Outer glow
            for i in range(3):
                glow_radius = radius + i * 2
                alpha = 100 - i * 30
                glow_color = (*self.color, alpha)
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), glow_radius, 1)

            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), radius, 2)
            symbol_text = small_font.render(self.symbol, True, WHITE)
            text_rect = symbol_text.get_rect(center=(self.x, self.y))
            surface.blit(symbol_text, text_rect)

    def check_collision(self, ball):
        if not self.active:
            return False
        dx = self.x - ball.x
        dy = self.y - ball.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < self.radius + ball.radius:
            self.active = False
            self.collected = True
            self.collect_animation = 10
            return True
        return False


# ------------------------- Ball Class -------------------------
class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 8
        self.color = WHITE
        self.active = True
        self.fire_mode = False
        self.fire_timer = 0
        self.pierce_mode = False
        self.pierce_count = 0
        self.last_positions = deque(maxlen=20)
        self.bricks_hit = []
        self.stopped = False
        self.landing_pos = (x, y)
        self.trail_alpha = 1.0
        self.glow_pulse = 0

    def move(self):
        if self.stopped:
            return

        self.last_positions.append((self.x, self.y))

        self.x += self.vx
        self.y += self.vy

        self.glow_pulse = (self.glow_pulse + 0.1) % (math.pi * 2)

        if self.fire_mode:
            self.fire_timer -= 1
            if self.fire_timer <= 0:
                self.fire_mode = False

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx * 0.95
        elif self.x + self.radius >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.vx = -self.vx * 0.95

        if self.y - self.radius <= HEADER_HEIGHT:
            self.y = HEADER_HEIGHT + self.radius
            self.vy = -self.vy * 0.95

        if self.y + self.radius >= SCREEN_HEIGHT - 20:
            self.stopped = True
            self.vx = 0
            self.vy = 0
            self.y = SCREEN_HEIGHT - 20 - self.radius
            self.landing_pos = (int(self.x), SCREEN_HEIGHT - 30)

    def draw(self, surface):
        if self.active:
            for i, pos in enumerate(self.last_positions):
                alpha = (i / len(self.last_positions)) * 0.5
                trail_radius = int(self.radius * alpha * 0.8)
                if trail_radius > 0:
                    if self.fire_mode:
                        trail_color = (255, int(100 * alpha), 0)
                    elif self.pierce_mode:
                        trail_color = (int(200 * alpha), 0, int(255 * alpha))
                    else:
                        trail_color = (int(180 * alpha), int(180 * alpha), int(255 * alpha))
                    pygame.draw.circle(surface, trail_color, (int(pos[0]), int(pos[1])), trail_radius)

            glow = math.sin(self.glow_pulse) * 2 + 3

            if self.fire_mode:
                ball_color = ORANGE
                for i in range(3):
                    aura_radius = self.radius + glow + i * 2
                    pygame.draw.circle(surface, (255, 100, 0, 50),
                                       (int(self.x), int(self.y)), int(aura_radius), 1)
            elif self.pierce_mode:
                ball_color = PURPLE
            else:
                ball_color = self.color

            pygame.draw.circle(surface, ball_color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)

            highlight_radius = self.radius - 3
            highlight_x = int(self.x - 2)
            highlight_y = int(self.y - 2)
            pygame.draw.circle(surface, (255, 255, 255, 100), (highlight_x, highlight_y), highlight_radius)

    def check_collision_with_brick(self, brick):
        if not brick.active:
            return False

        closest_x = max(brick.rect.left, min(self.x, brick.rect.right))
        closest_y = max(brick.rect.top, min(self.y, brick.rect.bottom))

        dx = self.x - closest_x
        dy = self.y - closest_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < self.radius:
            if distance == 0:
                distance = 0.01

            nx = dx / distance
            ny = dy / distance

            overlap = self.radius - distance
            self.x += nx * overlap
            self.y += ny * overlap

            dot = self.vx * nx + self.vy * ny
            if dot < 0:
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny

            return True
        return False


# ------------------------- Brick Class -------------------------
class Brick:
    def __init__(self, x, y, width, height, value):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.initial_value = value
        self.active = True
        self.hit_animation = 0
        self.contains_item = random.random() < 0.15
        self.item_type = random.choice(['extra_ball', 'fire_ball', 'pierce']) if self.contains_item else None

        self.update_color()

    def update_color(self):
        if self.value <= 2:
            self.color = (60, 255, 100)
        elif self.value <= 4:
            self.color = (255, 255, 50)
        elif self.value <= 7:
            self.color = (255, 140, 0)
        elif self.value <= 12:
            self.color = (255, 60, 60)
        else:
            self.color = (160, 60, 255)

    def draw(self, surface):
        if self.active:
            if self.hit_animation > 0:
                self.hit_animation -= 1
                scale = 1 + (self.hit_animation / 10) * 0.1
                rect = self.rect.inflate(-4, -4)
            else:
                rect = self.rect

            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)

            highlight_rect = rect.inflate(-4, -4)
            if highlight_rect.width > 0 and highlight_rect.height > 0:
                lighter_color = tuple(min(255, c + 50) for c in self.color)
                pygame.draw.rect(surface, lighter_color, highlight_rect, 1)

            if self.contains_item:
                item_color = Item.TYPES[self.item_type]['color']
                for i in range(2):
                    pygame.draw.circle(surface, item_color, rect.center, 8 + i * 2, 1)
                pygame.draw.circle(surface, item_color, rect.center, 7)
                pygame.draw.circle(surface, WHITE, rect.center, 7, 1)

            value_text = number_font.render(str(self.value), True, WHITE)
            text_rect = value_text.get_rect(center=rect.center)

            shadow_text = number_font.render(str(self.value), True, BLACK)
            shadow_rect = shadow_text.get_rect(center=(rect.centerx + 2, rect.centery + 2))
            surface.blit(shadow_text, shadow_rect)
            surface.blit(value_text, text_rect)

    def hit(self, damage=1):
        self.value -= damage
        self.hit_animation = 10
        if self.value <= 0:
            self.active = False
            return True
        self.update_color()
        return False


# ------------------------- Brick Grid Management -------------------------
class BrickGrid:
    def __init__(self):
        self.bricks = []
        self.current_level = 0
        self.brick_values_history = []
        self.create_initial_grid()

    def calculate_brick_width(self):
        return (SCREEN_WIDTH - (MAX_COLS + 1) * MARGIN) // MAX_COLS

    def create_initial_grid(self):
        self.bricks.clear()
        start_y = HEADER_HEIGHT + 20
        brick_width = self.calculate_brick_width()

        self.brick_values_history.append([1])

        for col in range(MAX_COLS):
            if random.random() < 0.5:
                x = MARGIN + col * (brick_width + MARGIN)
                y = start_y
                self.bricks.append(Brick(x, y, brick_width, BRICK_HEIGHT, 1))

    def move_down_and_add_row(self):
        global screen_shake
        screen_shake = 5

        for brick in self.bricks:
            brick.rect.y += BRICK_HEIGHT + MARGIN

        for brick in self.bricks:
            if brick.rect.bottom >= DEAD_ZONE_Y:
                return False

        self.current_level += 1

        brick_width = self.calculate_brick_width()
        start_y = HEADER_HEIGHT + 20

        base_value = 1 + self.current_level

        row_values = []

        for col in range(MAX_COLS):
            chance = 0.4 + (self.current_level * 0.03)
            if random.random() < min(chance, 0.75):
                x = MARGIN + col * (brick_width + MARGIN)
                y = start_y

                variation = random.randint(-1, 2)
                value = max(1, base_value + variation)

                if random.random() < 0.1:
                    value += random.randint(2, 4)

                row_values.append(value)
                self.bricks.append(Brick(x, y, brick_width, BRICK_HEIGHT, value))

        self.brick_values_history.append(row_values)
        return True

    def get_active_bricks(self):
        return [b for b in self.bricks if b.active]


# ------------------------- Visual Effects -------------------------
def draw_gradient_background(surface):
    for i in range(HEADER_HEIGHT, SCREEN_HEIGHT):
        ratio = (i - HEADER_HEIGHT) / GAME_AREA_HEIGHT
        r = int(18 + ratio * 10)
        g = int(18 + ratio * 10)
        b = int(24 + ratio * 20)
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, i), (SCREEN_WIDTH, i))


def draw_dead_zone(surface, alpha=255):
    pulse = math.sin(pygame.time.get_ticks() * 0.003) * 2
    line_y = DEAD_ZONE_Y + pulse

    for i in range(-2, 3):
        alpha_val = alpha - abs(i) * 50
        if alpha_val > 0:
            color = (255, 60, 60)
            pygame.draw.line(surface, color, (0, line_y + i), (SCREEN_WIDTH, line_y + i), 2)

    dead_text = small_font.render("DEAD ZONE", True, RED)
    text_rect = dead_text.get_rect(center=(SCREEN_WIDTH // 2, DEAD_ZONE_Y - 15))

    shadow_text = small_font.render("DEAD ZONE", True, (100, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 1, DEAD_ZONE_Y - 14))
    surface.blit(shadow_text, shadow_rect)
    surface.blit(dead_text, text_rect)


def draw_header(surface, score, available_balls, turn, best_score, phase):
    for i in range(HEADER_HEIGHT):
        ratio = i / HEADER_HEIGHT
        r = int(22 + ratio * 15)
        g = int(22 + ratio * 15)
        b = int(32 + ratio * 20)
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, i), (SCREEN_WIDTH, i))

    title_text = title_font.render("SWIPE BREAKER", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 25))

    glow_text = title_font.render("SWIPE BREAKER", True, CYAN)
    glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2 - 1, 24))
    surface.blit(glow_text, glow_rect)
    surface.blit(title_text, title_rect)

    phase_colors = {1: CYAN, 2: GREEN}
    phase_names = {1: "  PHASE 1  ", 2: "  PHASE 2  "}
    phase_text = small_font.render(phase_names.get(phase, f"PHASE {phase}"), True, phase_colors.get(phase, WHITE))
    phase_rect = phase_text.get_rect(center=(SCREEN_WIDTH // 2, 55))
    surface.blit(phase_text, phase_rect)

    boxes = [
        (15, 65, 110, 45, GOLD, "SCORE", str(score), WHITE),
        (140, 65, 110, 45, CYAN, "BALLS", str(available_balls), CYAN if available_balls > 0 else RED),
        (265, 65, 110, 45, PURPLE, "TURN", str(turn), WHITE),
        (390, 65, 110, 45, ORANGE, "BEST", str(best_score), ORANGE)
    ]

    for x, y, w, h, border_color, label, value, value_color in boxes:
        bg_rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, DARK_GRAY, bg_rect, border_radius=10)
        pygame.draw.rect(surface, border_color, bg_rect, 2, border_radius=10)

        label_surface = small_font.render(label, True, GRAY)
        surface.blit(label_surface, (x + 10, y + 5))

        value_surface = font.render(value, True, value_color)
        surface.blit(value_surface, (x + 10, y + 22))

    pygame.draw.line(surface, DARK_GRAY, (0, HEADER_HEIGHT), (SCREEN_WIDTH, HEADER_HEIGHT), 2)


def draw_menu(surface, buttons):
    # Beautiful gradient background
    for i in range(SCREEN_HEIGHT):
        ratio = i / SCREEN_HEIGHT
        r = int(15 + ratio * 20)
        g = int(15 + ratio * 15)
        b = int(25 + ratio * 30)
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, i), (SCREEN_WIDTH, i))

    # Animated stars
    for i in range(50):
        x = (i * 37 + pygame.time.get_ticks() * 0.01) % SCREEN_WIDTH
        y = (i * 23) % SCREEN_HEIGHT
        brightness = int(150 + 105 * math.sin(pygame.time.get_ticks() * 0.001 + i))
        pygame.draw.circle(surface, (brightness, brightness, brightness), (int(x), int(y)), 1)

    # Title with animation
    title_y = 150 + math.sin(pygame.time.get_ticks() * 0.002) * 10
    title_text = huge_font.render("SWIPE", True, CYAN)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, title_y))
    surface.blit(title_text, title_rect)

    subtitle_text = large_font.render("BRICK BREAKER", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, title_y + 70))
    surface.blit(subtitle_text, subtitle_rect)

    # Draw buttons
    for button in buttons:
        button.draw(surface)

    # Footer
    footer_text = small_font.render("© 2024 - Armin Naeini", True, GRAY)
    footer_rect = footer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
    surface.blit(footer_text, footer_rect)


def draw_stats_screen(surface, stats, back_button):
    # Dark overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))

    # Stats panel
    panel_rect = pygame.Rect(50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200)
    pygame.draw.rect(surface, DARK_GRAY, panel_rect, border_radius=20)
    pygame.draw.rect(surface, CYAN, panel_rect, 3, border_radius=20)

    # Title
    title = large_font.render("STATISTICS", True, CYAN)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 140))
    surface.blit(title, title_rect)

    # Stats
    stats_list = [
        f"Bricks Broken: {stats['bricks_broken']}",
        f"Total Shots: {stats['total_shots']}",
        f"Accuracy: {stats['accuracy']:.1f}%",
        f"Power-ups Collected: {stats['powerups_collected']}",
        f"Max Combo: {stats['max_combo']}x",
        f"Play Time: {stats['play_time']}s"
    ]

    y_pos = 250
    for stat in stats_list:
        text = font.render(stat, True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        surface.blit(text, rect)
        y_pos += 50

    # Back button
    back_button.draw(surface)


def draw_countdown(surface, countdown_value):
    if countdown_value > 0:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        countdown_text = huge_font.render(str(countdown_value), True, CYAN)
        text_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Pulsing effect
        scale = 1 + math.sin(pygame.time.get_ticks() * 0.005) * 0.1
        scaled_text = pygame.transform.scale(countdown_text,
                                             (int(text_rect.width * scale),
                                              int(text_rect.height * scale)))
        scaled_rect = scaled_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(scaled_text, scaled_rect)

        if countdown_value == 3:
            ready_text = font.render("Get Ready!", True, WHITE)
            ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            surface.blit(ready_text, ready_rect)


def draw_aim_line(surface, start_pos, end_pos):
    if start_pos and end_pos:
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = math.sqrt(dx ** 2 + dy ** 2)

        if length > 10:
            vx = dx * 0.14
            vy = dy * 0.14

            steps = int(length // 10)
            for i in range(steps):
                t = i / steps
                alpha = 1 - t * 0.5
                x1 = start_pos[0] + dx * t
                y1 = start_pos[1] + dy * t
                x2 = start_pos[0] + dx * (t + 1 / steps)
                y2 = start_pos[1] + dy * (t + 1 / steps)
                color = (255, int(255 * alpha), int(255 * alpha))
                pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2)


# ------------------------- Main Game -------------------------
def main():
    global screen_shake, countdown_value, countdown_timer, game_stats

    # Game state
    game_state = GameState.MENU
    best_score = SaveSystem.load_best_score()

    # Menu buttons
    menu_buttons = [
        Button(SCREEN_WIDTH // 2 - 100, 400, 200, 50, "START GAME", GREEN, SOFT_GREEN),
        Button(SCREEN_WIDTH // 2 - 100, 470, 200, 50, "QUIT", RED, (255, 100, 100))
    ]

    back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 120, 200, 50, "BACK", BLUE, LIGHT_BLUE)

    # Game variables
    grid = None
    balls = []
    items = []
    particles = []
    floating_texts = []

    available_balls = 3
    score = 0
    turn_count = 0
    phase = 1

    can_shoot = True
    waiting_for_return = False
    first_throw_done = False
    last_landing_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    swipe_start = None
    swipe_end = None
    is_dragging = False

    game_over = False
    game_start_time = 0

    # UI
    reset_button = Button(SCREEN_WIDTH - 120, HEADER_HEIGHT + 10, 100, 35, "MENU", DARK_GRAY, GRAY)

    # Background stars
    stars = [(random.randint(0, SCREEN_WIDTH), random.randint(HEADER_HEIGHT, SCREEN_HEIGHT),
              random.uniform(0.5, 2.0)) for _ in range(50)]

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Apply screen shake
        shake_offset_x = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
        shake_offset_y = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
        screen_shake = max(0, screen_shake - 1)

        # Update countdown
        if countdown_timer > 0:
            countdown_timer -= 1
            if countdown_timer == 0:
                countdown_value -= 1
                if countdown_value > 0:
                    countdown_timer = 60

        # ------------------------- Event Handling -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if game_state == GameState.MENU:
                for button in menu_buttons:
                    button.update(mouse_pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_buttons[0].is_clicked(mouse_pos):
                        # Start game
                        game_state = GameState.PLAYING
                        grid = BrickGrid()
                        balls.clear()
                        items.clear()
                        particles.clear()
                        floating_texts.clear()
                        available_balls = 3
                        score = 0
                        turn_count = 0
                        phase = 1
                        can_shoot = True
                        waiting_for_return = False
                        first_throw_done = False
                        game_over = False
                        last_landing_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

                        # Reset stats
                        game_stats = {
                            'bricks_broken': 0,
                            'total_shots': 0,
                            'accuracy': 0.0,
                            'powerups_collected': 0,
                            'max_combo': 0,
                            'play_time': 0
                        }

                        # Start countdown
                        countdown_value = 3
                        countdown_timer = 60
                        game_start_time = pygame.time.get_ticks()

                    elif menu_buttons[1].is_clicked(mouse_pos):
                        running = False
                        pygame.quit()
                        sys.exit()

            elif game_state == GameState.PLAYING:
                if countdown_value > 0:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    if reset_button.is_clicked(mouse_pos):
                        game_state = GameState.MENU
                        if not game_over:
                            SaveSystem.update_stats(games_played=1)
                        continue

                    if can_shoot and not game_over and available_balls > 0:
                        if my > SCREEN_HEIGHT - 150:
                            swipe_start = (mx, my)
                            swipe_end = (mx, my)
                            is_dragging = True

                if event.type == pygame.MOUSEMOTION:
                    if is_dragging:
                        swipe_end = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    if is_dragging and swipe_start and swipe_end and can_shoot:
                        dx = swipe_end[0] - swipe_start[0]
                        dy = swipe_end[1] - swipe_start[1]

                        vx = dx * 0.14
                        vy = dy * 0.14

                        if math.sqrt(vx ** 2 + vy ** 2) < 3.5:
                            vx = random.uniform(-0.8, 0.8)
                            vy = -6

                        shoot_x, shoot_y = last_landing_pos
                        new_ball = Ball(shoot_x, shoot_y - 10, vx, vy)
                        balls.append(new_ball)

                        available_balls -= 1
                        can_shoot = False
                        waiting_for_return = True
                        game_stats['total_shots'] += 1

                        shoot_sound.play()

                    is_dragging = False
                    swipe_start = None
                    swipe_end = None

            elif game_state == GameState.STATS:
                back_button.update(mouse_pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(mouse_pos):
                        game_state = GameState.MENU

        # ------------------------- Game Logic -------------------------
        if game_state == GameState.PLAYING and countdown_value == 0 and not game_over:
            # Update play time
            if game_start_time > 0:
                game_stats['play_time'] = (pygame.time.get_ticks() - game_start_time) // 1000

            # Update items
            for item in items:
                item.update()

            # Update floating texts
            for text in floating_texts[:]:
                text.update()
                if text.life <= 0:
                    floating_texts.remove(text)

            # Update reset button
            reset_button.update(mouse_pos)

            # Update balls
            for ball in balls[:]:
                if ball.active and not ball.stopped:
                    ball.move()

                if ball.active:
                    for brick in grid.bricks:
                        if brick.active:
                            if ball.check_collision_with_brick(brick):
                                damage = 2 if ball.fire_mode else 1
                                destroyed = brick.hit(damage)

                                if ball.pierce_mode:
                                    if brick not in ball.bricks_hit:
                                        ball.bricks_hit.append(brick)
                                        ball.pierce_count += 1
                                        if ball.pierce_count >= 3:
                                            ball.pierce_mode = False
                                    continue

                                for _ in range(8):
                                    particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color))

                                if destroyed:
                                    score += brick.initial_value * 10
                                    game_stats['bricks_broken'] += 1

                                    floating_texts.append(FloatingText(
                                        brick.rect.centerx, brick.rect.centery - 20,
                                        f"+{brick.initial_value * 10}", GOLD, 28
                                    ))

                                    if brick.contains_item and brick.item_type:
                                        items.append(Item(brick.rect.centerx, brick.rect.centery, brick.item_type))

                                    for _ in range(15):
                                        particles.append(Particle(brick.rect.centerx, brick.rect.centery, GOLD, 1.5))

                                    screen_shake = 3
                                    break_sound.play()

                    # Check item collisions
                    for item in items[:]:
                        if item.check_collision(ball):
                            if item.type == 'extra_ball':
                                available_balls += 1
                                game_stats['powerups_collected'] += 1
                                floating_texts.append(FloatingText(
                                    item.x, item.y - 30, "+1 BALL", CYAN, 28
                                ))
                            elif item.type == 'fire_ball':
                                ball.fire_mode = True
                                ball.fire_timer = 300
                                game_stats['powerups_collected'] += 1
                                floating_texts.append(FloatingText(
                                    item.x, item.y - 30, "FIRE!", ORANGE, 28
                                ))
                            elif item.type == 'pierce':
                                ball.pierce_mode = True
                                ball.pierce_count = 0
                                ball.bricks_hit.clear()
                                game_stats['powerups_collected'] += 1
                                floating_texts.append(FloatingText(
                                    item.x, item.y - 30, "PIERCE!", PURPLE, 28
                                ))

                            for _ in range(10):
                                particles.append(Particle(item.x, item.y, item.color))

                            powerup_sound.play()

                        if not item.active:
                            items.remove(item)

                # Ball stopped
                if ball.stopped and ball.active:
                    last_landing_pos = ball.landing_pos
                    waiting_for_return = False

                    if not first_throw_done:
                        first_throw_done = True
                        phase = 2
                        floating_texts.append(FloatingText(
                            SCREEN_WIDTH // 2, HEADER_HEIGHT + 100,
                            "PHASE 2 START!", GREEN, 36
                        ))

                    if first_throw_done:
                        if not grid.move_down_and_add_row():
                            game_over = True
                            game_state = GameState.STATS
                            game_over_sound.play()

                            # Calculate accuracy
                            if game_stats['total_shots'] > 0:
                                game_stats['accuracy'] = (game_stats['bricks_broken'] / game_stats['total_shots']) * 100

                            # Save best score
                            best_score = SaveSystem.save_best_score(score)
                            SaveSystem.update_stats(games_played=1, total_bricks=game_stats['bricks_broken'])

                            screen_shake = 10
                        else:
                            turn_count += 1
                            available_balls += 1
                            floating_texts.append(FloatingText(
                                SCREEN_WIDTH // 2, HEADER_HEIGHT + 150,
                                f"Turn {turn_count} - +1 Ball!", CYAN, 28
                            ))

                    can_shoot = True
                    ball.active = False

                if not ball.active:
                    balls.remove(ball)

            # Update particles
            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)

        # ------------------------- Rendering -------------------------
        if game_state == GameState.MENU:
            draw_menu(screen, menu_buttons)

        elif game_state == GameState.PLAYING:
            screen.fill(DARK_BG)
            draw_gradient_background(screen)

            # Draw stars
            for star_x, star_y, brightness in stars:
                twinkle = math.sin(pygame.time.get_ticks() * 0.001 + star_x) * 0.5 + 0.5
                color_val = int(100 + 155 * brightness * twinkle)
                color_val = max(0, min(255, color_val))
                draw_x = int(star_x + shake_offset_x * 0.5)
                draw_y = int(star_y + shake_offset_y * 0.5)
                if 0 <= draw_x < SCREEN_WIDTH and 0 <= draw_y < SCREEN_HEIGHT:
                    pygame.draw.circle(screen, (color_val, color_val, color_val), (draw_x, draw_y), 1)

            game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

            for brick in grid.bricks:
                brick.draw(game_surface)

            for item in items:
                item.draw(game_surface)

            for particle in particles:
                particle.draw(game_surface)

            for ball in balls:
                ball.draw(game_surface)

            draw_dead_zone(game_surface)

            if can_shoot and not game_over and countdown_value == 0:
                pulse = math.sin(pygame.time.get_ticks() * 0.005) * 3 + 8
                pygame.draw.circle(game_surface, GREEN, last_landing_pos, int(pulse), 2)
                pygame.draw.circle(game_surface, (100, 255, 100, 30), last_landing_pos, int(pulse + 5), 1)

                pos_label = small_font.render("Shoot from here", True, GREEN)
                label_rect = pos_label.get_rect(center=(last_landing_pos[0], last_landing_pos[1] - 35))
                game_surface.blit(pos_label, label_rect)

            screen.blit(game_surface, (shake_offset_x, shake_offset_y))

            for text in floating_texts:
                text.draw(screen)

            if is_dragging and swipe_start and swipe_end and countdown_value == 0:
                draw_aim_line(screen, last_landing_pos, swipe_end)
                pygame.draw.circle(screen, WHITE, last_landing_pos, 5)

            draw_header(screen, score, available_balls, turn_count, best_score, phase)

            reset_button.draw(screen)

            if waiting_for_return and countdown_value == 0:
                status_text = font.render("Ball in play...", True, YELLOW)
                status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.003)) * 50 + 200
                status_text_pulse = font.render("⚽ Ball in play... ⚽", True, (255, int(pulse), 0))
                screen.blit(status_text_pulse, status_rect)
            elif can_shoot and available_balls > 0 and not game_over and countdown_value == 0:
                if not first_throw_done:
                    status_text = font.render("First throw - Swipe up!", True, CYAN)
                else:
                    status_text = font.render(f" Turn {turn_count + 1} - Swipe up!", True, GREEN)
                status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
                screen.blit(status_text, status_rect)

            if countdown_value > 0:
                draw_countdown(screen, countdown_value)

        elif game_state == GameState.STATS:
            # Show game over screen with stats
            screen.fill(DARK_BG)
            draw_gradient_background(screen)

            # Draw game elements in background (dimmed)
            if grid:
                for brick in grid.bricks:
                    brick.draw(screen)

                for ball in balls:
                    ball.draw(screen)

            draw_stats_screen(screen, game_stats, back_button)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()