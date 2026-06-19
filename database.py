# -*- coding: utf-8 -*-
"""
🗄️ Ma'lumotlar bazasi (SQLite) — botning poydevori.

Bu yerda har bir foydalanuvchining doimiy ma'lumotlari saqlanadi:
daraja, XP, coin, streak (ketma-ket kunlar), referral (kim taklif qilgan).
Bot o'chib qayta yonsa ham ma'lumot saqlanib qoladi.

Barcha kelajakdagi imkoniyatlar shu bazaga ulanadi:
  • XP / Streak / Leaderboard   → users jadvali
  • Coin tizimi                 → users.coins
  • Referral (do'st olib kel)   → users.referred_by
  • Premium / to'lov            → keyinchalik users.premium_until
  • AI tutor                    → coin sarflash orqali
"""

import os
import sqlite3
from datetime import date, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot.db")

_conn = None


def _connect():
    """Yagona ulanish (PTB asyncio'da bitta oqimda ishlaydi)."""
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
    return _conn


def init_db():
    """Jadvallarni yaratadi (agar yo'q bo'lsa)."""
    conn = _connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id      INTEGER PRIMARY KEY,
            first_name   TEXT,
            level        TEXT,
            xp           INTEGER NOT NULL DEFAULT 0,
            coins        INTEGER NOT NULL DEFAULT 0,
            streak       INTEGER NOT NULL DEFAULT 0,
            last_active  TEXT,
            referred_by  INTEGER,
            joined       TEXT
        )
        """
    )
    # Migratsiya: yangi ustunlarni qo'shamiz (eski bazalar uchun)
    _add_column(conn, "users", "cert_level", "TEXT")
    _add_column(conn, "users", "cert_percent", "INTEGER NOT NULL DEFAULT 0")
    _add_column(conn, "users", "banned", "INTEGER NOT NULL DEFAULT 0")
    conn.commit()


def _add_column(conn, table: str, column: str, decl: str):
    """Ustun mavjud bo'lmasa, jadvalga qo'shadi."""
    cols = [r["name"] for r in conn.execute(f"PRAGMA table_info({table})")]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


# --------------------------------------------------------------------------- #
# Foydalanuvchi
# --------------------------------------------------------------------------- #

def ensure_user(user_id: int, first_name: str = "", referred_by: int | None = None) -> bool:
    """Foydalanuvchini bazaga qo'shadi (yangi bo'lsa). Yangi yaratilgan bo'lsa True qaytaradi."""
    conn = _connect()
    row = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if row:
        # Ismni yangilab qo'yamiz
        if first_name:
            conn.execute("UPDATE users SET first_name = ? WHERE user_id = ?", (first_name, user_id))
            conn.commit()
        return False
    conn.execute(
        "INSERT INTO users (user_id, first_name, referred_by, joined) VALUES (?, ?, ?, ?)",
        (user_id, first_name, referred_by, date.today().isoformat()),
    )
    conn.commit()
    return True


def get_user(user_id: int) -> sqlite3.Row | None:
    conn = _connect()
    return conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()


def set_level(user_id: int, level: str):
    conn = _connect()
    conn.execute("UPDATE users SET level = ? WHERE user_id = ?", (level, user_id))
    conn.commit()


def update_certificate(user_id: int, level: str, percent: int):
    """Eng yaxshi test natijasini sertifikat uchun saqlaydi (oldingidan yuqori bo'lsa)."""
    conn = _connect()
    row = conn.execute("SELECT cert_percent FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if row and (row["cert_percent"] or 0) < percent:
        conn.execute(
            "UPDATE users SET cert_level = ?, cert_percent = ? WHERE user_id = ?",
            (level, percent, user_id),
        )
        conn.commit()


# --------------------------------------------------------------------------- #
# XP va Coin
# --------------------------------------------------------------------------- #

def add_xp(user_id: int, amount: int):
    conn = _connect()
    conn.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()


def add_coins(user_id: int, amount: int):
    conn = _connect()
    conn.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()


def spend_coins(user_id: int, amount: int) -> bool:
    """Coin yetarli bo'lsa sarflaydi va True qaytaradi, aks holda False."""
    conn = _connect()
    row = conn.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if not row or row["coins"] < amount:
        return False
    conn.execute("UPDATE users SET coins = coins - ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    return True


# --------------------------------------------------------------------------- #
# Streak (ketma-ket faol kunlar)
# --------------------------------------------------------------------------- #

def touch_streak(user_id: int) -> int:
    """Kunlik faollikni belgilaydi va streak'ni yangilaydi. Yangi streak qiymatini qaytaradi.

    - Bugun allaqachon faol bo'lsa  → o'zgarmaydi
    - Kecha faol bo'lgan bo'lsa      → streak + 1
    - Aks holda (uzilish)            → streak = 1
    """
    conn = _connect()
    row = conn.execute("SELECT last_active, streak FROM users WHERE user_id = ?", (user_id,)).fetchone()
    today = date.today()
    if not row:
        return 0

    last = row["last_active"]
    streak = row["streak"] or 0

    if last == today.isoformat():
        return streak  # bugun allaqachon hisoblangan

    if last == (today - timedelta(days=1)).isoformat():
        streak += 1
    else:
        streak = 1

    conn.execute(
        "UPDATE users SET streak = ?, last_active = ? WHERE user_id = ?",
        (streak, today.isoformat(), user_id),
    )
    conn.commit()
    return streak


# --------------------------------------------------------------------------- #
# Referral (do'st olib kel)
# --------------------------------------------------------------------------- #

def referral_count(user_id: int) -> int:
    conn = _connect()
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM users WHERE referred_by = ?", (user_id,)
    ).fetchone()
    return row["c"] if row else 0


# --------------------------------------------------------------------------- #
# Leaderboard / reyting
# --------------------------------------------------------------------------- #

def leaderboard(limit: int = 10):
    conn = _connect()
    return conn.execute(
        "SELECT user_id, first_name, xp, streak FROM users ORDER BY xp DESC, streak DESC LIMIT ?",
        (limit,),
    ).fetchall()


def get_rank(user_id: int) -> int:
    """Foydalanuvchining XP bo'yicha o'rni (1 dan boshlab)."""
    conn = _connect()
    row = conn.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if not row:
        return 0
    higher = conn.execute(
        "SELECT COUNT(*) AS c FROM users WHERE xp > ?", (row["xp"],)
    ).fetchone()["c"]
    return higher + 1


def total_users() -> int:
    conn = _connect()
    return conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]


# --------------------------------------------------------------------------- #
# Admin
# --------------------------------------------------------------------------- #

def all_user_ids():
    """Broadcast uchun barcha (bloklanmagan) foydalanuvchi ID lari."""
    conn = _connect()
    rows = conn.execute(
        "SELECT user_id FROM users WHERE banned = 0 OR banned IS NULL"
    ).fetchall()
    return [r["user_id"] for r in rows]


def get_stats() -> dict:
    """Umumiy statistika."""
    conn = _connect()
    today = date.today().isoformat()
    total = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
    active = conn.execute(
        "SELECT COUNT(*) AS c FROM users WHERE last_active = ?", (today,)
    ).fetchone()["c"]
    coins = conn.execute("SELECT COALESCE(SUM(coins), 0) AS s FROM users").fetchone()["s"]
    xp = conn.execute("SELECT COALESCE(SUM(xp), 0) AS s FROM users").fetchone()["s"]
    return {"total": total, "active_today": active, "coins": coins, "xp": xp}


def set_banned(user_id: int, value: bool):
    conn = _connect()
    conn.execute("UPDATE users SET banned = ? WHERE user_id = ?", (1 if value else 0, user_id))
    conn.commit()


def is_banned(user_id: int) -> bool:
    conn = _connect()
    row = conn.execute("SELECT banned FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return bool(row and row["banned"])
