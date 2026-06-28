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

print("\nModlar:\n1. Tek Mesaj Modu (Ayni mesaji surekli atar)\n2. Kelime Listesi Modu (Kelimeleri sirayla atar)")
secim = input("Mod secin (1/2): ")
channel_id = input("Kanal ID girin: ")
delay = float(input("Kac saniyede bir gonderilsin? (Orn: 1.0): "))

url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

if secim == "1":
    mesaj = input("Gonderilecek tek mesaji yazin: ")
    print(Fore.YELLOW + "Sonsuz dongu basladi... Durdurmak icin Termux'ta CTRL+C yapabilirsiniz.")
    while True:
        requests.post(url, headers=headers, json={"content": mesaj})
        time.sleep(delay)

elif secim == "2":
    # 30 tane kelime boşluğun hazır kanka, içlerini doldurabilirsin:
    kelimeler = [
        "Lan", "Köpek", "Senin", "Anani", "S4kerim",
        "Sen", "Kimsin", "Baş", "Kaldiriyon", "Seni",
        "Yerden", "Yere", "Vururum", "#Domal", "Lan",
        "Benim", "Karşimda", "Floodu", "Karşila", "İt",
        "Seni", "Mal", "OROSPU", "ÇOÇUĞU ", "Baş",
        "Kaldir", "Lan", "Amina", "Korum", "Senin"
    ]

    print(Fore.YELLOW + f"\nListede {len(kelimeler)} kelime var. Sonsuz dongu basladi... Durdurmak icin Termux'ta CTRL+C yapabilirsiniz.")
    
    while True:
        for kelime in kelimeler:
            requests.post(url, headers=headers, json={"content": kelime})
            print(Fore.BLUE + f"[*] Gönderildi: {kelime}")
            time.sleep(delay)

else:
    print(Fore.RED + "Gecersiz secim yapildi!")
