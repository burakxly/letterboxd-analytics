import sqlite3
import os

if os.path.exists("letterboxd_master.db"):
    conn = sqlite3.connect("letterboxd_master.db")
    try:
        conn.execute("DELETE FROM movies WHERE Name = 'Sunset Boulevard'")
        conn.commit()
        print("Operasyon Başarılı: Sunset Boulevard zehri temizlendi!")
    except Exception as e:
        print(f"Hata: {e}")
    conn.close()
else:
    print("Veritabanı bu klasörde bulunamadı!")