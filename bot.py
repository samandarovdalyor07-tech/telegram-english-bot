# -*- coding: utf-8 -*-
"""
🎓 English Learning Bot — ishga tushirish nuqtasi (entry point).

Kod modullarga ajratilgan:
    config.py        — sozlamalar, token, API kalit, konstantalar
    keyboards.py     — barcha tugmalar
    helpers.py       — yordamchi funksiyalar (safe_edit, baho, ...)
    database.py      — SQLite baza (XP, coin, streak, referral)
    questions.py     — 📝 test savollari
    content.py       — 📖 matn, ✍️ yozish, 📚 lug'at kontenti
    handlers/
        menu.py      — start, profil, reyting, navigatsiya
        test.py      — 📝 Test
        reading.py   — 📖 Matn
        writing.py   — ✍️ Yozish
        vocabulary.py— 📚 Lug'at

Ishga tushirish:
    1. .env faylga BOT_TOKEN=... yozing
    2. python bot.py
"""

import logging

from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    TypeHandler,
    filters,
)

import database as db
from config import BOT_TOKEN
from handlers.menu import (
    start,
    help_command,
    menu_command,
    profile_command,
    leaderboard_command,
    on_menu,
    on_activity,
    on_level,
    on_text,
)
from handlers.test import on_answer, on_retake
from handlers.reading import on_reading_translate, on_reading_next
from handlers.vocabulary import on_vocab_meaning, on_vocab_next
from handlers.writing import on_writing_hint, on_writing_skip
from handlers.certificate import certificate_command
from handlers.ai import ai_start
from handlers.payment import buy_command, on_buy, on_pre_checkout, on_successful_payment
from handlers.admin import (
    myid_command,
    stats_command,
    broadcast_command,
    give_command,
    ban_command,
    unban_command,
    block_banned,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    """Telegram'ning ko'k 'Menu' tugmasidagi buyruqlar ro'yxatini o'rnatadi."""
    await application.bot.set_my_commands(
        [
            BotCommand("start", "🚀 Botni boshlash"),
            BotCommand("menu", "🏠 Bosh menyu"),
            BotCommand("profile", "👤 Mening profilim"),
            BotCommand("leaderboard", "🏆 Reyting (TOP 10)"),
            BotCommand("certificate", "📜 Sertifikat olish"),
            BotCommand("ai", "🤖 AI Tutor bilan suhbat"),
            BotCommand("buy", "💎 Coin sotib olish"),
            BotCommand("help", "ℹ️ Yordam"),
        ]
    )


def build_application(token: str) -> Application:
    """Application'ni yaratadi va barcha handlerlarni ulaydi."""
    app = Application.builder().token(token).post_init(post_init).build()

    # Bloklangan foydalanuvchilarni hamma narsadan oldin to'samiz
    app.add_handler(TypeHandler(Update, block_banned), group=-1)

    # Buyruqlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("leaderboard", leaderboard_command))
    app.add_handler(CommandHandler("certificate", certificate_command))
    app.add_handler(CommandHandler("ai", ai_start))
    app.add_handler(CommandHandler("buy", buy_command))

    # 🛡 Admin
    app.add_handler(CommandHandler("myid", myid_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("give", give_command))
    app.add_handler(CommandHandler("ban", ban_command))
    app.add_handler(CommandHandler("unban", unban_command))

    # Menyu / navigatsiya
    app.add_handler(CallbackQueryHandler(on_menu, pattern=r"^menu$"))
    app.add_handler(CallbackQueryHandler(on_activity, pattern=r"^act:"))
    app.add_handler(CallbackQueryHandler(on_level, pattern=r"^lvl:"))

    # 📝 Test
    app.add_handler(CallbackQueryHandler(on_answer, pattern=r"^ans:"))
    app.add_handler(CallbackQueryHandler(on_retake, pattern=r"^retake$"))

    # 📖 Matn
    app.add_handler(CallbackQueryHandler(on_reading_translate, pattern=r"^rtrans$"))
    app.add_handler(CallbackQueryHandler(on_reading_next, pattern=r"^rnext$"))

    # 📚 Lug'at
    app.add_handler(CallbackQueryHandler(on_vocab_meaning, pattern=r"^vmean$"))
    app.add_handler(CallbackQueryHandler(on_vocab_next, pattern=r"^vnext$"))

    # ✍️ Yozish
    app.add_handler(CallbackQueryHandler(on_writing_hint, pattern=r"^whint$"))
    app.add_handler(CallbackQueryHandler(on_writing_skip, pattern=r"^wskip$"))

    # 💎 To'lov (Telegram Stars)
    app.add_handler(CallbackQueryHandler(on_buy, pattern=r"^buy:"))
    app.add_handler(PreCheckoutQueryHandler(on_pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, on_successful_payment))

    # Matnli xabarlar (oxirida — menyu tugmalari, AI, yozish)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    return app


def main():
    if not BOT_TOKEN:
        raise SystemExit(
            "❌ BOT_TOKEN topilmadi!\n"
            "   .env faylga BOT_TOKEN=<token> yozing.\n"
            "   Token olish: Telegram'da @BotFather → /newbot"
        )

    db.init_db()   # bazani tayyorlaymiz
    app = build_application(BOT_TOKEN)

    logger.info("🤖 Bot ishga tushdi. To'xtatish: Ctrl+C")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
