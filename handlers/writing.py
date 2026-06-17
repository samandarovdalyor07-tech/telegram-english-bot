# -*- coding: utf-8 -*-
"""✍️ Yozish (Writing) bo'limi handlerlari."""

import difflib
import random

from telegram import Update
from telegram.ext import ContextTypes

import database as db
from config import XP_PER_CORRECT, COINS_PER_CORRECT, WRITE_CLOSE_RATIO
from content import get_writing
from helpers import grade_for, level_name, normalize, safe_edit
from keyboards import home_keyboard, result_keyboard, writing_keyboard


async def start_writing(query, context):
    level = context.user_data["level"]
    tasks = get_writing(level)
    random.shuffle(tasks)
    context.user_data["writing"] = tasks
    context.user_data["widx"] = 0
    context.user_data["wcorrect"] = 0
    if not tasks:
        await safe_edit(query, "⚠️ Bu daraja uchun mashq yo'q.", reply_markup=home_keyboard())
        return
    await send_writing_task(query, context)


def writing_task_text(data) -> str:
    idx, total = data["widx"], len(data["writing"])
    task = data["writing"][idx]
    return (
        f"✍️ Yozish {idx + 1}/{total} — {level_name(data['level'])}\n\n"
        f"Quyidagi gapni <b>ingliz tiliga</b> tarjima qilib yozing 👇\n\n"
        f"🇺🇿 <b>{task['uz']}</b>\n\n"
        f"<i>(Javobni shu yerga yozib yuboring)</i>"
    )


async def send_writing_task(query, context):
    """Callback orqali (xabarni tahrirlab) yangi mashqni ko'rsatadi."""
    await safe_edit(
        query, writing_task_text(context.user_data),
        parse_mode="HTML", reply_markup=writing_keyboard(),
    )


async def check_writing_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi yozgan matnni qabul qilingan javoblar bilan solishtiradi."""
    data = context.user_data
    task = data["writing"][data["widx"]]
    user_answer = normalize(update.message.text)
    accepted = [normalize(a) for a in task["answers"]]

    best = max(
        (difflib.SequenceMatcher(None, user_answer, a).ratio() for a in accepted),
        default=0,
    )

    if user_answer in accepted:
        data["wcorrect"] += 1
        feedback = "✅ <b>To'g'ri! Barakalla!</b>"
    elif best >= WRITE_CLOSE_RATIO:
        data["wcorrect"] += 1
        feedback = (
            "🟡 <b>Deyarli to'g'ri!</b> Kichik xato bor.\n"
            f"✔️ To'g'ri varianti: <b>{task['answers'][0]}</b>"
        )
    else:
        feedback = (
            "❌ <b>Noto'g'ri.</b>\n"
            f"✔️ To'g'ri javob: <b>{task['answers'][0]}</b>"
        )

    await update.message.reply_text(feedback, parse_mode="HTML")
    await advance_writing(update.message, context)


async def advance_writing(message, context):
    """Keyingi mashqqa o'tadi yoki yakunlaydi. Yangi xabar yuboradi."""
    data = context.user_data
    data["widx"] += 1

    if data["widx"] >= len(data["writing"]):
        total = len(data["writing"])
        correct = data["wcorrect"]
        percent = (correct / total) * 100 if total else 0
        mark, label, emoji = grade_for(percent)

        # Mukofot (shaxsiy chatda chat_id == user_id)
        user_id = message.chat_id
        xp, coins = correct * XP_PER_CORRECT, correct * COINS_PER_CORRECT
        db.ensure_user(user_id)
        db.add_xp(user_id, xp)
        db.add_coins(user_id, coins)
        streak = db.touch_streak(user_id)

        await message.reply_text(
            f"{emoji} <b>Yozish mashqi tugadi!</b>\n\n"
            f"✅ To'g'ri: {correct} / {total}\n"
            f"📈 Natija: {percent:.0f}%\n"
            f"🎯 Baho: <b>{mark} — {label}</b>\n\n"
            f"🏅 +{xp} XP, +{coins} 🪙   🔥 Streak: {streak} kun",
            parse_mode="HTML",
            reply_markup=result_keyboard(),
        )
        data["mode"] = None
    else:
        await message.reply_text(
            writing_task_text(data), parse_mode="HTML", reply_markup=writing_keyboard()
        )


async def on_writing_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = context.user_data
    if "writing" not in data:
        await query.answer()
        return
    task = data["writing"][data["widx"]]
    hint = task.get("hint", "Yordam yo'q")
    await query.answer(f"💡 {hint}", show_alert=True)


async def on_writing_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = context.user_data
    if "writing" not in data:
        await safe_edit(query, "⏳ /start bosing.", reply_markup=home_keyboard())
        return
    task = data["writing"][data["widx"]]
    await safe_edit(
        query,
        f"✍️ Yozish {data['widx'] + 1}/{len(data['writing'])} — {level_name(data['level'])}\n\n"
        f"🇺🇿 <b>{task['uz']}</b>\n\n"
        f"⏭ O'tkazib yuborildi. To'g'ri javob: <b>{task['answers'][0]}</b>",
        parse_mode="HTML",
    )
    await advance_writing(query.message, context)
