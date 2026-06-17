# -*- coding: utf-8 -*-
"""📚 Lug'at (Vocabulary) bo'limi handlerlari."""

import random

from telegram import Update
from telegram.ext import ContextTypes

from content import get_vocabulary
from helpers import level_name, safe_edit
from keyboards import home_keyboard, vocab_keyboard


async def start_vocab(query, context):
    level = context.user_data["level"]
    words = get_vocabulary(level)
    random.shuffle(words)
    context.user_data["vocab"] = words
    context.user_data["vidx"] = 0
    if not words:
        await safe_edit(query, "⚠️ Bu daraja uchun so'zlar yo'q.", reply_markup=home_keyboard())
        return
    await show_vocab(query, context, show_meaning=False)


async def show_vocab(query, context, show_meaning: bool):
    data = context.user_data
    idx, total = data["vidx"], len(data["vocab"])
    w = data["vocab"][idx]
    text = (
        f"📚 So'z {idx + 1}/{total} — {level_name(data['level'])}\n\n"
        f"🔤 <b>{w['word']}</b>\n"
        f"📝 <i>{w['example']}</i>"
    )
    if show_meaning:
        text += (
            f"\n\n🇺🇿 <b>{w['uz']}</b>\n"
            f"📝 {w['example_uz']}"
        )
    await safe_edit(
        query, text, parse_mode="HTML",
        reply_markup=vocab_keyboard(show_meaning),
    )


async def on_vocab_meaning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if "vocab" not in context.user_data:
        await safe_edit(query, "⏳ /start bosing.", reply_markup=home_keyboard())
        return
    await show_vocab(query, context, show_meaning=True)


async def on_vocab_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = context.user_data
    if "vocab" not in data:
        await safe_edit(query, "⏳ /start bosing.", reply_markup=home_keyboard())
        return
    data["vidx"] = (data["vidx"] + 1) % len(data["vocab"])
    await show_vocab(query, context, show_meaning=False)
