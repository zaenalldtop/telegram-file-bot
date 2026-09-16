import os
import requests
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "39206186").strip()) 
API_HASH = os.environ.get("API_HASH", "f1f40463bd79b121b4bff7a76c47ac16").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN").strip()

app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def generate_link(client, message):
    msg = await message.reply_text("⏳ *Sedang mengunduh file dari Telegram...*")
    
    # Mengunduh file sementara ke server Render
    local_path = await message.download()
    
    await msg.edit_text("⚡ *Sedang mengunggah ke server publik...*")
    
    try:
        # Mengunggah file ke layanan penyimpanan gratis Catbox
        with open(local_path, "rb") as file_data:
            response = requests.post(
                "https://catbox.moe",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": file_data}
            )
        
        if response.status_code == 200 and response.text.startswith("https"):
            download_link = response.text.strip()
            await msg.edit_text(f"✅ *File Berhasil Menjadi Link Publik!*\n\n🔗 Tautan Unduh:\n{download_link}\n\n_Tautan ini bisa dibuka di browser apa saja tanpa memerlukan Telegram._")
        else:
            await msg.edit_text("❌ Gagal mengunggah file ke server publik.")
            
    except Exception as e:
        await msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
    
    finally:
        # Menghapus file sampah di server agar penyimpanan tidak penuh
        if os.path.exists(local_path):
            os.remove(local_path)

if __name__ == "__main__":
    print("--- BOT LINK PUBLIK AKTIF ---")
    app.run()
