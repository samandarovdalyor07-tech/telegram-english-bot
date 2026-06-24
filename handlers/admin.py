# -*- coding: utf-8 -*-
"""🛡 Admin buyruqlari: /myid, /stats, /broadcast, /give, /ban, /unban."""

import asyncio
import logging

from telegram import Update
from telegram.ext import ApplicationHandlerStop, ContextTypes

import database as db
from config import (
    is_admin,
    DEVELOPER_NAME,
    DEVELOPER_USERNAME,
    DEVELOPER_CONTACT,
    DEVELOPER_ABOUT,
)

logger = logging.getLogger(__name__)


async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Har kim: bot foydalanuvchilarining joriy sonini ko'rsatadi."""
    total = db.total_users()
    s = db.get_stats()
    await update.message.reply_text(
        "👥 <b>Bot foydalanuvchilari</b>\n\n"
        f"📊 Jami foydalanuvchilar: <b>{total}</b>\n"
        f"🔥 Bugun faol: <b>{s['active_today']}</b>",
        parse_mode="HTML",
    )


async def developer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Har kim: bot dasturchisi haqida ma'lumot."""
    lines = [
        "👨‍💻 <b>Bot dasturchisi</b>\n",
        f"📝 Ishlanma: {DEVELOPER_ABOUT}",
        f"🧑 Dasturchi: <b>{DEVELOPER_NAME}</b>",
    ]
    if DEVELOPER_USERNAME:
        uname = DEVELOPER_USERNAME.lstrip("@")
        lines.append(f"💬 Telegram: @{uname}")
    if DEVELOPER_CONTACT:
        lines.append(f"📧 Aloqa: {DEVELOPER_CONTACT}")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def myid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Har kim: o'z Telegram ID raqamini ko'rsatadi (admin qilish uchun kerak)."""
    user = update.effective_user
    await update.message.reply_text(
        f"🆔 Sizning Telegram ID: <code>{user.id}</code>\n\n"
        "Admin qilish uchun shu raqamni egasiga yuboring.",
        parse_mode="HTML",
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    s = db.get_stats()
    await update.message.reply_text(
        "📊 <b>Statistika</b>\n\n"
        f"👥 Jami foydalanuvchi: <b>{s['total']}</b>\n"
        f"🔥 Bugun faol: <b>{s['active_today']}</b>\n"
        f"⭐ Jami XP: <b>{s['xp']}</b>\n"
        f"🪙 Jami coin: <b>{s['coins']}</b>",
        parse_mode="HTML",
    )


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    text = update.message.text.partition(" ")[2].strip()
    if not text:
        await update.message.reply_text("Foydalanish: <code>/broadcast xabar matni</code>", parse_mode="HTML")
        return
    ids = db.all_user_ids()
    await update.message.reply_text(f"📢 {len(ids)} kishiga yuborilmoqda…")
    sent = failed = 0
    for uid in ids:
        try:
            await context.bot.send_message(uid, text)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)   # Telegram flood limitidan saqlanish
    await update.message.reply_text(f"✅ Yuborildi: {sent}   ❌ Xato: {failed}")


async def give_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    args = context.args
    if len(args) != 2 or not args[0].isdigit() or not args[1].lstrip("-").isdigit():
        await update.message.reply_text("Foydalanish: <code>/give user_id coin_soni</code>", parse_mode="HTML")
        return
    uid, amount = int(args[0]), int(args[1])
    if not db.get_user(uid):
        await update.message.reply_text("⚠️ Bunday foydalanuvchi topilmadi.")
        return
    db.add_coins(uid, amount)
    await update.message.reply_text(f"✅ {uid} ga {amount} 🪙 berildi.")
    try:
        await context.bot.send_message(uid, f"🎁 Sizga {amount} 🪙 coin sovg'a qilindi!")
    except Exception:
        pass


async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Foydalanish: <code>/ban user_id</code>", parse_mode="HTML")
        return
    uid = int(context.args[0])
    db.set_banned(uid, True)
    await update.message.reply_text(f"🚫 {uid} bloklandi.")


async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Foydalanish: <code>/unban user_id</code>", parse_mode="HTML")
        return
    uid = int(context.args[0])
    db.set_banned(uid, False)
    await update.message.reply_text(f"✅ {uid} blokdan chiqarildi.")


async def maketeacher_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: foydalanuvchiga bepul o'qituvchilik beradi."""
    if not is_admin(update.effective_user.id):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Foydalanish: <code>/maketeacher user_id</code>", parse_mode="HTML")
        return
    uid = int(context.args[0])
    if not db.get_user(uid):
        await update.message.reply_text("⚠️ Bunday foydalanuvchi topilmadi (avval botga /start bossin).")
        return
    db.set_teacher(uid, True)
    await update.message.reply_text(f"🎓 {uid} ga o'qituvchilik berildi.")
    try:
        await context.bot.send_message(uid, "🎓 Sizga o'qituvchilik berildi! Tabriklaymiz.")
    except Exception:
        pass


async def removeteacher_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: o'qituvchilikni olib qo'yadi."""
    if not is_admin(update.effective_user.id):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Foydalanish: <code>/removeteacher user_id</code>", parse_mode="HTML")
        return
    uid = int(context.args[0])
    db.set_teacher(uid, False)
    await update.message.reply_text(f"✅ {uid} dan o'qituvchilik olindi.")


async def block_banned(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bloklangan foydalanuvchilarning barcha so'rovlarini to'xtatadi (group=-1)."""
    user = update.effective_user
    if user and db.is_banned(user.id):
        raise ApplicationHandlerStop
