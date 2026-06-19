# -*- coding: utf-8 -*-
"""
👨‍🏫 O'qituvchi nazorati — guruhda vazifa berish, javoblarni AI bilan
tekshirish va hisobot.

Oqim:
  O'qituvchi guruhda /assign <vazifa> yozadi → bot vazifani e'lon qiladi
  → o'quvchilar o'sha xabarga REPLY qilib javob yozadi (qo'lda, matn)
  → AI har bir javobni baholaydi (0-100 + izoh)
  → o'qituvchi /report bilan kim qanday bajarganini ko'radi
  📷 Rasm tashlasa — qabul qilinmaydi, "qo'lda yozing" deydi
"""

import logging
from html import escape

from telegram import Update
from telegram.ext import ContextTypes

import database as db
import ai_tutor
from config import is_admin

logger = logging.getLogger(__name__)


def _can_teach(user_id: int) -> bool:
    return db.is_teacher(user_id) or is_admin(user_id)


async def assign_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi: guruhda yangi vazifa beradi."""
    chat = update.effective_chat
    user = update.effective_user
    if chat.type not in ("group", "supergroup"):
        await update.message.reply_text("📝 Vazifa faqat GURUHDA beriladi (botni guruhga qo'shing).")
        return
    if not _can_teach(user.id):
        await update.message.reply_text(
            "⛔ Bu buyruq faqat o'qituvchilar uchun.\n"
            "O'qituvchi bo'lish: botga lichkada /teacher yozing."
        )
        return
    task = update.message.text.partition(" ")[2].strip()
    if not task:
        await update.message.reply_text(
            "Foydalanish: <code>/assign vazifa matni</code>\n"
            "Masalan: <code>/assign Translate to English: Men har kuni kitob o'qiyman</code>",
            parse_mode="HTML",
        )
        return
    sent = await update.message.reply_text(
        f"📝 <b>Yangi vazifa</b>\n\n{escape(task)}\n\n"
        "✍️ Javob berish uchun <b>shu xabarga reply qilib</b>, javobingizni "
        "<b>qo'lda yozib</b> yuboring.\n"
        "📷 Rasm qabul qilinmaydi.",
        parse_mode="HTML",
    )
    db.create_assignment(chat.id, user.id, task, sent.message_id)


async def on_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guruhda vazifa xabariga reply qilingan javoblarni qabul qiladi."""
    msg = update.message
    if not msg or not msg.reply_to_message:
        return
    a = db.get_active_assignment(update.effective_chat.id)
    if not a or msg.reply_to_message.message_id != a["message_id"]:
        return   # faol vazifaga reply emas — e'tibor bermaymiz
    student = update.effective_user
    if student.id == a["teacher_id"]:
        return   # o'qituvchining o'zi

    if not msg.text:   # rasm, stiker, fayl va h.k.
        await msg.reply_text(
            "📷 Rasm yoki fayl qabul qilinmaydi.\n"
            "Iltimos, javobni <b>qo'lda yozib</b> yuboring.",
            parse_mode="HTML",
        )
        return

    answer = msg.text.strip()
    score, feedback = None, None
    if ai_tutor.is_configured():
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        try:
            score, feedback = await ai_tutor.grade_answer(a["task"], answer)
        except Exception:
            logger.exception("Baholash xatosi")

    db.add_submission(a["id"], student.id, student.first_name, answer, score)

    if score is None:
        await msg.reply_text("✅ Javobingiz qabul qilindi.")
    else:
        emoji = "🟢" if score >= 70 else ("🟡" if score >= 50 else "🔴")
        await msg.reply_text(
            f"{emoji} <b>{escape(student.first_name)}</b> — ball: <b>{score}</b>/100\n"
            f"💬 {escape(feedback)}",
            parse_mode="HTML",
        )


async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi: joriy vazifa bo'yicha hisobot."""
    chat = update.effective_chat
    user = update.effective_user
    if chat.type not in ("group", "supergroup"):
        await update.message.reply_text("📊 Hisobot faqat guruhda ko'riladi.")
        return
    if not _can_teach(user.id):
        await update.message.reply_text("⛔ Faqat o'qituvchilar uchun.")
        return
    a = db.get_active_assignment(chat.id)
    if not a:
        await update.message.reply_text("Faol vazifa yo'q. /assign bilan vazifa bering.")
        return
    subs = db.get_submissions(a["id"])
    if not subs:
        await update.message.reply_text("Hali hech kim javob bermadi. 🤷")
        return

    lines = [f"📊 <b>Hisobot</b>\n📝 Vazifa: {escape(a['task'][:60])}\n"]
    total = counted = 0
    for s in subs:
        sc = s["score"]
        if sc is not None:
            lines.append(f"• {escape(s['student_name'])}: <b>{sc}</b>/100")
            total += sc
            counted += 1
        else:
            lines.append(f"• {escape(s['student_name'])}: ✅ (baholanmagan)")
    lines.append(f"\n👥 Javob berganlar: <b>{len(subs)}</b>")
    if counted:
        lines.append(f"📈 O'rtacha ball: <b>{total // counted}</b>/100")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")
