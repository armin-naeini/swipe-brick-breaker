import pygame
import sys
import math
import random
from collections import deque

# ------------------------- Initial Setup -------------------------
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 850
HEADER_HEIGHT = 120
GAME_AREA_HEIGHT = SCREEN_HEIGHT - HEADER_HEIGHT
DEAD_ZONE_Y = SCREEN_HEIGHT - 150

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
pygame.display.set_caption("✨ Brick Breaker - BBTAN Style ✨")
clock = pygame.time.Clock()

# Fonts with better styling
try:
    title_font = pygame.font.Font(None, 48)
    header_font = pygame.font.Font(None, 42)
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    large_font = pygame.font.Font(None, 72)
    number_font = pygame.font.Font(None, 32)
except:
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    header_font = pygame.font.SysFont('Arial', 42, bold=True)
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)
    large_font = pygame.font.SysFont('Arial', 72, bold=True)
    number_font = pygame.font.SysFont('Arial', 32, bold=True)

# Game constants
MAX_COLS = 7
MARGIN = 5
BRICK_HEIGHT = 32

# Animation variables
screen_shake = 0
transition_alpha = 0
brick_move_animation = 0


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
                # Add glow effect
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

        # Update glow pulse
        self.glow_pulse = (self.glow_pulse + 0.1) % (math.pi * 2)

        # Fire mode timer
        if self.fire_mode:
            self.fire_timer -= 1
            if self.fire_timer <= 0:
                self.fire_mode = False

        # Wall collisions with smooth bounce
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx * 0.95
        elif self.x + self.radius >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.vx = -self.vx * 0.95

        if self.y - self.radius <= HEADER_HEIGHT:
            self.y = HEADER_HEIGHT + self.radius
            self.vy = -self.vy * 0.95

        # Bottom collision - Stop immediately
        if self.y + self.radius >= SCREEN_HEIGHT - 20:
            self.stopped = True
            self.vx = 0
            self.vy = 0
            self.y = SCREEN_HEIGHT - 20 - self.radius
            self.landing_pos = (int(self.x), SCREEN_HEIGHT - 30)

    def draw(self, surface):
        if self.active:
            # Draw trail with gradient
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

            # Draw ball with effects
            glow = math.sin(self.glow_pulse) * 2 + 3

            if self.fire_mode:
                ball_color = ORANGE
                # Fire aura
                for i in range(3):
                    aura_radius = self.radius + glow + i * 2
                    pygame.draw.circle(surface, (255, 100, 0, 50),
                                       (int(self.x), int(self.y)), int(aura_radius), 1)
            elif self.pierce_mode:
                ball_color = PURPLE
            else:
                ball_color = self.color

            # Main ball
            pygame.draw.circle(surface, ball_color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)

            # Inner highlight
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

            # Bounce physics
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

        # Color gradient based on value
        self.update_color()

    def update_color(self):
        if self.value <= 2:
            self.color = (60, 255, 100)  # Green
        elif self.value <= 4:
            self.color = (255, 255, 50)  # Yellow
        elif self.value <= 7:
            self.color = (255, 140, 0)  # Orange
        elif self.value <= 12:
            self.color = (255, 60, 60)  # Red
        else:
            self.color = (160, 60, 255)  # Purple

    def draw(self, surface):
        if self.active:
            # Hit animation
            if self.hit_animation > 0:
                self.hit_animation -= 1
                scale = 1 + (self.hit_animation / 10) * 0.1
                rect = self.rect.inflate(-4, -4)
            else:
                rect = self.rect

            # Draw brick with gradient effect
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)

            # Inner highlight
            highlight_rect = rect.inflate(-4, -4)
            if highlight_rect.width > 0 and highlight_rect.height > 0:
                lighter_color = tuple(min(255, c + 50) for c in self.color[:3])
                pygame.draw.rect(surface, lighter_color, highlight_rect, 1)

            # Draw item indicator with glow
            if self.contains_item:
                item_color = Item.TYPES[self.item_type]['color']
                # Glow effect
                for i in range(2):
                    pygame.draw.circle(surface, item_color, rect.center, 8 + i * 2, 1)
                pygame.draw.circle(surface, item_color, rect.center, 7)
                pygame.draw.circle(surface, WHITE, rect.center, 7, 1)

            # Draw value with shadow
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
        self.brick_values_history = []  # Track values for progression
        self.create_initial_grid()

    def calculate_brick_width(self):
        return (SCREEN_WIDTH - (MAX_COLS + 1) * MARGIN) // MAX_COLS

    def create_initial_grid(self):
        """Create only ONE row with random empty spots"""
        self.bricks.clear()
        start_y = HEADER_HEIGHT + 20
        brick_width = self.calculate_brick_width()

        # Initial row values (all 1)
        self.brick_values_history.append([1])

        for col in range(MAX_COLS):
            if random.random() < 0.5:  # 50% chance for initial row
                x = MARGIN + col * (brick_width + MARGIN)
                y = start_y
                self.bricks.append(Brick(x, y, brick_width, BRICK_HEIGHT, 1))

    def move_down_and_add_row(self):
        """Move all bricks down and add a new stronger row"""
        global screen_shake
        screen_shake = 5  # Small screen shake

        # Move existing bricks down
        for brick in self.bricks:
            brick.rect.y += BRICK_HEIGHT + MARGIN

        # Check if any brick crossed dead zone
        for brick in self.bricks:
            if brick.rect.bottom >= DEAD_ZONE_Y:
                return False

        # Increment level
        self.current_level += 1

        brick_width = self.calculate_brick_width()
        start_y = HEADER_HEIGHT + 20

        # Calculate base value for new row (progressively stronger)
        base_value = 1 + self.current_level

        # Track values for this row
        row_values = []

        # Add new row with random gaps
        for col in range(MAX_COLS):
            chance = 0.4 + (self.current_level * 0.03)
            if random.random() < min(chance, 0.75):
                x = MARGIN + col * (brick_width + MARGIN)
                y = start_y

                # Value progression - each row gets stronger
                variation = random.randint(-1, 2)
                value = max(1, base_value + variation)

                # Occasional stronger brick
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
    """Draw a beautiful gradient background"""
    for i in range(HEADER_HEIGHT, SCREEN_HEIGHT):
        ratio = (i - HEADER_HEIGHT) / GAME_AREA_HEIGHT
        r = int(18 + ratio * 10)
        g = int(18 + ratio * 10)
        b = int(24 + ratio * 20)
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, i), (SCREEN_WIDTH, i))


def draw_dead_zone(surface, alpha=255):
    """Draw animated dead zone"""
    # Pulsing line
    pulse = math.sin(pygame.time.get_ticks() * 0.003) * 2
    line_y = DEAD_ZONE_Y + pulse

    # Gradient line
    for i in range(-2, 3):
        alpha_val = alpha - abs(i) * 50
        if alpha_val > 0:
            color = (255, 60, 60, alpha_val)
            pygame.draw.line(surface, RED, (0, line_y + i), (SCREEN_WIDTH, line_y + i), 2)

    # Warning text with glow
    dead_text = small_font.render("⚠ DEAD ZONE ⚠", True, RED)
    text_rect = dead_text.get_rect(center=(SCREEN_WIDTH // 2, DEAD_ZONE_Y - 15))

    # Text shadow
    shadow_text = small_font.render("⚠ DEAD ZONE ⚠", True, (100, 0, 0))
    shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 1, DEAD_ZONE_Y - 14))
    surface.blit(shadow_text, shadow_rect)
    surface.blit(dead_text, text_rect)


def draw_header(surface, score, available_balls, turn, best_score, phase):
    # Beautiful header gradient
    for i in range(HEADER_HEIGHT):
        ratio = i / HEADER_HEIGHT
        r = int(22 + ratio * 15)
        g = int(22 + ratio * 15)
        b = int(32 + ratio * 20)
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, i), (SCREEN_WIDTH, i))

    # Title with glow effect
    title_text = title_font.render("✨ BRICK BREAKER ✨", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 25))

    # Glow
    glow_text = title_font.render("✨ BRICK BREAKER ✨", True, CYAN)
    glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2 - 1, 24))
    surface.blit(glow_text, glow_rect)
    surface.blit(title_text, title_rect)

    # Phase indicator with animation
    phase_colors = {1: CYAN, 2: GREEN}
    phase_names = {1: "🌟 PHASE 1 - First Throw 🌟", 2: "⚡ PHASE 2 - Bricks Moving ⚡"}
    phase_text = small_font.render(phase_names.get(phase, f"PHASE {phase}"), True, phase_colors.get(phase, WHITE))
    phase_rect = phase_text.get_rect(center=(SCREEN_WIDTH // 2, 55))
    surface.blit(phase_text, phase_rect)

    # Stats boxes with rounded corners and gradients
    boxes = [
        (15, 65, 120, 45, GOLD, "SCORE", str(score), WHITE),
        (150, 65, 120, 45, CYAN, "BALLS", str(available_balls), CYAN if available_balls > 0 else RED),
        (285, 65, 120, 45, PURPLE, "TURN", str(turn), WHITE),
        (420, 65, 165, 45, ORANGE, "BEST", str(best_score), ORANGE)
    ]

    for x, y, w, h, border_color, label, value, value_color in boxes:
        # Background
        bg_rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, DARK_GRAY, bg_rect, border_radius=10)
        pygame.draw.rect(surface, border_color, bg_rect, 2, border_radius=10)

        # Label
        label_surface = small_font.render(label, True, GRAY)
        surface.blit(label_surface, (x + 10, y + 5))

        # Value
        value_surface = font.render(value, True, value_color)
        surface.blit(value_surface, (x + 10, y + 22))

    # Separator line with gradient
    for i in range(2):
        alpha = 100 - i * 50
        color = (50, 50, 60, alpha)
        pygame.draw.line(surface, DARK_GRAY, (0, HEADER_HEIGHT + i), (SCREEN_WIDTH, HEADER_HEIGHT + i), 1)


# ------------------------- Aim Prediction -------------------------
def predict_trajectory(start_x, start_y, vx, vy, steps=80):
    points = []
    x, y = start_x, start_y
    vel_x, vel_y = vx, vy

    for i in range(steps):
        x += vel_x
        y += vel_y

        if x <= 10 or x >= SCREEN_WIDTH - 10:
            vel_x = -vel_x
        if y <= HEADER_HEIGHT + 10:
            vel_y = -vel_y

        points.append((int(x), int(y)))

        if y >= SCREEN_HEIGHT - 30:
            break

    return points


def draw_aim_line(surface, start_pos, end_pos):
    if start_pos and end_pos:
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = math.sqrt(dx ** 2 + dy ** 2)

        if length > 10:
            vx = dx * 0.18
            vy = dy * 0.18

            # Main aim line with gradient
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

            # Predicted trajectory
            points = predict_trajectory(start_pos[0], start_pos[1], vx, vy)
            if len(points) > 1:
                for i in range(0, len(points) - 1):
                    alpha = 1 - (i / len(points)) * 0.7
                    color = (100, int(255 * alpha), 100)
                    pygame.draw.line(surface, color, points[i], points[i + 1], 1)


# ------------------------- Main Game -------------------------
def main():
    global screen_shake

    grid = BrickGrid()
    balls = []
    items = []
    particles = []
    floating_texts = []

    # Player resources
    available_balls = 3
    score = 0
    turn_count = 0
    best_score = 0
    phase = 1

    # Ball state
    can_shoot = True
    waiting_for_return = False
    first_throw_done = False
    last_landing_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

    # Swipe mechanics
    swipe_start = None
    swipe_end = None
    is_dragging = False

    # Game flow
    game_over = False

    # UI
    reset_button = pygame.Rect(SCREEN_WIDTH - 100, HEADER_HEIGHT + 10, 85, 35)

    # Background stars
    stars = [(random.randint(0, SCREEN_WIDTH), random.randint(HEADER_HEIGHT, SCREEN_HEIGHT),
              random.uniform(0.5, 2.0)) for _ in range(50)]

    running = True

    while running:
        # Apply screen shake
        shake_offset_x = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
        shake_offset_y = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
        screen_shake = max(0, screen_shake - 1)

        # ------------------------- Event Handling -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if reset_button.collidepoint(mx, my):
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

                    vx = dx * 0.18
                    vy = dy * 0.18

                    if math.sqrt(vx ** 2 + vy ** 2) < 4:
                        vx = random.uniform(-1, 1)
                        vy = -7

                    shoot_x, shoot_y = last_landing_pos
                    new_ball = Ball(shoot_x, shoot_y - 10, vx, vy)
                    balls.append(new_ball)

                    available_balls -= 1
                    can_shoot = False
                    waiting_for_return = True

                is_dragging = False
                swipe_start = None
                swipe_end = None

        # ------------------------- Game Logic -------------------------
        if not game_over:
            # Update items
            for item in items:
                item.update()

            # Update floating texts
            for text in floating_texts[:]:
                text.update()
                if text.life <= 0:
                    floating_texts.remove(text)

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

                                # Particles
                                for _ in range(8):
                                    particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color))

                                if destroyed:
                                    score += brick.initial_value * 10
                                    floating_texts.append(FloatingText(
                                        brick.rect.centerx, brick.rect.centery - 20,
                                        f"+{brick.initial_value * 10}", GOLD, 28
                                    ))

                                    if brick.contains_item and brick.item_type:
                                        items.append(Item(brick.rect.centerx, brick.rect.centery, brick.item_type))

                                    # More particles for destruction
                                    for _ in range(15):
                                        particles.append(Particle(brick.rect.centerx, brick.rect.centery, GOLD, 1.5))

                                    screen_shake = 3

                    # Check item collisions
                    for item in items[:]:
                        if item.check_collision(ball):
                            if item.type == 'extra_ball':
                                available_balls += 1
                                floating_texts.append(FloatingText(
                                    item.x, item.y - 30, "+1 BALL", CYAN, 28
                                ))
                            elif item.type == 'fire_ball':
                                ball.fire_mode = True
                                ball.fire_timer = 300
                                floating_texts.append(FloatingText(
                                    item.x, item.y - 30, "FIRE!", ORANGE, 28
                                ))
                            elif item.type == 'pierce':
                                ball.pierce_mode = True
                                ball.pierce_count = 0
                                ball.bricks_hit.clear()
                                floating_texts.append(FloatingText(
                                    item.x, item.y - 30, "PIERCE!", PURPLE, 28
                                ))

                            for _ in range(10):
                                particles.append(Particle(item.x, item.y, item.color))

                        if not item.active:
                            items.remove(item)

                # Ball stopped - immediately process next turn
                if ball.stopped and ball.active:
                    last_landing_pos = ball.landing_pos
                    waiting_for_return = False

                    # First throw completed
                    if not first_throw_done:
                        first_throw_done = True
                        phase = 2
                        floating_texts.append(FloatingText(
                            SCREEN_WIDTH // 2, HEADER_HEIGHT + 100,
                            "PHASE 2 START!", GREEN, 36
                        ))

                    # Move bricks down after EVERY throw (Phase 2+)
                    if first_throw_done:
                        if not grid.move_down_and_add_row():
                            game_over = True
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

            # Update best score
            if score > best_score:
                best_score = score

        # ------------------------- Rendering -------------------------
        screen.fill(DARK_BG)

        # Draw gradient background
        draw_gradient_background(screen)

        # Draw stars
        for star_x, star_y, brightness in stars:
            twinkle = math.sin(pygame.time.get_ticks() * 0.001 + star_x) * 0.5 + 0.5
            color_val = int(100 + 155 * brightness * twinkle)
            # Make sure color_val is between 0-255
            color_val = max(0, min(255, color_val))
            color = (color_val, color_val, color_val)
            # Check bounds before drawing
            draw_x = int(star_x + shake_offset_x * 0.5)
            draw_y = int(star_y + shake_offset_y * 0.5)
            if 0 <= draw_x < SCREEN_WIDTH and 0 <= draw_y < SCREEN_HEIGHT:
                try:
                    screen.set_at((draw_x, draw_y), color)
                except:
                    pass  # Skip if there's any error with this pixel

        # Draw game elements with shake
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Draw bricks
        for brick in grid.bricks:
            brick.draw(game_surface)

        # Draw items
        for item in items:
            item.draw(game_surface)

        # Draw particles
        for particle in particles:
            particle.draw(game_surface)

        # Draw balls
        for ball in balls:
            ball.draw(game_surface)

        # Draw dead zone
        draw_dead_zone(game_surface)

        # Draw landing position
        if can_shoot and not game_over:
            # Animated landing indicator
            pulse = math.sin(pygame.time.get_ticks() * 0.005) * 3 + 8
            pygame.draw.circle(game_surface, GREEN, last_landing_pos, int(pulse), 2)
            pygame.draw.circle(game_surface, (100, 255, 100, 30), last_landing_pos, int(pulse + 5), 1)

            pos_label = small_font.render("▼ Shoot from here ▼", True, GREEN)
            label_rect = pos_label.get_rect(center=(last_landing_pos[0], last_landing_pos[1] - 35))
            game_surface.blit(pos_label, label_rect)

        # Blit game surface with shake
        screen.blit(game_surface, (shake_offset_x, shake_offset_y))

        # Draw floating texts (not affected by shake)
        for text in floating_texts:
            text.draw(screen)

        # Draw aim line (on top)
        if is_dragging and swipe_start and swipe_end:
            draw_aim_line(screen, last_landing_pos, swipe_end)
            pygame.draw.circle(screen, WHITE, last_landing_pos, 5)

        # Draw header (not affected by shake)
        draw_header(screen, score, available_balls, turn_count, best_score, phase)

        # Reset button
        pygame.draw.rect(screen, DARK_GRAY, reset_button, border_radius=5)
        pygame.draw.rect(screen, WHITE, reset_button, 2, border_radius=5)
        reset_label = small_font.render("⟲ RESET", True, WHITE)
        screen.blit(reset_label, (reset_button.x + 15, reset_button.y + 10))

        # Status message
        if waiting_for_return:
            status_text = font.render("⚽ Ball in play... ⚽", True, YELLOW)
            status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))

            # Pulsing effect
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.003)) * 50 + 200
            status_text_pulse = font.render("⚽ Ball in play... ⚽", True, (255, int(pulse), 0))
            screen.blit(status_text_pulse, status_rect)
        elif can_shoot and available_balls > 0 and not game_over:
            if not first_throw_done:
                status_text = font.render("🎯 First throw - Swipe up! 🎯", True, CYAN)
            else:
                status_text = font.render(f"🎯 Turn {turn_count + 1} - Swipe up! 🎯", True, GREEN)
            status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
            screen.blit(status_text, status_rect)

        # Game Over overlay
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            over_text = large_font.render("💀 GAME OVER 💀", True, RED)
            text_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(over_text, text_rect)

            final_score = font.render(f"Final Score: {score}", True, WHITE)
            score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            screen.blit(final_score, score_rect)

            turns_text = small_font.render(f"Survived {turn_count} turns", True, GRAY)
            turns_rect = turns_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(turns_text, turns_rect)

            restart_text = small_font.render("Press RESET to play again", True, GRAY)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()