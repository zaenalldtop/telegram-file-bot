import os
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "39206186").strip()) 
API_HASH = os.environ.get("API_HASH", "f1f40463bd79b121b4bff7a76c47ac16").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN").strip()

# Domain profesional Cloud Percetakan Anda
CUSTOM_DOMAIN = "https://primadigitalprint.com"

app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def generate_link(client, message):
    msg = await message.reply_text("⏳ *Sedang menghasilkan tautan Cloud Percetakan...*")
    
    try:
        # Mengambil ID file unik langsung dari Telegram tanpa perlu mengunggah ke web lain
        if message.photo:
            file_id = message.photo.file_id
        else:
            file_id = getattr(message, message.media.value).file_id
            
        # Membuat format tautan kustom menggunakan domain Anda
        download_link = f"{CUSTOM_DOMAIN}/{file_id}"
        
        await msg.edit_text(
            f"✅ *File Sukses Dikonversi!*\n\n"
            f"🔗 *Tautan Unduh Publik:*\n{download_link}\n\n"
            f"_Tautan resmi Cloud Percetakan Prima Digital Print._"
        )
    except Exception as e:
        await msg.edit_text(f"❌ Terjadi galat sistem: {str(e)}")

if __name__ == "__main__":
    print("--- BOT SERVER TELEGRAM AKTIF ---")
    app.run()
