import pygame
import sys
import math
import random
from collections import deque

# ------------------------- Initial Setup -------------------------
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
GREEN = (50, 255, 100)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 255)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
CYAN = (0, 255, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Swipe Brick Breaker - Advanced")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 72)


# ------------------------- Power-up Class -------------------------
class PowerUp:
    TYPES = {
        'fire': {'color': ORANGE, 'symbol': 'FIRE', 'duration': 300},
        'multiball': {'color': CYAN, 'symbol': 'x3', 'duration': 0},
        'slow': {'color': GREEN, 'symbol': 'SLOW', 'duration': 180}
    }

    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.radius = 12
        self.vy = 2
        self.active = True
        self.color = self.TYPES[power_type]['color']
        self.symbol = self.TYPES[power_type]['symbol']

    def update(self):
        self.y += self.vy
        if self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)
            symbol_text = small_font.render(self.symbol, True, WHITE)
            text_rect = symbol_text.get_rect(center=(self.x, self.y))
            surface.blit(symbol_text, text_rect)


# ------------------------- Particle Class -------------------------
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.color = color
        self.life = 60
        self.max_life = 60
        self.size = random.randint(3, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = self.life / self.max_life
            size = int(self.size * alpha)
            if size > 0:
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)


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
        self.last_positions = deque(maxlen=10)
        self.last_chance_used = 0  # Counter for last chance mechanic

    def move(self):
        self.last_positions.append((self.x, self.y))

        self.x += self.vx
        self.y += self.vy

        if self.fire_mode:
            self.fire_timer -= 1
            if self.fire_timer <= 0:
                self.fire_mode = False
                self.color = WHITE

        # Wall collisions
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x + self.radius >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.vx = -self.vx

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = -self.vy

        # Bottom collision - Last Chance Mechanic
        if self.y - self.radius > SCREEN_HEIGHT:
            self.last_chance_used += 1
            if self.last_chance_used <= 3:  # Give 3 chances
                self.y = SCREEN_HEIGHT - self.radius
                self.vy = -self.vy * 0.7
                self.vx *= 0.8
                if abs(self.vy) < 3:
                    self.vy = -5
                if abs(self.vx) < 1:
                    self.vx = random.choice([-2, 2])
            else:
                self.active = False  # Remove ball after 3 chances

    def draw(self, surface):
        if self.active:
            # Draw trail
            for i, pos in enumerate(self.last_positions):
                alpha = i / len(self.last_positions)
                trail_radius = int(self.radius * alpha * 0.7)
                if trail_radius > 0:
                    trail_color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
                    pygame.draw.circle(surface, trail_color, (int(pos[0]), int(pos[1])), trail_radius)

            # Draw main ball
            ball_color = ORANGE if self.fire_mode else self.color
            pygame.draw.circle(surface, ball_color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 1)

            if self.fire_mode:
                pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), self.radius + 3, 2)

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

            if not self.fire_mode:
                dot = self.vx * nx + self.vy * ny
                if dot < 0:
                    self.vx -= 2 * dot * nx
                    self.vy -= 2 * dot * ny

            return True
        return False


# ------------------------- Brick Class -------------------------
class Brick:
    def __init__(self, x, y, width, height, color, is_powerup=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = 1
        self.active = True
        self.is_powerup = is_powerup
        self.powerup_type = random.choice(['fire', 'multiball', 'slow']) if is_powerup else None

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, 2)

            if self.is_powerup:
                star_text = small_font.render("*", True, WHITE)
                text_rect = star_text.get_rect(center=self.rect.center)
                surface.blit(star_text, text_rect)


# ------------------------- Brick Wall Creation -------------------------
def create_bricks(rows, cols, existing_bricks=None):
    """Create initial bricks or add a new row in endless mode"""
    bricks = []
    margin = 5
    brick_width = (SCREEN_WIDTH - (cols + 1) * margin) // cols
    brick_height = 20

    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

    # If we have existing bricks (Endless mode), move them down first
    if existing_bricks:
        game_over = False
        for brick in existing_bricks:
            brick.rect.y += brick_height + margin
            if brick.rect.bottom > SCREEN_HEIGHT - 200:
                game_over = True
            bricks.append(brick)

        if game_over:
            return None

    # Create new row at the top
    for col in range(cols):
        x = margin + col * (brick_width + margin)
        y = margin + 80
        is_powerup = random.random() < 0.2
        color = GOLD if is_powerup else colors[0]
        bricks.append(Brick(x, y, brick_width, brick_height, color, is_powerup))

    return bricks


# ------------------------- Drawing Functions -------------------------
def draw_aim_line(surface, start_pos, end_pos):
    if start_pos and end_pos:
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = math.sqrt(dx ** 2 + dy ** 2)

        if length > 10:
            pygame.draw.line(surface, WHITE, start_pos, end_pos, 2)
            steps = int(length // 15)
            if steps > 0:
                for i in range(steps):
                    t = i / steps
                    px = start_pos[0] + dx * t
                    py = start_pos[1] + dy * t
                    pygame.draw.circle(surface, (200, 200, 200), (int(px), int(py)), 3)


# ------------------------- Main Game Loop -------------------------
def main():
    # Game variables
    balls = []
    powerups = []
    particles = []
    score = 0
    game_active = True
    game_over = False
    victory = False

    # Combo system
    last_hit_time = 0
    combo_count = 0
    combo_timer = 0
    combo_display_timer = 0

    # Create initial bricks
    bricks = create_bricks(6, 8)

    # Swipe variables
    swipe_start = None
    swipe_end = None
    is_dragging = False
    drag_zone = pygame.Rect(0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150)

    # Buttons
    reset_button = pygame.Rect(SCREEN_WIDTH - 120, 10, 110, 40)

    running = True
    frame_count = 0

    while running:
        frame_count += 1

        # ------------------------- Event Handling -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if reset_button.collidepoint(mx, my):
                    balls.clear()
                    powerups.clear()
                    particles.clear()
                    bricks = create_bricks(6, 8)
                    score = 0
                    game_active = True
                    game_over = False
                    victory = False
                    combo_count = 0
                    continue

                if game_active and not game_over and not victory and drag_zone.collidepoint(mx, my):
                    swipe_start = (mx, my)
                    swipe_end = (mx, my)
                    is_dragging = True

            if event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    swipe_end = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if is_dragging and swipe_start and swipe_end and game_active and not game_over and not victory:
                    dx = swipe_end[0] - swipe_start[0]
                    dy = swipe_end[1] - swipe_start[1]

                    speed_scale = 0.25
                    vx = dx * speed_scale
                    vy = dy * speed_scale

                    if math.sqrt(vx ** 2 + vy ** 2) < 3:
                        vx = random.uniform(-2, 2)
                        vy = -7

                    new_ball = Ball(swipe_start[0], swipe_start[1] - 20, vx, vy)
                    balls.append(new_ball)

                is_dragging = False
                swipe_start = None
                swipe_end = None

        # ------------------------- Game Logic Update -------------------------
        if game_active and not game_over and not victory:
            # Move balls
            for ball in balls[:]:
                if ball.active:
                    ball.move()

                    for brick in bricks:
                        if brick.active:
                            if ball.check_collision_with_brick(brick):
                                brick.active = False

                                # Combo system
                                current_time = frame_count
                                if current_time - last_hit_time < 30:
                                    combo_count += 1
                                    combo_timer = 60
                                else:
                                    combo_count = 1
                                    combo_timer = 60
                                last_hit_time = current_time

                                combo_bonus = min(combo_count * 5, 50)
                                score += 10 + combo_bonus
                                combo_display_timer = 60

                                # Create particles
                                for _ in range(15):
                                    particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color))

                                # Create power-up
                                if brick.is_powerup and brick.powerup_type:
                                    powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery, brick.powerup_type))

                elif not ball.active:
                    balls.remove(ball)

            # Update power-ups
            for powerup in powerups[:]:
                powerup.update()

                # Auto-collect at bottom
                if powerup.y + powerup.radius >= SCREEN_HEIGHT - 50:
                    if powerup.type == 'multiball':
                        for angle in [-30, 30]:
                            rad = math.radians(angle)
                            vx = math.sin(rad) * 8
                            vy = -math.cos(rad) * 8
                            new_ball = Ball(powerup.x, powerup.y, vx, vy)
                            balls.append(new_ball)

                    elif powerup.type == 'fire':
                        for ball in balls:
                            ball.fire_mode = True
                            ball.fire_timer = PowerUp.TYPES['fire']['duration']
                            ball.color = ORANGE

                    elif powerup.type == 'slow':
                        for ball in balls:
                            ball.vx *= 0.5
                            ball.vy *= 0.5

                    powerup.active = False

                if not powerup.active:
                    powerups.remove(powerup)

            # Update particles
            for particle in particles[:]:
                particle.update()
                if particle.life <= 0:
                    particles.remove(particle)

            # Update combo timer
            if combo_timer > 0:
                combo_timer -= 1
                if combo_timer == 0:
                    combo_count = 0

            if combo_display_timer > 0:
                combo_display_timer -= 1

            # Check if all bricks are destroyed
            active_bricks = [b for b in bricks if b.active]
            if len(active_bricks) == 0:
                # Endless mode - add new row
                result = create_bricks(1, 8, bricks)
                if result is None:
                    game_over = True
                    game_active = False
                else:
                    bricks = result

        # ------------------------- Rendering -------------------------
        screen.fill(BLACK)

        # Draw background grid
        for i in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(screen, (10, 10, 20), (0, i), (SCREEN_WIDTH, i))

        # Draw bricks
        for brick in bricks:
            brick.draw(screen)

        # Draw power-ups
        for powerup in powerups:
            powerup.draw(screen)

        # Draw particles
        for particle in particles:
            particle.draw(screen)

        # Draw balls
        for ball in balls:
            ball.draw(screen)

        # Draw aim line
        if is_dragging and swipe_start and swipe_end:
            draw_aim_line(screen, swipe_start, swipe_end)
            pygame.draw.circle(screen, WHITE, swipe_start, 5, 1)

        # Draw swipe zone
        if game_active and not game_over and not victory:
            s = pygame.Surface((SCREEN_WIDTH, 150), pygame.SRCALPHA)
            s.fill((50, 50, 100, 50))
            screen.blit(s, (0, SCREEN_HEIGHT - 150))
            help_text = font.render("Swipe to Launch", True, GRAY)
            screen.blit(help_text, (20, SCREEN_HEIGHT - 40))

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        # Draw combo
        if combo_display_timer > 0 and combo_count > 1:
            combo_text = large_font.render(f"x{combo_count} COMBO!", True, YELLOW)
            text_rect = combo_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(combo_text, text_rect)

            bonus_text = font.render(f"+{min(combo_count * 5, 50)}", True, GREEN)
            bonus_rect = bonus_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(bonus_text, bonus_rect)

        # Draw power-up status
        y_offset = 60
        for ball in balls:
            if ball.fire_mode:
                fire_text = small_font.render(f"FIRE: {ball.fire_timer // 60}s", True, ORANGE)
                screen.blit(fire_text, (20, y_offset))
                y_offset += 25
                break

        # Draw ball count
        balls_text = font.render(f"Balls: {len(balls)}", True, WHITE)
        screen.blit(balls_text, (20, y_offset))

        # Draw reset button
        pygame.draw.rect(screen, DARK_GRAY, reset_button)
        pygame.draw.rect(screen, WHITE, reset_button, 2)
        reset_label = font.render("Reset", True, WHITE)
        screen.blit(reset_label, (reset_button.x + 15, reset_button.y + 8))

        # Draw game over/victory message
        if game_over:
            over_text = large_font.render("GAME OVER", True, RED)
            text_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(over_text, text_rect)

            restart_text = font.render("Press Reset to Play Again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()