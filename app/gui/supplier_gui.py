import tkinter as tk
from tkinter import ttk, messagebox
from app.core.supplier_core import semua_supplier, tambah_supplier, edit_supplier, hapus_supplier
print("Berhasil import semua_supplier:", semua_supplier)
import sys
print("PYTHON PATH:", sys.path)

# Setup Dasar
def buat_frame_supplier(parent):
    frame = tk.Frame(parent, bg="#f4f4f4")

    # Frame atas: Tambah + Filter

    frame_top = tk.Frame(frame, bg="#f4f4f4")
    frame_top.pack(pady=10)

    # Treview lebih dulu untuk lambda

    tree = ttk.Treeview(frame, columns=("id", "nama", "alamat", "no_hp"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("nama", text="Nama Supplier")
    tree.heading("alamat", text="Alamat")
    tree.heading("no_hp", text="No HP")
    tree.column("id", width=50)
    tree.column("nama", width=200)
    tree.column("alamat", width=250)
    tree.column("no_hp", width=150)

    tk.Button(frame_top, text="Tambah Supplier", command=lambda: buka_form_tambah_supplier(tree, frame)).pack(side="left", padx=5)

    # Cari Nama

    tk.Label(frame_top, text="Cari Nama:").pack(side="left", padx=5)
    entry_nama = tk.Entry(frame_top)
    entry_nama.pack(side="left", padx=5)
    tk.Button(frame_top, text="Cari", command=lambda: filter_supplier(tree, entry_nama)).pack(side="left", padx=5)
    tk.Button(frame_top, text="Reset", command=lambda: refresh_tree(tree)).pack(side="left", padx=5)

    # Tampilkan Treeview
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Frame Bawah: Edit + Hapus

    frame_bottom = tk.Frame(frame, bg="#f4f4f4")
    frame_bottom.pack(pady=10)

    tk.Button(frame_bottom, text="Hapus Supplier", command=lambda: hapus_supplier_gui(tree)).pack(side="left", padx=5)
    tk.Button(frame_bottom, text="Edit Supplier", command=lambda: buka_form_edit_supplier(tree, frame)).pack(side="left", padx=5)

    refresh_tree(tree)
    frame.pack(fill="both", expand=True)

def refresh_tree(tree):
    tree.delete(*tree.get_children())
    for s in semua_supplier():
        tree.insert("", tk.END, values=s)

# Tambah Supplier

def buka_form_tambah_supplier(tree, parent):
    form = tk.Toplevel(parent)
    form.title("Tambah Supplier")
    form.geometry("300x300")

    labels = ["Nama", "Alamat", "No HP"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(form, text=label).grid(row=i, column=0, padx=20, pady=5, sticky="e")
        entry = tk.Entry(form)
        entry.grid(row=i, column=1, padx=20, pady=5, sticky="w")
        entries.append(entry)
    
    def simpan():
        nama = entries[0].get().strip()
        alamat = entries[1].get().strip()
        no_hp = entries[2].get().strip()

        if not nama:
            messagebox.showerror("Error", "Nama supplier wajib diisi.")
            return
        
        tambah_supplier(nama, alamat, no_hp)
        messagebox.showinfo("Berhasil", f"Supplier '{nama}' ditambahkan.")
        form.destroy()
        refresh_tree(tree)
    tk.Button(form, text="Simpan", command=simpan).grid(row=3, column=0, columnspan=2, pady=20)

def hapus_supplier_gui(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Pilih Supplier", "Pilih supplier yang ingin dihapus.")
        return

    supplier_id = tree.item(selected[0])["values"][0]
    hapus_supplier(supplier_id)
    messagebox.showinfo("Berhasil", "Supplier berhasil dihapus.")
    refresh_tree(tree)

def buka_form_edit_supplier(tree, parent):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Pilih Supplier", "Pilih supplier yang ingin diedit.")
        return

    values = tree.item(selected[0])["values"]
    id_supplier, nama_awal, alamat_awal, no_hp_awal = values[:4]

    form = tk.Toplevel(parent)
    form.title("Edit Supplier")
    form.geometry("300x300")

    labels = ["Nama", "Alamat", "No HP"]
    entries = []


    for i, (label, value) in enumerate(zip(labels, [nama_awal, alamat_awal, no_hp_awal])):
        tk.Label(form, text=label).grid(row=i, column=0, padx=20, pady=5, sticky="e")
        entry = tk.Entry(form)
        entry.insert(0, value)
        entry.grid(row=i, column=1, padx=20, pady=5, sticky="w")
        entries.append(entry)
    
    def simpan():
        nama = entries[0].get().strip()
        alamat = entries[1].get().strip()
        no_hp = entries[2].get().strip()

        if not nama:
            messagebox.showerror("Error", "Nama supplier wajib diisi.")
            return
        
        edit_supplier(id_supplier, nama, alamat, no_hp)
        messagebox.showinfo("Berhasil", f"Supplier '{nama}' berhasil diperbarui.")
        refresh_tree(tree)
        form.destroy()
    
    tk.Button(form, text="Simpan Perubahan", command=simpan).grid(row=3, column=0, columnspan=2, pady=20)


def filter_supplier(tree, entry_nama):
    keyword = entry_nama.get().strip().lower()
    tree.delete(*tree.get_children())
    for s in semua_supplier():
        if keyword in s[1].lower(): 
            tree.insert("", tk.END, values=s)

if __name__ == "__main__":
    buat_frame_supplier()