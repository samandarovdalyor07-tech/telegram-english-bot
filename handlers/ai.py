# -*- coding: utf-8 -*-
"""🤖 AI Tutor bo'limi handlerlari."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

import database as db
import ai_tutor
from config import AI_COST_PER_MSG, AI_HISTORY_LIMIT
from helpers import level_name
from keyboards import home_keyboard

logger = logging.getLogger(__name__)


async def ai_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI suhbat rejimini boshlaydi."""
    user = update.effective_user
    db.ensure_user(user.id, user.first_name)

    if not ai_tutor.is_configured():
        await update.message.reply_text(
            "🤖 <b>AI Tutor hali sozlanmagan.</b>\n\n"
            "Ishlashi uchun <code>.env</code> faylga AI API kalit qo'shilishi kerak "
            "(<code>AI_API_KEY=...</code>).",
            parse_mode="HTML",
        )
        return

    context.user_data["mode"] = "ai"
    context.user_data["ai_history"] = []
    coins = db.get_user(user.id)["coins"]
    await update.message.reply_text(
        "🤖 <b>AI Tutor</b> yoqildi!\n\n"
        "Menga ingliz tilida (yoki o'zbekcha) xohlagan narsangizni yozing — "
        "savol bering, gap tuzing, men tekshiraman va tushuntiraman.\n\n"
        f"💬 Har bir savol: <b>{AI_COST_PER_MSG}</b> 🪙   "
        f"(sizda {coins} 🪙 bor)\n"
        "Chiqish uchun pastdagi <b>🏠 Bosh menyu</b> tugmasini bosing.",
        parse_mode="HTML",
    )


async def ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI rejimida foydalanuvchi xabariga Claude javob beradi (coin sarflab)."""
    user = update.effective_user
    db.ensure_user(user.id, user.first_name)
    u = db.get_user(user.id)

    if (u["coins"] or 0) < AI_COST_PER_MSG:
        await update.message.reply_text(
            f"🪙 AI savoli {AI_COST_PER_MSG} coin turadi, sizda {u['coins']} 🪙 bor.\n"
            "💎 Coin sotib oling yoki test/yozish bilan ishlab toping.",
        )
        return

    history = context.user_data.get("ai_history", [])
    text = (update.message.text or "").strip()

    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        answer = await ai_tutor.ask_tutor(u["level"], history, text)
    except Exception as exc:  # API xatosi — coin yechilmaydi
        logger.exception("AI xatosi")
        await update.message.reply_text(
            "⚠️ AI javob bera olmadi (texnik xato). Coin yechilmadi, qaytadan urinib ko'ring."
        )
        return

    # Muvaffaqiyat — coin yechamiz va tarixni yangilaymiz
    db.spend_coins(user.id, AI_COST_PER_MSG)
    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": answer})
    # tarixni cheklash (oxirgi N juftlik)
    context.user_data["ai_history"] = history[-AI_HISTORY_LIMIT * 2:]

    remaining = db.get_user(user.id)["coins"]
    await update.message.reply_text(
        f"{answer}\n\n<i>(-{AI_COST_PER_MSG} 🪙 · qoldi {remaining})</i>",
        parse_mode="HTML",
    )
