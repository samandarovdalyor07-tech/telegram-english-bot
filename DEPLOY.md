# 🚀 Serverga joylashtirish (24/7 ishlashi uchun)

Bot **polling** rejimida ishlaydi — istalgan doimiy ishlaydigan serverda ishlaydi.

> ⚠️ **Eng muhim qoidalar**
> 1. **Faqat bitta nusxa** polling qilishi mumkin. Server ishga tushsa, kompyuteringizdagi botni **to'xtating** (Ctrl+C).
> 2. **`bot.db`** saqlanishi uchun server doimiy diskka ega bo'lsin (VPS — avtomatik; PaaS — "volume" ulang).
> 3. Token/AI kalit serverda `.env` faylda yoki muhit o'zgaruvchisi sifatida beriladi. **Kodga yozmang**, `.env` ni gitga yubormang.

---

## 1-variant: VPS (Linux server) — tavsiya etiladi ✅

Eng ishonchli: ma'lumotlar saqlanadi, to'liq nazorat. Masalan Ubuntu 22.04 VPS
(ps.uz, ahost.uz, Hetzner, Contabo, DigitalOcean...). ~$4–6/oy.

```bash
# 1) Serverga SSH orqali kiring, kerakli narsalarni o'rnating
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git

# 2) Loyihani oling (GitHub'dan)
git clone https://github.com/samandarovdalyor07-tech/telegram-english-bot.git
cd telegram-english-bot

# 3) Virtual muhit va kutubxonalar
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 4) .env faylni yarating (tokeningizni qo'ying)
nano .env
#   BOT_TOKEN=8850425782:AAEq...
#   AI_API_KEY=sk-ant-...        (AI uchun, ixtiyoriy)

# 5) systemd xizmatini o'rnating (english-bot.service ichidagi USER/yo'llarni moslang)
sudo cp english-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now english-bot

# 6) Holat va loglar
systemctl status english-bot
journalctl -u english-bot -f
```

Endi bot doimiy ishlaydi, server o'chib yonsa ham avtomatik qayta ishga tushadi.
Yangilash: `git pull` → `sudo systemctl restart english-bot`.

---

## 2-variant: Railway / Render / Fly.io (git push bilan oson)

PaaS — kod yuborasiz, ular ishga tushiradi. `Procfile` va `Dockerfile` tayyor.

**Umumiy qadamlar:**
1. Loyihani GitHub'ga yuklang (allaqachon yuklangan).
2. Hosting saytida "New Project" → GitHub repo'ni tanlang.
3. **Muhit o'zgaruvchilari** (Variables) bo'limiga qo'shing:
   - `BOT_TOKEN` = tokeningiz
   - `AI_API_KEY` = AI kaliti (ixtiyoriy)
4. Bot turi: **Worker** (web emas — polling botda ochiq port yo'q).
5. 💾 **`bot.db` saqlanishi uchun "Volume" ulang** va uni `/app` ga mount qiling
   (aks holda har deploy'da ma'lumot o'chadi).

> Render'ning bepul tarifi vaqtincha uxlab qoladi — bot uchun "Background Worker"
> (pullik) yoki Fly.io/Railway ma'qul.

---

## 3-variant: Docker (har qanday serverda)

```bash
docker build -t english-bot .
docker run -d --name english-bot --restart=always \
  -e BOT_TOKEN=8850425782:AAEq... \
  -e AI_API_KEY=sk-ant-... \
  -v $(pwd)/data:/app/data \
  english-bot
```

> `bot.db` saqlanishi uchun `-v` (volume) bilan papka ulang.

---

## Tekshirish
- Loglar: `journalctl -u english-bot -f` (VPS) yoki hosting dagi "Logs"
- `🤖 Bot ishga tushdi` + `getUpdates ... 200 OK` ko'rinsa — ishlayapti
- Telegramda `/start` yozib sinang
