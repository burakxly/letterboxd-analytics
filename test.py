import sqlite3
import pandas as pd
import os

# Dosyanın varlığını kontrol et
db_name = "letterboxd_master.db"
if not os.path.exists(db_name):
    print(f"HATA: {db_name} dosyası bu klasörde bulunamadı!")
else:
    conn = sqlite3.connect(db_name)
    try:
        # Tabloyu ve içindeki dolu süreleri kontrol et
        df = pd.read_sql("SELECT Name, Runtime FROM movies WHERE Runtime > 0 LIMIT 10", conn)
        if df.empty:
            print("Tablo bulundu ama tüm süreler 0 veya boş.")
        else:
            print("BAŞARILI! İşte örnek veriler:")
            print(df)
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        conn.close()