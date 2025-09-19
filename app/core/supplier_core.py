from app.constants.config import get_connection
conn = get_connection()

# Add Supplier

def tambah_supplier(nama_supplier, alamat=None, no_hp=None, kode_supplier=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO supplier (nama_supplier, alamat, no_hp, kode_supplier)
                   VALUES (?, ?, ?, ?)
                """, (nama_supplier, alamat, no_hp, kode_supplier))
    conn.commit()
    conn.close()

# Edit Supplier

def edit_supplier(id_supplier, nama_supplier=None, alamat=None, no_hp=None, kode_supplier=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE supplier SET "
    fields = []
    values = []

    if nama_supplier:
        fields.append("nama_supplier = ?")
        values.append(nama_supplier)
    if alamat:
        fields.append("alamat = ?")
        values.append(alamat)
    if no_hp:
        fields.append("no_hp = ?")
        values.append(no_hp)
    if kode_supplier:
        fields.append("kode_supplier = ?")
        values.append(kode_supplier)

    query += ", ".join(fields)
    query += " WHERE id_supplier = ?"
    values.append(id_supplier)

    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()

# Delete Supplier

def hapus_supplier(id_supplier):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM supplier WHERE id_supplier = ?", (id_supplier,))
    conn.commit()
    conn.close()

# Take All Supplier

def semua_supplier():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM supplier")
    result = cursor.fetchall()
    conn.close()
    return result

# Take All Supplier Base on ID

def ambil_supplier():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_supplier, nama_supplier FROM supplier")
    result = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "nama": row[1]} for row in result]

