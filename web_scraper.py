import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser
import time
import json
import re
import os

# --- AYARLAR ---
DB_NAME = "letterboxd_master.db"
RSS_URL = "https://letterboxd.com/burakxly/rss/"
TMDB_KEY = os.environ.get("TMDB_API_KEY", "")
OMDB_KEY  = os.environ.get("OMDB_API_KEY", "")


# ─────────────────────────────────────────────────────────
# 0. VERİTABANI MIGRATION — yeni kolonları güvenle ekler
# ─────────────────────────────────────────────────────────
def migrate_db():
    conn = sqlite3.connect(DB_NAME)
    new_columns = [
        ("Community_Rating",  "REAL    DEFAULT 0"),
        ("Community_Votes",   "INTEGER DEFAULT 0"),
        ("Backdrop_URL",      "TEXT    DEFAULT ''"),
        ("Original_Language", "TEXT    DEFAULT ''"),
        ("TMDB_ID",           "INTEGER DEFAULT 0"),
        ("IMDb_ID",           "TEXT    DEFAULT ''"),
        ("IMDb_Rating",       "REAL    DEFAULT 0"),
        ("Oscar_Wins",        "INTEGER DEFAULT 0"),
        ("Oscar_Noms",        "INTEGER DEFAULT 0"),
    ]
    for col_name, col_def in new_columns:
        try:
            conn.execute(f"ALTER TABLE movies ADD COLUMN {col_name} {col_def}")
            print(f"[migration] Kolon eklendi: {col_name}")
        except sqlite3.OperationalError:
            pass  # zaten var
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────────
# 1. RSS SYNC — değişmedi
# ─────────────────────────────────────────────────────────
def sync_rss_to_db():
    print(f"[{time.ctime()}] RSS Kontrol ediliyor...")
    feed = feedparser.parse(RSS_URL)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    new_count = 0
    for entry in reversed(feed.entries):
        movie_name = getattr(entry, 'letterboxd_filmtitle', None)
        if not movie_name:
            continue
        raw_link    = getattr(entry, 'link', '')
        watched_date = getattr(entry, 'letterboxd_watcheddate', "")
        try:
            film_year = int(getattr(entry, 'letterboxd_filmyear', 0))
        except:
            film_year = 0

        match = re.search(r'/film/([^/]+)/', raw_link)
        movie_link = f"https://letterboxd.com/film/{match.group(1)}/" if match else raw_link

        try:
            raw_rating = float(entry.letterboxd_memberrating)
        except:
            raw_rating = 0.0

        cursor.execute(
            "SELECT * FROM movies WHERE Name = ? AND \"Watched Date\" = ? AND Year = ?",
            (movie_name, watched_date, film_year)
        )
        if cursor.fetchone() is None:
            print(f"Yeni keşif: {movie_name} ({film_year})")
            cursor.execute("""
                INSERT INTO movies
                    (Name, Rating, "Watched Date", "Letterboxd URI",
                     Runtime, Director, Genre, Year, Watched_Date_Log, Poster_URL)
                VALUES (?, ?, ?, ?, 0, '', '', ?, ?, '')
            """, (movie_name, raw_rating, watched_date, movie_link, film_year, watched_date))
            new_count += 1

    conn.commit()
    conn.close()
    print(f"Senkronizasyon: {new_count} yeni film eklendi.")


# ─────────────────────────────────────────────────────────
# 2. LETTERBOXD ENRİCHMENT — Director/Genre/Runtime/Poster
#    + Community_Rating (zaten aynı sayfa, bedava)
# ─────────────────────────────────────────────────────────
def enrich_movie_data():
    print(f"[{time.ctime()}] Letterboxd verisi kazınıyor...")
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("""
        SELECT * FROM movies
        WHERE Runtime = 0 OR Director = '' OR Genre = ''
           OR Poster_URL  IS NULL OR Poster_URL  = ''
           OR Community_Rating IS NULL OR Community_Rating = 0
    """, conn)

    if df.empty:
        print("Letterboxd verisi güncel.")
        conn.close()
        return

    for _, row in df.iterrows():
        original_url = row['Letterboxd URI'] or ''
        if not original_url or str(original_url) in ('nan', 'None'):
            continue
        original_url = str(original_url)
        match = re.search(r'/film/([^/]+)/', original_url)
        clean_url = f"https://letterboxd.com/film/{match.group(1)}/" if match else original_url

        print(f"Kazınıyor: {row['Name']}")
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            resp = requests.get(clean_url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'lxml')

            script_tag = soup.find('script', type='application/ld+json')
            if not script_tag:
                time.sleep(1)
                continue

            raw_json = script_tag.text.replace('/* <![CDATA[ */', '').replace('/* ]]> */', '').strip()
            data = json.loads(raw_json)

            # Poster
            poster_url = data.get('image', '')
            if not poster_url:
                og = soup.find('meta', property='og:image')
                if og:
                    poster_url = og.get('content', '')

            # Director
            directors = data.get('director', [])
            director_name = ", ".join([d.get('name') for d in directors]) if directors else ""

            # Genre
            genres = data.get('genre', [])
            genre_name = ", ".join(genres) if isinstance(genres, list) else genres

            # Runtime
            duration = data.get('duration', '0')
            runtime = int(''.join(filter(str.isdigit, str(duration)))) if duration != '0' else 0
            if runtime == 0:
                footer_p = soup.find('p', class_='text-link text-footer')
                if footer_p:
                    m = re.search(r'(\d+)\s*mins?', footer_p.text)
                    if m:
                        runtime = int(m.group(1))

            # Year
            released = data.get('releasedEvent', [])
            if isinstance(released, list) and released:
                year = released[0].get('startDate', '0')[:4]
            elif isinstance(released, dict):
                year = released.get('startDate', '0')[:4]
            else:
                year = 0

            # Community Rating (Letterboxd ortalama puanı) — yeni!
            agg = data.get('aggregateRating', {})
            community_rating = float(agg.get('ratingValue', 0) or 0)
            community_votes  = int(agg.get('ratingCount',  0) or 0)

            conn.execute("""
                UPDATE movies
                SET Director = ?, Genre = ?, Runtime = ?, Year = ?,
                    "Letterboxd URI" = ?, Poster_URL = ?,
                    Community_Rating = ?, Community_Votes = ?
                WHERE Name = ? AND "Letterboxd URI" = ?
            """, (director_name, genre_name, runtime, year,
                  clean_url, poster_url,
                  community_rating, community_votes,
                  row['Name'], original_url))
            conn.commit()
            print(f"[OK] {director_name} | {genre_name} | {runtime}dk | community={community_rating}")

            time.sleep(1)

        except Exception as e:
            print(f"Hata ({row['Name']}): {e}")

    conn.close()


# ─────────────────────────────────────────────────────────
# 3. TMDB + OMDB ENRİCHMENT — Backdrop / Dil / IMDb / Oscar
# ─────────────────────────────────────────────────────────
def enrich_extra_data():
    if not TMDB_KEY and not OMDB_KEY:
        print("[extra] TMDB_API_KEY ve OMDB_API_KEY bulunamadı, atlanıyor.")
        return

    print(f"[{time.ctime()}] TMDB/OMDB verisi çekiliyor...")
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("""
        SELECT rowid, Name, Year, "Letterboxd URI",
               Backdrop_URL, Original_Language, IMDb_Rating
        FROM movies
        WHERE (Backdrop_URL IS NULL OR Backdrop_URL = '')
           OR (Original_Language IS NULL OR Original_Language = '')
           OR (IMDb_Rating IS NULL OR IMDb_Rating = 0)
    """, conn)

    if df.empty:
        print("[extra] TMDB/OMDB verisi güncel.")
        conn.close()
        return

    print(f"{len(df)} film için TMDB/OMDB verisi çekiliyor...")

    for _, row in df.iterrows():
        name   = str(row['Name'])
        year   = int(row['Year'] or 0)
        rowid  = int(row['rowid'])

        backdrop_url = str(row.get('Backdrop_URL') or '')
        language     = str(row.get('Original_Language') or '')
        tmdb_id      = 0
        imdb_id      = ''
        imdb_rating  = float(row.get('IMDb_Rating') or 0)
        oscar_wins   = 0
        oscar_noms   = 0

        # ── TMDB ──────────────────────────────────────────
        if TMDB_KEY and (not backdrop_url or not language):
            try:
                params = {"query": name, "api_key": TMDB_KEY, "language": "en-US"}
                if year > 0:
                    params["year"] = year
                r = requests.get(
                    "https://api.themoviedb.org/3/search/movie",
                    params=params, timeout=8
                )
                results = r.json().get("results", [])
                if results:
                    tmdb_id = results[0]["id"]
                    d = requests.get(
                        f"https://api.themoviedb.org/3/movie/{tmdb_id}",
                        params={"api_key": TMDB_KEY}, timeout=8
                    ).json()
                    bp = d.get("backdrop_path", "")
                    backdrop_url = f"https://image.tmdb.org/t/p/w1280{bp}" if bp else ""
                    language = d.get("original_language", "")
                time.sleep(0.1)
            except Exception as e:
                print(f"TMDB hata ({name}): {e}")

        # ── OMDB ──────────────────────────────────────────
        if OMDB_KEY and imdb_rating == 0:
            try:
                params = {"t": name, "apikey": OMDB_KEY}
                if year > 0:
                    params["y"] = year
                r = requests.get("https://www.omdbapi.com/", params=params, timeout=8)
                data = r.json()
                if data.get("Response") == "True":
                    imdb_id = data.get("imdbID", "")
                    raw_imdb = data.get("imdbRating", "N/A")
                    imdb_rating = float(raw_imdb) if raw_imdb not in ("N/A", "", None) else 0.0
                    awards = data.get("Awards", "") or ""
                    if awards and awards != "N/A":
                        m = re.search(r'Won (\d+) Oscar', awards)
                        if m:
                            oscar_wins = int(m.group(1))
                        m = re.search(r'Nominated for (\d+) Oscar', awards)
                        if m:
                            oscar_noms = int(m.group(1))
                time.sleep(0.25)
            except Exception as e:
                print(f"OMDB hata ({name}): {e}")

        # ── KAYDET ────────────────────────────────────────
        conn.execute("""
            UPDATE movies SET
                Backdrop_URL      = CASE WHEN Backdrop_URL      IS NULL OR Backdrop_URL      = '' THEN ? ELSE Backdrop_URL      END,
                Original_Language = CASE WHEN Original_Language IS NULL OR Original_Language = '' THEN ? ELSE Original_Language END,
                TMDB_ID           = CASE WHEN TMDB_ID = 0 THEN ? ELSE TMDB_ID END,
                IMDb_ID           = CASE WHEN IMDb_ID  IS NULL OR IMDb_ID  = '' THEN ? ELSE IMDb_ID  END,
                IMDb_Rating       = CASE WHEN IMDb_Rating = 0   THEN ? ELSE IMDb_Rating       END,
                Oscar_Wins        = CASE WHEN Oscar_Wins = 0    THEN ? ELSE Oscar_Wins        END,
                Oscar_Noms        = CASE WHEN Oscar_Noms = 0    THEN ? ELSE Oscar_Noms        END
            WHERE rowid = ?
        """, (backdrop_url, language, tmdb_id, imdb_id,
              imdb_rating, oscar_wins, oscar_noms, rowid))
        conn.commit()

        parts = []
        if backdrop_url: parts.append("backdrop+")
        if language:     parts.append(f"lang={language}")
        if imdb_rating:  parts.append(f"imdb={imdb_rating}")
        if oscar_wins or oscar_noms: parts.append(f"oscar={oscar_wins}W/{oscar_noms}N")
        if parts:
            print(f"[OK] {name}: {' | '.join(parts)}")

    conn.close()
    print("[extra] Tamamlandı.")


# ─────────────────────────────────────────────────────────
# 4. WATCHED-ONLY SYNC — watched.csv'deki filmleri ekler
#    Diary'de olmayan (Watched Date = NULL) filmler için
#    sadece total sayısına katkı sağlar, tarih bazlı
#    metriklere (bu yıl, bu hafta) dahil edilmez.
# ─────────────────────────────────────────────────────────
MANUAL_CSV = os.path.join(os.path.dirname(__file__), "manual_watched.csv")

def sync_manual_watched():
    if not os.path.exists(MANUAL_CSV):
        return

    try:
        df = pd.read_csv(MANUAL_CSV)
    except Exception as e:
        print(f"[manual] CSV okunamadi: {e}")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    new_count = 0

    for _, row in df.iterrows():
        name = str(row.get("Name", "")).strip()
        year = int(row.get("Year", 0) or 0)
        uri  = str(row.get("Letterboxd URI", "")).strip()
        if not name:
            continue
        cursor.execute(
            'SELECT 1 FROM movies WHERE Name = ? AND Year = ?',
            (name, year)
        )
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO movies
                    (Name, Rating, "Watched Date", "Letterboxd URI",
                     Runtime, Director, Genre, Year, Watched_Date_Log, Poster_URL)
                VALUES (?, 0, NULL, ?, 0, '', '', ?, '', '')
            """, (name, uri, year))
            new_count += 1
            print(f"[manual] Eklendi: {name} ({year})")

    conn.commit()
    conn.close()
    print(f"[manual] {new_count} film eklendi.")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    migrate_db()
    sync_rss_to_db()
    sync_manual_watched()
    enrich_movie_data()
    enrich_extra_data()
