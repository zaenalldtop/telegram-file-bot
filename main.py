import os
import requests
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "39206186").strip()) 
API_HASH = os.environ.get("API_HASH", "f1f40463bd79b121b4bff7a76c47ac16").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN").strip()

CUSTOM_DOMAIN = "https://primadigitalprint.com"

app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def generate_link(client, message):
    msg = await message.reply_text("⏳ *Sedang memproses dokumen untuk Cloud Percetakan...*")
    
    local_path = await message.download()
    await msg.edit_text("⚡ *Sedang menyinkronkan file cetak...*")
    
    try:
        # Menggunakan server Litterbox yang mengizinkan semua jenis ekstensi file (.rar, .zip, .cdr)
        with open(local_path, "rb") as file_data:
            response = requests.post(
                "https://catbox.moe",
                data={"reqtype": "fileupload", "time": "72h"}, # File disimpan selama 72 jam (3 hari), sangat pas untuk antrean cetak bisnis
                files={"fileToUpload": file_data}
            )
        
        if response.status_code == 200 and response.text.startswith("https"):
            # Mengambil nama file dari server penyimpanan
            file_name = response.text.replace("https://catbox.moe", "").strip()
            
            # Membungkus dengan subdomain bisnis Anda
            download_link = f"{CUSTOM_DOMAIN}/{file_name}"
            
            await msg.edit_text(
                f"✅ *File Sukses Terunggah!*\n\n"
                f"🔗 *Tautan Unduh Publik (Aktif 3 Hari):*\n{download_link}\n\n"
                f"_Tautan resmi Cloud Percetakan Prima Digital Print._"
            )
        else:
            await msg.edit_text("❌ Server penyimpanan menolak berkas. Sila coba beberapa saat lagi.")
            
    except Exception as e:
        await msg.edit_text(f"❌ Terjadi galat sistem: {str(e)}")
    
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)

if __name__ == "__main__":
    print("--- BOT CLOUD PERCETAKAN SUKSES AKTIF ---")
    app.run()
