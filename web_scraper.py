# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import sqlite3
import pandas as pd

def scrape_film_data(uri):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(uri, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        scraped_data = {"Director": "Unknown", "Genre": [], "Country": "Unknown", "Runtime": 0}
        
        # 1. JSON-LD Verisi (Yönetmen, Tür, Ülke için en sağlam kaynak)
        json_ld_script = soup.find("script", type="application/ld+json")
        if json_ld_script:
            # CDATA etiketlerini temizle
            clean_json = json_ld_script.text.split('/* <![CDATA[ */')[-1].split('/* ]]> */')[0].strip()
            data = json.loads(clean_json)
            
            if "director" in data:
                directors = data["director"]
                scraped_data["Director"] = ", ".join([d.get("name", "Unknown") for d in directors]) if isinstance(directors, list) else directors.get("name", "Unknown")
            
            if "genre" in data:
                scraped_data["Genre"] = data["genre"]

        # 2. SÜRE (RUNTIME) ÇEKME - YENİ VE SAĞLAM YÖNTEM
        # Ekran görüntüsündeki "122 mins" yazan yeri arıyoruz
        runtime_tag = soup.find("p", class_="text-link text-footer")
        if runtime_tag:
            runtime_text = runtime_tag.get_text()
            # Sayı dışındaki her şeyi temizle (örn: "122 mins" -> 122)
            digits = "".join(filter(str.isdigit, runtime_text))
            if digits:
                scraped_data["Runtime"] = int(digits)
        
        # Eğer yukarıdaki yöntem bulamazsa alternatif (Twitter Meta)
        if scraped_data["Runtime"] == 0:
            runtime_meta = soup.find("meta", attrs={"name": "twitter:data2"})
            if runtime_meta:
                meta_text = runtime_meta.get("content", "")
                digits = "".join(filter(str.isdigit, meta_text))
                if digits:
                    scraped_data["Runtime"] = int(digits)
            
        return scraped_data
        
    except Exception as e:
        print(f"Hata - {uri}: {e}")
        return None

def enrich_master_database():
    db_path = "letterboxd_master.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM movies", conn)

    # Runtime sütunu yoksa oluştur
    if "Runtime" not in df.columns:
        df["Runtime"] = 0

    print("Eksik süreler tamamlanıyor...")

    for index, row in df.iterrows():
        # EĞER süre 0 ise kazı (Yönetmen dolu olsa bile süreyi tamir eder)
        if row["Runtime"] == 0 or pd.isna(row["Runtime"]):
            uri = row['Letterboxd URI']
            print(f"Süre çekiliyor: {row['Name']}")
            
            data = scrape_film_data(uri)
            
            if data and data["Runtime"] > 0:
                df.at[index, "Runtime"] = data["Runtime"]
                # Eğer yönetmen de eksikse onu da hazır gelmişken doldurur
                if pd.isna(row["Director"]) or row["Director"] == "Unknown":
                    df.at[index, "Director"] = data["Director"]
                
                # Checkpoint: Her başarılı işlemde kaydet
                df.to_sql('movies', conn, if_exists='replace', index=False)
                
                # Valf (6-10 saniye)
                time.sleep(random.uniform(6.0, 10.0))

    conn.close()
    print("Süre tamamlama işlemi bitti!")

if __name__ == "__main__":
    enrich_master_database()