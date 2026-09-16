import os
import requests
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "39206186").strip()) 
API_HASH = os.environ.get("API_HASH", "f1f40463bd79b121b4bff7a76c47ac16").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8913324140:AAFt0rHCeNPScTHThGPPmIR4S2cdLiZfMw4").strip()

CUSTOM_DOMAIN = "https://primadigitalprint.com"

app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def generate_link(client, message):
    msg = await message.reply_text("⏳ *Sedang memproses dokumen untuk Cloud Percetakan...*")
    
    local_path = await message.download()
    await msg.edit_text("⚡ *Sedang mengunggah ke Cloud Prima Digital Print...*")
    
    try:
        # Mengunggah file ke API Pixeldrain yang sangat cepat dan mendukung semua format (.rar, .cdr)
        with open(local_path, "rb") as file_data:
            response = requests.post(
                "https://pixeldrain.com",
                files={"file": file_data}
            )
        
        res_data = response.json()
        if response.status_code == 201 and res_data.get("success"):
            file_id = res_data.get("id")
            
            # Membuat format link profesional menggunakan domain Anda
            download_link = f"{CUSTOM_DOMAIN}/{file_id}"
            
            await msg.edit_text(
                f"✅ *File Sukses Terunggah!*\n\n"
                f"🔗 *Tautan Unduh Publik:*\n{download_link}\n\n"
                f"_Tautan resmi Cloud Percetakan Prima Digital Print._"
            )
        else:
            await msg.edit_text("❌ Server cloud sedang penuh. Silakan coba beberapa saat lagi.")
            
    except Exception as e:
        await msg.edit_text(f"❌ Terjadi galat sistem: {str(e)}")
    
    finally:
        # Menghapus file sampah di server Render agar tidak penuh
        if os.path.exists(local_path):
            os.remove(local_path)

if __name__ == "__main__":
    print("--- BOT CLOUD PERCETAKAN FINAL AKTIF ---")
    app.run()
