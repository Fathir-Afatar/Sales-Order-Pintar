import sqlite3
from app.constants.config import get_connection

DB_PATH = "C:/Users/Fathir/Documents/pos-pintar-by-fathir/data/pos.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

# Get Produk

def get_produk(kode_produk):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_produk, nama_produk, harga_jual FROM produk WHERE kode_produk = ?", (kode_produk,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id" : row [0],
            "nama" : row [1],
            "harga_jual" : row [2]
        }
    return None

# Add New Product (untuk transaksi pertama kali)

def tambah_produk(data):
       
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                   INSERT INTO produk (nama_produk, kode_produk, kategori_id, merk, harga_beli, harga_jual, stok, berat)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (data["nama"], data["kode_produk"], data["kategori_id"], data["merk"], data["harga_beli"], data["harga_jual"], data["stok"], data["berat"]))
        conn.commit()
        return True
    except Exception as e:
        print(f"Gagal tambah produk: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# Edit Product Price

def edit_harga_produk(id_produk, harga_baru):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE produk SET harga_jual = ? WHERE id_produk = ?
                """, (harga_baru, id_produk))
    conn.commit()
    conn.close()

# Delete Product

def hapus_produk(id_produk):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   DELETE FROM produk WHERE id_produk = ?
                """, (id_produk,))
    conn.commit()
    conn.close()

# Get Product Data by ID

def ambil_produk(id_produk):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM produk WHERE id_produk = ?
                """, (id_produk,))
    result = cursor.fetchone()
    conn.close()
    return result

# Update Produk

def update_produk(id_produk, nama, kode, kategori_id, merk, harga_beli, harga_jual, stok, berat):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if harga_jual < 0 or harga_beli < 0 or berat < 0 or stok < 0:
            print("Data produk tidak valid.")
            return False
    except TypeError as e:
        print("[ERROR] Tipe data tidak valid:", e)
        return False
    print("[DEBUG] Tipe data:")
    print("harga_beli:", type(harga_beli))
    print("harga_jual:", type(harga_jual))
    print("stok:", type(stok))
    print("berat:", type(berat))

    cursor.execute("""
                   UPDATE produk
                   SET nama_produk = ?, kode_produk = ?, kategori_id = ?, merk = ?, harga_beli = ?, harga_jual = ?, stok = ?, berat = ?
                   WHERE id_produk = ?
                """, (nama, kode, kategori_id, merk, harga_beli, harga_jual, stok, berat, id_produk))
    print("Menjalankan update_produk dengan:")
    print("ID:", id_produk)
    print("Nama:", nama)
    print("Kode:", kode)
    print("Kategori ID:", kategori_id)
    print("Harga Beli:", harga_beli)
    print("Harga Jual:", harga_jual)
    print("Stok:", stok)
    print("Berat:", berat)
    conn.commit()
    conn.close()
    return True

# Tambah stok (untuk transaksi yang kedua dan seterusnya dari produk atau supplier yang sama)

def tambah_stok(kode_produk: str, jumlah:int):
    """
    Menambahkan stok ke produk yang sudah ada.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE produk 
            SET stok = stok + ?
            WHERE kode_produk = ?    
            """, (jumlah, kode_produk))
        conn.commit()
        return True
    except Exception as e:
        print(f"Gagal menambahkan stok: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# Semua Produk

def semua_produk():
    conn = get_connection()
    cursor = conn.cursor()
    print("[INFO] Menjalankan query semua_produk dengan LEFT JOIN")
    cursor.execute("""SELECT produk.*, kategori.nama_kategori FROM produk LEFT JOIN kategori ON produk.kategori_id = kategori.id_kategori""")
    rows = cursor.fetchall()
    conn.close()

    # Buat list of object atau dict
    produk_list = []

    for row in rows:
        print("[DEBUG] Row:", row)
        produk = {
            "id_produk": row[0],
            "nama_produk": row[1],
            "kode_produk": row[2],
            "kategori_produk": row[3],
            "merk": row[4],
            "harga_beli": row[5],
            "harga_jual": row[6],
            "stok": row[7],
            "berat": row[8]
        }
        produk_list.append(produk)
    #keys = ["id_produk", "nama_produk", "kode_produk", "kategori_id", "merk", "harga_beli", "harga_jual", "stok", "berat","deleted_at", "nama_kategori"]
    #produk_list = [dict(zip(keys, row)) for row in rows]
    return produk_list

# Stok Product Check

def cek_stok(id_produk):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT stok FROM produk WHERE id_produk = ?
                   """, (id_produk,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_harga_beli(kode_produk):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT harga_beli FROM produk WHERE kode_produk = ?", (kode_produk,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def ambil_daftar_produk():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kode_produk, nama_produk, harga_beli FROM produk")
    hasil = cursor.fetchall()
    conn.close()
    return [{"kode_produk": row[0], "nama": row[1], "harga": row[2]} for row in hasil]

def kurangi_stok(kode_produk, jumlah):
    conn = get_connection()
    cursor = conn.cursor()

    # AMbil stok saat ini

    cursor.execute("SELECT stok FROM produk WHERE kode_produk =?", (kode_produk,))
    hasil = cursor.fetchone()

    if hasil :
        stok_sekarang = hasil[0]
        stok_baru = max(0, stok_sekarang - jumlah) # Hindari stok negatif

        cursor.execute("UPDATE produk SET stok = ? WHERE kode_produk = ?", (stok_baru, kode_produk))
        conn.commit()
    else:
        print(f"[ERROR] Produk dengan kode {kode_produk} tidak ditemukan.")
    
    conn.close()

def bersihkan_angka(nilai):
    try:
        nilai_bersih = str(nilai).replace("Rp", "").replace(",", "").strip()
        return float(nilai_bersih)
    except Exception as e:
        print("[ERROR] Gagal parsing angka:", nilai, e)
        return None

def get_kategori_id_by_nama(nama_kategori):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_kategori FROM kategori WHERE nama_kategori = ?", (nama_kategori,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def ambil_semua_kategori():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama_kategori FROM kategori ORDER BY nama_kategori ASC")
    hasil = cursor.fetchall()
    conn.close()
    return [row[0] for row in hasil]

def ambil_produk_by_kategori_id(kategori_id):
    conn = get_connection()
    cursor = conn.cursor()
    print("[INFO] Menjalankan query semua_produk dengan LEFT JOIN")
    cursor.execute("""
        SELECT produk.*, kategori.nama_kategori FROM produk LEFT JOIN kategori ON produk.kategori_id = kategori.id_kategori WHERE produk.kategori_id = ? """, (kategori_id,))
    rows = cursor.fetchall()
    conn.close()

    keys = ["id_produk", "nama_produk", "kode_produk", "kategori_id", "merk", "harga_beli", "harga_jual", "stok", "berat","deleted_at", "nama_kategori"]
    return [dict(zip(keys, row)) for row in rows]

def tambah_kategori(nama):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO kategori (nama_kategori) VALUES (?)", (nama,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
