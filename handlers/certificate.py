# -*- coding: utf-8 -*-
"""📜 Sertifikat bo'limi handleri."""

from datetime import date

from telegram import Update
from telegram.ext import ContextTypes

import database as db
from config import CERT_COST, CERT_MIN_PERCENT
from helpers import level_name
from certificate import make_certificate


def _clean_level(label: str) -> str:
    """Daraja nomidan boshidagi emojini olib tashlaydi (rasm uchun)."""
    parts = label.split(" ", 1)
    return parts[1] if len(parts) == 2 and not parts[0].isalnum() else label


async def certificate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shartlar bajarilsa, coin sarflab sertifikat rasmini yuboradi."""
    user = update.effective_user
    db.ensure_user(user.id, user.first_name)
    u = db.get_user(user.id)
    percent = u["cert_percent"] or 0

    # 1) Shart: testdan kamida CERT_MIN_PERCENT % to'plagan bo'lishi kerak
    if percent < CERT_MIN_PERCENT:
        await update.message.reply_text(
            f"📜 <b>Sertifikat</b>\n\n"
            f"Sertifikat olish uchun avval 📝 <b>Test</b>dan kamida "
            f"<b>{CERT_MIN_PERCENT}%</b> to'plang.\n"
            f"Eng yaxshi natijangiz: <b>{percent}%</b>.\n\n"
            f"Hoziroq test yechib ko'ring! 💪",
            parse_mode="HTML",
        )
        return

    # 2) Shart: coin yetarli bo'lishi kerak
    if (u["coins"] or 0) < CERT_COST:
        await update.message.reply_text(
            f"📜 <b>Sertifikat</b> narxi: <b>{CERT_COST}</b> 🪙\n"
            f"Sizda <b>{u['coins']}</b> 🪙 bor.\n\n"
            f"Ko'proq coin uchun test/yozish bajaring yoki "
            f"do'st taklif qiling (/profile).",
            parse_mode="HTML",
        )
        return

    # 3) Coin sarflab, sertifikat yuboramiz
    if not db.spend_coins(user.id, CERT_COST):
        await update.message.reply_text("🪙 Coin yetarli emas.")
        return

    lvl_full = level_name(u["cert_level"]) if u["cert_level"] else "English"
    lvl_clean = _clean_level(lvl_full)
    bio = make_certificate(user.first_name, lvl_clean, percent, date.today().isoformat())

    await update.message.reply_photo(
        photo=bio,
        caption=(
            f"🎉 Tabriklaymiz, <b>{user.first_name}</b>!\n"
            f"📜 <b>{lvl_clean}</b> darajasi bo'yicha sertifikatingiz tayyor "
            f"({percent}%).\n"
            f"💎 {CERT_COST} 🪙 sarflandi.\n\n"
            f"Do'stlaringizga ulashing! 🚀"
        ),
        parse_mode="HTML",
    )
