# -*- coding: utf-8 -*-
"""
🤖 AI tutor — OpenAI (GPT) yordamida ingliz tili repetitori.

Foydalanuvchi yozadi, GPT o'qituvchi sifatida javob beradi: xatolarni
to'g'rilaydi, o'zbekcha tushuntiradi, mashq qildiradi. API kalit `.env` dagi
AI_API_KEY dan olinadi (config orqali).
"""

from openai import AsyncOpenAI

from config import AI_API_KEY, AI_MODEL

_client = None


def is_configured() -> bool:
    """AI API kalit o'rnatilganmi?"""
    return bool(AI_API_KEY)


def _get_client():
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=AI_API_KEY)
    return _client


SYSTEM_PROMPT = (
    "You are a friendly, patient English tutor for an Uzbek-speaking learner "
    "whose level is approximately {level}. "
    "Help them practice English: answer their questions, gently correct their "
    "mistakes (show the corrected sentence), and explain grammar or vocabulary "
    "in simple Uzbek when it helps understanding. "
    "Keep replies short and encouraging (2-5 sentences), suitable for a chat. "
    "If the student writes in Uzbek, reply with the English they need plus a "
    "short Uzbek explanation. Always be supportive."
)


async def ask_tutor(level: str, history: list, user_message: str) -> str:
    """Suhbat tarixi va yangi xabar asosida GPT javobini qaytaradi.

    history — [{"role": "user"/"assistant", "content": "..."}] ko'rinishida.
    """
    client = _get_client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(level=level or "A2 (Elementary)")}
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = await client.chat.completions.create(
        model=AI_MODEL,
        max_tokens=600,
        messages=messages,
    )
    return (response.choices[0].message.content or "").strip() or "…"
