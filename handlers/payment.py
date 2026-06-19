# -*- coding: utf-8 -*-
"""💎 Coin sotib olish — Telegram Stars (XTR) orqali. Provayder token shart emas."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, Update
from telegram.ext import ContextTypes

import database as db
from config import COIN_PACKAGES, TEACHER_STARS


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


async def teacher_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🎓 O'qituvchi bo'lish — ma'lumot va Stars bilan sotib olish tugmasi."""
    user = update.effective_user
    db.ensure_user(user.id, user.first_name)
    if db.is_teacher(user.id):
        await update.message.reply_text("🎓 Siz allaqachon o'qituvchisiz! ✅")
        return
    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"🎓 O'qituvchi bo'lish — {TEACHER_STARS} ⭐",
                                  callback_data="buyteacher")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")],
        ]
    )
    await update.message.reply_text(
        "🎓 <b>O'qituvchi bo'lish</b>\n\n"
        "O'qituvchi o'z guruhiga botni qo'shib, o'quvchilarga vazifa beradi va "
        "ularning bajarganini kuzatadi.\n\n"
        f"💎 Narxi: <b>{TEACHER_STARS} ⭐</b> (Telegram Stars).\n"
        "Yoki adminga yozing — u bepul ham berishi mumkin.",
        parse_mode="HTML",
        reply_markup=kb,
    )


async def on_buy_teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchilik uchun Stars hisob-fakturasini yuboradi."""
    query = update.callback_query
    await query.answer()
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title="O'qituvchilik",
        description="English Learning Bot — o'qituvchi roli",
        payload="teacher",
        currency="XTR",
        prices=[LabeledPrice("O'qituvchilik", TEACHER_STARS)],
    )


async def on_pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To'lovdan oldingi tekshiruv — tasdiqlaymiz."""
    await update.pre_checkout_query.answer(ok=True)


async def on_successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To'lov muvaffaqiyatli — coin yoki o'qituvchilik beriladi."""
    payment = update.message.successful_payment
    payload = payment.invoice_payload
    user = update.effective_user
    db.ensure_user(user.id, user.first_name)

    if payload == "teacher":
        db.set_teacher(user.id, True)
        await update.message.reply_text(
            "🎓 <b>Tabriklaymiz! Endi siz o'qituvchisiz!</b>\n\n"
            "Tez orada o'z guruhingizga botni qo'shib, o'quvchilarga vazifa "
            "bera olasiz.\nRahmat! 🎉",
            parse_mode="HTML",
        )
        return

    if payload.startswith("coins:"):
        coins = int(payload.split(":", 1)[1])
        db.add_coins(user.id, coins)
        total = db.get_user(user.id)["coins"]
        await update.message.reply_text(
            f"✅ <b>To'lov qabul qilindi!</b>\n"
            f"+{coins} 🪙 qo'shildi. Jami: <b>{total}</b> 🪙\n\n"
            f"Rahmat! 🎉",
            parse_mode="HTML",
        )
