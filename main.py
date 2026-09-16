import os
from pyrogram import Client, filters

# Mengambil konfigurasi dari Environment Variables
API_ID = int(os.environ.get("API_ID", "123456")) # Dapatkan dari my.telegram.org jika diperlukan, atau isi default
API_HASH = os.environ.get("API_HASH", "abcdef") 
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SERVER_URL = os.environ.get("SERVER_URL") # URL Web Server Render Anda

app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def generate_link(client, message):
    msg = await message.reply_text("⏳ *Sedang memproses file Anda...*")
    
    # Menggunakan ID file Telegram sebagai jalur unduhan unik
    file_id = getattr(message, message.media.value).file_id
    
    # Tautan langsung ke server web yang akan kita buat
    download_link = f"{SERVER_URL}/download/{file_id}"
    
    await msg.edit_text(f"✅ *File Berhasil Dikonversi!*\n\n🔗 Tautan Anda:\n{download_link}")

if __name__ == "__main__":
    app.run()
