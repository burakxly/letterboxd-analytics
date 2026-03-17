import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser
import time
import json
import re

# --- AYARLAR ---
DB_NAME = "letterboxd_master.db"
RSS_URL = "https://letterboxd.com/burakxly/rss/"

def sync_rss_to_db():
    print(f"[{time.ctime()}] RSS Kontrol ediliyor...")
    feed = feedparser.parse(RSS_URL)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    new_count = 0
    for entry in reversed(feed.entries):
        movie_name = entry.letterboxd_filmtitle
        raw_link = entry.link
        watched_date = getattr(entry, 'letterboxd_watcheddate', "")
        
        # Linki temizle (Günlük sayfasından ana film sayfasına çevir)
        match = re.search(r'/film/([^/]+)/', raw_link)
        movie_link = f"https://letterboxd.com/film/{match.group(1)}/" if match else raw_link
        
        try:
            raw_rating = float(entry.letterboxd_memberrating)
        except:
            raw_rating = 0.0

        cursor.execute("SELECT * FROM movies WHERE Name = ? AND \"Watched Date\" = ?", (movie_name, watched_date))
        if cursor.fetchone() is None:
            print(f"Yeni keşif: {movie_name}")
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
    # Verisi eksik olanları tekrar çek
    df = pd.read_sql("SELECT * FROM movies WHERE Runtime = 0 OR Director = '' OR Genre = ''", conn)
    
    if df.empty:
        print("Tüm veriler güncel.")
        conn.close()
        return

    for index, row in df.iterrows():
        original_url = row['Letterboxd URI']
        
        # Eğer veritabanında eski bozuk link kaldıysa onu da anlık temizle
        match = re.search(r'/film/([^/]+)/', original_url)
        clean_url = f"https://letterboxd.com/film/{match.group(1)}/" if match else original_url

        print(f"Veri çekiliyor: {row['Name']}")
        try:
            # Bota sahte Chrome kimliği (User-Agent) takıyoruz ki site bizi insan sansın
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(clean_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            script_tag = soup.find('script', type='application/ld+json')
            if script_tag:
                # Kılıfı yırt
                raw_json = script_tag.text.replace('/* <![CDATA[ */', '').replace('/* ]]> */', '').strip()
                data = json.loads(raw_json)
                
                directors = data.get('director', [])
                director_name = ", ".join([d.get('name') for d in directors]) if directors else ""
                
                genres = data.get('genre', [])
                genre_name = ", ".join(genres) if isinstance(genres, list) else genres
                
                # ---- SÜRE (RUNTIME) KAZIMA BLOĞUNU BUNUNLA DEĞİŞTİR ----
                duration = data.get('duration', '0')
                runtime = int(''.join(filter(str.isdigit, str(duration)))) if duration != '0' else 0
                
                # Letterboxd JSON içine süreyi koymayı unuttuysa B Planı (HTML Metni)
                if runtime == 0:
                    footer_p = soup.find('p', class_='text-link text-footer')
                    if footer_p:
                        match = re.search(r'(\d+)\s*mins?', footer_p.text)
                        if match:
                            runtime = int(match.group(1))
                # --------------------------------------------------------
                
                # Yıl formatı bazen liste bazen dict geliyor, onu da sağlama aldık
                released = data.get('releasedEvent', [])
                if isinstance(released, list) and len(released) > 0:
                    year = released[0].get('startDate', '0')[:4]
                elif isinstance(released, dict):
                    year = released.get('startDate', '0')[:4]
                else:
                    year = 0

                # Veritabanını Düzelt (Link dahil her şeyi güncelle)
                conn.execute("""
                    UPDATE movies 
                    SET Director = ?, Genre = ?, Runtime = ?, Year = ?, "Letterboxd URI" = ? 
                    WHERE Name = ? AND "Letterboxd URI" = ?
                """, (director_name, genre_name, runtime, year, clean_url, row['Name'], original_url))
                conn.commit()
                print(f"Başarılı: {director_name} | {genre_name} | {runtime} dk")
            
            time.sleep(1)
        except Exception as e:
            print(f"Hata ({row['Name']}): {e}")
            
    conn.close()

if __name__ == "__main__":
    sync_rss_to_db()
    enrich_movie_data()