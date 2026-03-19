import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import time

DB_NAME = "letterboxd_master.db"

conn = sqlite3.connect(DB_NAME)

# Poster_URL kolonunu ekle (zaten varsa hata vermez)
try:
    conn.execute("ALTER TABLE movies ADD COLUMN Poster_URL TEXT DEFAULT ''")
    conn.commit()
    print("Poster_URL kolonu eklendi.")
except:
    print("Poster_URL kolonu zaten var.")

# Posteri olmayan filmleri çek
df_missing = conn.execute(
    "SELECT rowid, Name, \"Letterboxd URI\" FROM movies WHERE Poster_URL IS NULL OR Poster_URL = ''"
).fetchall()

print(f"{len(df_missing)} film için poster çekilecek...")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for i, (rowid, name, url) in enumerate(df_missing):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        script_tag = soup.find('script', type='application/ld+json')
        poster = ""
        if script_tag:
            raw_json = script_tag.text.replace('/* <![CDATA[ */', '').replace('/* ]]> */', '').strip()
            data = json.loads(raw_json)
            poster = data.get('image', '')
        
        if not poster:
            og = soup.find('meta', property='og:image')
            if og:
                poster = og.get('content', '')

        conn.execute("UPDATE movies SET Poster_URL = ? WHERE rowid = ?", (poster, rowid))
        conn.commit()
        print(f"[{i+1}/{len(df_missing)}] {name}: {poster[:50] if poster else 'BULUNAMADI'}")
        time.sleep(1)
    except Exception as e:
        print(f"Hata ({name}): {e}")

conn.close()
print("Tamamlandı.")