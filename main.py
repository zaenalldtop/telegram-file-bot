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
        # Langkah 1: Meminta alamat server kosong yang tersedia dari GoFile API
        server_response = requests.get("https://gofile.io")
        server_data = server_response.json()
        
        if server_data.get("status") == "ok":
            best_server = server_data["data"]["servers"][0]["name"]
            
            # Langkah 2: Mengunggah berkas ke server terbaik GoFile
            with open(local_path, "rb") as file_data:
                upload_url = f"https://{best_server}.gofile.io/contents/uploadfile"
                response = requests.post(upload_url, files={"file": file_data})
            
            res_data = response.json()
            if response.status_code == 200 and res_data.get("status") == "ok":
                # Mengambil ID berkas unik dari GoFile
                file_id = res_data["data"]["fileId"]
                
                # Membungkus dengan domain kustom bisnis Anda
                download_link = f"{CUSTOM_DOMAIN}/{file_id}"
                
                await msg.edit_text(
                    f"✅ *File Sukses Terunggah!*\n\n"
                    f"🔗 *Tautan Unduh Publik:*\n{download_link}\n\n"
                    f"_Tautan resmi Cloud Percetakan Prima Digital Print._"
                )
            else:
                await msg.edit_text("❌ Server GoFile menolak berkas. Sila coba sekejap lagi.")
        else:
            await msg.edit_text("❌ Gagal mendapatkan jalur server penyimpanan.")
            
    except Exception as e:
        await msg.edit_text(f"❌ Terjadi galat jaringan: {str(e)}")
    
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)

if __name__ == "__main__":
    print("--- BOT CLOUD PERCETAKAN GOFILE AKTIF ---")
    app.run()
