#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BBFS 8 DIGIT INTELLIGENCE v7.1
✅ Multi Pasaran
✅ BBFS 8 Digit
✅ Backtest 2D & 3D Otomatis
"""

import os
import sys
import time
from collections import Counter
from typing import List, Dict, Tuple

# ──────────────────────────────────────────────────────────────
# Warna & Tampilan
# ──────────────────────────────────────────────────────────────
RESET = "\033[0m"

def colored(text: str, color: str = "white", style: str = "normal") -> str:
    styles = {"normal": 0, "bold": 1, "dim": 2}
    colors = {
        "red": 31, "green": 32, "yellow": 33, "blue": 34,
        "magenta": 35, "cyan": 36, "white": 37,
        "bright_red": 91, "bright_green": 92, "bright_yellow": 93,
        "bright_blue": 94, "bright_magenta": 95, "bright_cyan": 96,
    }
    s = styles.get(style, 0)
    c = colors.get(color, 37)
    return f"\033[{s};{c}m{text}{RESET}"

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# ──────────────────────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────────────────────
BANNER = colored(r"""
   ____           _       _    ____ _  __
  / ___| ___ _ __| |_ ___| |  / ___| |/ /
 | |  _ / _ \ '__| __/ _ \ | | |   | ' / 
 | |_| |  __/ |  | ||  __/ | | |___| . \ 
  \____|\___|_|   \__\___|_|  \____|_|\_\
                                        
        🌏 BBFS 8 DIGIT v7.1
     + Backtest 3D Otomatis
""", "bright_cyan", "bold")

# ──────────────────────────────────────────────────────────────
# Konfigurasi Pasaran
# ──────────────────────────────────────────────────────────────
MARKETS = {
    "1": "hongkong_pools",
    "2": "sydney_pools",
    "3": "hongkong_lotto",
    "4": "sydney_lotto"
}

MARKET_NAMES = {
    "hongkong_pools": "🇭🇰 Hongkong Pools",
    "sydney_pools": "🇦🇺 Sydney Pools",
    "hongkong_lotto": "🎰 Hongkong Lotto",
    "sydney_lotto": "🎯 Sydney Lotto"
}

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_filepath(market: str) -> str:
    return os.path.join(DATA_DIR, f"{market}.txt")

def load_history(market: str) -> List[str]:
    filepath = get_filepath(market)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            return [line.strip() for line in f if line.strip().isdigit() and len(line.strip()) == 4]
    except:
        return []

def save_history(market: str, history: List[str]) -> None:
    filepath = get_filepath(market)
    with open(filepath, "w") as f:
        f.write("\n".join(history))

# ──────────────────────────────────────────────────────────────
# Deteksi Pola Otomatis
# ──────────────────────────────────────────────────────────────
def deteksi_pola(history: List[str]) -> Dict[str, any]:
    if len(history) < 5:
        return {"pola": "data_kurang"}

    ekors = [res[2:] for res in history]
    digits = [d for res in history for d in res]
    int_ekors = [int(e) for e in ekors]

    pola = {}

    # 1. 2D Terpanas
    freq_2d = Counter(ekors)
    pola["2d_terpanas"] = [pair for pair, _ in freq_2d.most_common(15)]

    # 2. Shio Ekor
    shio_ekor = [e % 12 for e in int_ekors]
    freq_shio = Counter(shio_ekor)
    pola["shio_ekor_kuat"] = [s for s, _ in freq_shio.most_common(3)]

    # 3. Kepala Kuat (digit ke-2)
    kepala = [res[1] for res in history]
    freq_kepala = Counter(kepala)
    pola["kepala_kuat"] = [d for d, _ in freq_kepala.most_common(3)]

    # 4. Angka Dingin
    freq_digit = Counter(digits)
    pola["angka_dingin"] = [d for d, cnt in freq_digit.items() if cnt < 2]

    # 5. Tren Genap-Ganjil
    genap = sum(1 for d in digits if int(d) % 2 == 0)
    ganjil = len(digits) - genap
    pola["tren_genap_ganjil"] = "genap" if genap > ganjil else "ganjil"

    # 6. Rata-rata perubahan ekor
    runs = []
    for i in range(1, len(int_ekors)):
        diff = int_ekors[i] - int_ekors[i-1]
        runs.append(diff)
    avg_run = sum(runs) / len(runs) if runs else 0
    pola["rata2_perubahan_ekor"] = round(avg_run, 1)

    return pola

# ──────────────────────────────────────────────────────────────
# Prediksi BBFS 8 Digit
# ──────────────────────────────────────────────────────────────
def generate_bbfs_8_cerdas(history: List[str]) -> Tuple[List[str], List[str]]:
    if len(history) < 10:
        return ["1", "2", "3", "4", "5", "6", "7", "8"], ["Data kurang"]

    pola = deteksi_pola(history)
    candidates = Counter()

    # 1. Dari 2D terpanas
    for d2 in pola["2d_terpanas"]:
        candidates[d2[0]] += 8
        candidates[d2[1]] += 10

    # 2. Shio ekor kuat
    for shio in pola["shio_ekor_kuat"]:
        digit = str(shio % 10)
        candidates[digit] += 6

    # 3. Kepala kuat
    for d in pola["kepala_kuat"]:
        candidates[d] += 5

    # 4. Angka dingin
    for d in pola["angka_dingin"]:
        candidates[d] += 12

    # 5. Tren genap/ganjil
    if pola["tren_genap_ganjil"] == "genap":
        for d in "02468":
            candidates[d] += 3
    else:
        for d in "13579":
            candidates[d] += 3

    # 6. Prediksi dari tren ekor
    last_ekor = int(history[-1][2:])
    pred_ekor = int((last_ekor + pola["rata2_perubahan_ekor"]) % 100)
    d3, d4 = f"{pred_ekor:02d}"
    candidates[d3] += 4
    candidates[d4] += 5

    top_8 = [item[0] for item in candidates.most_common(8)]
    alasan = [
        f"2D Panas: {len(pola['2d_terpanas'])} data",
        f"Shio: {pola['shio_ekor_kuat']}",
        f"Dingin: {pola['angka_dingin']}",
        f"Tren: {pola['tren_genap_ganjil']}, Δ={pola['rata2_perubahan_ekor']}",
        f"Prediksi ekor: {d3}{d4}"
    ]

    return sorted(top_8, key=lambda x: int(x)), alasan

# ──────────────────────────────────────────────────────────────
# Backtest 2D: Apakah 2D masuk BBFS?
# ──────────────────────────────────────────────────────────────
def backtest_2d(history: List[str]) -> None:
    if len(history) < 2:
        print(colored("\n❌ Butuh minimal 2 data!", "red"))
        input(colored("Enter...", "dim"))
        return

    tembus = 0
    total = len(history) - 1

    print(colored(f"\n🔍 BACKTEST 2D: Apakah 2D MASUK BBFS?", "bright_yellow", "bold"))

    for i in range(total):
        prev_batch = history[:i+1]
        actual = history[i+1]
        ekor = actual[2:]
        d3, d4 = ekor[0], ekor[1]

        bbfs, _ = generate_bbfs_8_cerdas(prev_batch)
        bbfs_set = set(bbfs)

        match = d3 in bbfs_set and d4 in bbfs_set
        status = "✅" if match else "❌"

        if match:
            tembus += 1
        print(f"{status} {prev_batch[-1]} → {actual} | 2D: {ekor}")

    akurasi = (tembus / total) * 100
    warna = "green" if akurasi >= 90 else "yellow" if akurasi >= 70 else "red"
    print(colored(f"\n🎯 Akurasi 2D: {tembus}/{total} → {akurasi:.1f}%", warna, "bold"))
    input(colored("\nTekan Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Backtest 3D: Apakah 3 digit terakhir MASUK BBFS?
# ──────────────────────────────────────────────────────────────
def backtest_3d(history: List[str]) -> None:
    if len(history) < 2:
        print(colored("\n❌ Butuh minimal 2 data!", "red"))
        input(colored("Enter...", "dim"))
        return

    tembus = 0
    total = len(history) - 1

    print(colored(f"\n🔍 BACKTEST 3D: Apakah 3D MASUK BBFS?", "bright_magenta", "bold"))

    for i in range(total):
        prev_batch = history[:i+1]
        actual = history[i+1]
        t3_actual = actual[1:]  # ratusan, puluhan, satuan
        d1, d2, d3 = t3_actual[0], t3_actual[1], t3_actual[2]

        bbfs, _ = generate_bbfs_8_cerdas(prev_batch)
        bbfs_set = set(bbfs)

        # Cek apakah ketiga digit ada di BBFS
        match = d1 in bbfs_set and d2 in bbfs_set and d3 in bbfs_set
        status = "✅" if match else "❌"

        if match:
            tembus += 1
        print(f"{status} {prev_batch[-1]} → {actual} | 3D: {t3_actual}")

    akurasi = (tembus / total) * 100
    warna = "green" if akurasi >= 85 else "yellow" if akurasi >= 60 else "red"
    print(colored(f"\n🎯 Akurasi 3D: {tembus}/{total} → {akurasi:.1f}%", warna, "bold"))
    input(colored("\nTekan Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Animasi
# ──────────────────────────────────────────────────────────────
def loading_animation():
    for _ in range(15):
        sys.stdout.write("\r" + colored("🧠", "cyan") + " AI menganalisis...")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ──────────────────────────────────────────────────────────────
# Menu Utama
# ──────────────────────────────────────────────────────────────
def menu():
    while True:
        clear_screen()
        print(BANNER)
        print(colored("\nPilih Pasaran:", "bright_blue", "bold"))
        for key, code in MARKETS.items():
            history = load_history(code)
            name = MARKET_NAMES[code]
            print(f" {key}. {name} {colored(f'({len(history)} data)', 'dim')}")

        print(colored("\nAksi:", "bright_blue", "bold"))
        print(" 5. Prediksi BBFS 8 Digit")
        print(" 6. Backtest 2D Otomatis")
        print(" 7. Backtest 3D Otomatis")
        print(" 8. Hapus Data Pasaran")
        print(" 9. Keluar\n")

        choice = input(colored("Pilih: ", "yellow")).strip()

        if choice in MARKETS:
            market_code = MARKETS[choice]
            market_name = MARKET_NAMES[market_code]
            history = load_history(market_code)

            print(colored(f"\n📁 {market_name} | {len(history)} data", "blue"))
            print(colored("\nMasukkan 4D (kosongkan untuk kembali):", "cyan"))
            added = 0
            while True:
                inp = input(f"Hasil {len(history) + added + 1}: ").strip()
                if not inp:
                    break
                if inp.isdigit() and len(inp) == 4:
                    history.append(inp)
                    added += 1
                    print(colored("✓", "green"))
                else:
                    print(colored("✗ 4 digit!", "red"))
            if added > 0:
                save_history(market_code, history)
                print(colored(f"💾 Disimpan: {market_name}", "bright_green"))

        elif choice == "5":
            print(colored("\nPilih pasaran untuk prediksi:", "cyan"))
            for key, code in MARKETS.items():
                name = MARKET_NAMES[code]
                hist = load_history(code)
                print(f" {key}. {name} {colored(f'({len(hist)} data)', 'dim')}")
            pick = input(colored("Pilih: ", "yellow")).strip()
            if pick not in MARKETS:
                print(colored("Pilihan salah!", "red"))
                input(colored("Enter...", "dim"))
                continue

            market_code = MARKETS[pick]
            market_name = MARKET_NAMES[market_code]
            history = load_history(market_code)

            if len(history) < 10:
                print(colored(f"\n⚠️ Butuh 10+ data {market_name}!", "yellow"))
                input(colored("Enter...", "dim"))
                continue

            loading_animation()
            bbfs, alasan = generate_bbfs_8_cerdas(history)
            clear_screen()
            print(BANNER)
            print(colored(f"\n🎯 PASARAN: {market_name}", "bright_magenta", "bold"))
            print(colored(f"BBFS 8 DIGIT:", "bright_green", "bold"))
            print(" → " + colored("  ".join(bbfs), "bright_yellow", "bold"))
            print(colored(f"\n💡 Alasan:", "dim"))
            for a in alasan:
                print(f"   • {a}")
            input(colored("\n\nEnter untuk kembali...", "dim"))

        elif choice == "6":
            print(colored("\nPilih pasaran untuk backtest 2D:", "cyan"))
            for key, code in MARKETS.items():
                name = MARKET_NAMES[code]
                hist = load_history(code)
                print(f" {key}. {name} {colored(f'({len(hist)} data)', 'dim')}")
            pick = input(colored("Pilih: ", "yellow")).strip()
            if pick not in MARKETS:
                print(colored("Salah!", "red"))
                input(colored("Enter...", "dim"))
                continue
            history = load_history(MARKETS[pick])
            backtest_2d(history)

        elif choice == "7":
            print(colored("\nPilih pasaran untuk backtest 3D:", "cyan"))
            for key, code in MARKETS.items():
                name = MARKET_NAMES[code]
                hist = load_history(code)
                print(f" {key}. {name} {colored(f'({len(hist)} data)', 'dim')}")
            pick = input(colored("Pilih: ", "yellow")).strip()
            if pick not in MARKETS:
                print(colored("Salah!", "red"))
                input(colored("Enter...", "dim"))
                continue
            history = load_history(MARKETS[pick])
            backtest_3d(history)

        elif choice == "8":
            print(colored("\nPilih pasaran untuk hapus:", "red"))
            for key, code in MARKETS.items():
                name = MARKET_NAMES[code]
                hist = load_history(code)
                print(f" {key}. {name} {colored(f'({len(hist)} data)', 'dim')}")
            pick = input(colored("Pilih: ", "red")).strip()
            if pick not in MARKETS:
                continue
            code = MARKETS[pick]
            if input(colored(f"Hapus {MARKET_NAMES[code]}? (y/t): ", "red")).lower() == 'y':
                filepath = get_filepath(code)
                if os.path.exists(filepath):
                    os.remove(filepath)
                print(colored(f"🗑️ {MARKET_NAMES[code]} dihapus", "green"))
                time.sleep(1)

        elif choice == "9":
            print(colored("\nSemoga JP besar di semua pasaran! 🍀", "bright_yellow"))
            break

        else:
            print(colored("Pilih 1-9!", "red"))
            input(colored("Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Jalankan
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(colored("\n\nDihentikan.", "red"))
