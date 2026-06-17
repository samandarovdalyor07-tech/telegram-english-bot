# -*- coding: utf-8 -*-
"""🛠 Umumiy yordamchi funksiyalar (barcha bo'limlar ishlatadi)."""

import random
import re

from telegram.error import BadRequest

from questions import get_levels, get_questions
from config import QUESTIONS_PER_TEST


def normalize(text: str) -> str:
    """Yozishni solishtirish uchun matnni soddalashtiradi."""
    text = text.lower().strip()
    text = text.replace("’", "'").replace("`", "'")
    text = re.sub(r"[.,!?;:\"()]", "", text)   # tinish belgilarni olib tashlaymiz
    text = re.sub(r"\s+", " ", text)            # ortiqcha bo'sh joylar
    return text


def grade_for(percent: float):
    """Foizga qarab (baho, izoh, emoji)."""
    if percent >= 90:
        return 5, "A'lo", "🏆"
    if percent >= 70:
        return 4, "Yaxshi", "👍"
    if percent >= 50:
        return 3, "Qoniqarli", "🙂"
    return 2, "Qoniqarsiz", "📚"


def build_test(level: str):
    """Daraja uchun aralashtirilgan test to'plamini tayyorlaydi."""
    questions = get_questions(level)
    random.shuffle(questions)
    questions = questions[:QUESTIONS_PER_TEST]
    prepared = []
    for item in questions:
        opts = item["options"][:]
        random.shuffle(opts)
        prepared.append(
            {"q": item["q"], "options": opts, "correct": opts.index(item["answer"])}
        )
    return prepared


def level_name(level: str) -> str:
    return get_levels().get(level, level)


async def safe_edit(query, text, reply_markup=None, parse_mode="HTML"):
    """Xabarni tahrirlaydi. Agar xabar topilmasa (eski yoki o'chirilgan),
    o'rniga yangi xabar yuboradi. 'not modified' xatosini e'tiborsiz qoldiradi.
    Shu tufayli bot eski tugmalardan ham yiqilmaydi."""
    try:
        await query.edit_message_text(
            text, parse_mode=parse_mode, reply_markup=reply_markup
        )
    except BadRequest as exc:
        if "not modified" in str(exc).lower():
            return
        # Xabarni tahrirlab bo'lmadi — yangisini yuboramiz
        await query.message.reply_text(
            text, parse_mode=parse_mode, reply_markup=reply_markup
        )
