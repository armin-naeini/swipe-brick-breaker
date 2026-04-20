import pygame
import sys
import math
import random

# ------------------------- تنظیمات اولیه -------------------------
pygame.init()

# ابعاد صفحه
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# رنگ‌ها (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
GREEN = (50, 255, 100)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# تنظیمات صفحه
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Swipe Brick Breaker - نسخه پیشرفته")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


# ------------------------- کلاس توپ (Ball) -------------------------
class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 8
        self.color = WHITE
        self.active = True  # توپ فعال است یا باید حذف شود

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # برخورد با دیواره‌های چپ و راست
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x + self.radius >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.vx = -self.vx

        # برخورد با سقف
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = -self.vy

        # اگر توپ از پایین صفحه خارج شد (باخت) -> غیرفعال می‌شود
        if self.y - self.radius > SCREEN_HEIGHT:
            self.active = False

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            # یک هاله نوری کوچک دور توپ
            pygame.draw.circle(surface, (100, 100, 255), (int(self.x), int(self.y)), self.radius + 2, 1)

    def check_collision_with_brick(self, brick):
        """بررسی و اعمال برخورد با یک آجر"""
        # نزدیک‌ترین نقطه آجر به مرکز توپ
        closest_x = max(brick.rect.left, min(self.x, brick.rect.right))
        closest_y = max(brick.rect.top, min(self.y, brick.rect.bottom))

        dx = self.x - closest_x
        dy = self.y - closest_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < self.radius:
            # جهت برخورد را مشخص می‌کنیم
            if distance == 0:
                distance = 0.01

            # بردار نرمال سطح
            nx = dx / distance
            ny = dy / distance

            # جابجا کردن توپ به بیرون از آجر
            overlap = self.radius - distance
            self.x += nx * overlap
            self.y += ny * overlap

            # تغییر سرعت (انعکاس)
            dot = self.vx * nx + self.vy * ny
            if dot < 0:
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny

            return True
        return False


# ------------------------- کلاس آجر (Brick) -------------------------
class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = 1  # آجرها یک ضربه‌ای هستند
        self.active = True

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, 2)  # حاشیه


# ------------------------- تابع ساخت دیوار آجری -------------------------
def create_bricks(rows, cols):
    bricks = []
    margin = 5
    # عرض آجر بر اساس عرض صفحه و تعداد ستون‌ها
    brick_width = (SCREEN_WIDTH - (cols + 1) * margin) // cols
    brick_height = 20

    # رنگ‌ها بر اساس ردیف
    colors = [RED, (255, 165, 0), YELLOW, GREEN, BLUE, PURPLE]

    for row in range(rows):
        for col in range(cols):
            x = margin + col * (brick_width + margin)
            y = margin + 80 + row * (brick_height + margin)  # 80 پیکسل فاصله از بالا
            color = colors[row % len(colors)]
            bricks.append(Brick(x, y, brick_width, brick_height, color))
    return bricks


# ------------------------- تابع رسم خط نشانه‌گیری (Swipe) -------------------------
def draw_aim_line(surface, start_pos, end_pos):
    if start_pos and end_pos:
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = math.sqrt(dx ** 2 + dy ** 2)

        if length > 10:  # فقط اگر کشیدگی حداقل ۱۰ پیکسل باشد
            # رسم خط اصلی
            pygame.draw.line(surface, WHITE, start_pos, end_pos, 2)

            # رسم نقاط جهت‌نما (نقطه چین)
            steps = int(length // 15)
            if steps > 0:
                for i in range(steps):
                    t = i / steps
                    px = start_pos[0] + dx * t
                    py = start_pos[1] + dy * t
                    pygame.draw.circle(surface, (200, 200, 200), (int(px), int(py)), 3)


# ------------------------- حلقه اصلی بازی -------------------------
def main():
    # متغیرهای بازی
    balls = []
    score = 0
    game_active = True

    # ساخت آجرها (6 ردیف، 8 ستون)
    bricks = create_bricks(6, 8)

    # متغیرهای Swipe
    swipe_start = None
    swipe_end = None
    is_dragging = False

    # ناحیه مجاز برای شروع کشیدن (قسمت پایین صفحه برای جلوگیری از تداخل با آجرها)
    drag_zone = pygame.Rect(0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150)

    # دکمه ریست
    reset_button = pygame.Rect(SCREEN_WIDTH - 120, 10, 110, 40)

    running = True
    while running:
        # ------------------------- مدیریت رویدادها -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # ماوس فشرده شد
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # بررسی کلیک روی دکمه ریست
                if reset_button.collidepoint(mx, my):
                    # ریست کردن کامل بازی
                    balls.clear()
                    bricks = create_bricks(6, 8)
                    score = 0
                    game_active = True
                    continue

                # شروع کشیدن فقط در ناحیه پایین (وقتی بازی فعال است)
                if game_active and drag_zone.collidepoint(mx, my):
                    swipe_start = (mx, my)
                    swipe_end = (mx, my)
                    is_dragging = True

            # ماوس در حال حرکت
            if event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    swipe_end = pygame.mouse.get_pos()

            # ماوس رها شد -> پرتاب توپ
            if event.type == pygame.MOUSEBUTTONUP:
                if is_dragging and swipe_start and swipe_end:
                    # محاسبه بردار سرعت
                    dx = swipe_end[0] - swipe_start[0]
                    dy = swipe_end[1] - swipe_start[1]

                    # مقیاس سرعت (هر چه بیشتر بکشید سریعتر)
                    speed_scale = 0.25
                    vx = dx * speed_scale
                    vy = dy * speed_scale

                    # محدودیت حداقل سرعت
                    if math.sqrt(vx ** 2 + vy ** 2) < 3:
                        vx = 0
                        vy = -7  # سرعت پیش‌فرض عمودی

                    # ایجاد توپ جدید در نقطه شروع کشیدن
                    # اما برای اینکه توپ به موس نخورد، کمی بالاتر از نقطه شروع ایجاد می‌کنیم
                    new_ball = Ball(swipe_start[0], swipe_start[1] - 20, vx, vy)
                    balls.append(new_ball)

                # پایان کشیدن
                is_dragging = False
                swipe_start = None
                swipe_end = None

        # ------------------------- بروزرسانی منطق بازی -------------------------
        if game_active:
            # حرکت توپ‌ها و بررسی برخورد
            for ball in balls[:]:  # [:] برای جلوگیری از خطای تغییر لیست در حین پیمایش
                if ball.active:
                    ball.move()

                    # بررسی برخورد با آجرها
                    for brick in bricks:
                        if brick.active:
                            if ball.check_collision_with_brick(brick):
                                brick.active = False
                                score += 10
                                # کمی سرعت را افزایش می‌دهیم تا بازی هیجان‌انگیزتر شود (اختیاری)
                                # ball.vx *= 1.02
                                # ball.vy *= 1.02
                else:
                    # حذف توپ‌های غیرفعال
                    balls.remove(ball)

            # بررسی شرط برد (همه آجرها نابود شده باشند)
            active_bricks = [b for b in bricks if b.active]
            if len(active_bricks) == 0:
                game_active = False  # پیروزی

        # ------------------------- رندر (نقاشی) -------------------------
        screen.fill(BLACK)

        # رسم یک گرادیان ساده در پس‌زمینه (خطوط افقی کم‌رنگ)
        for i in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(screen, (10, 10, 20), (0, i), (SCREEN_WIDTH, i))

        # رسم آجرها
        for brick in bricks:
            brick.draw(screen)

        # رسم توپ‌ها
        for ball in balls:
            ball.draw(screen)

        # رسم خط نشانه‌گیری (در حین کشیدن)
        if is_dragging and swipe_start and swipe_end:
            draw_aim_line(screen, swipe_start, swipe_end)
            # رسم یک دایره در نقطه شروع
            pygame.draw.circle(screen, WHITE, swipe_start, 5, 1)

        # رسم ناحیه Swipe (راهنمای بصری)
        if game_active:
            # مستطیل نیمه شفاف در پایین
            s = pygame.Surface((SCREEN_WIDTH, 150), pygame.SRCALPHA)
            s.fill((50, 50, 100, 50))
            screen.blit(s, (0, SCREEN_HEIGHT - 150))
            # متن راهنما
            help_text = font.render("برای پرتاب بکشید (Swipe)", True, GRAY)
            screen.blit(help_text, (20, SCREEN_HEIGHT - 40))

        # نمایش امتیاز
        score_text = font.render(f"امتیاز: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        # نمایش تعداد توپ‌های فعال
        balls_text = font.render(f"توپ‌ها: {len(balls)}", True, WHITE)
        screen.blit(balls_text, (20, 60))

        # دکمه ریست
        pygame.draw.rect(screen, DARK_GRAY, reset_button)
        pygame.draw.rect(screen, WHITE, reset_button, 2)
        reset_label = font.render("Reset", True, WHITE)
        screen.blit(reset_label, (reset_button.x + 15, reset_button.y + 8))

        # نمایش پیام برد / باخت (در صورت لزوم)
        if not game_active:
            active_bricks = [b for b in bricks if b.active]
            if len(active_bricks) == 0:
                win_text = font.render("پیروز شدی! (برای بازی دوباره Reset)", True, GREEN)
                screen.blit(win_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            # توجه: باخت خاصی در این نسخه نداریم چون بی‌نهایت توپ داریم
            # اما اگر همه توپ‌ها گم شوند و آجری باقی مانده باشد، بازی ادامه دارد.

        pygame.display.flip()
        clock.tick(60)  # 60 فریم بر ثانیه


if __name__ == "__main__":
    main()