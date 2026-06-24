# -*- coding: utf-8 -*-
"""
📖🎤 Guruhda ovozli o'qish + o'zaro (peer) baholash.

Oqim (faqat GURUHDA, o'qituvchi boshqaradi):
  1. O'qituvchi /read yozadi → hikoyani tanlaydi → bot hikoyani e'lon qiladi.
  2. O'quvchilar o'sha xabarga OVOZLI (voice) javob berib, hikoyani o'qiydi.
  3. O'qituvchi "✅ Baholashni boshlash" ni bosadi → o'zaro baholash ochiladi.
  4. O'quvchilar bir-biriga 1–5 ⭐ qo'yadi (o'ziga emas).
  5. O'qituvchi "📊 Natijalar" ni bosadi → baholar tablichkasini ko'radi va
     har bir o'quvchiga o'zining yakuniy ⭐ bahosini qo'yadi.
"""

from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

import database as db
from config import is_admin
from stories import get_story_pool


def _can_teach(user_id: int) -> bool:
    return db.is_teacher(user_id) or is_admin(user_id)


def _stars_row(prefix: str, reader_id: int) -> InlineKeyboardMarkup:
    """1–5 ⭐ tugmalari qatori. prefix: 'pg' (o'quvchi) yoki 'tg' (o'qituvchi)."""
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"{n}⭐", callback_data=f"rs:{prefix}:{reader_id}:{n}")
        for n in range(1, 6)
    ]])


def _control_kb() -> InlineKeyboardMarkup:
    """Hikoya xabaridagi o'qituvchi boshqaruv tugmalari."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Baholashni boshlash", callback_data="rs:grade")],
        [InlineKeyboardButton("📊 Natijalar / Tablichka", callback_data="rs:scores")],
        [InlineKeyboardButton("🛑 Sessiyani yakunlash", callback_data="rs:end")],
    ])


def _avg_str(avg, cnt) -> str:
    if not cnt:
        return "— (hali baho yo'q)"
    return f"{avg:.1f}⭐  ({cnt} ta baho)"


# --------------------------------------------------------------------------- #
# /read — sessiyani boshlash (hikoya tanlash)
# --------------------------------------------------------------------------- #

async def read_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    if chat.type not in ("group", "supergroup"):
        await update.message.reply_text(
            "📖 Ovozli o'qish faqat GURUHDA ishlaydi (botni guruhga qo'shing)."
        )
        return
    if not _can_teach(user.id):
        await update.message.reply_text(
            "⛔ Bu buyruq faqat o'qituvchilar uchun.\n"
            "O'qituvchi bo'lish: botga lichkada /teacher yozing."
        )
        return
    pool = get_story_pool()
    rows = [
        [InlineKeyboardButton(f"📖 {s['title']}", callback_data=f"rs:pick:{i}")]
        for i, s in enumerate(pool)
    ]
    await update.message.reply_text(
        "📚 <b>Hikoyani tanlang</b> — o'quvchilar uni ovozli o'qib berishadi:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(rows),
    )


# --------------------------------------------------------------------------- #
# Callback dispatcher (pattern ^rs:)
# --------------------------------------------------------------------------- #

async def on_reading_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    parts = query.data.split(":")
    action = parts[1]

    if action == "pick":
        await _on_pick(query, context, int(parts[2]))
    elif action == "grade":
        await _on_grade(query, context)
    elif action == "scores":
        await _on_scores(query, context)
    elif action == "pg":
        await _on_peer_grade(query, context, int(parts[2]), int(parts[3]))
    elif action == "tg":
        await _on_teacher_grade(query, context, int(parts[2]), int(parts[3]))
    elif action == "end":
        await _on_end(query, context)
    else:
        await query.answer()


async def _on_pick(query, context, idx: int):
    user = query.from_user
    if not _can_teach(user.id):
        await query.answer("⛔ Faqat o'qituvchi uchun.", show_alert=True)
        return
    pool = get_story_pool()
    if idx < 0 or idx >= len(pool):
        await query.answer("Hikoya topilmadi.", show_alert=True)
        return
    story = pool[idx]
    await query.answer()
    sent = await query.message.reply_text(
        f"📖 <b>{escape(story['title'])}</b>\n\n{escape(story['text'])}\n\n"
        "🎤 <b>O'quvchilar:</b> shu xabarga <b>OVOZLI (voice) javob</b> berib, "
        "hikoyani ingliz tilida o'qib bering!\n\n"
        "👨‍🏫 O'qituvchi: hamma o'qib bo'lgach, <b>Baholashni boshlash</b> ni bosing.",
        parse_mode="HTML",
        reply_markup=_control_kb(),
    )
    db.create_reading_session(query.message.chat_id, user.id, story["title"], sent.message_id)


async def _on_grade(query, context):
    chat_id = query.message.chat_id
    if not _can_teach(query.from_user.id):
        await query.answer("⛔ Faqat o'qituvchi boshlay oladi.", show_alert=True)
        return
    session = db.get_active_session(chat_id)
    if not session:
        await query.answer("Faol sessiya yo'q. /read bilan boshlang.", show_alert=True)
        return
    readers = db.get_readers(session["id"])
    if not readers:
        await query.answer("Hali hech kim ovozli o'qimadi. 🤷", show_alert=True)
        return
    db.set_session_phase(session["id"], "grading")
    await query.answer("Baholash ochildi ✅")
    await query.message.reply_text(
        "⭐ <b>O'zaro baholash boshlandi!</b>\n"
        "Har bir o'quvchining o'qishiga 1–5 ⭐ qo'ying "
        "(o'zingizni baholay olmaysiz).",
        parse_mode="HTML",
    )
    for r in readers:
        await query.message.reply_text(
            f"🎤 <b>{escape(r['student_name'])}</b> ning o'qishini baholang:",
            parse_mode="HTML",
            reply_markup=_stars_row("pg", r["id"]),
        )


async def _on_peer_grade(query, context, reader_id: int, stars: int):
    reader = db.get_reader(reader_id)
    if not reader:
        await query.answer("Topilmadi.", show_alert=True)
        return
    grader = query.from_user
    if grader.id == reader["student_id"]:
        await query.answer("❌ O'zingizni baholay olmaysiz.", show_alert=True)
        return
    if _can_teach(grader.id):
        await query.answer(
            "👨‍🏫 O'qituvchi bahosi 'Natijalar' bo'limida qo'yiladi.", show_alert=True
        )
        return
    db.add_peer_grade(reader_id, grader.id, stars)
    avg, cnt = db.peer_summary(reader_id)
    await query.answer(f"✅ {stars}⭐ qabul qilindi!")
    try:
        await query.edit_message_text(
            f"🎤 <b>{escape(reader['student_name'])}</b> ning o'qishini baholang:\n"
            f"📊 Hozircha: {_avg_str(avg, cnt)}",
            parse_mode="HTML",
            reply_markup=_stars_row("pg", reader_id),
        )
    except Exception:
        pass


async def _on_scores(query, context):
    chat_id = query.message.chat_id
    if not _can_teach(query.from_user.id):
        await query.answer("⛔ Faqat o'qituvchi uchun.", show_alert=True)
        return
    session = db.get_active_session(chat_id)
    if not session:
        await query.answer("Faol sessiya yo'q.", show_alert=True)
        return
    readers = db.get_readers(session["id"])
    if not readers:
        await query.answer("Hali hech kim o'qimadi.", show_alert=True)
        return
    await query.answer()

    lines = [f"📊 <b>Baholar tablichkasi</b>\n📖 {escape(session['story_title'])}\n"]
    for r in readers:
        avg, cnt = db.peer_summary(r["id"])
        t = f"{r['teacher_stars']}⭐" if r["teacher_stars"] else "—"
        lines.append(
            f"• <b>{escape(r['student_name'])}</b>\n"
            f"   👥 O'quvchilar: {_avg_str(avg, cnt)}\n"
            f"   👨‍🏫 O'qituvchi: {t}"
        )
    await query.message.reply_text("\n".join(lines), parse_mode="HTML")

    # O'qituvchi har bir o'quvchiga yakuniy baho qo'yishi uchun tugmalar
    await query.message.reply_text(
        "👨‍🏫 <b>Endi o'zingiz baho qo'ying:</b>", parse_mode="HTML"
    )
    for r in readers:
        await query.message.reply_text(
            f"👨‍🏫 <b>{escape(r['student_name'])}</b> ga baho:",
            parse_mode="HTML",
            reply_markup=_stars_row("tg", r["id"]),
        )


async def _on_teacher_grade(query, context, reader_id: int, stars: int):
    if not _can_teach(query.from_user.id):
        await query.answer("⛔ Faqat o'qituvchi baho qo'yadi.", show_alert=True)
        return
    reader = db.get_reader(reader_id)
    if not reader:
        await query.answer("Topilmadi.", show_alert=True)
        return
    db.set_teacher_stars(reader_id, stars)
    avg, cnt = db.peer_summary(reader_id)
    await query.answer(f"✅ {stars}⭐ qo'yildi!")
    try:
        await query.edit_message_text(
            f"👨‍🏫 <b>{escape(reader['student_name'])}</b> — yakuniy baho: <b>{stars}⭐</b>\n"
            f"👥 O'quvchilar bahosi: {_avg_str(avg, cnt)}",
            parse_mode="HTML",
        )
    except Exception:
        pass


async def _on_end(query, context):
    chat_id = query.message.chat_id
    if not _can_teach(query.from_user.id):
        await query.answer("⛔ Faqat o'qituvchi yakunlaydi.", show_alert=True)
        return
    session = db.get_active_session(chat_id)
    if session:
        db.end_session(session["id"])
    await query.answer("Sessiya yakunlandi 🛑")
    await query.message.reply_text("🛑 <b>O'qish sessiyasi yakunlandi.</b>", parse_mode="HTML")


# --------------------------------------------------------------------------- #
# Ovozli javob — o'quvchi hikoyani o'qib yubordi
# --------------------------------------------------------------------------- #

async def on_voice_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sessiya xabariga ovozli (voice/video_note) reply — o'quvchi o'qidi."""
    msg = update.message
    if not msg or not msg.reply_to_message:
        return
    session = db.get_active_session(update.effective_chat.id)
    if not session or session["phase"] != "reading":
        return
    if msg.reply_to_message.message_id != session["message_id"]:
        return
    student = update.effective_user
    if student.id == session["teacher_id"]:
        return
    db.add_reader(session["id"], student.id, student.first_name)
    count = len(db.get_readers(session["id"]))
    await msg.reply_text(
        f"✅ <b>{escape(student.first_name)}</b> o'qib bo'ldi! "
        f"(jami {count} ta o'quvchi)",
        parse_mode="HTML",
    )
