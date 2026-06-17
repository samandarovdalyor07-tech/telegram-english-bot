# 🎓 English Level Test Bot

Ingliz tili darajangizni tanlab, shu darajaga mos test savollariga javob
beradigan va oxirida **baho qo'yadigan** Telegram bot.

## ✨ Imkoniyatlar

- 5 ta daraja: **Beginner (A1), Elementary (A2), Intermediate (B1),
  Upper-Intermediate (B2), Advanced (C1)**
- Har bir daraja uchun alohida savollar bazasi
- Test (A/B/C/D) ko'rinishidagi savollar
- Savollar va variantlar har safar aralashtiriladi
- Har bir javobdan keyin **to'g'ri/noto'g'ri** ko'rsatiladi
- Oxirida foiz va **5 balli baho** (A'lo / Yaxshi / Qoniqarli / Qoniqarsiz)
- Testni qayta ishlash yoki boshqa daraja tanlash tugmalari

## 🚀 O'rnatish

```bash
# 1. Kerakli kutubxonani o'rnatish
pip install -r requirements.txt

# 2. Token sozlash
#    .env.example faylidan nusxa olib, .env deb saqlang
#    va ichiga BotFather'dan olgan tokeningizni yozing
#    (Windows PowerShell):
copy .env.example .env

# 3. Botni ishga tushirish
python bot.py
```

## 🔑 Token qayerdan olinadi?

1. Telegramda [@BotFather](https://t.me/BotFather) ni oching
2. `/newbot` buyrug'ini yuboring
3. Bot nomi va username'ini bering
4. Berilgan tokenni `.env` fayldagi `BOT_TOKEN=` ga qo'ying

## 💬 Buyruqlar

| Buyruq | Vazifasi |
|--------|----------|
| `/start` | Testni boshlash va daraja tanlash |
| `/help`  | Qisqa yo'riqnoma |

## 🧩 Tuzilma

```
bot.py            # Asosiy bot mantiqi (handlerlar, klaviaturalar)
questions.py      # Daraja bo'yicha savollar bazasi
requirements.txt  # Bog'liqliklar
.env.example      # Token namunasi
```

## ➕ Yangi savol qo'shish

`questions.py` faylidagi kerakli daraja ro'yxatiga quyidagi formatda
yangi savol qo'shing:

```python
{
    "q": "Savol matni",
    "options": ["A", "B", "C", "D"],
    "answer": "To'g'ri variant matni",   # options ichidan bittasi
}
```

## ⚙️ Sozlamalar

- Bir testdagi savollar sonini `bot.py` dagi `QUESTIONS_PER_TEST` orqali
  o'zgartirish mumkin (standart: 10).
- Baho mezonlari `bot.py` dagi `grade_for()` funksiyasida.
