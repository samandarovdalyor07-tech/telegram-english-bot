# -*- coding: utf-8 -*-
"""
⚔️ WORD CLASH — guruhда komandali ingliz tili o'yini.

Oqim:
  /wordclash (guruhда) → lobby (qo'shilish) → boshlovchi "Boshlash" bosadi
  → kapitanlar (2 kishi) navbatма-navbat jamoa tuzadi (draft)
  → 3 raund (🇬🇧→🇺🇿, 🇺🇿→🇬🇧, aralash), har raundда A/B/C/D savollar
  → birinchi to'g'ri bosgan jamoaга ball → g'olib aniqlanadi
"""

import random
from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from content import get_vocabulary
from questions import get_levels

MIN_PLAYERS = 2
ROUND_QUESTIONS = 3
ROUND_NAMES = [
    "🇬🇧 → 🇺🇿  (1-raund)",
    "🇺🇿 → 🇬🇧  (2-raund)",
    "🔀 Aralash  (final)",
]


# --------------------------------------------------------------------------- #
# Savollar (lug'atдан)
# --------------------------------------------------------------------------- #

def _all_words():
    words = []
    for lvl in get_levels():
        words += get_vocabulary(lvl)
    return words


def _make_question(words, mode):
    """mode: 'en2uz' yoki 'uz2en'."""
    w = random.choice(words)
    others = random.sample([x for x in words if x["word"] != w["word"]], 3)
    if mode == "en2uz":
        text = f"<b>{escape(w['word'])}</b> — o'zbekchasi qaysi?"
        correct = w["uz"]
        opts = [correct] + [o["uz"] for o in others]
    else:
        text = f"<b>{escape(w['uz'])}</b> — inglizchasi qaysi?"
        correct = w["word"]
        opts = [correct] + [o["word"] for o in others]
    random.shuffle(opts)
    return {"q": text, "options": opts, "correct": opts.index(correct)}


def _build_questions():
    words = _all_words()
    qs = []
    for _ in range(ROUND_QUESTIONS):
        qs.append(_make_question(words, "en2uz"))
    for _ in range(ROUND_QUESTIONS):
        qs.append(_make_question(words, "uz2en"))
    for _ in range(ROUND_QUESTIONS):
        qs.append(_make_question(words, random.choice(["en2uz", "uz2en"])))
    return qs


# --------------------------------------------------------------------------- #
# Klaviaturalar
# --------------------------------------------------------------------------- #

def _lobby_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✋ Qo'shilaman", callback_data="wc:join")],
        [InlineKeyboardButton("▶️ Boshlash", callback_data="wc:start")],
    ])


def _lobby_text(g):
    names = "\n".join(f"• {escape(n)}" for n in g["players"].values()) or "—"
    return (
        "⚔️ <b>WORD CLASH</b> boshlanmoqda!\n\n"
        f"Qo'shilish uchun tugmani bosing. Kamida {MIN_PLAYERS} kishi kerak.\n\n"
        f"👥 O'yinchilar ({len(g['players'])}):\n{names}"
    )


# --------------------------------------------------------------------------- #
# Handlerlar
# --------------------------------------------------------------------------- #

async def wordclash_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type not in ("group", "supergroup"):
        await update.message.reply_text(
            "⚔️ <b>Word Clash</b> faqat GURUHDA o'ynaladi.\n"
            "Botni guruhingizga qo'shing va u yerда /wordclash yozing.\n"
            "(Qo'shish havolasi: /group)",
            parse_mode="HTML",
        )
        return
    g = context.chat_data.get("wc")
    if g and g["phase"] != "done":
        await update.message.reply_text("⚠️ Bu guruhda o'yin allaqachon ketmoqda.")
        return
    context.chat_data["wc"] = {
        "phase": "lobby",
        "players": {},
        "host": update.effective_user.id,
    }
    await update.message.reply_text(
        _lobby_text(context.chat_data["wc"]),
        parse_mode="HTML",
        reply_markup=_lobby_kb(),
    )


async def on_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    g = context.chat_data.get("wc")
    if not g or g["phase"] != "lobby":
        await query.answer("O'yin topilmadi yoki boshlangan.", show_alert=True)
        return
    u = query.from_user
    if u.id in g["players"]:
        await query.answer("Siz allaqachon ro'yxatdasiz.")
        return
    g["players"][u.id] = u.first_name
    await query.answer("Qo'shildingiz! ✅")
    await query.edit_message_text(_lobby_text(g), parse_mode="HTML", reply_markup=_lobby_kb())


async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    g = context.chat_data.get("wc")
    if not g or g["phase"] != "lobby":
        await query.answer("O'yin topilmadi.", show_alert=True)
        return
    if query.from_user.id != g["host"]:
        await query.answer("Faqat o'yinni boshlagan kishi boshlay oladi.", show_alert=True)
        return
    if len(g["players"]) < MIN_PLAYERS:
        await query.answer(f"Kamida {MIN_PLAYERS} kishi kerak.", show_alert=True)
        return
    await query.answer()

    ids = list(g["players"].keys())
    random.shuffle(ids)
    cap1, cap2 = ids[0], ids[1]
    g["captains"] = [cap1, cap2]
    g["teams"] = {cap1: [cap1], cap2: [cap2]}
    g["team_of"] = {cap1: cap1, cap2: cap2}
    g["scores"] = {cap1: 0, cap2: 0}
    g["pool"] = ids[2:]

    if g["pool"]:
        g["phase"] = "draft"
        g["draft_turn"] = cap1
        await _show_draft(query, context)
    else:
        await _start_playing(query, context)


async def _show_draft(query, context):
    g = context.chat_data["wc"]
    cap = g["draft_turn"]
    buttons = [
        [InlineKeyboardButton(escape(g["players"][pid]), callback_data=f"wc:pick:{pid}")]
        for pid in g["pool"]
    ]
    await query.edit_message_text(
        "🧑‍✈️ <b>Jamoa tuzish</b>\n\n"
        f"Kapitan <b>{escape(g['players'][cap])}</b>, o'yinchini tanlang 👇",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def on_pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    g = context.chat_data.get("wc")
    if not g or g["phase"] != "draft":
        await query.answer()
        return
    if query.from_user.id != g["draft_turn"]:
        await query.answer("Hozir sizning navbatingiz emas.", show_alert=True)
        return
    pid = int(query.data.split(":")[2])
    if pid not in g["pool"]:
        await query.answer()
        return
    cap = g["draft_turn"]
    g["teams"][cap].append(pid)
    g["team_of"][pid] = cap
    g["pool"].remove(pid)
    await query.answer(f"{g['players'][pid]} tanlandi ✅")
    g["draft_turn"] = g["captains"][1] if cap == g["captains"][0] else g["captains"][0]
    if g["pool"]:
        await _show_draft(query, context)
    else:
        await _start_playing(query, context)


async def _start_playing(query, context):
    g = context.chat_data["wc"]
    g["phase"] = "playing"
    g["questions"] = _build_questions()
    g["qidx"] = 0
    g["answered"] = False
    c1, c2 = g["captains"]
    t1 = ", ".join(escape(g["players"][i]) for i in g["teams"][c1])
    t2 = ", ".join(escape(g["players"][i]) for i in g["teams"][c2])
    await query.edit_message_text(
        "⚔️ <b>Jamoalar tayyor!</b>\n\n"
        f"🔵 <b>{escape(g['players'][c1])}</b> jamoasi: {t1}\n"
        f"🔴 <b>{escape(g['players'][c2])}</b> jamoasi: {t2}\n\n"
        "O'yin boshlanmoqda… 🔥",
        parse_mode="HTML",
    )
    await _send_question(query.message, context)


async def _send_question(message, context):
    g = context.chat_data["wc"]
    idx = g["qidx"]
    q = g["questions"][idx]
    g["answered"] = False
    rnd = idx // ROUND_QUESTIONS
    labels = ["A", "B", "C", "D"]
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{labels[i]}) {opt}", callback_data=f"wc:ans:{i}")]
        for i, opt in enumerate(q["options"])
    ])
    c1, c2 = g["captains"]
    await message.reply_text(
        f"{ROUND_NAMES[rnd]}\n"
        f"❓ Savol {idx + 1}/{len(g['questions'])}   "
        f"🔵 {g['scores'][c1]} : {g['scores'][c2]} 🔴\n\n"
        f"{q['q']}\n\n"
        "<i>Birinchi to'g'ri bosgan ball oladi!</i>",
        parse_mode="HTML",
        reply_markup=kb,
    )


async def on_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    g = context.chat_data.get("wc")
    if not g or g["phase"] != "playing":
        await query.answer()
        return
    uid = query.from_user.id
    if uid not in g.get("team_of", {}):
        await query.answer("Siz bu o'yinda qatnashmaysiz.", show_alert=True)
        return
    if g["answered"]:
        await query.answer("Bu savolga allaqachon javob berildi.")
        return
    g["answered"] = True
    chosen = int(query.data.split(":")[2])
    q = g["questions"][g["qidx"]]
    team = g["team_of"][uid]
    name = escape(g["players"][uid])
    await query.answer()
    if chosen == q["correct"]:
        g["scores"][team] += 1
        result = f"✅ <b>{name}</b> to'g'ri javob berdi! +1 ball"
    else:
        result = (
            f"❌ <b>{name}</b> xato bosdi.\n"
            f"To'g'ri javob: <b>{escape(q['options'][q['correct']])}</b>"
        )
    await query.edit_message_text(f"{q['q']}\n\n{result}", parse_mode="HTML")
    g["qidx"] += 1
    if g["qidx"] >= len(g["questions"]):
        await _finish(query.message, context)
    else:
        await _send_question(query.message, context)


async def _finish(message, context):
    g = context.chat_data["wc"]
    g["phase"] = "done"
    c1, c2 = g["captains"]
    s1, s2 = g["scores"][c1], g["scores"][c2]
    if s1 > s2:
        winner = f"🔵 <b>{escape(g['players'][c1])}</b> jamoasi! 🏆"
    elif s2 > s1:
        winner = f"🔴 <b>{escape(g['players'][c2])}</b> jamoasi! 🏆"
    else:
        winner = "Durrang — teng! 🤝"
    await message.reply_text(
        "🏁 <b>WORD CLASH tugadi!</b>\n\n"
        f"🔵 {escape(g['players'][c1])}: <b>{s1}</b>\n"
        f"🔴 {escape(g['players'][c2])}: <b>{s2}</b>\n\n"
        f"G'olib: {winner}\n\n"
        "Yana o'ynash: /wordclash",
        parse_mode="HTML",
    )


async def group_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """➕ Botni guruhga qo'shish havolasi + Word Clash haqida."""
    url = f"https://t.me/{context.bot.username}?startgroup=true"
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("➕ Guruhga qo'shish", url=url)]])
    await update.message.reply_text(
        "⚔️ <b>Word Clash</b> — guruhда komandali ingliz tili o'yini!\n\n"
        "1. Botni guruhingizga qo'shing 👇\n"
        "2. Guruhда <b>/wordclash</b> yozing\n"
        "3. O'yinchilar qo'shiladi → kapitanlar jamoa tuzadi → 3 raund savol → g'olib!",
        parse_mode="HTML",
        reply_markup=kb,
    )
