import json
import os
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("verification_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

USER_DATA_FILE = "user_data.json"
WELCOME_IMAGE_PATH = "image.jpg"  # Pastikan file ada di direktori yang benar

# Load user data
try:
    with open(USER_DATA_FILE, "r") as file:
        user_shares = json.load(file)
except FileNotFoundError:
    user_shares = {}

# Save user data
def save_user_data():
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_shares, file)

# Handle new user join
@bot.on_message(filters.new_chat_members)
async def welcome(client, message):
    user_id = message.from_user.id

    if user_id not in user_shares:
        user_shares[user_id] = {"shared": 0, "verified": False}
    
    share_link = (
        "https://t.me/share/url?url=Gabung%20ke%20grup%20ini%20untuk%20media%20b0ch1l%20gratis!"
        "%20%F0%9F%92%A5%20%F0%9F%91%89%20https://t.me/+xrJpBvLHUQcwZDE0"
    )

    welcome_text = (
        f"👋 Selamat datang {message.from_user.mention}!\n\n"
        "Untuk membuka 4739 media grup, mohon bagikan ke 3 grup lain kemudian tekan VERIFIKASI."
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"BAGIKAN {user_shares[user_id]['shared']}/3", url=share_link)],
        [InlineKeyboardButton("VERIFIKASI ✅" if user_shares[user_id]["shared"] >= 3 else "VERIFIKASI ❌",
                              callback_data=f"verify_{user_id}")]
    ])

    # **Kirim pesan ke grup sebagai reply, tapi hanya user yang join yang bisa melihatnya**
    msg = await message.reply_photo(
        photo=WELCOME_IMAGE_PATH,
        caption=welcome_text,
        reply_markup=keyboard
    )

    # Hapus pesan setelah 30 detik agar tidak mengganggu grup
    await asyncio.sleep(30)
    await msg.delete()

    save_user_data()

bot.run()
