import tkinter as tk
from tkinter import ttk
from datetime import datetime
from app.core.stok_core import generate_kartu_stok, get_produk_id_by_nama, get_daftar_nama_barang, get_stok_akhir_semua_produk

def buat_frame_stok(parent):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tab_stok = ttk.Frame(frame)
    frame.add(tab_stok, text="Stok")

    daftar_nama_barang = get_daftar_nama_barang()
    daftar_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    daftar_tahun = ["2025", "2026"] # bisa diganti dengan query log_stok
    
    filter_frame = tk.Frame(tab_stok)
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Barang:").grid(row=0, column=0)
    barang_combo = ttk.Combobox(filter_frame, values=daftar_nama_barang)
    barang_combo.grid(row=0, column=1)

    tk.Label(filter_frame, text="Bulan:").grid(row=0, column=2)
    bulan_combo = ttk.Combobox(filter_frame, values=daftar_bulan)
    bulan_combo.grid(row=0, column=3)

    tk.Label(filter_frame, text="Tahun:").grid(row=0, column=4)
    tahun_combo = ttk.Combobox(filter_frame, values=daftar_tahun)
    tahun_combo.grid(row=0, column=5)

    tree_frame = tk.Frame(tab_stok)
    tree_frame.pack(fill="both", expand=True)

    stok_tree = ttk.Treeview(tree_frame, columns=("Tanggal", "Awal", "Masuk", "Keluar", "Akhir"), show="headings")
    for col in stok_tree["columns"]:
        stok_tree.heading(col, text=col)
        stok_tree.column(col, anchor="center", width=80)
    stok_tree.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=stok_tree.yview)
    scrollbar.pack(side="right", fill="y")
    stok_tree.config(yscrollcommand=scrollbar.set)

    def tampilkan_kartu_stok():
        nama_barang = barang_combo.get()
        bulan_index = bulan_combo.current() + 1  # JANUARI = index 0
        tahun_str = tahun_combo.get()

        if not nama_barang or bulan_index == -1 or not tahun_str:
            return

        bulan = bulan_index + 1
        tahun = int(tahun_str)
        produk_id = get_produk_id_by_nama(nama_barang)
        if produk_id is None:
            return
        
        kartu = generate_kartu_stok(produk_id, bulan, tahun)
        stok_tree.delete(*stok_tree.get_children())
        for row in kartu:
            stok_tree.insert("", "end", values=(row.get("tanggal"), "", f"{row.get('awal', 0):,}", f"{row.get('masuk', 0):,}", f"{row.get('akhir', 0):,}"))
                             
    tk.Button(filter_frame, text="Tampilkan", command=tampilkan_kartu_stok).grid(row=0, column=6, padx=10)

    # Frame untuk ringkasan stok harian
    frame_ringkasan = tk.Frame(tab_stok)
    frame_ringkasan.pack(pady=10)

    tk.Label(frame_ringkasan, text="Tanggal:").grid(row=0, column=0)
    tanggal_entry = tk.Entry(frame_ringkasan)
    tanggal_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    tree_ringkasan = ttk.Treeview(tab_stok, columns=("Kode", "Nama Produk", "Stok Akhir"), show="headings")
    for col in ("Kode", "Nama Produk", "Stok Akhir"):
        tree_ringkasan.heading(col, text=col)
        tree_ringkasan.column(col, text=col)
    tree_ringkasan.pack(fill="both", expand=True)

    def tampilkan_ringkasan():
        tanggal = tanggal_entry.get().strip()
        tampilkan_stok_harian(tree_ringkasan, tanggal)
    
    tk.Button(frame_ringkasan, text="Tampilkan Stok Hari Ini", command=tampilkan_ringkasan).grid(row=0, column=2, padx=10)

# 
def tampilkan_stok_harian(treeview, tanggal = None):
    if not tanggal:
        tanggal = datetime.now().strftime("%Y-%m-%d")
    data_stok = get_stok_akhir_semua_produk(tanggal)

    treeview.delete(*treeview.get_children())
    for row in data_stok:
        treeview.insert("", "end", values=(row["id"], row["nama"], f"{row['stok']:,}"))


if __name__ == "__main__":
    buat_frame_stok()