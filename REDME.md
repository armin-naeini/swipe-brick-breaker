# 🎮 Swipe Brick Breaker - BBTAN Style

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-purple.svg)]()

**A strategic brick breaker game with swipe mechanics, progressive difficulty, and beautiful visual effects**

[🇬🇧 English](#english) | [🇮🇷 فارسی](#فارسی)

<p align="center">
  <img src="screenshots/gameplay.gif" alt="Gameplay" width="600"/>
</p>

</div>

---

# 🇬🇧 English

## 📖 About The Project

**Swipe Brick Breaker** is a modern reimagining of the classic brick breaker genre, heavily inspired by popular mobile games like **BBTAN**. Unlike traditional brick breakers where you control a paddle, this game introduces strategic swipe mechanics where bricks progressively move down after each throw, creating an ever-increasing challenge that tests both your aim and tactical thinking.

### ✨ Key Features

#### 🎯 **Core Gameplay**
- **Intuitive Swipe Controls**: Drag and release to aim with precision trajectory prediction
- **Progressive Difficulty**: Bricks become stronger and move down one row after each turn
- **Strategic Depth**: Plan your shots carefully - every throw matters
- **Endless Mode**: Survive as many turns as possible against increasingly powerful bricks

#### 🎲 **Dynamic Brick Generation**
- **Random Gaps**: Each row has random empty spaces (not just a solid wall)
- **Variable Values**: Bricks range from 1 to increasingly higher values
- **Power-up Bricks**: Special golden bricks contain game-changing abilities
- **Visual Feedback**: Bricks flash when hit and explode with particle effects

#### ⚡ **Power-up System**
| Icon | Name | Effect | Duration |
|------|------|--------|----------|
| +1 | Extra Ball | Adds one ball to your inventory | Instant |
| 🔥 | Fire Ball | Deals 2x damage to bricks | 5 seconds |
| ⟋ | Pierce Shot | Passes through up to 3 bricks | 3 bricks |

#### 🎨 **Visual Excellence**
- **Particle System**: Hundreds of particles for explosions, trails, and effects
- **Screen Shake**: Impact feedback for powerful hits
- **Floating Text**: Damage numbers and combo indicators
- **Gradient Backgrounds**: Beautiful, modern aesthetic
- **Animated UI**: Smooth transitions and hover effects
- **Starfield Effect**: Twinkling stars in the background

#### 📊 **Progress Tracking**
- **Statistics Screen**: Detailed post-game analysis
- **Best Score**: Persistent local storage of your highest score
- **Performance Metrics**: Accuracy, shots fired, power-ups collected, and more
- **Play Time**: Track how long you survived

#### 🎵 **Audio Feedback**
- Shoot sounds
- Brick break effects
- Power-up collection chimes
- Game over fanfare

---

## 🎮 How to Play

### Phase 1: Getting Started
1. Launch the game to see the main menu
2. Click **START GAME**
3. Watch the 3-2-1 countdown
4. You start with **3 balls** and **1 row** of bricks (all value 1)

### Phase 2: Core Mechanics
1. **Aim**: Drag from the bottom area (swipe zone)
2. **Shoot**: Release to launch the ball
3. **Wait**: The ball bounces and eventually stops at the bottom
4. **Progress**: After the ball stops, bricks move down one row
5. **New Row**: A stronger row of bricks appears at the top
6. **Reward**: You receive +1 ball for completing the turn

### Phase 3: Advanced Strategies
- **Collect Power-ups**: Break golden bricks to get special abilities
- **Chain Hits**: Hit multiple bricks rapidly for combo bonuses
- **Pierce Strategically**: Use pierce shots to hit bricks behind others
- **Manage Resources**: Don't waste balls - every shot counts

### Victory & Defeat
- **Game Over**: Bricks reach the red "DEAD ZONE" at the bottom
- **Survival**: The game continues indefinitely - how long can you last?
- **High Score**: Try to beat your personal best

---

## 🕹️ Controls

| Action | Control | Description |
|--------|---------|-------------|
| Aim & Shoot | Mouse Drag (from bottom) | Drag to aim, release to shoot |
| Menu Navigation | Mouse Click | Click buttons to navigate |
| Return to Menu | MENU Button | Exit current game to main menu |
| Quit Game | Close Window / QUIT Button | Exit the application |

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/armin-naeini/swipe-brick-breaker.git
cd swipe-brick-breaker
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install pygame
```

4. **Run the game**
```bash
python main.py
```

### One-Line Install (if you have pygame)
```bash
git clone https://github.com/armin-naeini/swipe-brick-breaker.git && cd swipe-brick-breaker && python main.py
```

---

## 📁 Project Structure

```
swipe-brick-breaker/
├── main.py              # Main game file (all-in-one)
├── README.md            # Comprehensive documentation
├── LICENSE              # MIT License
├── .gitignore           # Git ignore rules
└── save_data.json       # Persistent save data (auto-generated)

```

---

## 🎯 Game Mechanics Deep Dive

### Brick Value Progression
- **Turn 1**: Base value = 1
- **Turn 2**: Base value = 2-3
- **Turn 5**: Base value = 5-7
- **Turn 10+**: Base value = 10+ with random variations

### Row Generation Algorithm
```python
For each of 7 columns:
    Fill chance = 40% + (turn_number × 3%)
    Maximum fill = 75%
    
If filled:
    Value = base_value + random(-1 to +2)
    10% chance for extra +2 to +4 bonus
```

### Scoring System
- **Base Score**: Brick value × 10
- **Combo Bonus**: +5 points per consecutive hit (max +50)
- **Power-up Bricks**: Same score as normal bricks
- **Total Score**: Sum of all destroyed brick scores

### Statistics Tracked
- Bricks Broken
- Total Shots Fired
- Accuracy (bricks/shot ratio)
- Power-ups Collected
- Maximum Combo Achieved
- Total Play Time

---

## 🔧 Configuration

### Adjusting Game Speed
In `main.py`, find line ~848:

```python
# Change this value to adjust ball speed
SPEED_MULTIPLIER = 0.14  # Default: 0.14 (0.18 in original)

# Lower = Slower, Higher = Faster
# Recommended values:
# Easy:   0.10
# Normal: 0.14
# Hard:   0.18
# Expert: 0.22
```

### Modifying Difficulty
```python
# Line ~851 - Minimum throw speed
MIN_SPEED = 3.5        # Default: 3.5
MIN_VERTICAL = -6      # Default: -6

# Line ~74 - Dead zone position
DEAD_ZONE_Y = SCREEN_HEIGHT - 150  # Higher = Harder

# Line ~68 - Starting balls
INITIAL_BALLS = 3      # Default: 3
```

---

## 🐛 Troubleshooting

### Common Issues

**Q: Game won't start - "No module named 'pygame'"**
```bash
pip install --upgrade pygame
```

**Q: Game runs slowly**
- Reduce particle count (line 627: change `range(8)` to `range(4)`)
- Disable starfield (comment out lines 860-868)

**Q: No sound**
- Check system volume
- Ensure audio files exist or remove sound code
- On Linux: `sudo apt-get install python3-pygame`

**Q: Save data not working**
- Check write permissions in game directory
- Delete `save_data.json` to reset

---

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can help:

### Ways to Contribute
- 🐛 **Report Bugs**: Open an issue with detailed steps to reproduce
- 💡 **Suggest Features**: Share your ideas for new mechanics
- 🎨 **Improve Graphics**: Better sprites, effects, or UI designs
- 🔊 **Add Sounds**: Create or find better sound effects
- 📝 **Documentation**: Fix typos or improve clarity
- 💻 **Code**: Submit PRs for bug fixes or new features

### Development Setup
```bash
# Fork and clone
git clone https://github.com/armin-naeini/swipe-brick-breaker.git
cd swipe-brick-breaker

# Create branch
git checkout -b feature/amazing-feature

# Make changes and commit
git add .
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- 📋 License and copyright notice required

---

## 🙏 Acknowledgments

### Inspiration
- **BBTAN** - The original mobile game that inspired this project
- **Arkanoid** - The classic that started it all
- **Breakout** - The grandfather of brick breakers

### Built With
- [Python](https://www.python.org/) - Programming language
- [Pygame](https://www.pygame.org/) - Game development library
- [SDL](https://www.libsdl.org/) - Underlying graphics library

### Special Thanks
- The Pygame community for excellent documentation
- All playtesters who provided valuable feedback
- You, for checking out this project!

---

## 📞 Contact & Support

- **Email**: arminneaini@gmail.com

---

## 🏆 Future Roadmap

### Version 2.1 (Coming Soon)
- [ ] Additional power-ups (Slow Time, Magnet, Laser)
- [ ] Daily challenges
- [ ] Achievement system
- [ ] Sound volume controls

### Version 2.5
- [ ] Different game modes (Time Attack, Puzzle)
- [ ] Boss battles every 10 turns
- [ ] Upgrade shop between turns
- [ ] Customizable ball skins

### Version 3.0
- [ ] Online leaderboards
- [ ] Level editor
- [ ] Multiplayer mode
- [ ] Replay system

---

<div align="center">

**⭐ If you enjoy this game, please star the repository! ⭐**

Made with ❤️ and ☕ using Python & Pygame

</div>

---

# 🇮🇷 فارسی

## 📖 درباره پروژه

**Swipe Brick Breaker** یک بازآفرینی مدرن از ژانر کلاسیک آجرشکن است که به شدت از بازی‌های موبایلی محبوب مانند **BBTAN** الهام گرفته شده. برخلاف آجرشکن‌های سنتی که شما یک تخته را کنترل می‌کنید، این بازی مکانیک‌های استراتژیک کشیدن و رها کردن را معرفی می‌کند که در آن آجرها پس از هر پرتاب به تدریج به سمت پایین حرکت می‌کنند و چالشی فزاینده ایجاد می‌کنند که هم هدف‌گیری و هم تفکر تاکتیکی شما را می‌آزماید.

### ✨ ویژگی‌های کلیدی

#### 🎯 **گیم‌پلی اصلی**
- **کنترل‌های لمسی شهودی**: بکشید و رها کنید تا با پیش‌بینی دقیق مسیر هدف‌گیری کنید
- **سختی پیشرونده**: آجرها قوی‌تر شده و پس از هر نوبت یک ردیف پایین می‌آیند
- **عمق استراتژیک**: شلیک‌های خود را با دقت برنامه‌ریزی کنید - هر پرتاب مهم است
- **حالت بی‌نهایت**: تا جایی که می‌توانید در برابر آجرهای قدرتمند زنده بمانید

#### 🎲 **تولید پویای آجر**
- **فضاهای خالی تصادفی**: هر ردیف دارای فضاهای خالی تصادفی است (نه فقط یک دیوار صلب)
- **مقادیر متغیر**: آجرها از ۱ تا مقادیر بالاتر متغیر هستند
- **آجرهای پاورآپ**: آجرهای طلایی ویژه حاوی قابلیت‌های تغییردهنده بازی
- **بازخورد بصری**: آجرها هنگام ضربه فلش می‌زنند و با افکت‌های ذره‌ای منفجر می‌شوند

#### ⚡ **سیستم پاورآپ**
| آیکون | نام | اثر | مدت زمان |
|-------|-----|-----|----------|
| +1 | توپ اضافی | یک توپ به موجودی اضافه می‌کند | آنی |
| 🔥 | توپ آتشین | آسیب ۲ برابر به آجرها | ۵ ثانیه |
| ⟋ | شلیک نفوذی | از ۳ آجر عبور می‌کند | ۳ آجر |

#### 🎨 **برتری بصری**
- **سیستم ذرات**: صدها ذره برای انفجارها، دنباله‌ها و افکت‌ها
- **لرزش صفحه**: بازخورد ضربه برای ضربات قدرتمند
- **متن شناور**: اعداد آسیب و نشانگرهای کمبو
- **پس‌زمینه گرادیانت**: زیبایی مدرن و چشم‌نواز
- **UI متحرک**: ترنزیشن‌های نرم و افکت‌های هاور
- **افکت ستاره‌ای**: ستاره‌های چشمک‌زن در پس‌زمینه

#### 📊 **پیگیری پیشرفت**
- **صفحه آمار**: تحلیل دقیق پس از بازی
- **بهترین امتیاز**: ذخیره‌سازی محلی ماندگار بالاترین امتیاز
- **معیارهای عملکرد**: دقت، تعداد شلیک، پاورآپ‌های جمع‌آوری شده و بیشتر
- **زمان بازی**: پیگیری مدت زمان بقا

#### 🎵 **بازخورد صوتی**
- صدای شلیک
- افکت‌های شکستن آجر
- زنگ‌های جمع‌آوری پاورآپ
- صدای پایان بازی

---

## 🎮 نحوه بازی

### فاز ۱: شروع کار
1. بازی را اجرا کنید تا منوی اصلی را ببینید
2. روی **START GAME** کلیک کنید
3. شمارش معکوس ۳-۲-۱ را تماشا کنید
4. شما با **۳ توپ** و **۱ ردیف** آجر (همگی ارزش ۱) شروع می‌کنید

### فاز ۲: مکانیک‌های اصلی
1. **هدف‌گیری**: از ناحیه پایین بکشید (ناحیه کشیدن)
2. **شلیک**: رها کنید تا توپ پرتاب شود
3. **انتظار**: توپ برمی‌گردد و در نهایت در پایین متوقف می‌شود
4. **پیشرفت**: پس از توقف توپ، آجرها یک ردیف پایین می‌آیند
5. **ردیف جدید**: یک ردیف قوی‌تر از آجرها در بالا ظاهر می‌شود
6. **پاداش**: شما برای تکمیل نوبت +۱ توپ دریافت می‌کنید

### فاز ۳: استراتژی‌های پیشرفته
- **جمع‌آوری پاورآپ**: آجرهای طلایی را بشکنید تا قابلیت‌های ویژه بگیرید
- **ضربات زنجیره‌ای**: چندین آجر را به سرعت بزنید برای پاداش کمبو
- **نفوذ استراتژیک**: از شلیک‌های نفوذی برای زدن آجرهای پشت سر استفاده کنید
- **مدیریت منابع**: توپ‌ها را هدر ندهید - هر شلیک مهم است

### پیروزی و شکست
- **پایان بازی**: آجرها به "منطقه مرگ" قرمز در پایین می‌رسند
- **بقا**: بازی به طور نامحدود ادامه دارد - چقدر می‌توانید دوام بیاورید؟
- **بالاترین امتیاز**: سعی کنید رکورد شخصی خود را بشکنید

---

## 🕹️ کنترل‌ها

| عملکرد | کنترل | توضیح |
|--------|-------|-------|
| هدف‌گیری و شلیک | کشیدن ماوس (از پایین) | بکشید تا هدف‌گیری کنید، رها کنید تا شلیک کنید |
| ناوبری منو | کلیک ماوس | برای ناوبری کلیک کنید |
| بازگشت به منو | دکمه MENU | خروج از بازی فعلی به منوی اصلی |
| خروج از بازی | بستن پنجره / دکمه QUIT | خروج از برنامه |

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- پایتون ۳.۸ یا بالاتر
- pip (مدیر بسته پایتون)

### راه‌اندازی گام به گام

1. **کلون کردن مخزن**
```bash
git clone https://github.com/armin-naeini/swipe-brick-breaker.git
cd swipe-brick-breaker
```

2. **ایجاد محیط مجازی (توصیه می‌شود)**
```bash
python -m venv venv

# در ویندوز:
venv\Scripts\activate

# در macOS/Linux:
source venv/bin/activate
```

3. **نصب وابستگی‌ها**
```bash
pip install pygame
```

4. **اجرای بازی**
```bash
python main.py
```

### نصب تک‌خطی (اگر pygame دارید)
```bash
git clone https://github.com/armin-naeini/swipe-brick-breaker.git && cd swipe-brick-breaker && python main.py
```

---

## 📁 ساختار پروژه

```
swipe-brick-breaker/
├── main.py              # فایل اصلی بازی (همه در یک)
├── README.md            # مستندات جامع
├── LICENSE              # مجوز MIT
└──  save_data.json       # داده‌های ذخیره ماندگار (خودکار ساخته می‌شود)

```

---

## 🎯 بررسی عمیق مکانیک‌های بازی

### پیشرفت ارزش آجرها
- **نوبت ۱**: ارزش پایه = ۱
- **نوبت ۲**: ارزش پایه = ۲-۳
- **نوبت ۵**: ارزش پایه = ۵-۷
- **نوبت ۱۰+**: ارزش پایه = ۱۰+ با تغییرات تصادفی

### الگوریتم تولید ردیف
```python
برای هر یک از ۷ ستون:
    شانس پر شدن = ۴۰٪ + (شماره_نوبت × ۳٪)
    حداکثر پر شدن = ۷۵٪
    
اگر پر شد:
    ارزش = ارزش_پایه + تصادفی(-۱ تا +۲)
    ۱۰٪ شانس برای +۲ تا +۴ اضافی
```

### سیستم امتیازدهی
- **امتیاز پایه**: ارزش آجر × ۱۰
- **پاداش کمبو**: +۵ امتیاز به ازای هر ضربه متوالی (حداکثر +۵۰)
- **آجرهای پاورآپ**: امتیاز مشابه آجرهای معمولی
- **امتیاز کل**: مجموع امتیازات تمام آجرهای نابود شده

### آمار پیگیری شده
- آجرهای شکسته شده
- کل شلیک‌ها
- دقت (نسبت آجر به شلیک)
- پاورآپ‌های جمع‌آوری شده
- حداکثر کمبو به دست آمده
- زمان کل بازی

---

## 🔧 پیکربندی

### تنظیم سرعت بازی
در `main.py`، حدود خط ۸۴۸ را پیدا کنید:

```python
# این مقدار را برای تنظیم سرعت توپ تغییر دهید
SPEED_MULTIPLIER = 0.14  # پیش‌فرض: 0.14 (در نسخه اصلی 0.18)

# کمتر = کندتر، بیشتر = سریعتر
# مقادیر پیشنهادی:
# آسان:   0.10
# معمولی: 0.14
# سخت:    0.18
# خبره:   0.22
```

### تغییر سختی
```python
# خط ~851 - حداقل سرعت پرتاب
MIN_SPEED = 3.5        # پیش‌فرض: 3.5
MIN_VERTICAL = -6      # پیش‌فرض: -6

# خط ~74 - موقعیت منطقه مرگ
DEAD_ZONE_Y = SCREEN_HEIGHT - 150  # بالاتر = سخت‌تر

# خط ~68 - توپ‌های شروع
INITIAL_BALLS = 3      # پیش‌فرض: 3
```

---

## 🐛 عیب‌یابی

### مشکلات رایج

**س: بازی شروع نمی‌شود - "No module named 'pygame'"**
```bash
pip install --upgrade pygame
```

**س: بازی کند اجرا می‌شود**
- تعداد ذرات را کاهش دهید (خط 627: `range(8)` را به `range(4)` تغییر دهید)
- ستاره‌های پس‌زمینه را غیرفعال کنید (خطوط 860-868 را کامنت کنید)

**س: صدا کار نمی‌کند**
- صدای سیستم را بررسی کنید
- مطمئن شوید فایل‌های صوتی وجود دارند یا کد صدا را حذف کنید
- در لینوکس: `sudo apt-get install python3-pygame`

**س: داده‌های ذخیره کار نمی‌کنند**
- مجوزهای نوشتن در دایرکتوری بازی را بررسی کنید
- `save_data.json` را برای بازنشانی حذف کنید

---

## 🤝 مشارکت

مشارکت‌ها خوش‌آمد و قدردانی می‌شوند! در اینجا نحوه کمک شما آمده است:

### راه‌های مشارکت
- 🐛 **گزارش باگ**: یک issue با مراحل دقیق بازتولید باز کنید
- 💡 **پیشنهاد ویژگی**: ایده‌های خود را برای مکانیک‌های جدید به اشتراک بگذارید
- 🎨 **بهبود گرافیک**: اسپرایت‌ها، افکت‌ها یا طراحی‌های UI بهتر
- 🔊 **افزودن صدا**: افکت‌های صوتی بهتر ایجاد یا پیدا کنید
- 📝 **مستندات**: اشتباهات تایپی را اصلاح یا وضوح را بهبود بخشید
- 💻 **کد**: PR برای رفع باگ یا ویژگی‌های جدید ارسال کنید

### راه‌اندازی توسعه
```bash
# Fork و clone
git clone https://github.com/yourusername/swipe-brick-breaker.git
cd swipe-brick-breaker

# ایجاد branch
git checkout -b feature/amazing-feature

# تغییرات را اعمال و commit کنید
git add .
git commit -m "Add amazing feature"

# Push و ایجاد PR
git push origin feature/amazing-feature
```

---

## 📝 مجوز

این پروژه تحت **مجوز MIT** منتشر شده است - برای جزئیات به فایل [LICENSE](LICENSE) مراجعه کنید.

### معنی این مجوز:
- ✅ استفاده تجاری مجاز است
- ✅ تغییر مجاز است
- ✅ توزیع مجاز است
- ✅ استفاده خصوصی مجاز است
- 📋 ذکر مجوز و کپی‌رایت الزامی است

---

## 🙏 تقدیر و تشکر

### الهام‌بخش
- **BBTAN** - بازی موبایل اصلی که این پروژه را الهام بخشید
- **Arkanoid** - کلاسیکی که همه چیز را شروع کرد
- **Breakout** - پدربزرگ آجرشکن‌ها

### ساخته شده با
- [Python](https://www.python.org/) - زبان برنامه‌نویسی
- [Pygame](https://www.pygame.org/) - کتابخانه توسعه بازی
- [SDL](https://www.libsdl.org/) - کتابخانه گرافیکی زیرین

### تشکر ویژه
- جامعه Pygame برای مستندات عالی
- تمام تست‌کننده‌هایی که بازخورد ارزشمند ارائه دادند
- شما، برای بررسی این پروژه!

---

## 📞 تماس و پشتیبانی

- **ایمیل**: arminneaini@gmail.com

---

## 🏆 نقشه راه آینده

### نسخه ۲.۱ (به زودی)
- [ ] پاورآپ‌های اضافی (زمان کند، مگنت، لیزر)
- [ ] چالش‌های روزانه
- [ ] سیستم دستاوردها
- [ ] کنترل‌های صدای موسیقی

### نسخه ۲.۵
- [ ] حالت‌های مختلف بازی (حمله زمانی، پازل)
- [ ] نبرد با غول آخر هر ۱۰ نوبت
- [ ] فروشگاه ارتقاء بین نوبت‌ها
- [ ] پوسته‌های قابل شخصی‌سازی توپ

### نسخه ۳.۰
- [ ] جدول امتیازات آنلاین
- [ ] ویرایشگر مرحله
- [ ] حالت چندنفره
- [ ] سیستم بازپخش

---

<div align="center">

**⭐ اگر از این بازی لذت می‌برید، لطفاً به مخزن ستاره دهید! ⭐**

ساخته شده با ❤️ و ☕ با استفاده از Python و Pygame

</div>