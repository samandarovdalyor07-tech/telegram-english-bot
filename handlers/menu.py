# -*- coding: utf-8 -*-
"""🏠 Asosiy menyu, profil, reyting va navigatsiya handlerlari."""

from telegram import Update
from telegram.ext import ContextTypes

import database as db
from config import ACTIVITIES, REPLY_BUTTONS, REFERRAL_XP, REFERRAL_COINS
from helpers import level_name, safe_edit
from keyboards import main_menu_keyboard, main_reply_keyboard, levels_keyboard

from handlers.test import start_test
from handlers.reading import start_reading
from handlers.writing import start_writing, check_writing_answer
from handlers.vocabulary import start_vocab
from handlers.certificate import certificate_command
from handlers.ai import ai_start, ai_message
from handlers.payment import buy_command
from handlers.wordclash import group_command


WELCOME = (
    "👋 Salom, {name}!\n\n"
    "Men <b>English Learning Bot</b> 🎓\n"
    "Men bilan ingliz tilini 4 xil usulda mashq qilasiz:\n\n"
    "📝 <b>Test</b> — daraja bo'yicha test va baho\n"
    "📖 <b>Matn</b> — ingliz matni + o'zbekcha tarjima\n"
    "✍️ <b>Yozish</b> — yozasiz, men tekshiraman\n"
    "📚 <b>Lug'at</b> — yangi so'zlarni yodlaysiz\n\n"
    "👇 Bo'limni tanlang:"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    user = update.effective_user

    # Referral: /start <taklif_qilgan_id> havolasi orqali kelganmi?
    ref = None
    if context.args and context.args[0].isdigit():
        ref = int(context.args[0])
        if ref == user.id:
            ref = None

    is_new = db.ensure_user(user.id, user.first_name, referred_by=ref)
    streak = db.touch_streak(user.id)

    # Yangi foydalanuvchi referral orqali kelgan bo'lsa — taklif qilganga bonus
    if is_new and ref and db.get_user(ref):
        db.add_xp(ref, REFERRAL_XP)
        db.add_coins(ref, REFERRAL_COINS)
        try:
            await context.bot.send_message(
                ref,
                f"🎉 Havolangiz orqali yangi do'st qo'shildi!\n"
                f"+{REFERRAL_XP} XP, +{REFERRAL_COINS} 🪙 oldingiz.",
            )
        except Exception:
            pass

    text = WELCOME.format(name=user.first_name)
    if streak > 1:
        text += f"\n\n🔥 Streak: {streak} kun ketma-ket!"
    await update.message.reply_text(
        text, parse_mode="HTML", reply_markup=main_reply_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ <b>Yo'riqnoma</b>\n\n"
        "/start — botni boshlash va menyu\n"
        "/menu — bosh menyuga qaytish\n"
        "/profile — profil: XP, coin, streak, reyting\n"
        "/leaderboard — TOP 10 reyting\n"
        "/help — yordam\n\n"
        "Menyudan bo'limni, so'ng darajangizni tanlang. Har to'g'ri javob uchun "
        "<b>XP</b> va <b>coin</b> 🪙 olasiz, har kuni kelsangiz <b>streak</b> 🔥 oshadi. "
        "Do'st taklif qilib ko'proq bonus oling (/profile da havola bor)!"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = None
    await update.message.reply_text(
        "🏠 <b>Bosh menyu</b>\nPastdagi tugmalardan bo'lim tanlang 👇",
        parse_mode="HTML",
        reply_markup=main_reply_keyboard(),
    )


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """👤 Foydalanuvchi profili: daraja, XP, coin, streak, reyting, referral havola."""
    user = update.effective_user
    db.ensure_user(user.id, user.first_name)
    u = db.get_user(user.id)
    rank = db.get_rank(user.id)
    refs = db.referral_count(user.id)
    lvl = level_name(u["level"]) if u["level"] else "—"
    invite = f"https://t.me/{context.bot.username}?start={user.id}"
    text = (
        f"👤 <b>{user.first_name}</b> — profil\n\n"
        f"📚 Daraja: {lvl}\n"
        f"⭐ XP: <b>{u['xp']}</b>\n"
        f"🪙 Coin: <b>{u['coins']}</b>\n"
        f"🔥 Streak: <b>{u['streak']}</b> kun\n"
        f"🏆 Reyting: <b>#{rank}</b>\n"
        f"👥 Takliflar: <b>{refs}</b> ta\n\n"
        f"🔗 Do'st taklif qiling — har biri uchun +{REFERRAL_XP} XP, +{REFERRAL_COINS} 🪙:\n"
        f"{invite}"
    )
    await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🏆 Eng ko'p XP to'plagan TOP 10 foydalanuvchi."""
    rows = db.leaderboard(10)
    medals = ["🥇", "🥈", "🥉"]
    lines = ["🏆 <b>Leaderboard — TOP 10</b>\n"]
    for i, r in enumerate(rows):
        place = medals[i] if i < 3 else f"{i + 1}."
        name = r["first_name"] or "Foydalanuvchi"
        lines.append(f"{place} {name} — {r['xp']} XP  🔥{r['streak']}")
    if not rows:
        lines.append("Hali hech kim yo'q — birinchi bo'ling!")
    rank = db.get_rank(update.effective_user.id)
    lines.append(f"\nSizning o'rningiz: <b>#{rank}</b>")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def on_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🏠 Bosh menyu tugmasi (inline)."""
    query = update.callback_query
    await query.answer()
    context.user_data["mode"] = None
    await safe_edit(query, "👇 Bo'limni tanlang:", reply_markup=main_menu_keyboard())


async def on_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bo'lim tanlangach, daraja so'raydi."""
    query = update.callback_query
    await query.answer()
    activity = query.data.split(":", 1)[1]
    name = ACTIVITIES.get(activity, activity)
    await safe_edit(
        query, f"{name}\n\n👇 Darajangizni tanlang:",
        reply_markup=levels_keyboard(activity),
    )


async def on_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daraja tanlangach, tegishli bo'limni boshlaydi."""
    query = update.callback_query
    await query.answer()
    _, activity, level = query.data.split(":", 2)
    context.user_data["level"] = level
    context.user_data["mode"] = activity
    db.ensure_user(query.from_user.id, query.from_user.first_name)
    db.set_level(query.from_user.id, level)

    if activity == "test":
        await start_test(query, context)
    elif activity == "read":
        await start_reading(query, context)
    elif activity == "write":
        await start_writing(query, context)
    elif activity == "vocab":
        await start_vocab(query, context)


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Matnli xabar: pastki menyu tugmasi yoki yozish javobi."""
    data = context.user_data
    text = (update.message.text or "").strip()

    # 1) Pastki doimiy menyu tugmalari
    if text in REPLY_BUTTONS:
        target = REPLY_BUTTONS[text]
        data["mode"] = None
        if target == "menu":
            await update.message.reply_text(
                "👇 Bo'limni tanlang:", reply_markup=main_menu_keyboard()
            )
        elif target == "profile":
            await profile_command(update, context)
        elif target == "leaderboard":
            await leaderboard_command(update, context)
        elif target == "certificate":
            await certificate_command(update, context)
        elif target == "ai":
            await ai_start(update, context)
        elif target == "buy":
            await buy_command(update, context)
        elif target == "wordclash":
            await group_command(update, context)
        else:
            name = ACTIVITIES.get(target, target)
            await update.message.reply_text(
                f"{name}\n\n👇 Darajangizni tanlang:",
                reply_markup=levels_keyboard(target),
            )
        return

    # 2) AI rejimida — Claude javob beradi
    if data.get("mode") == "ai":
        await ai_message(update, context)
        return

    # 3) Yozish rejimida — javobni tekshiramiz
    if data.get("mode") == "write" and "writing" in data:
        await check_writing_answer(update, context)
        return

    # 3) Aks holda — yo'naltiramiz
    await update.message.reply_text(
        "🤖 Pastdagi tugmalardan foydalaning yoki /menu bosing."
    )
