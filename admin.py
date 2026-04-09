import secrets
from datetime import datetime, timedelta
import sqlite3

def generate_code(username, credit, days):
    access_code = secrets.token_hex(8).upper()
    expiry_date = (datetime.now() + timedelta(days=days)).isoformat()
    
    conn = sqlite3.connect('/tmp/xiolim_web.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  access_code TEXT UNIQUE,
                  credit INTEGER DEFAULT 0,
                  expiry_date TIMESTAMP)''')
    c.execute("INSERT INTO users (username, access_code, credit, expiry_date) VALUES (?, ?, ?, ?)",
              (username, access_code, credit, expiry_date))
    conn.commit()
    conn.close()
    
    return access_code

if __name__ == "__main__":
    # Jalanin langsung dari terminal Vercel
    username = input("Username pelanggan: ")
    credit = int(input("Jumlah kredit: "))
    days = int(input("Masa aktif (hari): "))
    code = generate_code(username, credit, days)
    print(f"\n🔥 KODE AKSES: {code}")
    print(f"📅 Expiry: {(datetime.now() + timedelta(days=days)).date()}")
