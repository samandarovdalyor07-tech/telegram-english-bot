# -*- coding: utf-8 -*-
"""
Ingliz tili daraja bo'yicha test savollari bazasi.

Har bir savol formati:
    {
        "q": "Savol matni (ingliz tilida)",
        "options": ["variant1", "variant2", "variant3", "variant4"],
        "answer": "to'g'ri variant matni",   # options ichidan bittasi
    }

Bot variantlarni har safar aralashtirib chiqaradi, shuning uchun
"answer" indeks emas, balki to'g'ri variantning MATNI bo'lishi kerak.
"""

# Darajalar tartibi va ko'rsatiladigan nomlari
LEVELS = {
    "beginner": "🟢 Beginner (A1)",
    "elementary": "🔵 Elementary (A2)",
    "intermediate": "🟡 Intermediate (B1)",
    "upper": "🟠 Upper-Intermediate (B2)",
    "advanced": "🔴 Advanced (C1)",
}

QUESTIONS = {
    # ------------------------------------------------------------------ #
    "beginner": [
        {"q": "Choose the correct article:  ___ egg",
         "options": ["a", "an", "the", "—"], "answer": "an"},
        {"q": "My father ___ a doctor.",
         "options": ["am", "is", "are", "be"], "answer": "is"},
        {"q": "What is the plural of 'woman'?",
         "options": ["womans", "women", "womens", "woman"], "answer": "women"},
        {"q": "You ___ very kind.",
         "options": ["is", "am", "are", "be"], "answer": "are"},
        {"q": "Choose the correct article:  ___ umbrella",
         "options": ["a", "an", "some", "two"], "answer": "an"},
        {"q": "How many days are there in a week?",
         "options": ["five", "six", "seven", "ten"], "answer": "seven"},
        {"q": "___ this your bag?",
         "options": ["Am", "Is", "Are", "Do"], "answer": "Is"},
        {"q": "Opposite of 'hot':",
         "options": ["warm", "cold", "cool", "dry"], "answer": "cold"},
        {"q": "The dogs ___ in the garden.",
         "options": ["is", "am", "are", "be"], "answer": "are"},
        {"q": "Which word is a color?",
         "options": ["apple", "green", "run", "happy"], "answer": "green"},
        {"q": "I ___ a student.",
         "options": ["is", "are", "am", "be"], "answer": "am"},
        {"q": "Opposite of 'day':",
         "options": ["sun", "night", "week", "morning"], "answer": "night"},
        {"q": "She ___ got two sisters.",
         "options": ["have", "has", "is", "am"], "answer": "has"},
        {"q": "Count: one, two, ___, four",
         "options": ["three", "five", "six", "ten"], "answer": "three"},
    ],
    # ------------------------------------------------------------------ #
    "elementary": [
        {"q": "He ___ to school every day.",
         "options": ["go", "goes", "going", "gone"], "answer": "goes"},
        {"q": "Look! The baby ___ now.",
         "options": ["sleep", "sleeps", "is sleeping", "slept"], "answer": "is sleeping"},
        {"q": "There ___ some milk in the fridge.",
         "options": ["is", "are", "am", "be"], "answer": "is"},
        {"q": "We don't have ___ money.",
         "options": ["some", "any", "much", "a"], "answer": "any"},
        {"q": "The cat is ___ the table.",
         "options": ["in", "on", "at", "of"], "answer": "on"},
        {"q": "Choose the past form: 'go'",
         "options": ["goed", "gone", "went", "going"], "answer": "went"},
        {"q": "She ___ like coffee.",
         "options": ["don't", "doesn't", "isn't", "aren't"], "answer": "doesn't"},
        {"q": "How ___ books are there?",
         "options": ["much", "many", "some", "any"], "answer": "many"},
        {"q": "My birthday is ___ June.",
         "options": ["on", "at", "in", "to"], "answer": "in"},
        {"q": "This is ___ than that one.",
         "options": ["good", "better", "best", "the best"], "answer": "better"},
    ],
    # ------------------------------------------------------------------ #
    "intermediate": [
        {"q": "I ___ TV when the phone rang.",
         "options": ["watch", "watched", "was watching", "am watching"], "answer": "was watching"},
        {"q": "If it rains, we ___ at home.",
         "options": ["stay", "will stay", "stayed", "would stay"], "answer": "will stay"},
        {"q": "She is the ___ student in the class.",
         "options": ["clever", "cleverer", "cleverest", "more clever"], "answer": "cleverest"},
        {"q": "You ___ smoke here. It's not allowed.",
         "options": ["must", "mustn't", "should", "can"], "answer": "mustn't"},
        {"q": "I have lived here ___ 2010.",
         "options": ["for", "since", "from", "ago"], "answer": "since"},
        {"q": "He gave ___ a present.",
         "options": ["I", "my", "me", "mine"], "answer": "me"},
        {"q": "They ___ already finished the work.",
         "options": ["has", "have", "had", "having"], "answer": "have"},
        {"q": "Choose the correct: 'I'm interested ___ music.'",
         "options": ["on", "at", "in", "for"], "answer": "in"},
        {"q": "Past form of 'buy':",
         "options": ["buyed", "bought", "brought", "buy"], "answer": "bought"},
        {"q": "She suggested ___ to the cinema.",
         "options": ["go", "to go", "going", "went"], "answer": "going"},
    ],
    # ------------------------------------------------------------------ #
    "upper": [
        {"q": "The bridge ___ in 1995.",
         "options": ["built", "was built", "is built", "has built"], "answer": "was built"},
        {"q": "If I ___ rich, I would travel the world.",
         "options": ["am", "was", "were", "will be"], "answer": "were"},
        {"q": "By the time we arrived, the film ___.",
         "options": ["started", "has started", "had started", "was starting"], "answer": "had started"},
        {"q": "I'd rather you ___ smoke in here.",
         "options": ["don't", "didn't", "won't", "not"], "answer": "didn't"},
        {"q": "He denied ___ the money.",
         "options": ["to steal", "steal", "stealing", "stole"], "answer": "stealing"},
        {"q": "It's high time we ___ home.",
         "options": ["go", "went", "going", "will go"], "answer": "went"},
        {"q": "She is used to ___ early.",
         "options": ["get up", "got up", "getting up", "gets up"], "answer": "getting up"},
        {"q": "Not only ___ late, but he also forgot the keys.",
         "options": ["he was", "was he", "he is", "is he"], "answer": "was he"},
        {"q": "The report needs ___ before Friday.",
         "options": ["finish", "to finish", "finishing", "finished"], "answer": "finishing"},
        {"q": "I wish I ___ that yesterday.",
         "options": ["didn't say", "hadn't said", "wouldn't say", "haven't said"], "answer": "hadn't said"},
    ],
    # ------------------------------------------------------------------ #
    "advanced": [
        {"q": "Hardly ___ the door when the phone rang.",
         "options": ["I had opened", "had I opened", "I opened", "did I open"], "answer": "had I opened"},
        {"q": "The phrasal verb 'to put off' means:",
         "options": ["to wear", "to postpone", "to remove", "to start"], "answer": "to postpone"},
        {"q": "He spoke as though he ___ everything.",
         "options": ["knows", "knew", "had known", "would know"], "answer": "knew"},
        {"q": "'To let the cat out of the bag' means:",
         "options": ["to free an animal", "to reveal a secret", "to make a mess", "to be lazy"], "answer": "to reveal a secret"},
        {"q": "Were it not for your help, I ___ failed.",
         "options": ["will have", "would have", "had", "would"], "answer": "would have"},
        {"q": "Choose the most formal synonym for 'buy':",
         "options": ["get", "purchase", "grab", "pick up"], "answer": "purchase"},
        {"q": "Seldom ___ such a beautiful sunset.",
         "options": ["I have seen", "have I seen", "I saw", "did I saw"], "answer": "have I seen"},
        {"q": "The committee ___ divided over the issue.",
         "options": ["is", "are", "were", "be"], "answer": "are"},
        {"q": "'To bite the bullet' means to:",
         "options": ["eat quickly", "face a hard situation bravely", "stay silent", "get injured"], "answer": "face a hard situation bravely"},
        {"q": "No sooner had he left ___ it started to rain.",
         "options": ["when", "then", "than", "that"], "answer": "than"},
    ],
}


def get_levels():
    """Daraja kalitlari va nomlarini qaytaradi."""
    return LEVELS


def get_questions(level):
    """Berilgan daraja uchun savollar ro'yxatini qaytaradi (nusxa)."""
    return [dict(q) for q in QUESTIONS.get(level, [])]
