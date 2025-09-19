from collections import Counter
from datetime import datetime
import calendar
from app.constants.config import get_connection

# Ambil histori transaksi oleh member

def ambil_histori_member(kode_member):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tanggal, total_harga, produk
        FROM transaksi_penjualan
        WHERE kode_member = ?
        ORDER BY tanggal ASC
    """, (kode_member,))

    hasil = cursor.fetchall()
    conn.close
    return hasil

# Preferensi produk (paling sering dibeli)

def analisa_preferensi(histori):
    produk_counter = Counter()
    for h in histori:
        produk_counter[h["nama_produk"]] += h["qty"]
    return produk_counter.most_common(5)

def hitung_frekuensi(histori):  # untuk frekuensi member dalam transaksi / belanja
    bulan_counter = Counter()
    for h in histori:
        dt = datetime.strptime(h["tanggal"], "%Y-%m-%d")
        bulan_str = dt.strftime("%Y-%m")
        bulan_counter[bulan_counter] += 1
    return dict(bulan_counter)

# Total belanja member

def total_belanja(histori):
    return sum(h["qty"] * h["harga_jual"] for h in histori)

# Rekap lengkap laporan member

def buat_laporan_member(kode_member):
    # Ambil data transaksi berdasarkan kode member

    transaksi_member = [t for t in total_belanja if t['kode_member'] == kode_member]

    # Hitung total pembelian

    total_pembelian = sum(t['jumlah'] * t['harga'] for t in transaksi_member)

    # Buat laporan sederhana

    laporan = {
        'kode_member' : kode_member,
        'total_transaksi': len(transaksi_member),
        'total_pembelian': total_pembelian
    }

def hitung_produk_favorit(histori):
    from collections import Counter
    produk_terbeli = [row[2] for row in histori] #asumsi row[2] nama produk
    
    if not produk_terbeli:
        return None
    return Counter(produk_terbeli).most_common(1)[0][0]


def laporan_member_bulanan(bulan_str="2025-07"):  # Untuk rekap semua member berdasarkan bulan
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tp.kode_member, m.nama, COUNT(*) as total_transaksi, SUM(tp.total_harga) as total_belanja
        FROM transaksi_penjualan tp
        JOIN member m ON tp.kode_member = m.kode_member
        GROUP BY tp.kode_member       
    """, (bulan_str,))

    rows = cursor.fetchall()
    conn.close()

    laporan = []
    for r in rows:
        laporan.append({
            "kode_member": r[0],
            "nama": r[1],
            "total_transaksi": r[2],
            "total_belanja": r[3]
        })
    return laporan



