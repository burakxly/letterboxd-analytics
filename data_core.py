import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import streamlit as st

@st.cache_data(ttl=3600)
def fetch_poster_url(movie_page_url):
    if not movie_page_url: return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(movie_page_url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        script_tag = soup.find('script', type='application/ld+json')
        if script_tag:
            raw_json = script_tag.text.replace('/* <![CDATA[ */', '').replace('/* ]]> */', '').strip()
            data = json.loads(raw_json)
            if 'image' in data: return data['image']
                
        og_image = soup.find('meta', property='og:image')
        if og_image: return og_image.get('content')
    except: pass
    return "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"

@st.cache_data(ttl=3600)  
def load_data():
    conn = sqlite3.connect("letterboxd_master.db")
    df = pd.read_sql("SELECT * FROM movies", conn)
    conn.close()
    
    if 'Runtime' not in df.columns: df['Runtime'] = 0
    if 'Year' not in df.columns: df['Year'] = 0
    if 'Rating' not in df.columns: df['Rating'] = 0
    if 'Director' not in df.columns: df['Director'] = "Unknown"
    if 'Genre' not in df.columns: df['Genre'] = "Unknown"

    if 'Watched_Date_Log' in df.columns:
        df['Watched_Date_Log'] = pd.to_datetime(df['Watched_Date_Log'], errors='coerce')
    if 'Watched Date' in df.columns:
        df['Watched Date'] = pd.to_datetime(df['Watched Date'], errors='coerce') 
        
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0)
    df['Runtime'] = pd.to_numeric(df['Runtime'], errors='coerce').fillna(0)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0)
    
    return df

def get_latest_movie():
    conn = sqlite3.connect("letterboxd_master.db")
    last_movie_query = """
        SELECT Name, Rating, Director, Runtime, "Letterboxd URI" FROM movies 
        WHERE "Watched Date" IS NOT NULL AND "Watched Date" != ''
        ORDER BY date("Watched Date") DESC, rowid DESC LIMIT 1
    """
    last_movie_df = pd.read_sql(last_movie_query, conn)
    conn.close()

    if not last_movie_df.empty:
        last_name = str(last_movie_df['Name'].iloc[0]).upper()
        last_dir = str(last_movie_df['Director'].iloc[0]).split(',')[0]
        last_runtime = int(last_movie_df['Runtime'].iloc[0])
        last_url = str(last_movie_df['Letterboxd URI'].iloc[0])
        try: raw_rating = float(last_movie_df['Rating'].iloc[0])
        except: raw_rating = 0.0
        poster_url = str(last_movie_df['Poster_URL'].iloc[0]) or fetch_poster_url(last_url)
    else:
        last_name, last_dir, last_runtime, raw_rating, poster_url, last_url = "VERI YOK", "Unknown", 0, 0.0, "", "#"
        
    return last_name, last_dir, last_runtime, raw_rating, poster_url, last_url

def get_kpis(df_all, df_rated):
    # Filmleri İsim/Yönetmen üzerinden değil, eşsiz Linkleri üzerinden sayıyoruz
    total_films = len(df_all.drop_duplicates(subset=['Letterboxd URI']))
    total_hours = int(df_all['Runtime'].sum()) / 60 

    df_dir = df_rated.assign(Director=df_rated['Director'].str.split(', ')).explode('Director')
    df_dir = df_dir[~df_dir['Director'].isin(['Unknown', '', None])]
    dir_stats = df_dir.groupby('Director').agg(Film_Count=('Name', 'count'), Avg_Rating=('Rating', 'mean'))
    valid_dirs = dir_stats[dir_stats['Film_Count'] >= 5]

    if not valid_dirs.empty:
        best_dir_row = valid_dirs.sort_values(by='Avg_Rating', ascending=False).iloc[0]
        best_dir_name, best_dir_avg = best_dir_row.name, best_dir_row['Avg_Rating']
    else:
        best_dir_name, best_dir_avg = "N/A", 0.0

    df_genre = df_rated.assign(Genre=df_rated['Genre'].str.split(', ')).explode('Genre')
    df_genre = df_genre[~df_genre['Genre'].isin(['Unknown', '', None])]
    genre_stats = df_genre.groupby('Genre').agg(Film_Count=('Name', 'count'), Avg_Rating=('Rating', 'mean'))
    valid_genres = genre_stats[genre_stats['Film_Count'] >= 10].copy()

    if not valid_genres.empty:
        max_c, min_c = valid_genres['Film_Count'].max(), valid_genres['Film_Count'].min()
        max_r, min_r = valid_genres['Avg_Rating'].max(), valid_genres['Avg_Rating'].min()
        range_c = max_c - min_c if max_c > min_c else 1
        range_r = max_r - min_r if max_r > min_r else 1
        valid_genres['Combined_Score'] = ((valid_genres['Film_Count'] - min_c) / range_c) + ((valid_genres['Avg_Rating'] - min_r) / range_r)
        best_genre = valid_genres.sort_values(by='Combined_Score', ascending=False).iloc[0]
        best_genre_name, best_genre_avg, best_genre_count = best_genre.name, best_genre['Avg_Rating'], int(best_genre['Film_Count'])
    else:
        best_genre_name, best_genre_avg, best_genre_count = "N/A", 0.0, 0
        
    return total_films, total_hours, best_dir_name, best_dir_avg, best_genre_name, best_genre_avg, best_genre_count