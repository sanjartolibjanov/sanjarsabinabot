
import asyncio
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile,
)


# =========================================================
# SOZLAMALAR
# =========================================================

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = -1003687513132

ADMIN = "@sabina_tezbot"

CHANNEL_1 = "https://t.me/+0kRe29vvp8AxNTAy"
CHANNEL_2 = "https://t.me/+_-ijYqQG8cI5ZDAy"
CHANNEL_3 = "https://t.me/+spYYMT9HYaE2ZjFi"

# O'zbekiston vaqti UTC+5
UZ_TIMEZONE = timezone(timedelta(hours=5))

# Kunlik limit
DAILY_LIMIT = 300

# 3-5 daqiqa
MIN_DELAY = 180
MAX_DELAY = 300

# Rasm bot.py bilan bir papkada
PHOTO_PATH = Path(__file__).parent / "promo.png"


router = Router()

sabina_running = False
sending_task = None

last_full_name = ""
last_card = ""


# =========================================================
# QIZ ISMLARI
# =========================================================

GIRL_NAMES = [
    "Madina", "Sabina", "Dilnoza", "Malika", "Shahnoza",
    "Zarina", "Mohira", "Sevinch", "Diyora", "Nilufar",
    "Gulnoza", "Shahzoda", "Munisa", "Feruza", "Maftuna",
    "Nargiza", "Lola", "Rayhona", "Mubina", "Iroda",
    "Gulbahor", "Durdona", "Zebo", "Aziza", "Shirin",
    "Zilola", "Nodira", "Umida", "Nigina", "Gulrux",
    "Gulchehra", "Mohinur", "Oydin", "Oygul", "Sitora",
    "Zuhra", "Mavluda", "Marjona", "Robiya", "Fotima",
    "Hadicha", "Maryam", "Sabrina", "Asal", "Sevara",
    "Shahlo", "Komila", "Lobar", "Laylo", "Dildora",
    "Dilafruz", "Dilrabo", "Gulhayo", "Gulnora", "Nasiba",
    "Nasrin", "Nigora", "Nafisa", "Nozima", "Nozli",
    "Oysha", "Omina", "Ruxsora", "Ruxshona", "Sarvinoz",
    "Shabnam", "Shahina", "Shukrona", "Tamanno", "Vasila",
    "Yulduz", "Yasmina", "Yagona", "Zarnigor", "Ziyoda",
    "Zulfiza", "Zulfiya", "Anora", "Barno", "Bonu",
    "Charos", "E'zoza", "Gulandom", "Gulira'no", "Gulshan",
    "Hulkar", "Iqbol", "Jasmina", "Kamola", "Karima",
    "Laziza", "Mehribon", "Mehriniso", "Muqaddas", "Muslima",
    "Oydinoy", "Parizoda", "Ra'no", "Saida", "Samira",
]


# =========================================================
# O'G'IL ISMLARI
# =========================================================

BOY_NAMES = [
    "Azizbek", "Javohir", "Bekzod", "Sardor", "Diyor",
    "Muhammad", "Akmal", "Oybek", "Bobur", "Islom",
    "Shoxrux", "Abror", "Asadbek", "Jasur", "Temur",
    "Umid", "Farrux", "Sherzod", "Ibrohim", "Samandar",
    "Abdulloh", "Abdulaziz", "Abdurahmon", "Alisher", "Anvar",
    "Asilbek", "Bahodir", "Behruz", "Bektemir", "Bunyod",
    "Davron", "Dilmurod", "Doniyor", "Elyor", "Erkin",
    "Fazliddin", "Firdavs", "G'ayrat", "Hamza", "Hasan",
    "Husan", "Ilhom", "Iskandar", "Jamshid", "Jahongir",
    "Javlon", "Kamron", "Komil", "Laziz", "Mansur",
    "Mirjalol", "Mirkomil", "Mirzo", "Muhammadali",
    "Muhammadyusuf", "Murod", "Murodjon", "Mustafa", "Nodir",
    "Olim", "Otabek", "Ozodbek", "Qobil", "Qodir",
    "Qobiljon", "Rahmatulloh", "Rustam", "Sanjar", "Sarvar",
    "Sirojiddin", "Sohib", "Suhrob", "Tolib", "Tohir",
    "Ulug'bek", "Valijon", "Xurshid", "Yusuf", "Zafar",
    "Zohid", "Zokir", "Zubayr", "Abbos", "Adham",
    "Adil", "Akbar", "Alibek", "Amir", "Arslon",
    "Azamat", "Bahriddin", "Botir", "Dilshod", "Doston",
    "Elbek", "Emin", "Fozil", "Ismat", "Jaloliddin",
    "Javod", "Kamol", "Karim", "Mahmud", "Maqsud",
    "Maruf", "Muzaffar", "Nazar", "Odil", "Orif",
    "Ravshan", "Shavkat", "Shuhrat", "Sunnat", "Tursun",
    "Yunus", "Yorqin",
]


# =========================================================
# FAMILIYALAR
# =========================================================

LAST_NAMES = [
    "Karimov", "Abdullayev", "Xasanov", "Rahimov", "Aliyev",
    "Tursunov", "Ismoilov", "Akbarov", "Qodirov", "Yusupov",
    "Saidov", "Nazarov", "Usmonov", "Rustamov", "Ergashev",
    "Mamatov", "Sobirov", "Hamidov", "Raxmonov", "Jalilov",
    "Ortiqov", "Yoqubov", "Mirzayev", "Azimov", "Soliyev",
    "Abduqodirov", "Olimov", "Mahmudov", "Hasanov", "Husanov",
    "Isroilov", "Ibragimov", "Yunusov", "Zokirov", "Zohidov",
    "Valiyev", "Niyozov", "Shukurov", "Toirov", "Sattorov",
    "Rasulov", "Murodov", "Davronov", "Norqulov", "Bozorov",
    "Sirojov", "Fozilov", "G'ulomov", "Rahmonov", "Jabborov",
    "Jumayev", "Qo'chqorov", "Toshpulatov", "Xolmatov",
    "Xudoyberdiyev", "Matkarimov", "Eshonqulov", "Abbosov",
    "Adhamov", "Anvarov", "Asqarov", "Azamatov", "Bahodirov",
    "Bekmurodov", "Berdiyorov", "Boboyev", "Daminov", "Donoqulov",
    "Egamov", "Fayzullayev", "Gafurov", "Hamroyev", "Isakov",
    "Jumanazarov", "Kamilov", "Komilov", "Latipov", "Mahkamov",
    "Mansurov", "Mirjalolov", "Mo'minov", "Nabiev", "Nazarbekov",
    "Nosirov", "Odilov", "Olimjonov", "Oripov", "Otajonov",
    "Pulatov", "Rizayev", "Samatov", "Sharipov", "Shermatov",
    "Sodiqov", "Sultonov", "Tojiboyev", "Umarov", "Usarov",
    "Xolboyev", "Zaripov", "Ziyodullayev", "Zufarov", "Yuldashev",
    "Qurbonov",
]


# =========================================================
# KARTA TURLARI
# =========================================================

CARD_TYPES = [
    "TEZCARD",
    "HUMO",
    "UZCARD",
]


# =========================================================
# START TUGMALARI
# =========================================================

def subscription_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanal 1",
                    url=CHANNEL_1
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 Kanal 2",
                    url=CHANNEL_2
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 Kanal 3",
                    url=CHANNEL_3
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Obunani tekshirish",
                    callback_data="check_subscription"
                )
            ]
        ]
    )


# =========================================================
# /START
# =========================================================

@router.message(CommandStart())
async def start_command(message: Message):

    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Iltimos, quyidagi 3 ta kanalga obuna bo‘ling:\n\n"
        "1️⃣ Kanal 1\n"
        "2️⃣ Kanal 2\n"
        "3️⃣ Kanal 3\n\n"
        "Obuna bo‘lgach, tekshirish tugmasini bosing.",
        reply_markup=subscription_keyboard()
    )


# =========================================================
# OBUNANI TEKSHIRISH
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "check_subscription"
)
async def check_subscription(callback: CallbackQuery):

    await callback.answer(
        "Obuna tekshirildi ✅",
        show_alert=True
    )

    await callback.message.answer(
        "✅ Rahmat!\n"
        "Obuna tekshirildi."
    )


# =========================================================
# RANDOM ISM-FAMILIYA
# =========================================================

def random_full_name():

    global last_full_name

    while True:

        if random.random() < 0.5:
            first_name = random.choice(GIRL_NAMES)
        else:
            first_name = random.choice(BOY_NAMES)

        surname = random.choice(LAST_NAMES)

        full_name = f"{first_name} {surname}"

        if full_name != last_full_name:

            last_full_name = full_name

            return full_name


# =========================================================
# RANDOM KARTA
# =========================================================

def random_card():

    global last_card

    while True:

        # 1-9 orasidan 4 ta raqam
        ending = "".join(
            random.choice("123456789")
            for _ in range(4)
        )

        card_type = random.choice(CARD_TYPES)

        card = f"{card_type} *{ending}"

        if card != last_card:

            last_card = card

            return card


# =========================================================
# XABAR MATNI
# =========================================================

def create_message():

    name = random_full_name()
    card = random_card()

    now = datetime.now(UZ_TIMEZONE)

    current_time = now.strftime(
        "%H:%M %d.%m.%Y"
    )

    return (
        f"👤 {name}\n"
        f"➖ 800 000 UZS\n"
        f"📍 test P2P TEZ B.N\n"
        f"💳 {card}\n"
        f"🕓 {current_time}\n\n"
        f"BOT @kartd_tez_bot"
    )


# =========================================================
# RASM + XABAR YUBORISH
# =========================================================

async def send_messages(bot: Bot):

    global sabina_running

    sent = 0

    # Rasm mavjudligini tekshirish
    if not PHOTO_PATH.exists():

        print(
            f"XATO: {PHOTO_PATH} topilmadi!"
        )

        sabina_running = False

        return

    while sabina_running and sent < DAILY_LIMIT:

        try:

            photo = FSInputFile(
                PHOTO_PATH
            )

            caption = create_message()

            # RASM + CAPTION
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo,
                caption=caption
            )

            sent += 1

            print(
                f"Rasm + xabar yuborildi: "
                f"{sent}/{DAILY_LIMIT}"
            )

            # Har 20 ta xabardan keyin
            if sent % 20 == 0:

                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=(
                        "Salom obunachlar! "
                        "Test xabarlar o‘z vaqtida yuborilmoqda.\n"
                        "Kimda savol bo‘lsa adminga yozing.\n\n"
                        f"Admin {ADMIN}"
                    )
                )

            # 3-5 daqiqalik random interval
            delay = random.randint(
                MIN_DELAY,
                MAX_DELAY
            )

            print(
                f"Keyingi xabar "
                f"{delay // 60} daqiqadan keyin."
            )

            await asyncio.sleep(delay)

        except asyncio.CancelledError:

            print("Yuborish to‘xtatildi.")

            break

        except Exception as error:

            print(
                "Xatolik:",
                error
            )

            await asyncio.sleep(30)

    if sent >= DAILY_LIMIT:

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=(
                "✅ Bugungi 300 ta "
                "test xabar yuborildi."
            )
        )

        sabina_running = False


# =========================================================
# /SABINA VA /SABINASTOP
# =========================================================

@router.channel_post()
async def channel_commands(
    message: Message,
    bot: Bot
):

    global sabina_running
    global sending_task

    if not message.text:
        return

    command = message.text.strip().lower()

    # -------------------------
    # START
    # -------------------------

    if command == "/sabina":

        if sabina_running:

            await bot.send_message(
                chat_id=CHANNEL_ID,
                text="⚠️ SabinaBot allaqachon ishlayapti."
            )

            return

        sabina_running = True

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text="🟢 SabinaBot ishga tushdi."
        )

        sending_task = asyncio.create_task(
            send_messages(bot)
        )

    # -------------------------
    # STOP
    # -------------------------

    elif command == "/sabinastop":

        sabina_running = False

        if sending_task:

            sending_task.cancel()

            sending_task = None

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text="🔴 SabinaBot to‘xtatildi."
        )


# =========================================================
# BOTNI ISHGA TUSHIRISH
# =========================================================

async def main():

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()

    dp.include_router(router)

    print("=" * 40)
    print("SabinaBot ishga tushdi!")
    print(f"Kanal: {CHANNEL_ID}")
    print(f"Rasm: {PHOTO_PATH}")
    print(f"Kunlik limit: {DAILY_LIMIT}")
    print("Interval: 3-5 daqiqa")
    print("=" * 40)

    await dp.start_polling(
        bot,
        allowed_updates=[
            "message",
            "callback_query",
            "channel_post"
        ]
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())
