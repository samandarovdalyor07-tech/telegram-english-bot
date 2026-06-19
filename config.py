# -*- coding: utf-8 -*-
"""
⚙️ Sozlamalar — botning barcha kalitlari va o'zgaruvchilari shu yerda.

Maxfiy kalitlar (token, AI API kalit) KODDA emas, `.env` faylda saqlanadi.
`.env` git'ga tushmaydi (.gitignore), shuning uchun xavfsiz.
"""

import os

_BASE = os.path.dirname(os.path.abspath(__file__))


def _env(key: str, default: str = "") -> str:
    """Avval muhit o'zgaruvchisidan, bo'lmasa .env fayldan qiymat o'qiydi."""
    val = os.environ.get(key)
    if val:
        return val.strip()
    env_path = os.path.join(_BASE, ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == key:
                    return v.strip().strip('"').strip("'")
    return default


# ── Maxfiy kalitlar (.env fayldan) ──────────────────────────────────────────
BOT_TOKEN = _env("BOT_TOKEN")        # @BotFather bergan token
AI_API_KEY = _env("AI_API_KEY")      # AI tutor uchun (keyinroq ishlatiladi)

# Adminlar — .env da vergul bilan: ADMIN_IDS=123456,789012
ADMIN_IDS = [
    int(x) for x in _env("ADMIN_IDS").replace(" ", "").split(",") if x.isdigit()
]


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ── O'yin sozlamalari ───────────────────────────────────────────────────────
QUESTIONS_PER_TEST = 10              # bitta testdagi savollar soni
WRITE_CLOSE_RATIO = 0.85            # yozishda "deyarli to'g'ri" chegarasi (0..1)

XP_PER_CORRECT = 10                 # har bir to'g'ri javob uchun XP
COINS_PER_CORRECT = 2               # har bir to'g'ri javob uchun coin
REFERRAL_XP = 50                    # do'st taklif qilgani uchun XP
REFERRAL_COINS = 20                # do'st taklif qilgani uchun coin

# Sertifikat
CERT_MIN_PERCENT = 70               # sertifikat ochilishi uchun kamida shu % kerak
CERT_COST = 50                      # sertifikat narxi (coin)

# 🤖 AI tutor (OpenAI)
AI_MODEL = "gpt-4o-mini"            # arzon va tez (kuchliroq: "gpt-4o")
AI_COST_PER_MSG = 5                 # har bir AI savoli narxi (coin)
AI_HISTORY_LIMIT = 8               # AI eslab qoladigan oxirgi xabarlar soni

# 💎 Coin to'plamlari — Telegram Stars (⭐) orqali sotib olinadi
COIN_PACKAGES = [
    {"coins": 100, "stars": 15},
    {"coins": 300, "stars": 40},
    {"coins": 1000, "stars": 100},
]

# ── Bo'limlar (faoliyat turlari) ────────────────────────────────────────────
ACTIVITIES = {
    "test": "📝 Test",
    "read": "📖 Matn (Reading)",
    "write": "✍️ Yozish (Writing)",
    "vocab": "📚 Lug'at (Vocabulary)",
}

# Pastki doimiy menyu tugmasi -> faoliyat kaliti
REPLY_BUTTONS = {
    "📝 Test": "test",
    "📖 Matn": "read",
    "✍️ Yozish": "write",
    "📚 Lug'at": "vocab",
    "🏆 Reyting": "leaderboard",
    "👤 Profil": "profile",
    "📜 Sertifikat": "certificate",
    "🤖 AI Tutor": "ai",
    "💎 Coin": "buy",
    "🏠 Bosh menyu": "menu",
}
