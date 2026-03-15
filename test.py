import sqlite3
import pandas as pd
conn = sqlite3.connect("letterboxd_master.db")
# Tarihi olmayan (sadece izledim denen) filmleri listeler
check = pd.read_sql("SELECT Name FROM movies WHERE Watched_Date_Log IS NULL OR Watched_Date_Log = ''", conn)
print("Loglanmamış (Sadece izlendi işaretli) Filmler:")
print(check)
conn.close()