# -*- coding: utf-8 -*-
"""
📖 Guruhda ovozli o'qish (peer-reading) uchun hikoyalar to'plami.

Bu yerda maxsus qisqa ingliz hikoyalari saqlanadi (Quyon va Sher va b.).
get_story_pool() yangi hikoyalarni Reading bo'limidagi mavjud matnlar bilan
birlashtirib qaytaradi — shuning uchun o'qituvchi keng tanlovga ega bo'ladi.
"""

from content import READING

# Guruhda ovoz bilan o'qish uchun maxsus hikoyalar
STORIES = [
    {
        "title": "The Lion and the Rabbit",
        "text": (
            "Once a fierce lion lived in a forest. Every day he killed many "
            "animals. The animals were afraid, so they made a plan. Each day "
            "one animal would go to the lion. One day it was the rabbit's turn. "
            "The rabbit came late, and the lion was angry. The clever rabbit "
            "said, 'Another lion wanted to eat me.' The lion roared, 'Where is "
            "he?' The rabbit showed him a deep well. The lion looked inside and "
            "saw his own reflection. He thought it was another lion and jumped "
            "in. That was the end of the cruel lion."
        ),
        "uz": (
            "Bir o'rmonda yovvoyi sher yashardi. U har kuni ko'p hayvonlarni "
            "o'ldirardi. Hayvonlar qo'rqib, reja tuzishdi: har kuni bitta "
            "hayvon sherning oldiga borardi. Bir kuni quyonning navbati keldi. "
            "Quyon kech keldi, sher jahli chiqdi. Aqlli quyon: 'Boshqa sher "
            "meni yemoqchi bo'ldi', dedi. Sher: 'U qayerda?' deb o'kirdi. Quyon "
            "unga chuqur quduqni ko'rsatdi. Sher ichiga qaradi va o'z aksini "
            "ko'rdi. Uni boshqa sher deb o'ylab, quduqqa sakradi. Shafqatsiz "
            "sherning oxiri shunday bo'ldi."
        ),
    },
    {
        "title": "The Ant and the Dove",
        "text": (
            "An ant was thirsty and went to the river to drink. Suddenly she "
            "fell into the water. A dove saw the ant and dropped a leaf into "
            "the water. The ant climbed onto the leaf and was saved. Later, a "
            "hunter wanted to catch the dove. The ant bit his foot. The hunter "
            "shouted, and the dove flew away. Kindness is never wasted."
        ),
        "uz": (
            "Bir chumoli chanqab, suv ichgani daryoga bordi. To'satdan u suvga "
            "tushib ketdi. Kaptar buni ko'rib, suvga barg tashladi. Chumoli "
            "bargga chiqib, qutulib qoldi. Keyinroq ovchi kaptarni tutmoqchi "
            "bo'ldi. Chumoli uning oyog'ini chaqdi. Ovchi qichqirdi va kaptar "
            "uchib ketdi. Yaxshilik hech qachon zoye ketmaydi."
        ),
    },
    {
        "title": "The Tortoise and the Hare",
        "text": (
            "A hare laughed at a slow tortoise. 'Let's have a race,' said the "
            "tortoise. The hare ran very fast and then slept under a tree. The "
            "tortoise walked slowly but never stopped. When the hare woke up, "
            "the tortoise was already at the finish line. Slow and steady wins "
            "the race."
        ),
        "uz": (
            "Quyon sekin toshbaqa ustidan kuldi. 'Keling, poyga qilaylik', dedi "
            "toshbaqa. Quyon juda tez yugurdi, keyin daraxt tagida uxlab qoldi. "
            "Toshbaqa sekin yurdi, lekin hech to'xtamadi. Quyon uyg'onganda, "
            "toshbaqa allaqachon marraga yetib bo'lgan edi. Sekin va barqaror "
            "yurgan g'olib bo'ladi."
        ),
    },
    {
        "title": "The Boy Who Cried Wolf",
        "text": (
            "A boy looked after sheep near a village. He was bored, so he "
            "shouted, 'Wolf! Wolf!' The villagers ran to help, but there was no "
            "wolf. He did this again, and they were angry. One day a real wolf "
            "came. The boy shouted, 'Wolf!' but nobody came. The wolf ate many "
            "sheep. Nobody believes a liar, even when he tells the truth."
        ),
        "uz": (
            "Bir bola qishloq yonida qo'ylarni boqardi. Zerikkanidan: 'Bo'ri! "
            "Bo'ri!' deb qichqirdi. Qishloq aholisi yordamga yugurdi, lekin "
            "bo'ri yo'q edi. U buni yana qildi, odamlar jahli chiqdi. Bir kuni "
            "haqiqiy bo'ri keldi. Bola: 'Bo'ri!' deb qichqirdi, ammo hech kim "
            "kelmadi. Bo'ri ko'p qo'ylarni yedi. Yolg'onchiga, hatto rost "
            "gapirsa ham, hech kim ishonmaydi."
        ),
    },
    {
        "title": "The Fox and the Grapes",
        "text": (
            "A hungry fox saw sweet grapes high on a vine. He jumped again and "
            "again, but he could not reach them. At last he gave up and walked "
            "away. 'They are sour anyway,' he said. It is easy to hate what you "
            "cannot have."
        ),
        "uz": (
            "Och tulki tok ustidagi shirin uzumlarni ko'rdi. U qayta-qayta "
            "sakradi, lekin yetib ololmadi. Oxiri taslim bo'lib, ketib qoldi. "
            "'Baribir nordon ekan', dedi u. Qo'lga kirita olmagan narsangni "
            "yomon ko'rish oson."
        ),
    },
]


def get_story_pool():
    """Maxsus hikoyalar + Reading bo'limidagi mavjud matnlar (birlashtirilgan).

    Har bir element: {"title", "text", "uz"}.
    """
    pool = [dict(s) for s in STORIES]
    seen = {s["title"] for s in pool}
    for level_texts in READING.values():
        for item in level_texts:
            if item["title"] not in seen:
                pool.append({
                    "title": item["title"],
                    "text": item["text"],
                    "uz": item.get("uz", ""),
                })
                seen.add(item["title"])
    return pool
