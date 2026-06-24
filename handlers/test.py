# -*- coding: utf-8 -*-
"""📝 Test bo'limi handlerlari."""

from telegram import Update
from telegram.ext import ContextTypes

import database as db
from config import XP_PER_CORRECT, COINS_PER_CORRECT, CERT_MIN_PERCENT
from helpers import build_test, grade_for, level_name, safe_edit
from keyboards import options_keyboard, home_keyboard, result_keyboard


async def start_test(query, context):
    level = context.user_data["level"]
    context.user_data["test"] = build_test(level)
    context.user_data["idx"] = 0
    context.user_data["score"] = 0
    if not context.user_data["test"]:
        await safe_edit(query, "⚠️ Savollar topilmadi.", reply_markup=home_keyboard())
        return
    await send_question(query, context)


async def send_question(query, context):
    data = context.user_data
    idx, total = data["idx"], len(data["test"])
    question = data["test"][idx]
    text = (
        f"📝 Savol {idx + 1}/{total}   ✅ {data['score']}\n\n"
        f"<b>{question['q']}</b>"
    )
    await safe_edit(
        query, text, parse_mode="HTML",
        reply_markup=options_keyboard(question["options"], question["correct"]),
    )


async def on_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = context.user_data
    if "test" not in data or data.get("idx", 0) >= len(data.get("test", [])):
        await query.answer()
        await safe_edit(query, "⏳ Sessiya tugagan. /start bosing.", reply_markup=home_keyboard())
        return
    # To'g'ri/noto'g'ri tugmaning o'zidan o'qiladi (ans:<1|0>:<indeks>),
    # shuning uchun ekrandagi tugma bilan baho doim mos keladi.
    parts = query.data.split(":")
    is_correct = len(parts) > 1 and parts[1] == "1"
    question = data["test"][data["idx"]]
    if is_correct:
        data["score"] += 1
        await query.answer("✅ To'g'ri!")
    else:
        correct = question["correct"]
        await query.answer(
            f"❌ Noto'g'ri. To'g'ri javob: {question['options'][correct]}", show_alert=True
        )
    data["idx"] += 1
    if data["idx"] >= len(data["test"]):
        await finish_test(query, context)
    else:
        await send_question(query, context)


async def finish_test(query, context):
    data = context.user_data
    score, total = data["score"], len(data["test"])
    percent = (score / total) * 100 if total else 0
    mark, label, emoji = grade_for(percent)

    # Mukofot: XP + coin + streak
    user_id = query.from_user.id
    xp, coins = score * XP_PER_CORRECT, score * COINS_PER_CORRECT
    db.ensure_user(user_id, query.from_user.first_name)
    db.add_xp(user_id, xp)
    db.add_coins(user_id, coins)
    streak = db.touch_streak(user_id)

    # Sertifikat uchun eng yaxshi natijani saqlaymiz
    db.update_certificate(user_id, data["level"], int(percent))

    text = (
        f"{emoji} <b>Test yakunlandi!</b>\n\n"
        f"📚 Daraja: {level_name(data['level'])}\n"
        f"✅ To'g'ri javoblar: {score} / {total}\n"
        f"📈 Natija: {percent:.0f}%\n"
        f"🎯 Bahoyingiz: <b>{mark} — {label}</b>\n\n"
        f"🏅 +{xp} XP, +{coins} 🪙   🔥 Streak: {streak} kun"
    )
    if int(percent) >= CERT_MIN_PERCENT:
        text += "\n\n📜 <b>Sertifikat ochildi!</b> Olish uchun /certificate"
    await safe_edit(query, text, parse_mode="HTML", reply_markup=result_keyboard())


async def on_retake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not context.user_data.get("level"):
        await safe_edit(query, "⏳ /start bosing.", reply_markup=home_keyboard())
        return
    context.user_data["mode"] = "test"
    await start_test(query, context)
