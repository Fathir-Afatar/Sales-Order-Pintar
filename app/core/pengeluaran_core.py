# Pengeluaran di luar sembako, pengadaan, transaksi.
# Digunakan seperti gaji, token listrik, truk dll
from datetime import datetime

from app.constants.config import get_connection

def tambah_pengeluaran(nama_pengeluaran, kategori, nominal, keterangan=None):
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    cursor = conn.cursor()
    if not isinstance(nominal, (int, float)):
        raise ValueError("Nominal harus berupa angka")
    if not kategori:
        raise ValueError("Kategori tidak boleh kosong")
    cursor.execute("""
                   INSERT INTO pengeluaran (tanggal, nama_pengeluaran, kategori, nominal, keterangan)
                   VALUES (?, ?, ?, ?, ?)
                """, (tanggal, nama_pengeluaran, kategori, nominal, keterangan))
    conn.commit()
    conn.close()

def semua_pengeluaran(limit = None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM pengeluaran ORDER BY tanggal DESC"
    if limit:
        query += f" LIMIT {limit}"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def pengeluaran_per_bulan(bulan: str, tahun: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM pengeluaran
        WHERE strftime('%m', tanggal) = ?
        AND strftime ('%Y', tanggal) = ?
    """, (bulan, str(tahun)))
    result = cursor.fetchall()
    conn.close()
    return result

def pengeluaran_per_kategori(kategori: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM pengeluaran
        WHERE kategori = ?
        ORDER BY tanggal DESC
    """, (kategori,))
    result = cursor.fetchall()
    conn.close()
    return result

def pengeluaran_bulan_kategori(bulan: str, tahun: int, kategori:str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM pengeluaran
        WHERE strftime ('%m', tanggal) = ?
        AND strftime('%Y', tanggal) = ?
        AND kategori = ?
    """, (bulan, str(tahun), kategori))
    result = cursor.fetchall()
    conn.close()
    return result

def total_pengeluaran_kategori(kategori: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM (nominal) FROM pengeluaran
        WHERE kategori = ?
    """,(kategori,))
    total = cursor.fetchone()[0]
    return total or 0

def hapus_pengeluaran(id_pengeluaran: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pengeluaran WHERE id_pengeluaran =?", (id_pengeluaran,))
    conn.commit()
    conn.close()

def edit_pengeluaran(id_pengeluaran: int,tanggal: str ,nama_pengeluaran: str, kategori: str, nominal: float, keterangan: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pengeluaran
        SET tanggal = ?, nama_pengeluaran = ?, kategori = ?, nominal = ?, keterangan = ?
        WHERE id_pengeluaran = ?
        """, (tanggal ,nama_pengeluaran, kategori, nominal, keterangan, id_pengeluaran))
    conn.commit()
    conn.close()