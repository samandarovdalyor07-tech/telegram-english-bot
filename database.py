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
    _add_column(conn, "users", "teacher", "INTEGER NOT NULL DEFAULT 0")

    # O'qituvchi vazifalari va o'quvchi javoblari
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS assignments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id    INTEGER,
            teacher_id  INTEGER,
            task        TEXT,
            message_id  INTEGER,
            active      INTEGER NOT NULL DEFAULT 1,
            created     TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER,
            student_id    INTEGER,
            student_name  TEXT,
            answer        TEXT,
            score         INTEGER,
            created       TEXT,
            UNIQUE(assignment_id, student_id)
        )
        """
    )
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


# --------------------------------------------------------------------------- #
# O'qituvchi roli
# --------------------------------------------------------------------------- #

def set_teacher(user_id: int, value: bool):
    conn = _connect()
    conn.execute("UPDATE users SET teacher = ? WHERE user_id = ?", (1 if value else 0, user_id))
    conn.commit()


def is_teacher(user_id: int) -> bool:
    conn = _connect()
    row = conn.execute("SELECT teacher FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return bool(row and row["teacher"])


# --------------------------------------------------------------------------- #
# Vazifalar (o'qituvchi nazorati)
# --------------------------------------------------------------------------- #

def create_assignment(group_id: int, teacher_id: int, task: str, message_id: int) -> int:
    """Guruh uchun yangi vazifa yaratadi (eskisini nofaol qiladi)."""
    conn = _connect()
    conn.execute("UPDATE assignments SET active = 0 WHERE group_id = ? AND active = 1", (group_id,))
    cur = conn.execute(
        "INSERT INTO assignments (group_id, teacher_id, task, message_id, active, created) "
        "VALUES (?, ?, ?, ?, 1, ?)",
        (group_id, teacher_id, task, message_id, date.today().isoformat()),
    )
    conn.commit()
    return cur.lastrowid


def get_active_assignment(group_id: int):
    conn = _connect()
    return conn.execute(
        "SELECT * FROM assignments WHERE group_id = ? AND active = 1 ORDER BY id DESC LIMIT 1",
        (group_id,),
    ).fetchone()


def add_submission(assignment_id: int, student_id: int, name: str, answer: str, score):
    """O'quvchi javobini saqlaydi (qayta yuborsa, yangilaydi). score None bo'lishi mumkin."""
    conn = _connect()
    conn.execute(
        "INSERT OR REPLACE INTO submissions "
        "(assignment_id, student_id, student_name, answer, score, created) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (assignment_id, student_id, name, answer, score, date.today().isoformat()),
    )
    conn.commit()


def get_submissions(assignment_id: int):
    conn = _connect()
    return conn.execute(
        "SELECT student_name, score, answer FROM submissions "
        "WHERE assignment_id = ? ORDER BY (score IS NULL), score DESC",
        (assignment_id,),
    ).fetchall()
