import sqlite3
from datetime import datetime
from app.core.product_core import tambah_stok, kurangi_stok
from app.core.stok_core import catat_log_stok, get_stok_terakhir

DB_PATH = "C:/Users/Fathir/Documents/pos-pintar-by-fathir/data/pos.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def tambah_pembelian(supplier_id: str, daftar_barang:list):
    if not daftar_barang:
        print("[ERROR] Daftar barang kosong.")
        return False

    for item in daftar_barang:
        if item["qty"] <= 0 or item["harga_beli"] <= 0:
            print(f"[ERROR] Item tidak valid: {item}")
            return False
    tanggal = datetime.now().strftime("%Y-%m-%d")
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        total_harga = sum(item["qty"] * item["harga_beli"] for item in daftar_barang)

        # Simpan transaksi pembelian
        cursor.execute("""
                INSERT INTO transaksi_pembelian (supplier_id, tanggal, total_harga)
                       VALUES (?, ?, ?)
                       """, (supplier_id, tanggal, total_harga))
        pembelian_id = cursor.lastrowid

        # simpan detail + update stok
        for item in daftar_barang:
            cursor.execute("""
                           INSERT INTO detail_pembelian (pembelian_id, kode_produk, qty, harga_beli)
                           VALUES (?, ?, ?, ?)
                           """, (pembelian_id, item["kode_produk"], item["qty"], item["harga_beli"]))
            # Gunakan koneksi yang sama untuk update stok
            cursor.execute("""
                UPDATE produk SET stok = stok + ? WHERE kode_produk = ?
            """,(item["qty"], item["kode_produk"]))

            # Ambil stok sebelum update
            stok_awal = get_stok_terakhir(item["kode_produk"])
            stok_akhir = stok_awal + item["qty"]

            cursor.execute("""
                UPDATE produk SET stok = stok + ? WHERE kode_produk = ?
            """, (item["qty"], item["kode_produk"]))

            # Catat log stok
            catat_log_stok(item["kode_produk"], stok_awal, stok_akhir, "MASUK")
        conn.commit()
        print(f"[INFO] Pembelian berhasil disimpan. ID: {pembelian_id}")
        return pembelian_id

    except Exception as e:
        print(f"[ERROR] Gagal menyimpan pembelian: {e}")
        if conn:
            conn.rollback()
        return False
    
    finally:
        if conn:
            conn.close()

def get_histori_pembelian():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tp.id_pembelian, tp.tanggal, s.nama_supplier, tp.total_harga
        FROM transaksi_pembelian tp
        JOIN supplier s ON tp.supplier_id = s.id_supplier
        ORDER BY tp.tanggal DESC    
    """)
    hasil = cursor.fetchall()
    conn.close()
    return hasil

def get_pembelian(pembelian_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kode_produk, qty, harga_beli
        FROM detail_pembelian
        WHERE pembelian_id = ?
    """, (pembelian_id,))
    hasil = cursor.fetchall()
    conn.close()
    return hasil

def validasi_keranjang(daftar_barang):
    if not daftar_barang:
        return False
    for item in daftar_barang:
        if item["qty"] <= 0 or item["harga_beli"] <= 0:
            return False
    return True

def get_pembelian_untuk_koreksi(pembelian_id):
    header = get_histori_pembelian()
    detail = get_histori_pembelian(pembelian_id)
    return {"header":header, "detail": detail}

def hapus_pembelian(pembelian_id):
    try:
        conn = get_connection
        cursor = conn.cursor()
        # Ambil detail dulu untuk rollback ke stok
        cursor.execute("""
            SELECT kode_produk, qty FROM detail_pembelian
            WHERE pembelian_id = ?
        """, (pembelian_id,))

        detail = cursor.fetchall()

        for kode_produk, qty in detail:
            # Kurangi stok karena pembelian dibatalkan
            kurangi_stok(kode_produk, qty)

        # Hapus detail dan header
        cursor.execute("DELETE FROM detaul_pembelian WHERE pembelian_id = ?", (pembelian_id,))
        cursor.execute("DELETE FROM transaksi_pembelian WHERE id_pembelian = ?", (pembelian_id,))
        conn.commit()
        print(f"[INFO] Transaksi pembelian {pembelian_id} berhasil dihapus.")
        return True
    except Exception as e:
        print(f"[ERROR] gagal menghapus pembelian: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_detail_pembelian(pembelian_id):
    conn = get_connection()
    cursor= conn.cursor()
    cursor.execute("""
        SELECT kode_produk, qty, harga_beli
        FROM detail_pembelian
        WHERE pembelian_id = ?
    """, (pembelian_id,))
    hasil = cursor.fetchall()
    conn.close()
    return hasil

def update_pembelian(pembelian_id, hasil_koreksi):
    conn = get_connection()
    cursor = conn.cursor()
    # Hapus detail lama
    cursor.execute("DELETE FROM detail_pembelian WHERE pembelian_id = ?", (pembelian_id,))
    # Tambahkan detail baru
    for item in hasil_koreksi:
        cursor.execute("""
            INSERT INTO detail_pembelian (pembelian_id, kode_produk, qty, harga_beli)
            VALUES (?, ?, ?, ?)   
        """, (
            pembelian_id,
            item["kode_produk"],
            item["qty"],
            item["harga_beli"]
        ))
        total_baru = sum(item["qty"] * item["harga_beli"] for item in hasil_koreksi)
        cursor.execute("UPDATE transaksi_pembelian SET total_harga = ? WHERE id_pembelian = ?", (total_baru, pembelian_id))
    conn.commit()
    conn.close()