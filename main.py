import os
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", "39206186").strip()) 
API_HASH = os.environ.get("API_HASH", "f1f40463bd79b121b4bff7a76c47ac16").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8913324140:AAFt0rHCeNPScTHThGPPmIR4S2cdLiZfMw4").strip()

# ⚠️ TEMPELKAN URL .WORKERS.DEV ANDA DI SINI (Ganti teks di bawah ini dengan hasil salinan dari Cloudflare)
CLOUDFLARE_WORKER_URL = "https://cloud.primadigitalprint.com/" 

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Server Cloud Percetakan Aktif")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

app = Client("file_to_link_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def generate_link(client, message):
    local_path = await message.download()
    file_name = os.path.basename(local_path)
    
    # Membersihkan URL dari tanda garis miring di ujung jika ada
    base_url = CLOUDFLARE_WORKER_URL.rstrip('/')
    
    try:
        # Mengirim berkas langsung ke server internal Cloudflare Workers Anda
        with open(local_path, "rb") as file_data:
            response = requests.post(
                f"{base_url}/d/{file_name}",
                data=file_data
            )
        
        if response.status_code == 200:
            download_link = f"{base_url}/d/{file_name}".replace(" ", "%20")
            await message.reply_text(
                f"✅ *File Sukses Terunggah!*\n\n"
                f"🔗 *Tautan Unduh Publik:*\n{download_link}\n\n"
                f"_Tautan resmi Penyimpanan Berkas Prima Digital Print._"
            )
        else:
            await message.reply_text(f"❌ Cloudflare menolak berkas (Status: {response.status_code})")
            
    except Exception as e:
        await message.reply_text(f"❌ Terjadi galat jaringan: {str(e)}")
    
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    print("--- BOT JALUR DIREK WORKERS AKTIF ---")
    app.run()
