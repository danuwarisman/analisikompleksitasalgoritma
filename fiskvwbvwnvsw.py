import time
import sys
import csv
import os

# Konfigurasi batas rekursi
sys.setrecursionlimit(100000)

# Nama file Output
FILENAME = "hasil_benchmark.csv"

# 1. ALGORITMA BINARY SEARCH
def binary_search_iterative(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def binary_search_recursive(arr, low, high, target):
    if high >= low:
        mid = (high + low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return binary_search_recursive(arr, low, mid - 1, target)
        else:
            return binary_search_recursive(arr, mid + 1, high, target)
    else:
        return -1

# 2. FUNGSI SIMPAN KE EXCEL (FORMAT TABEL)
def simpan_ke_excel(n, t_iter, t_rec, loops, selisih, pemenang):
    file_exists = os.path.isfile(FILENAME)
    
    try:
        with open(FILENAME, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            
            if not file_exists:
                writer.writerow(["Input (N)", "Jumlah Loop", "Waktu Iteratif (ms)", "Waktu Rekursif (ms)", "Selisih (ms)", "Pemenang"])
            
            # Isi Data
            t_iter_str = f"{t_iter:.6f}".replace('.', ',')
            t_rec_str = f"{t_rec:.6f}".replace('.', ',')
            selisih_str = f"{selisih:.6f}".replace('.', ',')
            
            writer.writerow([n, loops, t_iter_str, t_rec_str, selisih_str, pemenang])
            
    except PermissionError:
        print(f"\n[ERROR] Tutup dulu file '{FILENAME}' di Excel sebelum lanjut!")

# 3. PROGRAM UTAMA
def main():
    print("\n==========================================================================")
    print("                 PROGRAM ANALISIS BINARY SEARCH")
    print("==========================================================================\n")
    
    # Cetak Header Tabel di Terminal
    print(f"{'No':<3} | {'Input (N)':<12} | {'Iteratif (ms)':<15} | {'Rekursif (ms)':<15} | {'Kesimpulan':<15}")
    print("-" * 75)
    
    nomor = 1
    
    while True:
        try:
            input_str = input(f"\n>> Masukkan N ke-{nomor} (atau 'q' keluar): ")
            if input_str.lower() == 'q': break
            
            n = int(input_str)
            if n <= 0: continue
            
        except ValueError:
            print("   [!] Harap masukkan angka bulat.")
            continue

        # Setup Data
        data_id = list(range(0, n * 2, 2))
        target = data_id[-1] # Worst case
        
        if n < 1000: loops = 100000
        elif n < 100000: loops = 10000
        else: loops = 1000
            
        # Proses Benchmarking (Silent)
        # Iteratif
        start = time.perf_counter()
        for _ in range(loops): binary_search_iterative(data_id, target)
        t_iter = (time.perf_counter() - start) * 1000 
        
        # Rekursif
        start = time.perf_counter()
        for _ in range(loops): binary_search_recursive(data_id, 0, len(data_id)-1, target)
        t_rec = (time.perf_counter() - start) * 1000 

        # Hitung Data
        selisih = abs(t_iter - t_rec)
        pemenang = "Iteratif" if t_iter < t_rec else "Rekursif"
        
        simpan_ke_excel(n, t_iter, t_rec, loops, selisih, pemenang)
        
        sys.stdout.write("\033[F") 
        sys.stdout.write("\033[K") 
        print(f"{nomor:<3} | {n:<12} | {t_iter:<15.4f} | {t_rec:<15.4f} | {pemenang} Unggul")
        
        nomor += 1

    print("\n==========================================================================")
    print("Data selesai disimpan. Silakan buka file Excel-nya.")

if __name__ == "__main__":
    main()
