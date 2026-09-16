import os
import requests
import urllib3
from pyrogram import Client, filters

# Menonaktifkan peringatan tidak aman karena bypass SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        with open(local_path, "rb") as file_data:
            # Menambahkan verify=False untuk melewati bentrokan protokol SSL Render
            response = requests.post(
                "https://pixeldrain.com",
                files={"file": file_data},
                verify=False
            )
        
        res_data = response.json()
        if response.status_code == 201 and res_data.get("success"):
            file_id = res_data.get("id")
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
        if os.path.exists(local_path):
            os.remove(local_path)

if __name__ == "__main__":
    print("--- BOT CLOUD PERCETAKAN FINAL SUKSES BERJALAN ---")
    app.run()
