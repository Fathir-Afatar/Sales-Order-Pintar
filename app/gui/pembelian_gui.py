import tkinter as tk
from tkinter import ttk, messagebox
from app.core.pembelian_core import tambah_pembelian, get_detail_pembelian, get_connection, get_histori_pembelian, update_pembelian
from app.core.supplier_core import ambil_supplier
from app.core.product_core import ambil_daftar_produk
from tkinter import simpledialog


def buat_frame_pembelian(parent):
    font_normal = ("Segoe UI", 10)
    frame = tk.Frame(parent, bg="#f4f4f4")

    # 1.  Supplier Dropdown
    frame_supplier = tk.Frame(frame)
    frame_supplier.pack(fill="x", padx=10, pady=5)

    supplier_data = ambil_supplier()
    supplier_map = {sup["nama"]: sup["id"] for sup in supplier_data}
    
    tk.Label(frame_supplier, text="Pilih Supplier:", font=font_normal).pack(side="left")
    combo_supplier = ttk.Combobox(frame_supplier, values=list(supplier_map.keys()), state="readonly")
    combo_supplier.pack(side="left", padx=5)


    # 2. Daftar Produk
    frame_input = tk.Frame(frame)
    frame_input.pack(fill="both", expand=True, padx=10, pady=5)
    # Treeview Produk (Input Pembelian)
    tk.Label(frame_input, text="Daftar Produk", font=font_normal).pack(anchor="w")
    # Search bar + Reset
    frame_search = tk.Frame(frame_input)
    frame_search.pack(pady=5)

    entry_cari = tk.Entry(frame_search, width=30)
    entry_cari.pack(side="left", pady=(0, 5))
    entry_cari.insert(0, "cari produk berdasarkan nama atau kode ...")
    entry_cari.bind("<FocusIn>", lambda e: entry_cari.delete(0, "end"))
    entry_cari.bind("<Key>", lambda e: filter_produk(entry_cari.get())) 

    btn_reset = tk.Button(frame_search, text="🔄 Reset", command=lambda:reset_pencarian())
    btn_reset.pack(side="left")

    # Frame isi: Treeview + Scrollbar
    frame_input_scroll = tk.Frame(frame_input)
    frame_input_scroll.pack(fill="both", expand=True)

    scroll_produk = tk.Scrollbar(frame_input_scroll, orient="vertical")
    tree_input = ttk.Treeview(frame_input_scroll, columns=("Pilih", "Kode", "Nama", "Jumlah", "Harga"), show="headings", yscrollcommand=scroll_produk.set)
    scroll_produk.config(command=tree_input.yview)
    tree_input.heading("Pilih", text="✔")
    
    for col in ("Pilih", "Kode", "Nama", "Jumlah", "Harga"):
        tree_input.heading(col, text=col if col != "Pilih" else "✔")
        tree_input.column(col, width=40 if col == "Pilih" else 120, anchor="center")
    
    tree_input.pack(side="left", fill="both", expand=True)
    scroll_produk.pack(side="right", fill="y")    

    def filter_produk(keyword):
        print("[DEBUG] Struktur produk:", produk_list[0])
        keyword = keyword.lower()
        if not keyword or keyword == "cari produk berdasarkan nama atau kode ...":
            tampilkan_produk(produk_list)
            return
        
        hasil = []
        for produk in produk_list:
            if keyword in produk["kode_produk"].lower() or keyword in produk["nama"].lower():
                print("[DEBUG] Produk yang cocok:", produk_list)
                hasil.append({"kode_produk": produk["kode_produk"], "nama":produk["nama"], "harga":produk["harga"], "jumlah": produk.get("jumlah",0)})
        tampilkan_produk(hasil)
    
    def tampilkan_produk(list_produk):
        tree_input.delete(*tree_input.get_children())
        for p in list_produk:
            try:
                harga_format = f"Rp {int(float(p.get('harga', 0))):,}"
            except Exception as e:
                print("[ERROR] Format harga gagal:", e)
                harga_format = "Rp -"

            tree_input.insert("", "end", values=("",p.get("kode_produk", "-"), p.get("nama", "-"), p.get("jumlah", 0), harga_format))   

    def reset_pencarian():
        entry_cari.delete(0, "end") # Kosongkan kotak pencarian
        #entry_cari.insert(0, "cari produk berdasarkan nama atau kode ...")
        tampilkan_produk(produk_list)

    # Event Handel untuk Toggle "✔"
    def toogle_pilih(event):
        item_id = tree_input.identify_row(event.y)
        col = tree_input.identify_column(event.x)
        if not item_id or col != "#1": # Pastikan klik di kolom "Pilih"
            return
        values = tree_input.item(item_id)["values"]
        values[0] = "✔" if values[0] == "" else ""
        tree_input.item(item_id, values=values)
    tree_input.bind("<Button-1>", toogle_pilih)


    # 3. Histori Pembelian
    frame_histori = tk.Frame(frame)
    frame_histori.pack(fill="both", expand=True, padx=10, pady=5)

    # Frame isi: Label + Treeview + Scrollbar
    tk.Label(frame_histori, text="Histori Pembelian", font=font_normal).pack(anchor="w")
    frame_histori_scroll = tk.Frame(frame_histori)
    frame_histori_scroll.pack(fill="both", expand=True)

    scroll_histori = tk.Scrollbar(frame_histori_scroll, orient="vertical")
    tree_histori = ttk.Treeview(frame_histori_scroll, columns=("ID", "Tanggal", "Supplier", "Total"), show="headings", yscrollcommand=scroll_histori.set)
    for col in ("ID", "Tanggal", "Supplier", "Total"):
        tree_histori.heading(col, text=col)
        tree_histori.column(col, anchor="center", width=100)
    scroll_histori.config(command=tree_histori.yview)
    tree_histori.pack(side="left", fill="both", expand=True)
    scroll_histori.pack(side="right", fill="y")

    # 4. Detail Transaksi
    #frame_detail = tk.Frame(root)
    #frame_detail.pack(fill="both", expand=True, padx=10, pady=5)
       
    #tk.Label(frame_detail, text="Detail Transaksi", font=font_normal).pack(anchor="w")
    #frame_detail_scroll = tk.Frame(frame_detail)
    #frame_detail_scroll.pack(fill="both", expand=True)

    #scroll_detail = tk.Scrollbar(frame_detail_scroll, orient="vertical")
    #tree_detail = ttk.Treeview(frame_detail_scroll, columns=("Kode Produk", "Nama Produk", "Qty", "Harga Beli"), show="headings", yscrollcommand=scroll_detail.set)
    #scroll_detail.config(command=tree_detail.yview)
    #tree_detail.pack(side="left", fill="both", expand=True)
    #scroll_detail.pack(side="right", fill="y")

    produk_list = ambil_daftar_produk()
    tampilkan_produk(produk_list)
    #for item in produk_list:
     #   tree_input.insert("", "end", values=("", item["kode_produk"], item["nama"], 0, item["harga"]))
    
    # Edit Jumlah (dual click)
    def edit_jumlah(event):
        item_id = tree_input.focus()
        if not item_id:
            return
        current = tree_input.item(item_id)["values"]
        if len(current) < 5:
            return
        nama_produk = current[2]
        try:
            jumlah_sekarang = int(current[3])
        except:
            jumlah_sekarang = 0
        jumlah_baru = simpledialog.askinteger("Edit Jumlah", f"Masukkan jumlah untuk {nama_produk}", initialvalue=jumlah_sekarang, minvalue=0)
        if jumlah_baru is not None:
            current[3] = jumlah_baru
            tree_input.item(item_id, values=current)
        if current[0] != "✔":
            messagebox.showinfo("Info", "Silakan centang produk terlebih dahulu.")
            return
    tree_input.bind("<Double-1>", edit_jumlah)

    # Buka konfirmasi pembelian 
    def buka_konfirmasi_pembelian():
        print("Fungsi konfirmasi dipanggil")
        produk_terpilih = ambil_produk_terpilih()
        if not produk_terpilih:
            messagebox.showinfo("Info", "Tidak ada produk yang dipilih.")
            return
        
        supplier_nama = combo_supplier.get()
        if not supplier_nama:
            messagebox.showinfo("Info", "Silakan pilih supplier terlebih dahulu.")
            return
        
        window = tk.Toplevel(frame, bg="lightyellow")
        window.title("Konfirmasi Pembelian")
        window.geometry("500x400")
        
        tk.Label(window, text=f"Supplier: {supplier_nama}", font=("Segoe UI", 10, "bold")).pack(pady=5)
        
        frame_produk = tk.Frame(window)
        frame_produk.pack(fill="both", expand=True)

        frame_total = tk.Frame(window)
        frame_total.pack(fill="x", pady=5)

        scroll_konfirmasi = ttk.Scrollbar(frame_produk, orient="vertical")
        
        tree_konfirmasi = ttk.Treeview(frame_produk, columns=("Kode", "Nama", "Qty", "Harga", "Subtotal"), show="headings", yscrollcommand=scroll_konfirmasi.set)
        scroll_konfirmasi.config(command=tree_konfirmasi.yview)

        for col in ("Kode", "Nama", "Qty", "Harga", "Subtotal"):
            tree_konfirmasi.heading(col, text=col)
            tree_konfirmasi.column(col, anchor="center", width=100)
        
        tree_konfirmasi.pack(side="left", fill="both", expand=True)
        scroll_konfirmasi.pack(side="right", fill="y")

        total = 0
        for item in produk_terpilih:
            try :
                harga_format = f"Rp {int(float(item.get('harga_beli', 0))):,}"
                subtotal = item.get("qty", 0) * item.get("harga_beli", 0)
                subtotal_format = f"Rp {int(subtotal):,}"
            except Exception as e:
                print("[ERROR] Format gagal:", e)
                harga_format = "Rp -"
                subtotal_format = "Rp -"
            
            tree_konfirmasi.insert("", "end", values=(item.get("kode_produk"), item.get("nama"), item.get("qty"), harga_format, subtotal_format))
        total_harga = sum(item.get("qty", 0) * item.get("harga_beli", 0) for item in produk_terpilih)
        total_format = f"Rp {int(total_harga):,}"

        label_total = tk.Label(frame_total, text=f"Total Harga: {total_format}", font=("Segoe UI", 10, "bold"))
        label_total.pack(pady=5)

        def simpan_ke_db():
            supplier_id = supplier_map[supplier_nama]
            tambah_pembelian(supplier_id, produk_terpilih)
            messagebox.showinfo("Sukses", "Pembelian berhasil disimpan.")
            window.destroy()
            muat_histori()
        tk.Button(window, text="OK", command=simpan_ke_db).pack(side="left", padx=20, pady=10)
        tk.Button(window, text="Batal", command=window.destroy).pack(side="right", padx=20, pady=10)

    # fungsi untuk merubah format rupiah ke logika yang diterima oleh DB
    def bersihkan_rupiah(rp_string):
        try :
            angka = rp_string.replace("Rp", "").replace(",","").strip()
            return float(angka)
        except Exception as e:
            print("[ERROR] Gagal parsing harga:", rp_string, e)
            return 0.0

    # Simpan Pembelian
    def simpan_pembelian():
        supplier_nama = combo_supplier.get()
        supplier_id = supplier_map.get(supplier_nama)
        if not supplier_id:
            messagebox.showerror("Error", "Supplier belum dipilih.")
            return

        daftar_barang = []
        for row_id in tree_input.get_children():
            values = tree_input.item(row_id)["values"]
            if len (values) < 4:
                continue
            _, kode_produk, nama, qty_raw, harga_raw = values
            try:
                qty = int(qty_raw)
                harga_beli = int(float(harga_raw))
                if qty > 0:
                    daftar_barang.append({"kode_produk": kode_produk, "nama": nama, "qty": qty, "harga_beli": harga_beli})
                    print("[DITAMBAHKAN]", kode_produk, nama, qty, harga_beli)
            except Exception as e:
                print("[ERROR konversi]", e)
                continue

        if not daftar_barang:
            messagebox.showwarning("Kosong", "Tidak ada barang yang dibeli.")
            return

        hasil = tambah_pembelian(supplier_id, daftar_barang)
        if hasil:
            messagebox.showinfo("Sukses", "Transaksi pembelian berhasil disimpan.")
            combo_supplier.set("")
            for row_id in tree_input.get_children():
                values = tree_input.item(row_id)["values"]
                values[2] = 0 # Reset Jumlah
                tree_input.item(row_id, values=values)
        else:
            messagebox.showerror("Gagal", "Transaksi gagal disimpan.")
        muat_histori()

    btn_simpan = tk.Button(frame_supplier, text="Simpan Pembelian", command=buka_konfirmasi_pembelian)
    btn_simpan.pack(side="left", padx=10)
    
    #btn_konfirmasi = tk.Button(root, text="Konfirmasi Pembelian", command=buka_konfirmasi_pembelian)
    #btn_konfirmasi.pack(pady=10)
 
    def ambil_detail_terformat(pembelian_id):
        detail = get_detail_pembelian(pembelian_id)
        hasil = []
        for kode, qty, harga in detail:
            nama = get_produk_nama(kode)
            hasil.append({
            "kode_produk": kode,
            "nama_produk": nama,
            "qty": qty,
            "harga_beli": harga
            })
        print(f"[DEBUG] Kode: {kode}, Nama: {nama}")
        return hasil
    
    def muat_histori():
        for row in tree_histori.get_children():
            tree_histori.delete(row)
        histori = get_histori_pembelian()
        for id_pembelian, tanggal, supplier_nama, total in histori:
            try:
                total_format = f"Rp {int(float(total)):,}"
            except Exception as e:
                print("[ERROR] Format total gagal:", e)
                total_format = "Rp -"

            tree_histori.insert("", "end", values=(id_pembelian, tanggal, supplier_nama, total_format))

    def tampilkan_detail_manual():
        selected = tree_histori.focus()
        if not selected:
            messagebox.showerror("Info", "Silakan pilih histori pembelian terlebih dahulu.")
            return
        values = tree_histori.item(selected)["values"]
        pembelian_id = values[0] # Asumsi kolom pertama adalah ID
        detail = ambil_detail_terformat(pembelian_id)
        if not detail:
            messagebox.showinfo("Info", "Detail transaksi tidak ditemukan.")
            return
        window = tk.Toplevel(frame)
        window.title(f"Detail Transaksi #{pembelian_id}")
        window.geometry("500x400")

        tree_popup = ttk.Treeview(window, columns=("Kode", "Nama", "Qty", "Harga"), show="headings")

        frame_popup_scroll = tk.Frame(window)
        frame_popup_scroll.pack(fill="both", expand=True)

        scroll_popup = tk.Scrollbar(frame_popup_scroll, orient="vertical")
        
        tree_popup = ttk.Treeview(frame_popup_scroll, columns=("Kode", "Nama", "Qty", "Harga"), show="headings", yscrollcommand=scroll_popup.set)
        scroll_popup.config(command = tree_popup.yview)

        for col in ("Kode", "Nama", "Qty", "Harga"):
            tree_popup.heading(col, text=col)
            tree_popup.column(col, anchor="center", width=100)
        tree_popup.pack(side="left", fill="both", expand=True)
        scroll_popup.pack(side="right", fill="y")
        for item in detail:
            try:
                harga_format = f"Rp {int(float(item.get('harga_beli', 0))):,}"
            except Exception as e:
                print("[ERROR] Format harga gagal:", e)
                harga_format = "Rp -"
        tree_popup.insert("", "end", values=(item.get("kode_produk", "-"), item.get("nama_produk", "-"), item.get("qty", 0), harga_format))
        #label_total = tk.Label(window, text=f"Total harga: Rp {total_harga:,}", font=("Segoe UI", 10, "bold"))
        #label_total.pack(pady=5)

        def edit_jumlah_popup(event):
            item_id = tree_popup.focus()
            if not item_id:
                return
            values = tree_popup.item(item_id)["values"]
            nama_produk = values[1]
            try:
                jumlah_sekarang = int(values[2])
            except:
                jumlah_sekarang = 0
            jumlah_baru = simpledialog.askinteger("Edit Jumlah", f"Masukkan jumlah baru untuk {nama_produk}", initialvalue=jumlah_sekarang, minvalue=0)
            if jumlah_baru is not None:
                if jumlah_baru == 0:
                    messagebox.showwarning("Invalid", "Jumlah tidak boleh nol. Silakan isi minimal 1.")
                    return
                values[2] = jumlah_baru
                tree_popup.item(item_id, values=values)

                # Update total harga setelah koreksi
                total = 0
                for iid in tree_popup.get_children():
                    v = tree_popup.item(iid)["values"]
                    total += int(v[2]) * int(float(v[3]))
                label_total.config(text=f"Total Harga: Rp {total:,}")
        tree_popup.bind("<Double-1>", edit_jumlah_popup)

        for item in detail:
            tree_popup.insert("", "end", values=(
                item["kode_produk"],
                item["nama_produk"],
                item["qty"],
                item["harga_beli"]
            ))
        total_harga = sum(item["qty"] * item["harga_beli"] for item in detail)
        label_total = tk.Label(window, text=f"Total harga: Rp {total_harga:,}", font=("Segoe UI", 10, "bold"))
        label_total.pack(pady=5)

        def simpan_koreksi():
            hasil_koreksi = []
            for iid in tree_popup.get_children():
                v = tree_popup.item(iid)["values"]
                hasil_koreksi.append({"kode_produk": v[0], "nama_produk":v[1], "qty":int(v[2]), "harga_beli": int(float(v[3]))})
            # Validasi: pastikan ada qty>0
            if not any(item["qty"] > 0 for item in hasil_koreksi):
                messagebox.showwarning("Gagal", "Semua jumlah produk nol. Koreksi tidak disimpan.")
                return
            konfirmasi = messagebox.askyesno("Konfirmasi", "Yakin ingi menyimpan koreksi transaksi.")
            if not konfirmasi:
                return
            update_pembelian(pembelian_id, hasil_koreksi)
            messagebox.showinfo("Sukses", "Koreksi berhasil disimpan.")
            window.destroy()
            muat_histori()

        def batal_koreksi():
            window.destroy()
        frame_btn = tk.Frame(window)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Simpan Koreksi", command=simpan_koreksi).pack(side="left", padx=10)
        tk.Button(frame_btn, text="Batal", command=batal_koreksi).pack(side="right", padx=10)

    btn_lihat_detail = tk.Button(frame_histori, text="Lihat Detail Transaksi", command=tampilkan_detail_manual)
    btn_lihat_detail.pack(pady=5)

    # Tombol Simpan
    #btn_simpan = tk.Button(root, text="Simpan Pembelian", command=simpan_pembelian)
    #btn_simpan.pack()

    def ambil_produk_terpilih():
        hasil = []
        for item_id in tree_input.get_children():
            values = tree_input.item(item_id)["values"]
            if values[0] == "✔" and int(values[3]) > 0:
                hasil.append({"kode_produk":values[1], "nama":values[2], "qty":int(values[3]), "harga_beli":int(bersihkan_rupiah(values[4]))})
        return hasil
    muat_histori()
    frame.pack(fill="both", expand=True)

def hitung_total_keranjang(daftar_barang):  # Untuk menampilkan total sebelum simpan
    return sum(item["qty"] * item["harga_beli"] for item in daftar_barang)

def ambil_supplier_nama(supplier_id): # Untuk tampilkan histori atau detail pembelian
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama FROM supplier WHERE id = ?", (supplier_id,))
    hasil = cursor.fetchone()
    conn.close()
    return hasil [0] if hasil else "-"

def get_produk_nama(kode_produk): # memperjelas tampilan detail pembelian
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama_produk FROM produk WHERE kode_produk = ?", (kode_produk,))
    hasil = cursor.fetchone()
    conn.close()
    return hasil[0] if hasil else "-"

if __name__ == "__main__":
    buat_frame_pembelian()