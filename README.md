# 🎓 English Learning Bot (v2.0)

Ingliz tilini o'rganish uchun ko'p bo'limli Telegram bot. Menyu tugmalari
orqali bo'lim va darajangizni tanlaysiz, hammasi **o'zbekcha tushuntirish**
bilan beriladi.

## ✨ Bo'limlar

| Bo'lim | Tavsifi |
|--------|---------|
| 📝 **Test** | Daraja bo'yicha A/B/C/D test, oxirida foiz va **5 balli baho** |
| 📖 **Matn (Reading)** | Darajaga mos ingliz matni + **o'zbekcha tarjimasi** |
| ✍️ **Yozish (Writing)** | O'zbekcha gapni inglizchaga yozasiz, **bot tekshiradi** (kichik xatolarga ham moslashadi) |
| 📚 **Lug'at (Vocabulary)** | Yangi so'zlar — tarjima va misol gap bilan **flashcard** uslubida yodlash |

- 5 ta daraja: **Beginner (A1), Elementary (A2), Intermediate (B1),
  Upper-Intermediate (B2), Advanced (C1)**
- Savollar, matnlar, so'zlar va mashqlar har safar aralashtiriladi
- Har bir javobdan keyin darhol fikr-mulohaza (✅ / 🟡 / ❌)
- Istalgan paytda **🏠 Bosh menyu** tugmasi bilan qaytish

## 🚀 O'rnatish

```bash
# 1. Kerakli kutubxonani o'rnatish
pip install -r requirements.txt

# 2. Token sozlash: .env.example dan nusxa olib, .env deb saqlang
#    va ichiga BotFather tokeningizni yozing (Windows PowerShell):
copy .env.example .env

# 3. Botni ishga tushirish
python bot.py
```

## 🔑 Token qayerdan olinadi?

1. Telegramda [@BotFather](https://t.me/BotFather) ni oching
2. `/newbot` buyrug'ini yuboring → bot nomi va username'ini bering
3. Berilgan tokenni `.env` fayldagi `BOT_TOKEN=` ga qo'ying

## 💬 Buyruqlar

| Buyruq | Vazifasi |
|--------|----------|
| `/start` | Botni boshlash va bosh menyu |
| `/menu`  | Bosh menyuga qaytish |
| `/help`  | Qisqa yo'riqnoma |

## 🧩 Tuzilma

```
bot.py            # Asosiy bot mantiqi (menyu, handlerlar, klaviaturalar)
questions.py      # 📝 Test savollari bazasi (daraja bo'yicha)
content.py        # 📖 Matn, ✍️ Yozish, 📚 Lug'at kontenti (daraja bo'yicha)
requirements.txt  # Bog'liqliklar
.env.example      # Token namunasi
```

## ➕ Kontent qo'shish

**Test savoli** — `questions.py`:
```python
{"q": "Savol matni", "options": ["A", "B", "C", "D"], "answer": "To'g'ri variant"}
```

**Yangi so'z** — `content.py` → `VOCABULARY`:
```python
{"word": "apple", "uz": "olma", "example": "I eat an apple.", "example_uz": "Men olma yeyman."}
```

**Matn** — `content.py` → `READING`:
```python
{"title": "Sarlavha", "text": "English text...", "uz": "O'zbekcha tarjima..."}
```

**Yozish mashqi** — `content.py` → `WRITING`:
```python
{"uz": "O'zbekcha gap", "answers": ["accepted english", "variant 2"], "hint": "izoh"}
```

## ⚙️ Sozlamalar (`bot.py`)

- `QUESTIONS_PER_TEST` — bitta testdagi savollar soni (standart: 10)
- `WRITE_CLOSE_RATIO` — yozishda "deyarli to'g'ri" chegarasi (standart: 0.85)
- `grade_for()` — baho mezonlari
