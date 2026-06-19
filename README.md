# 🎓 English Learning Bot

Ingliz tilini o'rganish uchun ko'p funksiyali Telegram bot. O'yin elementlari,
AI tutor, to'lov, sertifikat, o'qituvchi paneli va guruh o'yini bilan — hammasi
**o'zbekcha tushuntirish** bilan.

> ✅ **Serverda 24/7 ishlaydi** (Hetzner VPS, systemd) · GitHub'da to'liq saqlangan.

---

## ✨ Imkoniyatlar

### 📚 O'quv bo'limlari (daraja bo'yicha, A1–C1)
| Bo'lim | Tavsifi |
|--------|---------|
| 📝 **Test** | A/B/C/D test, oxirida foiz va **5 balli baho** |
| 📖 **Matn (Reading)** | Ingliz matni + **o'zbekcha tarjima** |
| ✍️ **Yozish (Writing)** | O'zbekchadan inglizchaga yozasiz, bot tekshiradi |
| 📚 **Lug'at (Vocabulary)** | Yangi so'zlar — tarjima va misol bilan |

### 🏆 Geymifikatsiya (SQLite)
- **XP**, **coin**, **streak** (ketma-ket kunlar), **reyting** (leaderboard), **profil**
- 👥 **Referral** — do'st taklif qilsa bonus (`/profile` da havola)

### 🤖 AI Tutor
- Foydalanuvchi yozadi → **GPT (OpenAI)** o'qituvchi sifatida tekshiradi, tushuntiradi
- Coin bilan cheklangan

### 📜 Sertifikat
- Test ≥70% → chiroyli **PNG sertifikat** (ism, daraja, ball, sana)

### 💎 To'lov — Telegram Stars (⭐)
- Coin sotib olish va o'qituvchilik — **avtomatik**, kartasiz

### 🛡 Admin paneli
- `/stats` (statistika) · `/broadcast` (e'lon) · `/give` (coin sovg'a) · `/ban` `/unban` · `/maketeacher`

### 🎓 O'qituvchi + guruh nazorati
- O'qituvchilik: Stars bilan avtomatik yoki admin bepul beradi
- Guruhda `/assign` — vazifa beradi → o'quvchilar javob yozadi → **AI baholaydi** → `/report` hisobot

### ⚔️ Word Clash (guruh o'yini)
- Guruhda komandali o'yin: kapitanlar jamoa tuzadi, **3 raund** (🇬🇧→🇺🇿, 🇺🇿→🇬🇧, aralash), A/B/C/D, g'olib aniqlanadi

---

## 📋 Buyruqlar

**Foydalanuvchi:** `/start` `/menu` `/profile` `/leaderboard` `/certificate` `/ai` `/buy` `/teacher` `/help`
**Guruh:** `/group` `/wordclash` `/assign` `/report`
**Admin:** `/stats` `/broadcast` `/give` `/ban` `/unban` `/maketeacher` `/removeteacher`

---

## 🚀 O'rnatish

```bash
pip install -r requirements.txt       # kutubxonalar
copy .env.example .env                # so'ng .env ga token va kalitlarni yozing
python bot.py
```

`.env` faylida:
```
BOT_TOKEN=...          # @BotFather token (majburiy)
AI_API_KEY=...         # OpenAI kalit (AI tutor uchun)
ADMIN_IDS=123,456      # adminlar ID (vergul bilan)
```

## ☁️ Serverda 24/7 (deploy)
To'liq qo'llanma: [DEPLOY.md](DEPLOY.md). Qisqacha (VPS):
```bash
git clone https://github.com/samandarovdalyor07-tech/telegram-english-bot.git
cd telegram-english-bot
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
# .env yarating, so'ng systemd xizmati (english-bot.service)
```
Yangilash: `git pull && systemctl restart english-bot`

---

## 🧩 Tuzilma
```
bot.py            # ishga tushirish nuqtasi
config.py         # sozlamalar, token, API kalit, konstantalar
keyboards.py      # tugmalar
helpers.py        # yordamchilar (safe_edit, baho, ...)
database.py       # SQLite (XP, coin, streak, referral, vazifalar)
questions.py      # test savollari
content.py        # matn, yozish, lug'at
certificate.py    # sertifikat (Pillow PNG)
ai_tutor.py       # AI tutor + javob baholash (OpenAI)
handlers/
   menu, test, reading, writing, vocabulary,
   certificate, ai, payment, admin, teacher, wordclash
```

## ⚙️ Texnologiya
Python · `python-telegram-bot` 22.x · `openai` · `Pillow` · SQLite
