import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser
import time
import json

# --- AYARLAR ---
DB_NAME = "letterboxd_master.db"
RSS_URL = "https://letterboxd.com/burakxly/rss/"

def sync_rss_to_db():
    print(f"[{time.ctime()}] RSS Kontrol ediliyor...")
    feed = feedparser.parse(RSS_URL)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    new_count = 0
    for entry in feed.entries:
        movie_name = entry.letterboxd_filmtitle
        movie_link = entry.link
        watched_date = getattr(entry, 'letterboxd_watcheddate', "")
        
        try:
            raw_rating = int(entry.letterboxd_memberrating) / 2
        except:
            raw_rating = 0.0

        # Veritabanında bu film (bu tarihle) var mı?
        cursor.execute("SELECT * FROM movies WHERE Name = ? AND \"Watched Date\" = ?", (movie_name, watched_date))
        if cursor.fetchone() is None:
            print(f"Yeni keşif: {movie_name}")
            # İlk başta boş verilerle ekliyoruz, enrich_data() hepsini dolduracak
            cursor.execute("""
                INSERT INTO movies (Name, Rating, "Watched Date", "Letterboxd URI", Runtime, Director, Genre, Year, Watched_Date_Log)
                VALUES (?, ?, ?, ?, 0, '', '', 0, ?)
            """, (movie_name, raw_rating, watched_date, movie_link, watched_date))
            new_count += 1
    
    conn.commit()
    conn.close()
    print(f"Senkronizasyon: {new_count} yeni film eklendi.")

def enrich_movie_data():
    print(f"[{time.ctime()}] Eksik veriler (Yönetmen, Tür, Süre) kazınıyor...")
    conn = sqlite3.connect(DB_NAME)
    # Verisi eksik olanları seç (Runtime 0 olanlar veya Director'ı boş olanlar)
    df = pd.read_sql("SELECT * FROM movies WHERE Runtime = 0 OR Director = '' OR Genre = ''", conn)
    
    if df.empty:
        print("Tüm veriler güncel.")
        conn.close()
        return

    for index, row in df.iterrows():
        url = row['Letterboxd URI']
        print(f"Veri çekiliyor: {row['Name']}")
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Letterboxd verileri JSON-LD içinde yapılandırılmış halde tutar (En temiz yöntem)
            script_tag = soup.find('script', type='application/ld+json')
            if script_tag:
                data = json.loads(script_tag.string)
                
                # 1. Yönetmen (Birden fazlaysa virgülle ayırır)
                directors = data.get('director', [])
                director_name = ", ".join([d.get('name') for d in directors]) if directors else ""
                
                # 2. Türler (Genre)
                genres = data.get('genre', [])
                genre_name = ", ".join(genres) if isinstance(genres, list) else genres
                
                # 3. Süre (Runtime)
                duration = data.get('duration', '0') # Format: PT124M
                runtime = int(''.join(filter(str.isdigit, duration))) if duration != '0' else 0
                
                # 4. Yıl (Release Year)
                released = data.get('releasedEvent', {})
                year = released.get('startDate', '0')[:4] if released else 0

                # Veritabanını güncelle
                conn.execute("""
                    UPDATE movies 
                    SET Director = ?, Genre = ?, Runtime = ?, Year = ? 
                    WHERE Name = ? AND "Letterboxd URI" = ?
                """, (director_name, genre_name, runtime, year, row['Name'], url))
                conn.commit()
                print(f"Başarılı: {director_name} | {genre_name} | {runtime} dk")
            
            time.sleep(1) # Letterboxd'dan ban yememek için kısa bir mola
        except Exception as e:
            print(f"Hata ({row['Name']}): {e}")
            
    conn.close()

if __name__ == "__main__":
    sync_rss_to_db()
    enrich_movie_data()
