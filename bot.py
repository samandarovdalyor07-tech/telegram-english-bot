# -*- coding: utf-8 -*-
"""
🎓 English Level Test Bot
Foydalanuvchi ingliz tili darajasini tanlaydi, shu darajaga mos
test savollariga javob beradi va oxirida baho oladi.

Ishga tushirish:
    1. BotFather'dan token oling
    2. .env faylga BOT_TOKEN=... yozing (yoki muhit o'zgaruvchisi sifatida bering)
    3. python bot.py
"""

import logging
import os
import random

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from questions import get_levels, get_questions

# --------------------------------------------------------------------------- #
# Sozlamalar
# --------------------------------------------------------------------------- #

# Har bir testdagi savollar soni (darajada shundan kam bo'lsa, hammasi olinadi)
QUESTIONS_PER_TEST = 10

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def _load_token() -> str:
    """BOT_TOKEN ni muhitdan yoki .env fayldan o'qiydi."""
    token = os.environ.get("BOT_TOKEN")
    if token:
        return token.strip()

    # python-dotenv bo'lmasa ham .env ni qo'lda o'qiymiz
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("BOT_TOKEN") and "=" in line:
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


# --------------------------------------------------------------------------- #
# Klaviaturalar
# --------------------------------------------------------------------------- #

def levels_keyboard() -> InlineKeyboardMarkup:
    """Daraja tanlash klaviaturasi."""
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"lvl:{key}")]
        for key, name in get_levels().items()
    ]
    return InlineKeyboardMarkup(buttons)


def options_keyboard(options) -> InlineKeyboardMarkup:
    """Joriy savol variantlari klaviaturasi (A, B, C, D)."""
    labels = ["A", "B", "C", "D", "E", "F"]
    buttons = [
        [InlineKeyboardButton(f"{labels[i]}) {opt}", callback_data=f"ans:{i}")]
        for i, opt in enumerate(options)
    ]
    return InlineKeyboardMarkup(buttons)


def result_keyboard() -> InlineKeyboardMarkup:
    """Test tugagandan keyingi klaviatura."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔁 Qayta ishlash", callback_data="retake")],
            [InlineKeyboardButton("📊 Boshqa daraja", callback_data="change")],
        ]
    )


# --------------------------------------------------------------------------- #
# Yordamchi funksiyalar
# --------------------------------------------------------------------------- #

def build_test(level: str):
    """Daraja uchun aralashtirilgan savollar to'plamini tayyorlaydi.

    Har bir savolning variantlari ham aralashtiriladi va to'g'ri javob
    indeksi qayta hisoblanadi.
    """
    questions = get_questions(level)
    random.shuffle(questions)
    questions = questions[:QUESTIONS_PER_TEST]

    prepared = []
    for item in questions:
        opts = item["options"][:]
        random.shuffle(opts)
        prepared.append(
            {
                "q": item["q"],
                "options": opts,
                "correct": opts.index(item["answer"]),
            }
        )
    return prepared


def grade_for(percent: float):
    """Foizga qarab (baho_raqami, izoh, emoji) qaytaradi."""
    if percent >= 90:
        return 5, "A'lo", "🏆"
    if percent >= 70:
        return 4, "Yaxshi", "👍"
    if percent >= 50:
        return 3, "Qoniqarli", "🙂"
    return 2, "Qoniqarsiz", "📚"


async def send_question(query, context: ContextTypes.DEFAULT_TYPE):
    """Joriy savolni tahrirlash orqali ko'rsatadi."""
    data = context.user_data
    idx = data["idx"]
    total = len(data["test"])
    question = data["test"][idx]

    text = (
        f"📝 Savol {idx + 1}/{total}\n"
        f"✅ To'g'ri javoblar: {data['score']}\n\n"
        f"<b>{question['q']}</b>"
    )
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=options_keyboard(question["options"]),
    )


async def finish_test(query, context: ContextTypes.DEFAULT_TYPE):
    """Test natijasini va bahoni ko'rsatadi."""
    data = context.user_data
    score = data["score"]
    total = len(data["test"])
    percent = (score / total) * 100 if total else 0
    mark, label, emoji = grade_for(percent)
    level_name = get_levels().get(data["level"], data["level"])

    text = (
        f"{emoji} <b>Test yakunlandi!</b>\n\n"
        f"📚 Daraja: {level_name}\n"
        f"✅ To'g'ri javoblar: {score} / {total}\n"
        f"📈 Natija: {percent:.0f}%\n\n"
        f"🎯 Bahoyingiz: <b>{mark} — {label}</b>"
    )
    await query.edit_message_text(
        text, parse_mode="HTML", reply_markup=result_keyboard()
    )


# --------------------------------------------------------------------------- #
# Handlerlar
# --------------------------------------------------------------------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start — salomlashish va daraja tanlash."""
    context.user_data.clear()
    user = update.effective_user
    text = (
        f"👋 Salom, {user.first_name}!\n\n"
        "Men <b>English Level Test</b> botiman. 🎓\n"
        "Ingliz tili darajangizni tanlang — men shu darajaga mos "
        "test savollarini beraman va oxirida baho qo'yaman.\n\n"
        "👇 Darajani tanlang:"
    )
    await update.message.reply_text(
        text, parse_mode="HTML", reply_markup=levels_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help — qisqa yo'riqnoma."""
    text = (
        "ℹ️ <b>Yo'riqnoma</b>\n\n"
        "/start — testni boshlash va daraja tanlash\n"
        "/help — ushbu yordam\n\n"
        "Daraja tanlagach, har bir savol uchun A/B/C/D variantlardan "
        "birini bosing. Oxirida natija va bahoyingizni ko'rasiz."
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def on_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daraja tanlanganda testni boshlaydi."""
    query = update.callback_query
    await query.answer()
    level = query.data.split(":", 1)[1]

    context.user_data["level"] = level
    context.user_data["test"] = build_test(level)
    context.user_data["idx"] = 0
    context.user_data["score"] = 0

    if not context.user_data["test"]:
        await query.edit_message_text("⚠️ Bu daraja uchun savollar topilmadi.")
        return

    await send_question(query, context)


async def on_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Javob bosilganda to'g'ri/noto'g'riligini tekshiradi."""
    query = update.callback_query
    data = context.user_data

    # Holat yo'qolgan bo'lsa (bot qayta ishga tushgan) — qayta boshlash
    if "test" not in data:
        await query.answer()
        await query.edit_message_text(
            "⏳ Sessiya tugagan. /start bosib qaytadan boshlang."
        )
        return

    idx = data["idx"]
    question = data["test"][idx]
    chosen = int(query.data.split(":", 1)[1])
    correct = question["correct"]

    if chosen == correct:
        data["score"] += 1
        await query.answer("✅ To'g'ri!")
    else:
        right = question["options"][correct]
        await query.answer(f"❌ Noto'g'ri. To'g'ri javob: {right}", show_alert=True)

    data["idx"] += 1
    if data["idx"] >= len(data["test"]):
        await finish_test(query, context)
    else:
        await send_question(query, context)


async def on_retake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xuddi shu daraja bo'yicha testni qaytadan boshlaydi."""
    query = update.callback_query
    await query.answer()
    level = context.user_data.get("level")
    if not level:
        await query.edit_message_text("⏳ /start bosib qaytadan boshlang.")
        return
    context.user_data["test"] = build_test(level)
    context.user_data["idx"] = 0
    context.user_data["score"] = 0
    await send_question(query, context)


async def on_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daraja tanlash menyusiga qaytaradi."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "👇 Darajani tanlang:", reply_markup=levels_keyboard()
    )


# --------------------------------------------------------------------------- #
# Ishga tushirish
# --------------------------------------------------------------------------- #

def main():
    token = _load_token()
    if not token:
        raise SystemExit(
            "❌ BOT_TOKEN topilmadi!\n"
            "   .env faylga BOT_TOKEN=<token> yozing yoki muhit "
            "o'zgaruvchisi sifatida bering.\n"
            "   Token olish: Telegram'da @BotFather → /newbot"
        )

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(on_level, pattern=r"^lvl:"))
    app.add_handler(CallbackQueryHandler(on_answer, pattern=r"^ans:"))
    app.add_handler(CallbackQueryHandler(on_retake, pattern=r"^retake$"))
    app.add_handler(CallbackQueryHandler(on_change, pattern=r"^change$"))

    logger.info("🤖 Bot ishga tushdi. To'xtatish: Ctrl+C")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
