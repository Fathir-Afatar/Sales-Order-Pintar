import sqlite3

from app.constants.config import get_connection

# Add New Member

def tambah_member(nama, alamat=None, nomor=None, tipe=None, ranting=None, kode_member=None):
    if not nama or not kode_member:
        raise ValueError("Nama dan kode member wajib diisi.")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO member (nama, alamat, no_hp, tipe, ranting, kode_member)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, (nama, alamat, nomor, tipe, ranting, kode_member))
    conn.commit()
    conn.close()

# Update Member Data

def update_member(id_member, nama, nomor, alamat, tipe, ranting, kode_member):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE member
                   SET nama = ?, no_hp=?, alamat = ?, tipe = ?, ranting = ?, kode_member = ?
                   WHERE id_member = ?
                """, (nama, nomor, alamat, tipe, ranting, kode_member, id_member))
    print("[DEBUG] UPDATE query berhasil? Rows affected:", cursor.rowcount)
    if cursor.rowcount == 0:
        print("[DEBUG] Tidak ada data yang diubah. Periksa id_member dan kode_member")
    conn.commit()
    conn.close()

# Delete Member

def hapus_member(id_member):
    print("[DEBUG] SQL Dijalankan")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM member WHERE id_member = ?", (id_member,))
    conn.commit()
    conn.close()

# Take All Member

def semua_member():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_member, nama, no_hp, alamat, tipe, ranting, kode_member FROM member")
    rows = cursor.fetchall()
    conn.close()

    member_list = []
    for row in rows:
        member = {
            "id_member": row[0],
            "nama" : row[1],
            "no_hp":row[2],
            "alamat":row[3],
            "tipe":row[4],
            "ranting":row[5],
            "kode_member":row[6]
            }
        member_list.append(member)
    return member_list

# Retrieved Member Based on ID

def ambil_by_kode_member(kode_member):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_member, nama, no_hp, alamat, tipe, ranting, kode_member
        FROM member
        WHERE kode_member = ?
    """, (kode_member,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id_member": row[0],
            "nama": row[1],
            "no_hp": row[2],
            "alamat": row[3],
            "tipe": row[4],
            "ranting": row[5],
            "kode_member": row[6]
        }
    return None

# Cari Member

def cari_member(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_member, nama, no_hp, alamat, tipe, ranting, kode_member
        FROM member
        WHERE nama LIKE ? OR no_hp LIKE ?
        """, (f'%{keyword}%', f'%{keyword}%'))
    hasil = cursor.fetchall()
    conn.close()

    return [
        {
            "id_member": row[0],
            "nama": row [1],
            "no_hp": row[2],
            "alamat": row[3],
            "tipe": row[4],
            "ranting": row[5],
            "kode_member": row[6]
        }
        for row in hasil
    ]

def semua_member_dropdown():
    members = semua_member()

    return [f"{m['id_member']} - {m['nama']}" for m in members]