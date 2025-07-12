import csv
import os
from datetime import datetime

MENU_FILE = "menu.csv"
TRANSAKSI_FILE = "transaksi.csv"

def init_files():
    if not os.path.exists(MENU_FILE):
        with open(MENU_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([
                # Kategori, Nama, Harga
                ["Kopi", "Kopi Hitam", 10000],
                ["Kopi", "Cappuccino", 15000],
                ["Kopi", "Latte", 17000],
                ["Kopi", "Espresso", 12000],
                ["Kopi", "Americano", 13000],
                ["Kopi", "Caramel Macchiato", 20000],
                ["Kopi", "Vanilla Latte", 19000],
                ["Kopi", "Mocha", 18000],

                ["Non-Kopi", "Matcha Latte", 22000],
                ["Non-Kopi", "Chocolate Milk", 15000],
                ["Non-Kopi", "Red Velvet", 17000],
                ["Non-Kopi", "Thai Tea", 16000],
                ["Non-Kopi", "Teh Tarik", 12000],
                ["Non-Kopi", "Air Mineral", 5000],

                ["Makanan", "Roti Bakar", 12000],
                ["Makanan", "Croissant", 15000],
                ["Makanan", "Donat", 8000],
                ["Makanan", "Cheesecake", 20000]
            ])
    if not os.path.exists(TRANSAKSI_FILE):
        with open(TRANSAKSI_FILE, mode='w', newline='') as f:
            pass

def tampilkan_menu():
    print("\n=== MENU COFFEE SHOP ===")
    with open(MENU_FILE, mode='r') as file:
        reader = csv.reader(file)
        menu = list(reader)

    kategori = {
        "Kopi": [],
        "Non-Kopi": [],
        "Makanan": []
    }

    for item in menu:
        if len(item) == 3:
            kategori[item[0]].append(item)

    nomor = 1
    mapping = {}
    for k in kategori:
        print(f"\n--- {k.upper()} ---")
        for item in kategori[k]:
            print(f"{nomor}. {item[1]} - Rp{item[2]}")
            mapping[nomor] = item
            nomor += 1

    return mapping


def pesan_kopi():
    mapping = tampilkan_menu()
    try:
        nomor = int(input("\nPilih nomor menu: "))
        jumlah = int(input("Jumlah pesanan: "))
    except ValueError:
        print("❌ Input harus angka!\n")
        return

    if nomor in mapping:
        kategori, nama, harga = mapping[nomor]
        total = int(harga) * jumlah
        print(f"✅ Anda memesan {jumlah} {nama} | Total: Rp{total}")
        tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(TRANSAKSI_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tanggal, nama, jumlah, total])
    else:
        print("❌ Nomor menu tidak valid.\n")

def login_admin():
    print("\n=== Login Admin ===")
    username = input("Username: ")
    password = input("Password: ")
    return username == "admin" and password == "admin123"

def tambah_menu():
    nama = input("Nama kopi baru: ")
    harga = input("Harga: ").replace(".", "").replace(",", "")
    try:
        harga = int(harga)
    except ValueError:
        print("❌ Harga harus angka!\n")
        return

    with open(MENU_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nama, harga])
    print("✅ Menu berhasil ditambahkan.\n")

def edit_menu():
    tampilkan_menu()
    try:
        nomor = int(input("Pilih nomor menu yang ingin diedit: ")) - 1
    except ValueError:
        print("❌ Input tidak valid.")
        return

    with open(MENU_FILE, mode='r') as file:
        menu = list(csv.reader(file))

    if 0 <= nomor < len(menu):
        nama_baru = input(f"Nama baru (kosongkan jika tidak diubah): ") or menu[nomor][0]
        harga_baru = input(f"Harga baru (kosongkan jika tidak diubah): ")
        harga_baru = harga_baru.replace(".", "").replace(",", "") or menu[nomor][1]
        try:
            menu[nomor] = [nama_baru, int(harga_baru)]
        except ValueError:
            print("❌ Harga tidak valid.\n")
            return
        with open(MENU_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(menu)
        print("✅ Menu berhasil diedit.\n")
    else:
        print("❌ Nomor menu tidak valid.\n")

def hapus_menu():
    tampilkan_menu()
    try:
        nomor = int(input("Pilih nomor menu yang ingin dihapus: ")) - 1
    except ValueError:
        print("❌ Input tidak valid.")
        return

    with open(MENU_FILE, mode='r') as file:
        menu = list(csv.reader(file))

    if 0 <= nomor < len(menu):
        menu.pop(nomor)
        with open(MENU_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(menu)
        print("✅ Menu berhasil dihapus.\n")
    else:
        print("❌ Nomor menu tidak valid.\n")

def laporan_penjualan():
    print("\n=== Laporan Penjualan ===")
    total = 0
    with open(TRANSAKSI_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"{row[0]} - {row[1]} x{row[2]} = Rp{row[3]}")
            total += int(row[3])
    print(f"Total Penjualan: Rp{total}\n")

def menu_admin():
    while True:
        print("""
=== MENU ADMIN ===
1. Tambah Menu 
2. Edit Menu
3. Hapus Menu
4. Laporan Penjualan
0. Logout
""")
        pilihan = input("Pilih: ")
        if pilihan == "1":
            tambah_menu()
        elif pilihan == "2":
            edit_menu()
        elif pilihan == "3":
            hapus_menu()
        elif pilihan == "4":
            laporan_penjualan()
        elif pilihan == "0":
            break
        else:
            print("❌ Pilihan tidak valid.\n")

def main():
    init_files()
    while True:
        print("""
=== SISTEM MANAJEMEN COFFEE SHOP ===
1. Kasir 
2. Admin
0. Keluar
""")
        pilihan = input("Pilih: ")
        if pilihan == "1":
            pesan_kopi()
        elif pilihan == "2":
            if login_admin():
                menu_admin()
            else:
                print("❌ Login gagal.\n")
        elif pilihan == "0":
            print("Terima kasih. Sampai jumpa!\n")
            break
        else:
            print("❌ Pilihan tidak valid.\n")

if __name__ == "__main__":
    main()
