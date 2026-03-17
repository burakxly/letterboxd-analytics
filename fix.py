import sqlite3

conn = sqlite3.connect("letterboxd_master.db")

# Aynı İsim, Aynı Tarih ve Aynı Yıl'a sahip filmlerin sadece İLK eklenen (orijinal) halini tutup, 
# botun az önce yanlışlıkla eklediği tüm kopyaları siliyoruz.
query = """
DELETE FROM movies 
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM movies 
    GROUP BY Name, "Watched Date", Year
)
"""
conn.execute(query)
conn.commit()
conn.close()

print("Veritabanı temizlendi, az önce eklenen kopyalar yok edildi!")