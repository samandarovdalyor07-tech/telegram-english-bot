# -*- coding: utf-8 -*-
"""
📖 Matn (Reading), ✍️ Yozish (Writing), 📚 Lug'at (Vocabulary) bo'limlari uchun
kontent bazasi. Hammasi daraja bo'yicha ajratilgan va o'zbekcha tarjima/izoh
bilan beriladi.

Yangi material qo'shish juda oson — kerakli daraja ro'yxatiga shu formatda
yangi element qo'shing.
"""

# ============================================================================ #
# 📚 LUG'AT (Vocabulary) — yangi so'zlar yodlash
#   word        — inglizcha so'z
#   uz          — o'zbekcha tarjimasi
#   example     — inglizcha misol gap
#   example_uz  — misolning o'zbekcha tarjimasi
# ============================================================================ #

VOCABULARY = {
    "beginner": [
        {"word": "apple", "uz": "olma", "example": "I eat an apple.", "example_uz": "Men olma yeyman."},
        {"word": "water", "uz": "suv", "example": "I drink water.", "example_uz": "Men suv ichaman."},
        {"word": "house", "uz": "uy", "example": "This is my house.", "example_uz": "Bu mening uyim."},
        {"word": "book", "uz": "kitob", "example": "I read a book.", "example_uz": "Men kitob o'qiyman."},
        {"word": "friend", "uz": "do'st", "example": "She is my friend.", "example_uz": "U mening do'stim."},
        {"word": "school", "uz": "maktab", "example": "I go to school.", "example_uz": "Men maktabga boraman."},
        {"word": "family", "uz": "oila", "example": "I love my family.", "example_uz": "Men oilamni yaxshi ko'raman."},
        {"word": "food", "uz": "ovqat", "example": "The food is good.", "example_uz": "Ovqat mazali."},
        {"word": "day", "uz": "kun", "example": "Have a nice day.", "example_uz": "Kuningiz yaxshi o'tsin."},
        {"word": "happy", "uz": "baxtli", "example": "I am happy.", "example_uz": "Men baxtliman."},
    ],
    "elementary": [
        {"word": "weather", "uz": "ob-havo", "example": "The weather is nice today.", "example_uz": "Bugun ob-havo yaxshi."},
        {"word": "market", "uz": "bozor", "example": "We buy fruit at the market.", "example_uz": "Biz bozordan meva sotib olamiz."},
        {"word": "breakfast", "uz": "nonushta", "example": "I have breakfast at 8.", "example_uz": "Men soat 8 da nonushta qilaman."},
        {"word": "travel", "uz": "sayohat qilmoq", "example": "I like to travel.", "example_uz": "Men sayohat qilishni yoqtiraman."},
        {"word": "money", "uz": "pul", "example": "I don't have money.", "example_uz": "Mening pulim yo'q."},
        {"word": "healthy", "uz": "sog'lom", "example": "Fruit is healthy.", "example_uz": "Meva sog'lom."},
        {"word": "busy", "uz": "band", "example": "I am busy today.", "example_uz": "Men bugun bandman."},
        {"word": "beautiful", "uz": "chiroyli", "example": "The city is beautiful.", "example_uz": "Shahar chiroyli."},
        {"word": "neighbour", "uz": "qo'shni", "example": "My neighbour is kind.", "example_uz": "Mening qo'shnim mehribon."},
        {"word": "language", "uz": "til", "example": "English is a world language.", "example_uz": "Ingliz tili — jahon tili."},
    ],
    "intermediate": [
        {"word": "experience", "uz": "tajriba", "example": "She has work experience.", "example_uz": "Uning ish tajribasi bor."},
        {"word": "decision", "uz": "qaror", "example": "It was a hard decision.", "example_uz": "Bu qiyin qaror edi."},
        {"word": "environment", "uz": "atrof-muhit", "example": "We must protect the environment.", "example_uz": "Biz atrof-muhitni asrashimiz kerak."},
        {"word": "opportunity", "uz": "imkoniyat", "example": "This is a great opportunity.", "example_uz": "Bu ajoyib imkoniyat."},
        {"word": "knowledge", "uz": "bilim", "example": "Knowledge is power.", "example_uz": "Bilim — kuch."},
        {"word": "develop", "uz": "rivojlantirmoq", "example": "We develop new skills.", "example_uz": "Biz yangi ko'nikmalarni rivojlantiramiz."},
        {"word": "increase", "uz": "oshirmoq / ortmoq", "example": "Prices increase every year.", "example_uz": "Narxlar har yili ortadi."},
        {"word": "suggest", "uz": "taklif qilmoq", "example": "I suggest a short break.", "example_uz": "Men qisqa tanaffusni taklif qilaman."},
        {"word": "although", "uz": "garchi / ... bo'lsa-da", "example": "Although it was late, he worked.", "example_uz": "Kech bo'lsa-da, u ishladi."},
        {"word": "however", "uz": "biroq / lekin", "example": "It is hard; however, it is possible.", "example_uz": "Bu qiyin; biroq, bu mumkin."},
    ],
    "upper": [
        {"word": "achievement", "uz": "yutuq", "example": "This is a great achievement.", "example_uz": "Bu katta yutuq."},
        {"word": "consequence", "uz": "oqibat", "example": "Every action has consequences.", "example_uz": "Har bir harakatning oqibati bor."},
        {"word": "significant", "uz": "muhim / sezilarli", "example": "There was a significant change.", "example_uz": "Sezilarli o'zgarish bo'ldi."},
        {"word": "behaviour", "uz": "xulq / xatti-harakat", "example": "His behaviour was strange.", "example_uz": "Uning xulqi g'alati edi."},
        {"word": "attitude", "uz": "munosabat", "example": "She has a positive attitude.", "example_uz": "Uning ijobiy munosabati bor."},
        {"word": "available", "uz": "mavjud / bo'sh", "example": "The book is available online.", "example_uz": "Kitob internetda mavjud."},
        {"word": "require", "uz": "talab qilmoq", "example": "This job requires patience.", "example_uz": "Bu ish sabr talab qiladi."},
        {"word": "encourage", "uz": "rag'batlantirmoq", "example": "Teachers encourage students.", "example_uz": "O'qituvchilar o'quvchilarni rag'batlantiradi."},
        {"word": "despite", "uz": "...ga qaramay", "example": "Despite the rain, we went out.", "example_uz": "Yomg'irga qaramay, biz chiqdik."},
        {"word": "therefore", "uz": "shuning uchun", "example": "He was ill; therefore, he stayed home.", "example_uz": "U kasal edi; shuning uchun uyda qoldi."},
    ],
    "advanced": [
        {"word": "comprehensive", "uz": "keng qamrovli", "example": "We need a comprehensive plan.", "example_uz": "Bizga keng qamrovli reja kerak."},
        {"word": "inevitable", "uz": "muqarrar", "example": "Change is inevitable.", "example_uz": "O'zgarish muqarrar."},
        {"word": "ambiguous", "uz": "noaniq / ikki ma'noli", "example": "His answer was ambiguous.", "example_uz": "Uning javobi noaniq edi."},
        {"word": "profound", "uz": "chuqur (ma'noli)", "example": "It had a profound effect.", "example_uz": "U chuqur ta'sir ko'rsatdi."},
        {"word": "deteriorate", "uz": "yomonlashmoq", "example": "His health deteriorated.", "example_uz": "Uning sog'lig'i yomonlashdi."},
        {"word": "advocate", "uz": "yoqlamoq / targ'ib qilmoq", "example": "They advocate clean energy.", "example_uz": "Ular toza energiyani yoqlaydi."},
        {"word": "resilient", "uz": "bardoshli / chidamli", "example": "Children are resilient.", "example_uz": "Bolalar bardoshli bo'ladi."},
        {"word": "prevalent", "uz": "keng tarqalgan", "example": "This habit is prevalent today.", "example_uz": "Bu odat bugun keng tarqalgan."},
        {"word": "nonetheless", "uz": "shunga qaramay", "example": "It was risky; nonetheless, they tried.", "example_uz": "Bu xavfli edi; shunga qaramay, ular urindi."},
        {"word": "scrutiny", "uz": "sinchkovlik bilan tekshirish", "example": "The plan is under scrutiny.", "example_uz": "Reja sinchkovlik bilan tekshirilmoqda."},
    ],
}


# ============================================================================ #
# 📖 MATN (Reading) — o'qish va o'zbekcha tarjima
#   title — sarlavha
#   text  — inglizcha matn
#   uz    — o'zbekcha tarjimasi
# ============================================================================ #

READING = {
    "beginner": [
        {
            "title": "My Day",
            "text": "Hello! My name is Sara. I am ten years old. "
                    "I get up at seven. I go to school. I like English. "
                    "After school I play with my friends. I am happy.",
            "uz": "Salom! Mening ismim Sara. Men o'n yoshdaman. "
                  "Men soat yettida turaman. Men maktabga boraman. Men ingliz tilini yoqtiraman. "
                  "Maktabdan keyin do'stlarim bilan o'ynayman. Men baxtliman.",
        },
        {
            "title": "My Family",
            "text": "I have a small family. I have a mother, a father, and one brother. "
                    "My father is a doctor. My mother is a teacher. "
                    "We live in a big house. I love my family.",
            "uz": "Mening kichik oilam bor. Onam, otam va bitta akam bor. "
                  "Otam shifokor. Onam o'qituvchi. "
                  "Biz katta uyda yashaymiz. Men oilamni yaxshi ko'raman.",
        },
    ],
    "elementary": [
        {
            "title": "A Busy Morning",
            "text": "Every morning Tom wakes up at six o'clock. He takes a shower and has "
                    "breakfast with his family. Then he takes the bus to work. "
                    "The bus is usually crowded, but Tom doesn't mind. "
                    "He listens to music and reads the news on his phone.",
            "uz": "Har kuni ertalab Tom soat oltida uyg'onadi. U dush qabul qiladi va "
                  "oilasi bilan nonushta qiladi. Keyin ishga avtobusda boradi. "
                  "Avtobus odatda gavjum bo'ladi, lekin Tom bunga e'tibor bermaydi. "
                  "U musiqa tinglaydi va telefonida yangiliklarni o'qiydi.",
        },
        {
            "title": "Shopping at the Market",
            "text": "On Saturdays, Lola goes to the market with her mother. "
                    "They buy fresh fruit and vegetables. The market is colourful and noisy. "
                    "Lola likes the smell of fresh bread. After shopping, they have tea together.",
            "uz": "Shanba kunlari Lola onasi bilan bozorga boradi. "
                  "Ular yangi meva va sabzavot sotib olishadi. Bozor rang-barang va shovqinli. "
                  "Lolaga yangi nonning hidi yoqadi. Xariddan keyin ular birga choy ichishadi.",
        },
    ],
    "intermediate": [
        {
            "title": "Learning a Language",
            "text": "Learning a new language takes time and patience. Many people give up "
                    "because they expect quick results. However, the secret is practice. "
                    "If you study a little every day, you will make progress. "
                    "Mistakes are normal and they help you learn.",
            "uz": "Yangi til o'rganish vaqt va sabr talab qiladi. Ko'p odamlar tez natija "
                  "kutgani uchun voz kechadi. Biroq, sirning kaliti — mashq. "
                  "Agar har kuni ozgina o'qisangiz, oldinga siljiysiz. "
                  "Xatolar normal holat va ular o'rganishga yordam beradi.",
        },
        {
            "title": "A Healthy Lifestyle",
            "text": "A healthy lifestyle is not only about food. Of course, eating vegetables "
                    "is important, but sleep and exercise matter too. Experts suggest walking "
                    "for thirty minutes a day. Although it sounds simple, regular exercise "
                    "improves both your body and your mood.",
            "uz": "Sog'lom turmush tarzi faqat ovqat haqida emas. Albatta, sabzavot yeyish "
                  "muhim, lekin uyqu va jismoniy mashq ham ahamiyatli. Mutaxassislar kuniga "
                  "o'ttiz daqiqa yurishni tavsiya qiladi. Garchi oddiy tuyulsa-da, muntazam "
                  "mashq ham tanangizni, ham kayfiyatingizni yaxshilaydi.",
        },
    ],
    "upper": [
        {
            "title": "The Power of Habits",
            "text": "Habits shape our daily lives more than we realise. Small actions, repeated "
                    "every day, eventually lead to significant results. The good news is that "
                    "habits can be changed. Experts encourage people to start with one tiny "
                    "habit and build on it. Despite occasional failures, consistency is what "
                    "truly matters in the long run.",
            "uz": "Odatlar kunlik hayotimizni biz o'ylaganimizdan ko'ra ko'proq shakllantiradi. "
                  "Har kuni takrorlanadigan kichik harakatlar, oxir-oqibat, sezilarli "
                  "natijalarga olib keladi. Yaxshi xabar shuki, odatlarni o'zgartirish mumkin. "
                  "Mutaxassislar bitta kichik odatdan boshlab, uni rivojlantirishni "
                  "rag'batlantiradi. Vaqti-vaqti bilan muvaffaqiyatsizliklarga qaramay, "
                  "uzoq muddatda haqiqatan ham muhimi — izchillik.",
        },
    ],
    "advanced": [
        {
            "title": "Technology and Society",
            "text": "The rapid development of technology has transformed nearly every aspect of "
                    "modern life. While it offers comprehensive access to information and "
                    "connects people across the globe, it also raises profound concerns. "
                    "The consequences of constant connectivity are still ambiguous. Nonetheless, "
                    "few would deny that technology, used wisely, remains one of humanity's "
                    "most powerful tools.",
            "uz": "Texnologiyaning jadal rivojlanishi zamonaviy hayotning deyarli har bir "
                  "jabhasini o'zgartirdi. U axborotga keng qamrovli kirish imkonini bersa va "
                  "odamlarni butun dunyo bo'ylab bog'lasa-da, chuqur xavotirlarni ham keltirib "
                  "chiqaradi. Doimiy bog'lanishning oqibatlari hali noaniq. Shunga qaramay, "
                  "texnologiya oqilona ishlatilsa, insoniyatning eng kuchli vositalaridan biri "
                  "bo'lib qolishini kam odam inkor etadi.",
        },
    ],
}


# ============================================================================ #
# ✍️ YOZISH (Writing) — o'zbekchadan inglizchaga tarjima qilib yozish
#   uz       — o'zbekcha gap (foydalanuvchi shuni inglizchaga yozadi)
#   answers  — qabul qilinadigan inglizcha javoblar (bittadan ortiq bo'lishi mumkin)
#   hint     — yordam (ixtiyoriy)
# ============================================================================ #

WRITING = {
    "beginner": [
        {"uz": "Mening ismim Ali.", "answers": ["my name is ali"], "hint": "name = ism"},
        {"uz": "Men o'quvchiman.", "answers": ["i am a student", "i'm a student"], "hint": "student = o'quvchi"},
        {"uz": "Bu mening kitobim.", "answers": ["this is my book"], "hint": "book = kitob"},
        {"uz": "Men suv ichaman.", "answers": ["i drink water"], "hint": "drink = ichmoq"},
        {"uz": "U mening do'stim.", "answers": ["he is my friend", "she is my friend", "he's my friend", "she's my friend"], "hint": "friend = do'st"},
        {"uz": "Men baxtliman.", "answers": ["i am happy", "i'm happy"], "hint": "happy = baxtli"},
    ],
    "elementary": [
        {"uz": "Men har kuni maktabga boraman.", "answers": ["i go to school every day", "i go to school everyday"], "hint": "every day = har kuni"},
        {"uz": "U futbol o'ynashni yoqtiradi.", "answers": ["he likes to play football", "he likes playing football", "she likes to play football", "she likes playing football"], "hint": "like + to/-ing"},
        {"uz": "Bugun ob-havo yaxshi.", "answers": ["the weather is nice today", "today the weather is nice", "the weather is good today"], "hint": "weather = ob-havo"},
        {"uz": "Bizning pulimiz yo'q.", "answers": ["we don't have money", "we do not have money", "we have no money"], "hint": "don't have = yo'q"},
        {"uz": "Men ertalab nonushta qilaman.", "answers": ["i have breakfast in the morning"], "hint": "have breakfast = nonushta qilmoq"},
    ],
    "intermediate": [
        {"uz": "Men ikki yildan beri ingliz tilini o'rganyapman.", "answers": ["i have been learning english for two years", "i have been studying english for two years"], "hint": "for + davomiylik, Present Perfect Continuous"},
        {"uz": "Agar yomg'ir yog'sa, biz uyda qolamiz.", "answers": ["if it rains we will stay at home", "if it rains we will stay home", "we will stay at home if it rains"], "hint": "First Conditional: if + Present, will + V"},
        {"uz": "U menga yordam berishni taklif qildi.", "answers": ["he offered to help me", "she offered to help me", "he suggested helping me", "she suggested helping me"], "hint": "offer to / suggest + -ing"},
        {"uz": "Bu mening hayotimdagi eng yaxshi qaror edi.", "answers": ["it was the best decision in my life", "it was the best decision of my life"], "hint": "the best = eng yaxshi"},
        {"uz": "Garchi charchagan bo'lsam-da, men ishlashda davom etdim.", "answers": ["although i was tired i kept working", "although i was tired i continued working", "although i was tired i continued to work"], "hint": "although = garchi"},
    ],
    "upper": [
        {"uz": "Bu ko'prik 1995-yilda qurilgan.", "answers": ["this bridge was built in 1995", "the bridge was built in 1995"], "hint": "Passive: was built"},
        {"uz": "Yomg'irga qaramay, biz sayrga chiqdik.", "answers": ["despite the rain we went out", "despite the rain we went for a walk", "in spite of the rain we went out"], "hint": "despite = ...ga qaramay"},
        {"uz": "Agar ko'proq o'qiganimda, imtihondan o'tardim.", "answers": ["if i had studied more i would have passed the exam", "if i had studied harder i would have passed the exam"], "hint": "Third Conditional: if + Past Perfect, would have + V3"},
        {"uz": "U go'yo hamma narsani bilgandek gapirdi.", "answers": ["he spoke as if he knew everything", "she spoke as if she knew everything", "he talked as if he knew everything"], "hint": "as if + Past"},
        {"uz": "Bu ish katta sabr talab qiladi.", "answers": ["this job requires a lot of patience", "this work requires a lot of patience", "this job requires great patience"], "hint": "require = talab qilmoq"},
    ],
    "advanced": [
        {"uz": "Eshikni endigina ochgan edimki, telefon jiringladi.", "answers": ["hardly had i opened the door when the phone rang", "no sooner had i opened the door than the phone rang"], "hint": "Inversion: Hardly had I ... when / No sooner had I ... than"},
        {"uz": "O'zgarish muqarrar, shuning uchun biz moslashishimiz kerak.", "answers": ["change is inevitable so we must adapt", "change is inevitable therefore we must adapt", "change is inevitable so we have to adapt"], "hint": "inevitable = muqarrar"},
        {"uz": "Sizning yordamingiz bo'lmaganida, men muvaffaqiyatsizlikka uchrardim.", "answers": ["were it not for your help i would have failed", "if it were not for your help i would have failed", "but for your help i would have failed"], "hint": "Were it not for ... = ... bo'lmaganida"},
        {"uz": "Reja sinchkovlik bilan tekshirilmoqda.", "answers": ["the plan is under scrutiny", "the plan is being scrutinised", "the plan is being scrutinized"], "hint": "under scrutiny = tekshiruv ostida"},
        {"uz": "Bu odat bugungi kunda keng tarqalgan.", "answers": ["this habit is prevalent today", "this habit is widespread today", "this habit is common today"], "hint": "prevalent = keng tarqalgan"},
    ],
}


# --------------------------------------------------------------------------- #
# Yordamchi olish funksiyalari
# --------------------------------------------------------------------------- #

def get_vocabulary(level):
    return [dict(x) for x in VOCABULARY.get(level, [])]


def get_reading(level):
    return [dict(x) for x in READING.get(level, [])]


def get_writing(level):
    return [dict(x) for x in WRITING.get(level, [])]
