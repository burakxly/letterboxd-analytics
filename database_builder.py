# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
import os

def create_master_database():
    # 1. Dosya Yollarının Dinamik Tanımlanması [cite: 32, 33, 34, 35]
    data_dir = "letterboxd_data"
    watched_path = os.path.join(data_dir, "watched.csv")
    ratings_path = os.path.join(data_dir, "ratings.csv")
    diary_path = os.path.join(data_dir, "diary.csv")
    reviews_path = os.path.join(data_dir, "reviews.csv")

    # 2. Verilerin Yüklenmesi (Ana İskelet: watched.csv) [cite: 39]
    # Watched dosyasını tam olarak alıyoruz.
    df_watched = pd.read_csv(watched_path)
    # Çakışmaları önlemek için sütun ismini değiştiriyoruz [cite: 40]
    df_watched.rename(columns={'Date': 'Watched_Date_Log'}, inplace=True)

    # 3. Diğer Verilerin Çekilmesi (Sütun Filtreleme ile Çakışma Önleme) [cite: 37, 41, 46, 51]
    # Sadece bize lazım olan sütunları alıyoruz ki 'Name' ve 'Year' gibi isimler çakışmasın.
    try:
        df_ratings = pd.read_csv(ratings_path, usecols=['Letterboxd URI', 'Rating'])
    except FileNotFoundError:
        df_ratings = pd.DataFrame(columns=['Letterboxd URI', 'Rating'])

    try:
        df_diary = pd.read_csv(diary_path, usecols=['Letterboxd URI', 'Watched Date', 'Rewatch', 'Tags'])
    except FileNotFoundError:
        df_diary = pd.DataFrame(columns=['Letterboxd URI', 'Watched Date', 'Rewatch', 'Tags'])

    try:
        df_reviews = pd.read_csv(reviews_path, usecols=['Letterboxd URI', 'Review'])
    except FileNotFoundError:
        df_reviews = pd.DataFrame(columns=['Letterboxd URI', 'Review'])

    # 4. Left Join ile Verilerin Birleştirilmesi [cite: 18, 21, 57]
    # Ortak anahtarımız en güvenli tanımlayıcı olan 'Letterboxd URI' [cite: 20]
    master_df = pd.merge(df_watched, df_ratings, on='Letterboxd URI', how='left') 
    master_df = pd.merge(master_df, df_diary, on='Letterboxd URI', how='left') 
    master_df = pd.merge(master_df, df_reviews, on='Letterboxd URI', how='left') 

    # 5. Veri Temizliği (Data Cleaning)
    # Sayısal sütunlar (Rating, Year) için boşlukları 0.0 ile dolduruyoruz 
  
    master_df['Rating'] = pd.to_numeric(master_df['Rating'], errors='coerce').fillna(0.0)
    
    # Geri kalan tüm metinsel boşlukları güvenli bir şekilde dolduruyoruz [cite: 65, 66]
    master_df = master_df.fillna("")

    # 6. SQLite Veritabanına Yazma [cite: 26, 68, 70]
    db_path = "letterboxd_master.db"
    conn = sqlite3.connect(db_path) 
    
    # 'movies' adında bir tablo oluşturuyoruz [cite: 71]
    master_df.to_sql('movies', conn, if_exists='replace', index=False) 
    conn.close() 

    print(f"Master Database başarıyla oluşturuldu! Toplam İşlenen Film Sayısı: {len(master_df)}") 
    return master_df

if __name__ == "__main__":
    create_master_database()