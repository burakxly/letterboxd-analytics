# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
import os

def create_master_database():
    data_dir = "letterboxd_data"
    watched_path = os.path.join(data_dir, "watched.csv")
    ratings_path = os.path.join(data_dir, "ratings.csv")
    diary_path = os.path.join(data_dir, "diary.csv")
    reviews_path = os.path.join(data_dir, "reviews.csv")

    # 1. Ana İskelet (Watched)
    df_watched = pd.read_csv(watched_path)
    df_watched.rename(columns={'Date': 'Watched_Date_Log'}, inplace=True)

    # 2. Puanlar (Ratings)
    try:
        df_ratings = pd.read_csv(ratings_path, usecols=['Name', 'Rating'])
    except FileNotFoundError:
        df_ratings = pd.DataFrame(columns=['Name', 'Rating'])

    # 3. Günlük (Diary)
    try:
        df_diary = pd.read_csv(diary_path, usecols=['Name', 'Watched Date', 'Rewatch', 'Tags'])
        df_diary = df_diary.sort_values('Watched Date').drop_duplicates('Name', keep='last')
    except FileNotFoundError:
        df_diary = pd.DataFrame(columns=['Name', 'Watched Date', 'Rewatch', 'Tags'])

    # 4. İncelemeler (Reviews)
    try:
        df_reviews = pd.read_csv(reviews_path, usecols=['Name', 'Review'])
    except FileNotFoundError:
        df_reviews = pd.DataFrame(columns=['Name', 'Review'])

    # 5. BİRLEŞTİRME 
    master_df = pd.merge(df_watched, df_ratings, on='Name', how='left') 
    master_df = pd.merge(master_df, df_diary, on='Name', how='left') 
    master_df = pd.merge(master_df, df_reviews, on='Name', how='left') 

    # --- BÜYÜK KURTARMA OPERASYONU (YENİ EKLENEN KISIM) ---
    db_path = "letterboxd_master.db"
    if os.path.exists(db_path):
        try:
            old_conn = sqlite3.connect(db_path)
            # Mevcut veritabanındaki tüm veriyi çek
            old_df = pd.read_sql("SELECT * FROM movies", old_conn)
            old_conn.close()
            
            # Eğer eski veritabanında Runtime, Director gibi sütunlar varsa onları tespit et
            cols_to_rescue = ['Name']
            for col in ['Runtime', 'Director', 'Genre', 'Country']:
                if col in old_df.columns:
                    cols_to_rescue.append(col)
            
            # Eğer Name dışında kurtaracak bir şey bulduysa (yani scraper daha önce çalışmışsa)
            if len(cols_to_rescue) > 1:
                old_df_rescued = old_df[cols_to_rescue].drop_duplicates('Name')
                # Eski kazınmış verileri, yeni CSV verileriyle birleştir
                master_df = pd.merge(master_df, old_df_rescued, on='Name', how='left')
                print(f"Eski veritabanından {len(cols_to_rescue)-1} adet özel sütun başarıyla kurtarıldı!")
        except Exception as e:
            print(f"Uyarı - Eski veriler kurtarılamadı (İlk kurulum olabilir): {e}")
    # -------------------------------------------------------

    # 6. Veri Temizliği
    master_df['Rating'] = pd.to_numeric(master_df['Rating'], errors='coerce').fillna(0.0)
    master_df = master_df.fillna("")

    # 7. Veritabanına Yazma
    conn = sqlite3.connect(db_path) 
    master_df.to_sql('movies', conn, if_exists='replace', index=False) 
    conn.close() 

    print(f"Master Database başarıyla oluşturuldu! Toplam İşlenen Film Sayısı: {len(master_df)}") 
    return master_df

if __name__ == "__main__":
    create_master_database()