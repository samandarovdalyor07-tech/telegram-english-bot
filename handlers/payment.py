# -*- coding: utf-8 -*-
"""💎 Coin sotib olish — Telegram Stars (XTR) orqali. Provayder token shart emas."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, Update
from telegram.ext import ContextTypes

import database as db
from config import COIN_PACKAGES


async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Coin to'plamlarini tugmalar bilan ko'rsatadi."""
    buttons = [
        [InlineKeyboardButton(
            f"{p['coins']} 🪙  —  {p['stars']} ⭐",
            callback_data=f"buy:{i}",
        )]
        for i, p in enumerate(COIN_PACKAGES)
    ]
    buttons.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")])
    await update.message.reply_text(
        "💎 <b>Coin sotib olish</b>\n\n"
        "Coinlar AI Tutor va sertifikat uchun ishlatiladi.\n"
        "To'lov Telegram <b>Stars (⭐)</b> orqali — qulay va xavfsiz.\n\n"
        "👇 To'plamni tanlang:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def on_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tanlangan to'plam uchun Stars hisob-fakturasini yuboradi."""
    query = update.callback_query
    await query.answer()
    idx = int(query.data.split(":", 1)[1])
    if idx < 0 or idx >= len(COIN_PACKAGES):
        return
    pkg = COIN_PACKAGES[idx]
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title=f"{pkg['coins']} coin",
        description=f"English Learning Bot uchun {pkg['coins']} 🪙 coin",
        payload=f"coins:{pkg['coins']}",
        currency="XTR",                                  # Telegram Stars
        prices=[LabeledPrice(f"{pkg['coins']} coin", pkg["stars"])],
    )


async def on_pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To'lovdan oldingi tekshiruv — tasdiqlaymiz."""
    await update.pre_checkout_query.answer(ok=True)


async def on_successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To'lov muvaffaqiyatli — coinlarni hisobga qo'shamiz."""
    payment = update.message.successful_payment
    payload = payment.invoice_payload
    if not payload.startswith("coins:"):
        return
    coins = int(payload.split(":", 1)[1])
    user = update.effective_user
    db.ensure_user(user.id, user.first_name)
    db.add_coins(user.id, coins)
    total = db.get_user(user.id)["coins"]
    await update.message.reply_text(
        f"✅ <b>To'lov qabul qilindi!</b>\n"
        f"+{coins} 🪙 qo'shildi. Jami: <b>{total}</b> 🪙\n\n"
        f"Rahmat! 🎉",
        parse_mode="HTML",
    )
