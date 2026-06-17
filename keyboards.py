# -*- coding: utf-8 -*-
"""⌨️ Barcha tugmalar (inline va reply klaviaturalar) shu yerda."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from questions import get_levels
from config import ACTIVITIES


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Asosiy inline menyu — bo'lim tanlash."""
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"act:{key}")]
        for key, name in ACTIVITIES.items()
    ]
    return InlineKeyboardMarkup(buttons)


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Yozish maydoni tagidagi doimiy menyu."""
    return ReplyKeyboardMarkup(
        [
            ["📝 Test", "📖 Matn"],
            ["✍️ Yozish", "📚 Lug'at"],
            ["🏆 Reyting", "👤 Profil"],
            ["🤖 AI Tutor", "📜 Sertifikat"],
            ["💎 Coin", "🏠 Bosh menyu"],
        ],
        resize_keyboard=True,
        input_field_placeholder="Menyudan tanlang yoki javob yozing…",
    )


def levels_keyboard(activity: str) -> InlineKeyboardMarkup:
    """Tanlangan bo'lim uchun daraja tanlash."""
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"lvl:{activity}:{key}")]
        for key, name in get_levels().items()
    ]
    buttons.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="menu")])
    return InlineKeyboardMarkup(buttons)


def options_keyboard(options) -> InlineKeyboardMarkup:
    """Test savoli variantlari (A, B, C, D)."""
    labels = ["A", "B", "C", "D", "E", "F"]
    buttons = [
        [InlineKeyboardButton(f"{labels[i]}) {opt}", callback_data=f"ans:{i}")]
        for i, opt in enumerate(options)
    ]
    return InlineKeyboardMarkup(buttons)


def home_keyboard() -> InlineKeyboardMarkup:
    """Faqat asosiy menyuga qaytish tugmasi."""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")]]
    )


def reading_keyboard(show_translation: bool) -> InlineKeyboardMarkup:
    rows = []
    if not show_translation:
        rows.append([InlineKeyboardButton("🇺🇿 Tarjimani ko'rish", callback_data="rtrans")])
    rows.append([InlineKeyboardButton("➡️ Keyingi matn", callback_data="rnext")])
    rows.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")])
    return InlineKeyboardMarkup(rows)


def vocab_keyboard(show_meaning: bool) -> InlineKeyboardMarkup:
    rows = []
    if not show_meaning:
        rows.append([InlineKeyboardButton("🇺🇿 Tarjimasini ko'rish", callback_data="vmean")])
    rows.append([InlineKeyboardButton("➡️ Keyingi so'z", callback_data="vnext")])
    rows.append([InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")])
    return InlineKeyboardMarkup(rows)


def writing_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💡 Yordam", callback_data="whint"),
             InlineKeyboardButton("⏭ O'tkazib yuborish", callback_data="wskip")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")],
        ]
    )


def result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔁 Qayta ishlash", callback_data="retake")],
            [InlineKeyboardButton("🏠 Bosh menyu", callback_data="menu")],
        ]
    )
