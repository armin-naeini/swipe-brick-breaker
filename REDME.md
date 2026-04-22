# 🎮 Swipe Brick Breaker - BBTAN Style

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A strategic brick breaker game with swipe mechanics and progressive difficulty**

[English](#english) | [فارسی](#فارسی)

</div>

---

# English

## 📖 About The Project

Swipe Brick Breaker is a modern take on the classic brick breaker genre, inspired by popular mobile games like BBTAN. Unlike traditional brick breakers, this game introduces strategic elements where bricks move down after each throw, creating an ever-increasing challenge.

### ✨ Features

- **🎯 Swipe Mechanics**: Intuitive drag-and-release controls for precise aiming
- **📊 Progressive Difficulty**: Bricks become stronger and move down with each turn
- **🎲 Random Generation**: Each row has random gaps and varied brick values
- **💫 Visual Effects**: Particles, screen shake, floating text, and smooth animations
- **⚡ Power-ups**: Fire balls, pierce shots, and extra balls
- **🔄 Endless Gameplay**: Survive as many turns as possible
- **🎨 Beautiful UI**: Gradient backgrounds, glowing effects, and polished visuals

### 🎮 How to Play

1. **Phase 1**: Start with one row of bricks (value 1)
2. **Swipe to Shoot**: Drag from the bottom area to aim and release to shoot
3. **Ball Returns**: The ball stops at the bottom after each throw
4. **Phase 2+**: After the first throw, bricks move down and a new stronger row appears
5. **Collect Power-ups**: Break special bricks to get powerful abilities
6. **Survive**: Don't let bricks reach the red "Dead Zone"

### 🕹️ Controls

| Action | Control |
|--------|---------|
| Aim & Shoot | Drag mouse from bottom area |
| Reset Game | Click RESET button |
| Exit | Close window or `Ctrl+C` |

### 💎 Power-ups

| Icon | Name | Effect |
|------|------|--------|
| +1 | Extra Ball | Adds one ball to your inventory |
| 🔥 | Fire Ball | Deals 2x damage to bricks |
| ⟋ | Pierce Shot | Passes through up to 3 bricks |

### 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/armin-naeini/swipe-brick-breaker.git
cd swipe-brick-breaker
```

2. **Install dependencies**
```bash
pip install pygame
```

3. **Run the game**
```bash
python main.py
```

### 📁 Project Structure

```
swipe-brick-breaker/
├── main.py          # Main game file
├── README.md        # Documentation
└── LICENSE          # MIT License
```

### 🎯 Game Mechanics

- **Brick Values**: Start from 1 and increase progressively
- **Row Generation**: 7 column grid with random gaps (40-75% fill rate)
- **Turn System**: Each completed throw = 1 turn + 1 extra ball
- **Scoring**: 10 points × brick value when destroyed
- **Combo System**: Rapid hits increase score multiplier

### 🔧 Requirements

- Python 3.8 or higher
- Pygame 2.0 or higher
- 600x850 screen resolution support

### 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

### 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- Inspired by BBTAN and similar mobile games
- Built with Pygame community
- Special thanks to all contributors

---

# فارسی

## 📖 درباره پروژه

Swipe Brick Breaker یک نسخه مدرن از بازی‌های آجرشکن کلاسیک است که از بازی‌های موبایلی محبوب مانند BBTAN الهام گرفته شده. برخلاف آجرشکن‌های سنتی، این بازی عناصر استراتژیک را معرفی می‌کند که در آن آجرها پس از هر پرتاب به سمت پایین حرکت می‌کنند و چالشی فزاینده ایجاد می‌کنند.

### ✨ ویژگی‌ها

- **🎯 مکانیک کشیدن و رها کردن**: کنترل دقیق با کشیدن ماوس برای نشانه‌گیری
- **📊 سختی پیشرونده**: آجرها در هر مرحله قوی‌تر شده و به پایین حرکت می‌کنند
- **🎲 تولید تصادفی**: هر ردیف دارای فضاهای خالی و مقادیر متنوع است
- **💫 جلوه‌های بصری**: ذرات، لرزش صفحه، متن‌های شناور و انیمیشن‌های نرم
- **⚡ آیتم‌های ویژه**: توپ آتشین، شلیک نفوذی و توپ اضافی
- **🔄 گیم‌پلی بی‌نهایت**: تا جایی که می‌توانید زنده بمانید
- **🎨 رابط کاربری زیبا**: پس‌زمینه گرادیانت، افکت‌های درخشان و جلوه‌های بصری حرفه‌ای

### 🎮 نحوه بازی

1. **فاز ۱**: شروع با یک ردیف آجر (ارزش ۱)
2. **کشیدن برای شلیک**: از ناحیه پایین صفحه بکشید تا نشانه‌گیری کنید و رها کنید
3. **بازگشت توپ**: توپ پس از هر پرتاب در پایین صفحه متوقف می‌شود
4. **فاز ۲ به بعد**: پس از اولین پرتاب، آجرها پایین آمده و ردیف جدید قوی‌تر اضافه می‌شود
5. **جمع‌آوری آیتم‌ها**: آجرهای ویژه را بشکنید تا قدرت‌های خاص بگیرید
6. **بقا**: نگذارید آجرها به "منطقه مرگ" قرمز رنگ برسند

### 🕹️ کنترل‌ها

| عملکرد | کنترل |
|--------|-------|
| نشانه‌گیری و شلیک | کشیدن ماوس از ناحیه پایین |
| شروع مجدد | کلیک روی دکمه RESET |
| خروج | بستن پنجره یا `Ctrl+C` |

### 💎 آیتم‌های ویژه

| آیکون | نام | اثر |
|-------|-----|-----|
| +1 | توپ اضافی | یک توپ به موجودی اضافه می‌کند |
| 🔥 | توپ آتشین | آسیب ۲ برابر به آجرها |
| ⟋ | شلیک نفوذی | از ۳ آجر عبور می‌کند |

### 🚀 نصب و راه‌اندازی

1. **کلون کردن مخزن**
```bash
git clone https://github.com/armin-naeini/swipe-brick-breaker.git
cd swipe-brick-breaker
```

2. **نصب پیش‌نیازها**
```bash
pip install pygame
```

3. **اجرای بازی**
```bash
python main.py
```

### 📁 ساختار پروژه

```
swipe-brick-breaker/
├── main.py          # فایل اصلی بازی
├── README.md        # مستندات
└── LICENSE          # مجوز MIT
```

### 🎯 مکانیک‌های بازی

- **ارزش آجرها**: از ۱ شروع شده و به تدریج افزایش می‌یابد
- **تولید ردیف**: شبکه ۷ ستونی با فضاهای خالی تصادفی (۴۰-۷۵٪ پرشدگی)
- **سیستم نوبت**: هر پرتاب کامل = ۱ نوبت + ۱ توپ اضافی
- **امتیازدهی**: ۱۰ امتیاز × ارزش آجر هنگام نابودی
- **سیستم کمبو**: ضربات سریع امتیاز را چند برابر می‌کند

### 🔧 نیازمندی‌ها

- پایتون ۳.۸ یا بالاتر
- Pygame ۲.۰ یا بالاتر
- پشتیبانی از رزولوشن ۸۵۰×۶۰۰

### 🤝 مشارکت

مشارکت‌های شما خوش‌آمد است! می‌توانید:
- باگ‌ها را گزارش دهید
- ویژگی‌های جدید پیشنهاد دهید
- درخواست Pull Request ارسال کنید

## 📜 مجوز (License)

این پروژه تحت مجوز MIT منتشر شده است. این یعنی شما می‌توانید:

- ✅ از کد به صورت رایگان استفاده کنید
- ✅ کد را تغییر دهید و شخصی‌سازی کنید
- ✅ کد را در پروژه‌های تجاری استفاده کنید
- ✅ کد را توزیع مجدد کنید

تنها شرط این است که:
- 📋 نام کپی‌رایت و مجوز اصلی را حفظ کنید
- ⚠️ نرم‌افزار "همانطور که هست" ارائه می‌شود و هیچ ضمانتی ندارد

متن کامل مجوز در فایل [LICENSE](LICENSE) موجود است.

### 🙏 تقدیر و تشکر

- الهام گرفته از BBTAN و بازی‌های موبایلی مشابه
- ساخته شده با جامعه Pygame
- تشکر ویژه از تمام مشارکت‌کنندگان

---

<div align="center">

**🎮 Enjoy the Game! | از بازی لذت ببرید! 🎮**

Made with ❤️ using Python and Pygame

</div>