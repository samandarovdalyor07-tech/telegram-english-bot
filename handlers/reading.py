# -*- coding: utf-8 -*-
"""📖 Matn (Reading) bo'limi handlerlari."""

import random

from telegram import Update
from telegram.ext import ContextTypes

from content import get_reading
from helpers import level_name, safe_edit
from keyboards import home_keyboard, reading_keyboard


async def start_reading(query, context):
    level = context.user_data["level"]
    texts = get_reading(level)
    random.shuffle(texts)
    context.user_data["reading"] = texts
    context.user_data["ridx"] = 0
    if not texts:
        await safe_edit(query, "⚠️ Bu daraja uchun matn yo'q.", reply_markup=home_keyboard())
        return
    await show_reading(query, context, show_translation=False)


async def show_reading(query, context, show_translation: bool):
    data = context.user_data
    idx, total = data["ridx"], len(data["reading"])
    item = data["reading"][idx]
    text = (
        f"📖 Matn {idx + 1}/{total} — {level_name(data['level'])}\n\n"
        f"<b>{item['title']}</b>\n\n{item['text']}"
    )
    if show_translation:
        text += f"\n\n🇺🇿 <b>Tarjima:</b>\n{item['uz']}"
    await safe_edit(
        query, text, parse_mode="HTML",
        reply_markup=reading_keyboard(show_translation),
    )


async def on_reading_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if "reading" not in context.user_data:
        await safe_edit(query, "⏳ /start bosing.", reply_markup=home_keyboard())
        return
    await show_reading(query, context, show_translation=True)


async def on_reading_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = context.user_data
    if "reading" not in data:
        await safe_edit(query, "⏳ /start bosing.", reply_markup=home_keyboard())
        return
    data["ridx"] = (data["ridx"] + 1) % len(data["reading"])
    await show_reading(query, context, show_translation=False)
