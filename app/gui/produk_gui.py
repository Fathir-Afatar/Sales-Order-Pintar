import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from app.core.product_core import tambah_produk, semua_produk,  update_produk, hapus_produk, bersihkan_angka, get_kategori_id_by_nama, ambil_semua_kategori, ambil_produk_by_kategori_id, tambah_kategori
from app.constants.config import get_connection

def refresh_tree(kategori=None, nama_produk=None):
    print("[INFO] Memuat ulang daftar produk . . .")
    
    for item in tree.get_children():
        tree.delete(item)

    for p in semua_produk():
        print("[DEBUG] Produk:", p.get("nama_produk"), " | Kategori:", p.get("nama_kategori", "Kategori tidak tersedia"))

        # Filter Kategori

        if kategori and kategori not in (p.get("nama_kategori") or "").lower():
            continue
        # Filter nama (case-insensitive)

        if nama_produk and nama_produk.lower() not in p["nama_produk"].lower():
            continue

        tree.insert("", tk.END, values=(p["id_produk"], p.get("nama_produk",""), p.get("kode_produk",""), p.get("nama_kategori",""), p.get("merk",""), format_rupiah(p.get("harga_beli",0)), format_rupiah(p.get("harga_jual",0)), p.get("stok",0), p.get("berat",0)))


def filter_kategori_dan_nama():
    kategori = entry_filter_kategori.get().strip().lower()
    keyword = entry_cari.get().strip().lower()
    print(f"[INFO] Terapkan filter: Nama = '{keyword}', Kategori = '{kategori}'")
    refresh_tree(kategori=kategori, nama_produk=keyword)

def filter_produk_by_kategori(nama_kategori):
    tree.delete(*tree.get_children())

    if nama_kategori == "Semua":
        produk_list = semua_produk()
    else:
        kategori_id = get_kategori_id_by_nama(nama_kategori)
        produk_list = ambil_produk_by_kategori_id(kategori_id)
    for p in produk_list:
        tree.insert("", tk.END, values=(p["id_produk"], p.get("nama_produk", ""), p.get("kode_produk", ""), nama_kategori, p.get("merk", ""), format_rupiah(p.get("harga_beli", 0)), format_rupiah(p.get("harga_jual", 0)), p.get("stok", 0), p.get("berat",0)))

def cari_produk_nama():
    keyword = entry_cari.get()
    refresh_tree(nama_produk=keyword)


def reset_filter():
    entry_filter_kategori.delete(0, tk.END) # Kosongkan pilihan kategori
    entry_cari.delete(0, tk.END)
    refresh_tree() # Tampilkan semua data
    print("[INFO] Filter direset.")
    
def on_tree_select(event):
    if not entry_nama or not str(entry_nama):
        print("[WARNING] entry_nama belum tersedia atau sudah dihapus.")
        return
    selected = tree.focus()
    if not selected: return
    values = tree.item(selected, 'values')
    entry_nama.delete(0, tk.END)
    entry_nama.insert(0, values[1])
    entry_kode.delete(0, tk.END)
    entry_kode.insert(0, values[2])
    entry_harga_jual.delete(0, tk.END)
    entry_harga_jual.insert(0, values[3])
    entry_stok.delete(0, tk.END)
    entry_stok.insert(0, values[4])
    if not buka_form_tambah_produk:
        print("[INFO] Form edit belum aktif.")
        return
    # ID disimpan untuk edit/delete

    global selected_id
    selected_id = values[0]

form_produk_aktif = False

def buka_form_tambah_kategori():
    form_kategori = tk.Toplevel(window)
    form_kategori.title("Tambah Kategori")
    form_kategori.geometry("300x150")

    tk.Label(form_kategori, text="Nama Kategori").pack(pady=(20, 5))
    entry_nama_kategori = tk.Entry(form_kategori)
    entry_nama_kategori.pack(pady=5)

    def simpan_kategori():
        nama = entry_nama_kategori.get().strip()
        if not nama:
            messagebox.showerror("Error", "nama kategori tidak boleh kosong.")
            return
        if tambah_kategori(nama):
            messagebox.showinfo("Berhasil", f"Kategori '{nama}' berhasil ditambahkan.")
            form_kategori.destroy()
            # Refresh Combobox kategori di form produk jika tersedia
            try:
                kategori_baru = ambil_semua_kategori()
                entry_kategori["values"] = kategori_baru
                entry_kategori.set(nama)
            except:
                print("[WARNING] Tidak bisa refresh Combobox kategori.")
        else:
                messagebox.showerror("Gagal", f"Kategori '{nama}' sudah ada atau gagal ditambahkan.")
    tk.Button(form_kategori, text="Simpan", command=simpan_kategori).pack(pady=10)

def buka_form_tambah_produk():
    global entry_nama, entry_kode, entry_kategori, entry_merk, entry_harga_beli, entry_harga_jual, entry_stok, entry_berat
    form_produk = tk.Toplevel(window)
    form_produk.title("Tambah Produk")
    form_produk.geometry("500x400")
    print("[INFO] Membuka form tambah produk...")
    print("[INFO] Form tambah produk selesai dibuat.")
    # konfigurasi kolom agar layout lebih seimbang

    form_produk.grid_columnconfigure(0, weight=1)
    form_produk.grid_columnconfigure(1, weight=2)

    entry_nama = tk.Entry(form_produk)
    entry_kode = tk.Entry(form_produk)
    kategori_list = ambil_semua_kategori()
    if not kategori_list:
        kategori_list = ["(Belum Ada Kategori)"]
    entry_kategori = ttk.Combobox(form_produk, values=kategori_list, state="readonly")
    entry_kategori.set(kategori_list[0]) # Default pilihan
    btn_tambah_kategori = tk.Button(form_produk, text="+ Tambah Kategori", command=buka_form_tambah_kategori)
    btn_tambah_kategori.grid(row=2, column=2, padx=(0, 10), pady=5)

    entry_merk = tk.Entry(form_produk)
    entry_harga_beli = tk.Entry(form_produk)
    entry_harga_jual = tk.Entry(form_produk)
    entry_stok = tk.Entry(form_produk)
    entry_berat = tk.Entry(form_produk)

    entries = [entry_nama, entry_kode, entry_kategori, entry_merk, entry_harga_beli, entry_harga_jual, entry_stok, entry_berat]

    labels = ["Nama", "Kode", "Kategori ID", "Merk", "Harga Beli", "Harga Jual", "Stok", "Berat"]
    for i, (label_text, entry) in enumerate(zip(labels, entries)):
        tk.Label(form_produk, text=label_text).grid(row=i, column=0, padx=(30,10), pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=(10, 30), pady=5, sticky="w")
    print("[INFO] Membuka form tambah produk...")
    print("[INFO] Form tambah produk selesai dibuat.")

    def tambah_produk_gui():
        print("Fungsi tambah_produk_gui dipanggil")
        print("[DEBUG] kategori_list:", kategori_list)
        
        global form_produk_aktif
        form_produk_aktif = True
        
        nama_kategori  = entry_kategori.get().strip()
        
        if nama_kategori == "(Belum Ada Kategori)":
            messagebox.showwarning("Kategori Belum Dipilih", "Silakan tambahkan kategori terlebih dahulu.")
            return

        kategori_id = get_kategori_id_by_nama(nama_kategori)

        if kategori_id is None:
            messagebox.showerror("Kategori Tidak Valid", f"Kategori '{nama_kategori}' tidak ditemukan.")
            print("Debug kategori:", repr(nama_kategori))
            return
        try:
            harga_beli = bersihkan_angka(entry_harga_beli.get())
            harga_jual = bersihkan_angka(entry_harga_jual.get())
            stok = int(entry_stok.get().strip())
            berat = float(entry_berat.get().strip())
        except ValueError as e:
            messagebox.showerror("Input Invalid", f"Pastikan semua angka valid: {e}")
            print("Debug kategori:", repr(entry_kategori.get()))
            print("Debug harga_beli:", repr(entry_harga_beli.get()))
            print("Debug harga_jual:", repr(entry_harga_jual.get()))
            print("Debug stok:", repr(entry_stok.get()))
            print("Debug berat:", repr(entry_berat.get()))
            return

        data = {
            "nama" : entry_nama.get().strip(),
            "kode_produk": entry_kode.get().strip(),
            "kategori_id": kategori_id,
            "merk": entry_merk.get().strip(),
            "harga_beli": harga_beli,
            "harga_jual": harga_jual,
            "stok": stok,
            "berat": berat
        }
        print("Data siap ditambahkan:", data)
        if tambah_produk(data):
            messagebox.showinfo("Berhasil", f"Produk'{data['nama']}' berhasil ditambahkan.")
            for entry in entries: entry.delete(0, tk.END)
            refresh_tree()
        else:
            messagebox.showerror("Gagal", "Gagal menambahkan produk.")

    # Tombol Simpan

    btn_simpan = tk.Button(form_produk, text="Simpan Produk", command=tambah_produk_gui)
    btn_simpan.grid(row=len(entries), column=0, columnspan=2, pady=20, padx=30)

    # Tombol Import Excel

    btn_import = tk.Button(form_produk, text="Import dari Excel", command=import_produk_excel)
    btn_import.grid(row=len(entries)+1, column=0, columnspan=2, pady=5)

    # Untuk menengahkan jendela saat input produk

    form_produk.update_idletasks()
    w = form_produk.winfo_width()
    h = form_produk.winfo_height()
    x = (form_produk.winfo_screenmmwidth() // 2) - (w // 10)
    y = (form_produk.winfo_screenheight() // 2) - (h // 2)
    form_produk.geometry(f"+{x}+{y}")

def import_produk_excel():
    file_path = filedialog.askopenfile(filetypes=[("Excel files", ".xlsx")])
    if file_path:
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            nama = row['Nama Produk']
            kategori = row['Kategori']
            harga = row['Harga']
            stok = row['Stok']
            #simpan_produk(nama, kategori, harga, stok)
        refresh_tree

# Untuk Edit Produk, buka form edit, dan update produk

def buka_form_edit_produk():
    global entry_nama, entry_kode, entry_kategori, entry_merk, entry_harga_beli, entry_harga_jual, entry_stok, entry_berat, selected_id

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Tidak Ada Pilihan", "Pilih produk yang ingin diedit di tabel.")
        return

    values = tree.item(selected_item[0], "values")
    selected_id = values[0]
    print("Selected ID:", selected_id)
    produk = get_produk_by_id(selected_id)

    if not produk:
        messagebox.showerror("Produk Tidak Ditemukan", f"Tidak ada produk dengan ID {selected_id}.")
        return
    print("[DEBUG] Tipe Produk:", type(produk))
    form_edit = tk.Toplevel(window)
    form_edit.title("Edit Produk")
    form_edit.geometry("500x400")
    form_edit.grid_columnconfigure(0, weight=1)
    form_edit.grid_columnconfigure(1, weight=2)

    labels = ["Nama", "Kode", "Kategori ID", "Merk", "Harga Beli", "Harga Jual", "Stok", "Berat"]
    keys = ["nama_produk", "kode_produk", "kategori_id", "merk", "harga_beli", "harga_jual", "stok", "berat"]
    entries = []
    print("[DEBUG] Panjang labels:", len(labels))
    print("[DEBUG] Panjang keys:", len(keys))
    print("[DEBUG] Isi labels:", labels)
    print("[DEBUG] Isi keys:", keys)

    for i, (label_text, key) in enumerate(zip(labels, keys)):
        tk.Label(form_edit, text=label_text).grid(row=i, column=0, padx=(30, 10), pady=5, sticky="e")
        entry = tk.Entry(form_edit)
        value = produk.get(key)
        if value is None:
            print(f"[WARNING] Key '{key}' tidak ditemukan atau bernilai None.")
            value = ""
        entry.insert(0, str(value))
        entry.grid(row=i, column=1, padx=(10,30), pady=5, sticky="w")
        entries.append(entry)
        print(f"[DEBUG] Membuat Entry untuk: {label_text} key: {key}")
    if len(entries) < 8:
        messagebox.showerror("Error", f"Entry tidak lengkap. Hanya {len(entries)} yang dibuat.")
        return
    entry_nama = entries[0]
    entry_kode = entries[1]
    entry_kategori = entries[2]
    entry_merk = entries[3]
    entry_harga_beli = entries[4]
    entry_harga_jual = entries[5]
    entry_stok = entries[6]
    entry_berat = entries[7]
    
    # Tombol Simpan
    btn_simpan = tk.Button(form_edit, text="Simpan Perubahan", command=lambda:simpan_perubahan_produk(form_edit, selected_id, entries))
    btn_simpan.grid(row=len(entries), column=0, columnspan=2,  pady=20, padx=30)

def update_produk_by_id(id_produk, data):
    try:
        print("[DEBUG] Harga Beli:", data['harga_beli'], type(data['harga_beli']))
        print("[DEBUG] Harga jual:", data['harga_jual'], type(data['harga_jual']))
        for key in ["harga_beli", "harga_jual", "stok", "berat"]:
            if not isinstance(data[key], (int, float)):
                print(f"[ERROR] {key} bukan angka valid:", data[key])
                return False
            
        return update_produk(
            id_produk,
            data['nama'],
            data['kode'],
            data['kategori_id'],
            data['merk'],
            data['harga_beli'],
            data['harga_jual'],
            int(data['stok']),
            float(data['berat'])
        )
    except Exception as e:
        print(f"Error saat update produk: {e}")
        return False

def simpan_perubahan_produk(form, id_produk, entries):
    for i, label in enumerate(["Nama", "Kode", "Kategori", "Merk", "harga Beli", "Harga Jual", "Stok", "Berat"]):
        print(f"[DEBUG] {label}: '{entries[i].get().strip()}'")
        if entries[i].get().strip() == "":
            messagebox.showerror("Input Kosong", f"{label} tidak boleh kosong.")
            return
    try:
        data = {
            "nama":entries[0].get().strip(),
            "kode": entries[1].get().strip(),
            "kategori_id": int(entries[2].get().strip()),
            "merk": entries[3].get().strip(),
            "harga_beli": bersihkan_angka(entries[4].get()),
            "harga_jual": bersihkan_angka(entries[5].get()),
            "stok": int(entries[6].get().strip()),
            "berat": float(entries[7].get().strip())
        }
        
    except ValueError as e:
        messagebox.showerror("Input Invalid", f"Pastikan semua angka valid: {e}")
        return

    if data["harga_beli"] is None or data["harga_jual"] is None:
        messagebox.showerror("Input Invalid", "Pastikan harga beli dan jual berupa angka valid.")
        return

    # Update ke database
    print("Data yang dikirim ke update_produk_by_id:")
    for k, v in data.items():
        print(f"{k}: {v} (type : {type(v)})")

    if update_produk_by_id(id_produk, data):
        messagebox.showinfo("Berhasil", f"Produk '{data['nama']}' berhasil diperbarui.")
        form.destroy()
        refresh_tree()
    else:
        print("Gagal", "Gagal memperbarui produk.")

def get_produk_by_id(id_produk):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_produk, nama_produk, kode_produk, kategori_id, merk, harga_beli, harga_jual, stok, berat FROM produk WHERE id_produk = ?", (id_produk,))
    row = cursor.fetchone()
    print(f"Hasil query: {row}")
    conn.close()

    if row:
        keys = ["id_produk","nama_produk","kode_produk","kategori_produk",
            "merk","harga_beli","harga_jual","stok","berat"]
        return dict(zip(keys, row))
    return None
    
# Untuk hapus produk

def hapus_produk_gui():
    if not selected_id:
        messagebox.showwarning("Tidak Ada Pilihan", "Pilih produk yang akan dihapus di tabel.")
        return
    konfirmasi = messagebox.askyesno("Konfirmasi Hapus", "Yakin ingin menghapus produk ini?")
    if konfirmasi:
        try:
            hapus_produk(selected_id)
            messagebox.showinfo("Dihapus", "Produk berhasil dihapus.")
            refresh_tree()
            for entry in entries: entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Gagal Hapus", str(e))

def format_rupiah(nilai):
    try:
        return f"Rp {int(float(nilai)):,}"
    except (ValueError, TypeError):
        return "Rp 0"

def buat_frame_produk(parent):
    global window, entry_nama, entry_kode, entry_kategori, entry_merk
    global entry_harga_beli, entry_harga_jual, entry_stok, entry_berat
    global tree, selected_id, entry_filter_kategori
    selected_id = None

    frame = tk.Frame(parent, bg="#f4f4f4")

    #________ Frame control atas

    frame_kontrol = tk.Frame(frame, pady=10, bg="#f4f4f4")
    frame_kontrol.pack()

    # ------ Form Input ----
    frame_form = tk.Frame(frame, bg="#f4f4f4")  # Form Input produk
    frame_form.pack_forget()   # sembunyikan 

    def toggle_form_produk():
        if frame_form.winfo_ismapped():
            frame_form.pack_forget() # sembunyikan form
        else:
            frame_form.pack() # tampilkan form

    tk.Button(frame_kontrol, text="Tambah Produk", command=buka_form_tambah_produk).grid(row=0, column=0, padx=5)

    def create_labeled_entry(label):
        tk.Label(frame_form, text=label).pack()
        e = tk.Entry(frame_form)
        e.pack()
        return e
    
    entry_nama = create_labeled_entry("Nama Produk")
    entry_kode = create_labeled_entry("Kode Produk")
    entry_kategori = create_labeled_entry("ID Kategori")
    entry_merk = create_labeled_entry("Merk")
    entry_harga_beli = create_labeled_entry("Harga Beli")
    entry_harga_jual = create_labeled_entry("Harga Jual")
    entry_stok = create_labeled_entry("Stok Awal")
    entry_berat = create_labeled_entry("Berat (Kg)")

    global entries, dropdown_kategori, entry_cari
    entries = [entry_nama, entry_kode, entry_kategori, entry_merk,
               entry_harga_beli, entry_harga_jual, entry_stok, entry_berat]

    # Entry cari
    entry_cari = tk.Entry(frame_kontrol, width=20)
    entry_cari.grid(row=0, column=1, padx=5)
    # Tombol cari  --> hanya nama
    tk.Button(frame_kontrol, text="Cari", command=cari_produk_nama).grid(row=0, column=2, padx=5)

    # Filter Kategori
    frame_filter = tk.Frame(frame, bg="#f4f4f4")
    frame_filter.pack(pady=10)

    tk.Label(frame_filter, text="Nama Kategori:").grid(row=0, column=2, padx=5)
    entry_filter_kategori = tk.Entry(frame_filter)
    entry_filter_kategori.grid(row=0, column=3, padx=5)

    btn_filter = tk.Button(frame_filter, text="Terapkan Filter", command=filter_kategori_dan_nama)
    btn_filter.grid(row=0, column=4, padx=5)

    tk.Button(frame_kontrol, text="Reset Filter", command=reset_filter).grid(row=0, column=5, padx=5)

    # --- TreeView Produk ---

    tree = ttk.Treeview(frame, columns=("id", "nama", "kode", "kategori", "merk", "harga_beli", "harga_jual", "stok", "berat"), show="headings")
    for col, label in [("nama", "Nama"), ("kode","Kode"), ("kategori","Kategori"), ("merk","Merk"),("harga_beli","Harga Beli"),("harga_jual","Harga Jual"), ("stok","Stok"), ("berat", "Berat")]:
        tree.heading(col, text=label)
        

    tree.bind("<<TreeviewSelect>>", on_tree_select)
    tree.column("nama", width=150)
    tree.column("kode", width=100)
    tree.column("kategori", width=120)
    tree.column("merk", width=120)
    tree.column("harga_beli", anchor="e", width=100)
    tree.column("harga_jual", anchor="center", width=80)
    tree.column("stok", anchor="center", width=80)
    tree.column("berat", anchor="center", width=80)

    tree.pack(fill="both", expand=True, padx=10, pady=10)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scroll_x.set)
    scroll_x.pack(side="bottom", fill="x")

    tk.Button(frame, text="Edit Produk", command=buka_form_edit_produk).pack(pady=2)
    tk.Button(frame, text="Hapus Produk", command=hapus_produk_gui).pack(pady=2)

    refresh_tree()
    frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    buat_frame_produk()


#python -m app.gui.produk_gui