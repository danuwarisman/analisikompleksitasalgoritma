import time
import sys
import csv
import os
import matplotlib.pyplot as plt


sys.setrecursionlimit(100000)

FILENAME = "hasil_benchmark.csv"
LOOPS = 100   # Jumlah loop benchmark (KONSTAN untuk semua N)


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
    if low > high:
        return -1

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search_recursive(arr, low, mid - 1, target)
    else:
        return binary_search_recursive(arr, mid + 1, high, target)

# SIMPAN DATA KE FILE CSV (FORMAT EXCEL)

def simpan_ke_excel(n, t_iter, t_rec, loops, selisih, pemenang):
    file_exists = os.path.isfile(FILENAME)

    try:
        with open(FILENAME, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')

            if not file_exists:
                writer.writerow([
                    "Input (N)",
                    "Jumlah Loop",
                    "Waktu Iteratif (ms)",
                    "Waktu Rekursif (ms)",
                    "Selisih (ms)",
                    "Pemenang"
                ])

            writer.writerow([
                n,
                loops,
                f"{t_iter:.6f}".replace('.', ','),
                f"{t_rec:.6f}".replace('.', ','),
                f"{selisih:.6f}".replace('.', ','),
                pemenang
            ])

    except PermissionError:
        print(f"\n[ERROR] Tutup file '{FILENAME}' di Excel sebelum lanjut.")


# TAMPILKAN GRAFIK HASIL BENCHMARK


def tampilkan_grafik():
    n_values = []
    iter_times = []
    rec_times = []

    try:
        with open(FILENAME, newline='') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                n_values.append(int(row["Input (N)"]))
                iter_times.append(float(row["Waktu Iteratif (ms)"].replace(',', '.')))
                rec_times.append(float(row["Waktu Rekursif (ms)"].replace(',', '.')))

        plt.figure()
        plt.plot(n_values, iter_times, marker='o', label='Iteratif')
        plt.plot(n_values, rec_times, marker='o', label='Rekursif')

        plt.xlabel("Ukuran Input (N)")
        plt.ylabel("Waktu Eksekusi (ms)")
        plt.title("Perbandingan Binary Search Iteratif vs Rekursif")
        plt.legend()
        plt.grid(True)
        plt.show()

    except FileNotFoundError:
        print("File CSV tidak ditemukan.")

# MAIN

def main():
    print("\n==========================================================================")
    print("                 PROGRAM ANALISIS BINARY SEARCH")
    print("==========================================================================\n")

    print(f"{'No':<3} | {'Input (N)':<12} | {'Iteratif (ms)':<15} | {'Rekursif (ms)':<15} | {'Kesimpulan'}")
    print("-" * 80)

    nomor = 1

    while True:
        try:
            user_input = input(f"\n>> Masukkan N ke-{nomor} (atau 'q' untuk keluar): ")
            if user_input.lower() == 'q':
                break

            n = int(user_input)
            if n <= 0:
                continue

        except ValueError:
            print("[!] Harap masukkan angka bulat.")
            continue

        data = list(range(0, n * 2, 2))
        target = data[-1]  # Worst case

        # Benchmark Iteratif
        start = time.perf_counter()
        for _ in range(LOOPS):
            binary_search_iterative(data, target)
        t_iter = (time.perf_counter() - start) * 1000

        # Benchmark Rekursif
        start = time.perf_counter()
        for _ in range(LOOPS):
            binary_search_recursive(data, 0, len(data) - 1, target)
        t_rec = (time.perf_counter() - start) * 1000

        selisih = abs(t_iter - t_rec)
        pemenang = "Iteratif" if t_iter < t_rec else "Rekursif"

        simpan_ke_excel(n, t_iter, t_rec, LOOPS, selisih, pemenang)

        print(f"{nomor:<3} | {n:<12} | {t_iter:<15.4f} | {t_rec:<15.4f} | {pemenang} Unggul")

        nomor += 1

    print("\n==========================================================================")
    print("Data selesai disimpan. Silakan buka file Excel.")
    tampilkan_grafik()


if __name__ == "__main__":
    main()
