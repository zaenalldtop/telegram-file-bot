import os
from pyrogram import Client, filters

# Mengambil konfigurasi dan memastikan API_ID dibaca wajib sebagai angka murni (int)
API_ID = int(os.environ.get("API_ID", "39206186").strip()) 
API_HASH = os.environ.get("API_HASH", "f1f40463bd79b121b4bff7a76c47ac16").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN").strip()

app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def generate_link(client, message):
    msg = await message.reply_text("⏳ *Sedang memproses file Anda...*")
    
    # Mengambil ID file unik dari media Telegram
    file_id = getattr(message, message.media.value).file_id
    
    # Membuat tautan unduh publik dummy (silakan sesuaikan jika Anda memiliki server streamer)
    download_link = f"https://t.me{client.me.username}?start={file_id}"
    
    await msg.edit_text(f"✅ *File Berhasil Dikonversi!*\n\n🔗 Tautan Anda:\n{download_link}")

if __name__ == "__main__":
    print("--- BOT SEDANG BERJALAN DAN AKTIF ---")
    app.run()
