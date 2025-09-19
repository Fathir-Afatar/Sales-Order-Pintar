import sqlite3

DB_PATH = "C:/Users/Fathir/Documents/pos-pintar-by-fathir/data/pos.db"

def ambil_detail_transaksi(id_transaksi, tipe):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Akses kolom by name

    cursor = conn.cursor()

    if tipe == "penjualan":
        cursor.execute("""
            SELECT nama_produk, jumlah, harga_satuan, subtotal
            FROM detail_penjualan
            WHERE transaksi_id = ?
        """, (id_transaksi,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    elif tipe == "pembelian":
        cursor.execute("""
        SELECT produk_id, qty, harga_beli
        FROM detail_pembelian
        WHERE pembelian_id = ?
        """, (id_transaksi,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    elif tipe == "pengeluaran":
        cursor.execute("""
        SELECT kategori, keterangan, tanggal, nominal
        FROM pengeluaran
        WHERE id_pengeluaran = ?
        """, (id_transaksi,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {}
    
    else:
        conn.close()
        return []

def get_detail_transaksi(id_transaksi, tipe):
    print("Mendapatkan detail transaksi untuk tipe:", tipe)
    if tipe == "penjualan":
        return ambil_detail_transaksi(id_transaksi, tipe)
    elif tipe == "pembelian":
        return ambil_detail_transaksi(id_transaksi, tipe)
    elif tipe == "pengeluaran":
        return ambil_detail_transaksi(id_transaksi, tipe)
    
def get_ringkasan_laporan(tanggal_awal, tanggal_akhir):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total Penjualan

    cursor.execute("""
        SELECT SUM(total_harga) FROM transaksi_penjualan
        WHERE DATE(tanggal) BETWEEN DATE(?) AND DATE(?)
    """, (tanggal_awal, tanggal_akhir))
    total_penjualan = cursor.fetchone()[0] or 0

    # Total Pembelian

    cursor.execute("""
        SELECT SUM(total_harga) FROM transaksi_pembelian
        WHERE DATE(tanggal) BETWEEN DATE(?) AND DATE(?)
    """, (tanggal_awal, tanggal_akhir))
    total_pembelian = cursor.fetchone()[0] or 0

    # Total Pengeluaran

    cursor.execute("""
        SELECT SUM(nominal) FROM pengeluaran
        WHERE DATE(tanggal) BETWEEN DATE(?) AND DATE(?)
    """, (tanggal_awal, tanggal_akhir))
    total_pengeluaran = cursor.fetchone()[0] or 0

    conn.close()

    return {
        "penjualan": total_penjualan,
        "pembelian": total_pembelian,
        "pengeluaran": total_pengeluaran
    }
