import requests
import time
import os
from colorama import Fore, init

init(autoreset=True)

print(Fore.GREEN + "--- EdGhost Discord Typer Tool (Gelismis) ---")
token = input("token: ")

headers = {'Authorization': token, 'Content-Type': 'application/json'}
validate = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

if validate.status_code == 200:
    print(Fore.GREEN + "[✓] Token gecerli!")
else:
    print(Fore.RED + "[X] Token gecersiz!")
    exit()

print("\nModlar:\n1. Tek Mesaj Modu (Ayni mesaji surekli atar)\n2. Kelime Listesi Modu (100+ kelimeyi sirayla atar)")
secim = input("Mod secin (1/2): ")
channel_id = input("Kanal ID girin: ")
delay = float(input("Kac saniyede bir gonderilsin? (Orn: 1.0): "))

url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

if secim == "1":
    mesaj = input("Gonderilecek tek mesajı yazın: ")
    print(Fore.YELLOW + "Sonsuz dongu basladi... Durdurmak icin Termux'ta CTRL+C yapabilirsin.")
    while True:
        requests.post(url, headers=headers, json={"content": mesaj})
        time.sleep(delay)

elif secim == "2":
    # Buraya tırnak içinde virgülle ayırarak istediğin kadar kelime ekleyebilirsin kanka!
    kelimeler = [
        "merhaba", "selam", "naber", "nasılsın", "kod", "python", 
        "termux", "discord", "bot", "ghost", "empire", "yükseliş"
    ]
    
    print(Fore.YELLOW + f"Listede {len(kelimeler)} kelime var. Sirayla gonderiliyor...")
    
    for kelime in kelimeler:
        requests.post(url, headers=headers, json={"content": kelime})
        print(Fore.BLUE + f"Gonderildi: {kelime}")
        time.sleep(delay)
        
    print(Fore.GREEN + "Tüm kelime listesi başarıyla gönderildi!")
