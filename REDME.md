# 🎮 Swipe Brick Breaker

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.5.0-purple.svg)]()

**A strategic brick breaker game with swipe mechanics, multiple difficulty levels, and stunning visual effects**

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
- **Multiball System**: Random chance to receive extra balls during gameplay

#### ⚙️ **Advanced Settings System**
- **Theme Selection**: Choose between Dark and Light themes
- **Three Difficulty Levels**: Easy, Normal, and Hard
- **Persistent Settings**: All preferences saved automatically
- **Real-time Theme Switching**: Change appearance without restarting

#### 🎲 **Dynamic Brick Generation**
- **Random Gaps**: Each row has random empty spaces (not just a solid wall)
- **Variable Values**: Bricks range from 1 to increasingly higher values with decimal precision
- **Clean Display**: Values show as integers or with one decimal place (e.g., 3 or 3.5)
- **Power-up Bricks**: Special golden bricks contain game-changing abilities
- **Visual Feedback**: Bricks flash when hit and explode with particle effects

#### ⚡ **Power-up System**
| Icon | Name | Effect | Duration |
|------|------|--------|----------|
| +1 | Extra Ball | Adds one ball to your inventory | Instant |
| 🔥 | Fire Ball | Deals 2x damage to bricks | 5 seconds |
| ⟋ | Pierce Shot | Passes through up to 3 bricks | 3 bricks |

#### 📊 **Difficulty Settings Impact**

| Parameter | Easy | Normal | Hard |
|-----------|------|--------|------|
| Ball Speed | 0.10x | 0.14x | 0.18x |
| Brick Damage | 1.5x | 1.0x | 0.7x |
| Power-up Chance | 20% | 15% | 10% |
| Extra Balls/Turn | 2 | 1 | 1 |
| Multiball Chance | 15% | 10% | 5% |
| Ball Trail Length | 25 | 20 | 15 |
| Particle Count | 12 | 8 | 5 |
| Dead Zone Offset | +50 | 0 | -30 |
| Enemy Health | 0.7x | 1.0x | 1.3x |

#### 🎨 **Visual Excellence**
- **Dual Themes**: Complete Dark and Light mode support
- **Particle System**: Hundreds of particles for explosions, trails, and effects
- **Screen Shake**: Impact feedback for powerful hits
- **Floating Text**: Damage numbers and combo indicators
- **Gradient Backgrounds**: Beautiful, modern aesthetic with theme adaptation
- **Animated UI**: Smooth transitions and hover effects
- **Starfield Effect**: Twinkling stars in the background

#### 📊 **Progress Tracking**
- **Statistics Screen**: Detailed post-game analysis including:
  - Bricks Broken
  - Total Shots Fired
  - Accuracy Percentage
  - Power-ups Collected
  - Multiball Triggers
  - Maximum Combo Achieved
  - Total Play Time
- **Best Score**: Persistent local storage of your highest score
- **Settings Save**: Theme and difficulty preferences remembered

#### 🎵 **Audio Feedback**
- Shoot sounds
- Brick break effects
- Power-up collection chimes
- Multiball activation fanfare
- Game over fanfare

---

## 🎮 How to Play

### Phase 1: Getting Started
1. Launch the game to see the main menu
2. Configure settings (optional):
   - Choose Dark or Light theme
   - Select difficulty (Easy/Normal/Hard)
3. Click **START GAME**
4. Watch the 3-2-1 countdown
5. You start with **3 balls** and **1 row** of bricks (value 1)

### Phase 2: Core Mechanics
1. **Aim**: Drag from the bottom area (swipe zone)
2. **Shoot**: Release to launch the ball
3. **Wait**: The ball bounces and eventually stops at the bottom
4. **Progress**: After the ball stops, bricks move down one row
5. **New Row**: A stronger row of bricks appears at the top
6. **Reward**: You receive extra balls for completing the turn (amount depends on difficulty)

### Phase 3: Advanced Strategies
- **Collect Power-ups**: Break golden bricks to get special abilities
- **Chain Hits**: Hit multiple bricks rapidly for combo bonuses
- **Pierce Strategically**: Use pierce shots to hit bricks behind others
- **Manage Resources**: Don't waste balls - every shot counts
- **Multiball Luck**: Hope for multiball triggers to boost your arsenal

### Victory & Defeat
- **Game Over**: Bricks reach the red "DEAD ZONE" at the bottom
- **Survival**: The game continues indefinitely - how long can you last?
- **High Score**: Try to beat your personal best across all difficulties

---

## 🕹️ Controls

| Action | Control | Description |
|--------|---------|-------------|
| Aim & Shoot | Mouse Drag (from bottom) | Drag to aim, release to shoot |
| Menu Navigation | Mouse Click | Click buttons to navigate |
| Settings Toggle | Left/Right Click | Change theme and difficulty |
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
git clone https://github.com/armin-naini/swipe-brick-breaker.git
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
git clone https://github.com/armin-naini/swipe-brick-breaker.git && cd swipe-brick-breaker && python main.py
```

---

## 📁 Project Structure

```
swipe-brick-breaker/
├── main.py              # Main game file (all-in-one)
├── README.md            # Comprehensive documentation
├── LICENSE              # MIT License
├── settings.json        # Theme and difficulty preferences (auto-generated)
└── save_data.json       # Persistent game statistics (auto-generated)

```

---

## 🎯 Game Mechanics Deep Dive

### Brick Value Progression
- **Turn 1**: Base value = 1
- **Turn 2**: Base value = 2-3
- **Turn 5**: Base value = 5-7
- **Turn 10+**: Base value = 10+ with random variations
- **Decimal Precision**: Values display cleanly (3 or 3.5, never 3.500000)

### Row Generation Algorithm
```python
For each of 7 columns:
    Fill chance = 40% + (turn_number × 3%)
    Maximum fill = 75%
    
If filled:
    Value = base_value × difficulty_multiplier + random(-1 to +2)
    10% chance for extra +2 to +4 bonus
```

### Scoring System
- **Base Score**: Brick value × 10
- **Combo Bonus**: +5 points per consecutive hit (max +50)
- **Power-up Bricks**: Same score as normal bricks
- **Total Score**: Sum of all destroyed brick scores

### Multiball System
- Random chance to trigger after each turn
- Awards 1-2 extra balls
- Chance varies by difficulty (Easy: 15%, Normal: 10%, Hard: 5%)
- Visual and audio feedback when triggered

---

## 🔧 Configuration

### Persistent Settings
The game automatically saves:
- Theme preference (Dark/Light)
- Difficulty selection (Easy/Normal/Hard)
- Best score per difficulty
- Total games played and statistics

### Manual Configuration
For advanced users, edit `settings.json`:
```json
{
    "theme": "Dark",
    "difficulty": "Normal"
}
```

---

## 🐛 Troubleshooting

### Common Issues

**Q: Game won't start - "No module named 'pygame'"**
```bash
pip install --upgrade pygame
```

**Q: Game runs slowly**
- Switch to Light theme (fewer visual effects)
- Reduce to Easy difficulty (fewer particles)
- Close background applications

**Q: No sound**
- Check system volume
- Ensure audio drivers are working
- Game works fine without sound files

**Q: Settings not saving**
- Check write permissions in game directory
- Delete `settings.json` to reset

**Q: Display issues with decimal numbers**
- Update to latest version (fixed in v2.5.0)
- Numbers now display cleanly as integers or with 1 decimal

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
git clone https://github.com/armin-naini/swipe-brick-breaker.git
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

- **Email**: arminneaini@gmail.com.com

---

## 🏆 Future Roadmap

### Version 2.6 (Coming Soon)
- [ ] Additional power-ups (Slow Time, Magnet, Laser)
- [ ] Daily challenges with rewards
- [ ] Achievement system with 20+ achievements
- [ ] Sound volume controls

### Version 3.0
- [ ] Different game modes (Time Attack, Puzzle, Zen)
- [ ] Boss battles every 10 turns with unique mechanics
- [ ] Upgrade shop between turns
- [ ] Customizable ball skins and effects

### Version 3.5
- [ ] Online leaderboards with difficulty filters
- [ ] Level editor for custom challenges
- [ ] Local multiplayer (2 players)
- [ ] Replay system with sharing

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
- **سیستم چند توپی**: شانس دریافت توپ‌های اضافی در طول بازی

#### ⚙️ **سیستم تنظیمات پیشرفته**
- **انتخاب تم**: تم تاریک و روشن
- **سه سطح سختی**: آسان، معمولی و سخت
- **ذخیره تنظیمات**: تمام تنظیمات به صورت خودکار ذخیره می‌شوند
- **تغییر تم در لحظه**: تغییر ظاهر بدون نیاز به راه‌اندازی مجدد

#### 🎲 **تولید پویای آجر**
- **فضاهای خالی تصادفی**: هر ردیف دارای فضاهای خالی تصادفی است (نه فقط یک دیوار صلب)
- **مقادیر متغیر**: آجرها از ۱ تا مقادیر بالاتر با دقت اعشاری متغیر هستند
- **نمایش تمیز**: مقادیر به صورت اعداد صحیح یا با یک رقم اعشار (مثلاً ۳ یا ۳.۵)
- **آجرهای پاورآپ**: آجرهای طلایی ویژه حاوی قابلیت‌های تغییردهنده بازی
- **بازخورد بصری**: آجرها هنگام ضربه فلش می‌زنند و با افکت‌های ذره‌ای منفجر می‌شوند

#### ⚡ **سیستم پاورآپ**
| آیکون | نام | اثر | مدت زمان |
|-------|-----|-----|----------|
| +1 | توپ اضافی | یک توپ به موجودی اضافه می‌کند | آنی |
| 🔥 | توپ آتشین | آسیب ۲ برابر به آجرها | ۵ ثانیه |
| ⟋ | شلیک نفوذی | از ۳ آجر عبور می‌کند | ۳ آجر |

#### 📊 **تأثیر تنظیمات سختی**

| پارامتر | آسان | معمولی | سخت |
|---------|------|--------|------|
| سرعت توپ | ۰.۱۰x | ۰.۱۴x | ۰.۱۸x |
| آسیب به آجر | ۱.۵x | ۱.۰x | ۰.۷x |
| شانس پاورآپ | ۲۰٪ | ۱۵٪ | ۱۰٪ |
| توپ اضافی/نوبت | ۲ | ۱ | ۱ |
| شانس چند توپی | ۱۵٪ | ۱۰٪ | ۵٪ |
| طول دنباله توپ | ۲۵ | ۲۰ | ۱۵ |
| تعداد ذرات | ۱۲ | ۸ | ۵ |
| موقعیت منطقه مرگ | ۵۰+ | ۰ | ۳۰- |
| سلامت دشمن | ۰.۷x | ۱.۰x | ۱.۳x |

#### 🎨 **برتری بصری**
- **دو تم کامل**: پشتیبانی از حالت تاریک و روشن
- **سیستم ذرات**: صدها ذره برای انفجارها، دنباله‌ها و افکت‌ها
- **لرزش صفحه**: بازخورد ضربه برای ضربات قدرتمند
- **متن شناور**: اعداد آسیب و نشانگرهای کمبو
- **پس‌زمینه گرادیانت**: زیبایی مدرن با انطباق تم
- **UI متحرک**: ترنزیشن‌های نرم و افکت‌های هاور
- **افکت ستاره‌ای**: ستاره‌های چشمک‌زن در پس‌زمینه

#### 📊 **پیگیری پیشرفت**
- **صفحه آمار**: تحلیل دقیق پس از بازی شامل:
  - آجرهای شکسته شده
  - کل شلیک‌ها
  - درصد دقت
  - پاورآپ‌های جمع‌آوری شده
  - فعال‌سازی‌های چند توپی
  - حداکثر کمبو
  - زمان کل بازی
- **بهترین امتیاز**: ذخیره‌سازی محلی ماندگار بالاترین امتیاز
- **ذخیره تنظیمات**: به خاطر سپردن تم و سطح سختی

#### 🎵 **بازخورد صوتی**
- صدای شلیک
- افکت‌های شکستن آجر
- زنگ‌های جمع‌آوری پاورآپ
- صدای فعال‌سازی چند توپی
- صدای پایان بازی

---

## 🎮 نحوه بازی

### فاز ۱: شروع کار
1. بازی را اجرا کنید تا منوی اصلی را ببینید
2. تنظیمات را پیکربندی کنید (اختیاری):
   - تم تاریک یا روشن را انتخاب کنید
   - سختی را انتخاب کنید (آسان/معمولی/سخت)
3. روی **START GAME** کلیک کنید
4. شمارش معکوس ۳-۲-۱ را تماشا کنید
5. شما با **۳ توپ** و **۱ ردیف** آجر (ارزش ۱) شروع می‌کنید

### فاز ۲: مکانیک‌های اصلی
1. **هدف‌گیری**: از ناحیه پایین بکشید (ناحیه کشیدن)
2. **شلیک**: رها کنید تا توپ پرتاب شود
3. **انتظار**: توپ برمی‌گردد و در نهایت در پایین متوقف می‌شود
4. **پیشرفت**: پس از توقف توپ، آجرها یک ردیف پایین می‌آیند
5. **ردیف جدید**: یک ردیف قوی‌تر از آجرها در بالا ظاهر می‌شود
6. **پاداش**: شما توپ‌های اضافی برای تکمیل نوبت دریافت می‌کنید (مقدار بستگی به سختی دارد)

### فاز ۳: استراتژی‌های پیشرفته
- **جمع‌آوری پاورآپ**: آجرهای طلایی را بشکنید تا قابلیت‌های ویژه بگیرید
- **ضربات زنجیره‌ای**: چندین آجر را به سرعت بزنید برای پاداش کمبو
- **نفوذ استراتژیک**: از شلیک‌های نفوذی برای زدن آجرهای پشت سر استفاده کنید
- **مدیریت منابع**: توپ‌ها را هدر ندهید - هر شلیک مهم است
- **شانس چند توپی**: امیدوار به فعال‌سازی چند توپی برای تقویت زرادخانه خود باشید

### پیروزی و شکست
- **پایان بازی**: آجرها به "منطقه مرگ" قرمز در پایین می‌رسند
- **بقا**: بازی به طور نامحدود ادامه دارد - چقدر می‌توانید دوام بیاورید؟
- **بالاترین امتیاز**: سعی کنید رکورد شخصی خود را در تمام سطوح سختی بشکنید

---

## 🕹️ کنترل‌ها

| عملکرد | کنترل | توضیح |
|--------|-------|-------|
| هدف‌گیری و شلیک | کشیدن ماوس (از پایین) | بکشید تا هدف‌گیری کنید، رها کنید تا شلیک کنید |
| ناوبری منو | کلیک ماوس | برای ناوبری کلیک کنید |
| تغییر تنظیمات | کلیک چپ/راست | تغییر تم و سختی |
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
git clone https://github.com/armin-naini/swipe-brick-breaker.git
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
git clone https://github.com/armin-naini/swipe-brick-breaker.git && cd swipe-brick-breaker && python main.py
```

---

## 📁 ساختار پروژه

```
swipe-brick-breaker/
├── main.py              # فایل اصلی بازی (همه در یک)
├── README.md            # مستندات جامع
├── LICENSE              # مجوز MIT
├── settings.json        # تنظیمات تم و سختی (خودکار ساخته می‌شود)
└── save_data.json       # آمار بازی ماندگار (خودکار ساخته می‌شود)


```

---

## 🎯 بررسی عمیق مکانیک‌های بازی

### پیشرفت ارزش آجرها
- **نوبت ۱**: ارزش پایه = ۱
- **نوبت ۲**: ارزش پایه = ۲-۳
- **نوبت ۵**: ارزش پایه = ۵-۷
- **نوبت ۱۰+**: ارزش پایه = ۱۰+ با تغییرات تصادفی
- **دقت اعشاری**: مقادیر به صورت تمیز نمایش داده می‌شوند (۳ یا ۳.۵، نه ۳.۵۰۰۰۰۰)

### الگوریتم تولید ردیف
```python
برای هر یک از ۷ ستون:
    شانس پر شدن = ۴۰٪ + (شماره_نوبت × ۳٪)
    حداکثر پر شدن = ۷۵٪
    
اگر پر شد:
    ارزش = ارزش_پایه × ضریب_سختی + تصادفی(-۱ تا +۲)
    ۱۰٪ شانس برای +۲ تا +۴ اضافی
```

### سیستم امتیازدهی
- **امتیاز پایه**: ارزش آجر × ۱۰
- **پاداش کمبو**: +۵ امتیاز به ازای هر ضربه متوالی (حداکثر +۵۰)
- **آجرهای پاورآپ**: امتیاز مشابه آجرهای معمولی
- **امتیاز کل**: مجموع امتیازات تمام آجرهای نابود شده

### سیستم چند توپی
- شانس تصادفی برای فعال‌سازی پس از هر نوبت
- اعطای ۱-۲ توپ اضافی
- شانس بر اساس سختی متغیر است (آسان: ۱۵٪، معمولی: ۱۰٪، سخت: ۵٪)
- بازخورد بصری و صوتی هنگام فعال‌سازی

---

## 🔧 پیکربندی

### تنظیمات ماندگار
بازی به طور خودکار ذخیره می‌کند:
- ترجیح تم (تاریک/روشن)
- انتخاب سختی (آسان/معمولی/سخت)
- بهترین امتیاز برای هر سختی
- تعداد کل بازی‌ها و آمار

### پیکربندی دستی
برای کاربران پیشرفته، فایل `settings.json` را ویرایش کنید:
```json
{
    "theme": "Dark",
    "difficulty": "Normal"
}
```

---

## 🐛 عیب‌یابی

### مشکلات رایج

**س: بازی شروع نمی‌شود - "No module named 'pygame'"**
```bash
pip install --upgrade pygame
```

**س: بازی کند اجرا می‌شود**
- به تم روشن تغییر دهید (افکت‌های بصری کمتر)
- به سختی آسان کاهش دهید (ذرات کمتر)
- برنامه‌های پس‌زمینه را ببندید

**س: صدا کار نمی‌کند**
- صدای سیستم را بررسی کنید
- مطمئن شوید درایورهای صدا کار می‌کنند
- بازی بدون فایل‌های صوتی هم خوب کار می‌کند

**س: تنظیمات ذخیره نمی‌شوند**
- مجوزهای نوشتن در دایرکتوری بازی را بررسی کنید
- برای بازنشانی `settings.json` را حذف کنید

**س: مشکلات نمایش اعداد اعشاری**
- به آخرین نسخه به‌روزرسانی کنید (رفع شده در v2.5.0)
- اعداد حالا به صورت صحیح یا با یک رقم اعشار نمایش داده می‌شوند

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
git clone https://github.com/armin-naini/swipe-brick-breaker.git
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

### نسخه ۲.۶ (به زودی)
- [ ] پاورآپ‌های اضافی (زمان کند، مگنت، لیزر)
- [ ] چالش‌های روزانه با پاداش
- [ ] سیستم دستاوردها با ۲۰+ دستاورد
- [ ] کنترل‌های صدای موسیقی

### نسخه ۳.۰
- [ ] حالت‌های مختلف بازی (حمله زمانی، پازل، ذن)
- [ ] نبرد با غول آخر هر ۱۰ نوبت با مکانیک‌های منحصربفرد
- [ ] فروشگاه ارتقاء بین نوبت‌ها
- [ ] پوسته‌های توپ و افکت‌های قابل شخصی‌سازی

### نسخه ۳.۵
- [ ] جدول امتیازات آنلاین با فیلترهای سختی
- [ ] ویرایشگر مرحله برای چالش‌های سفارشی
- [ ] حالت چندنفره محلی (۲ نفر)
- [ ] سیستم بازپخش با قابلیت اشتراک‌گذاری

---

<div align="center">

**⭐ اگر از این بازی لذت می‌برید، لطفاً به مخزن ستاره دهید! ⭐**

ساخته شده با ❤️ و ☕ با استفاده از Python و Pygame

</div>