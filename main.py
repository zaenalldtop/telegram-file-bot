import os
import requests
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "39206186").strip()) 
API_HASH = os.environ.get("API_HASH", "f1f40463bd79b121b4bff7a76c47ac16").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN").strip()

# Domain kustom Anda
CUSTOM_DOMAIN = "https://primadigitalprint.com"

app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def generate_link(client, message):
    msg = await message.reply_text("⏳ *Sedang memproses file untuk Cloud Percetakan...*")
    
    local_path = await message.download()
    await msg.edit_text("⚡ *Sedang menyinkronkan ke cloud publik...*")
    
    try:
        with open(local_path, "rb") as file_data:
            response = requests.post(
                "https://catbox.moe",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": file_data}
            )
        
        if response.status_code == 200 and response.text.startswith("https"):
            # Mengambil nama unik file dari hasil unggahan catbox
            file_name = response.text.replace("https://catbox.moe", "").strip()
            
            # Membungkus tautan menggunakan domain pribadi Anda
            download_link = f"{CUSTOM_DOMAIN}/{file_name}"
            
            await msg.edit_text(
                f"✅ *File Sukses Terunggah!*\n\n"
                f"🔗 *Tautan Unduh Publik:*\n{download_link}\n\n"
                f"_Tautan resmi Cloud Percetakan Prima Digital Print._"
            )
        else:
            await msg.edit_text("❌ Gagal mengunggah ke cloud.")
            
    except Exception as e:
        await msg.edit_text(f"❌ Terjadi galat: {str(e)}")
    
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)

if __name__ == "__main__":
    print("--- BOT CLOUD PERCETAKAN AKTIF ---")
    app.run()
