# Letterboxd Analytics Dashboard

**Canlı Site:** https://letterboxd-analytics-3s9w.vercel.app

Letterboxd izleme geçmişimi otomatik olarak senkronize eden, zenginleştiren ve görselleştiren tam kapsamlı bir veri mühendisliği + full-stack web projesi.

---

## Projeye Genel Bakış

Bu proje üç ana katmandan oluşur:

1. **Veri Katmanı** — SQLite veritabanı + GitHub Actions ile otomatik senkronizasyon
2. **Backend Katmanı** — FastAPI ile yazılmış REST API, Render üzerinde çalışır
3. **Frontend Katmanı** — Next.js ile yazılmış dashboard, Vercel üzerinde çalışır

Her gece saat 03:00 UTC'de GitHub Actions devreye girer, Letterboxd RSS beslemesinden yeni filmleri çeker, metadata'yı TMDB/OMDB'den zenginleştirir, veritabanını günceller ve otomatik deploy tetikler.

---

## Klasör ve Dosya Yapısı

```
letterboxdbot/
│
├── web_scraper.py           ← Ana veri boru hattı (RSS + scraping + enrichment)
├── database_builder.py      ← Tek seferlik veritabanı kurulum scripti
├── add_watched.py           ← manual_watched.csv'yi DB'ye ekleyen yardımcı script
├── manual_watched.csv       ← Diary'ye loglanmamış, manuel eklenen filmler
├── letterboxd_master.db     ← Ana SQLite veritabanı (git'e commit edilir)
│
├── letterboxd_data/         ← Letterboxd'dan indirilen ham CSV dışa aktarımları
│   ├── watched.csv
│   ├── diary.csv
│   ├── ratings.csv
│   └── reviews.csv
│
├── .github/workflows/
│   └── main.yml             ← GitHub Actions: her gece otomatik senkronizasyon
│
├── backend/
│   ├── main.py              ← FastAPI uygulaması, tüm API endpoint'leri
│   ├── data_core.py         ← Veri işleme katmanı, thread-safe 1 saatlik TTL önbellek
│   ├── requirements.txt     ← Python bağımlılıkları
│   ├── render.yaml          ← Render deployment yapılandırması
│   └── Procfile             ← uvicorn başlatma komutu
│
└── frontend/
    ├── app/
    │   └── page.tsx         ← Ana dashboard sayfası (tek sayfa uygulama)
    ├── components/          ← 12 adet React bileşeni
    │   ├── WeekFilmList.tsx
    │   ├── HofMosaic.tsx
    │   ├── CustomCursor.tsx
    │   ├── OpeningSequence.tsx
    │   ├── AnimatedNumber.tsx
    │   ├── AnimatedGoalBar.tsx
    │   ├── DecadesSlider.tsx
    │   ├── PosterTilt.tsx
    │   ├── ScrollReveal.tsx
    │   ├── ScrollProgress.tsx
    │   ├── HeroParallexImage.tsx
    │   └── KeepAlive.tsx
    ├── lib/
    │   └── api.ts           ← API istemcisi, tüm fetch çağrıları
    └── package.json         ← Next.js 16, React 19, TypeScript
```

---

## Veri Akışı — Adım Adım

### 1. İlk Kurulum (Tek Seferlik)

Proje ilk kurulurken Letterboxd'dan manuel olarak CSV dışa aktarımı yapılır ve `letterboxd_data/` klasörüne yerleştirilir. Ardından `database_builder.py` çalıştırılarak bu CSV'ler birleştirilir ve `letterboxd_master.db` SQLite veritabanı oluşturulur.

```bash
python database_builder.py
```

Veritabanı şu sütunları içerir: `Name`, `Rating`, `Watched Date`, `Letterboxd URI`, `Runtime`, `Director`, `Genre`, `Year`, `Poster_URL`, `Community_Rating`, `Community_Votes`, `Backdrop_URL`, `Original_Language`, `TMDB_ID`, `IMDb_ID`, `IMDb_Rating`, `Oscar_Wins`, `Oscar_Noms`, `Enrichment_Tried`

### 2. Günlük Otomatik Senkronizasyon (`web_scraper.py`)

`web_scraper.py` her gece GitHub Actions tarafından çalıştırılır ve şu 4 aşamayı sırayla işler:

**Aşama 0 — `migrate_db()`**
Veritabanına yeni sütunların güvenli bir şekilde eklenmesini sağlar. Sütun zaten mevcutsa atlar, yoksa ekler. Bu sayede schema değişiklikleri mevcut veriyi bozmaz.

**Aşama 1 — `sync_rss_to_db()`**
Letterboxd RSS beslemesini (`/rss/`) feedparser ile okur. Her entry için film adı, izleme tarihi, yıl ve puan çekilir. Aynı film zaten veritabanında varsa atlanır, yoksa eklenir. Bu aşama yalnızca diary'ye loglanmış filmleri yakalar.

**Aşama 2 — `enrich_movie_data()`**
Runtime, Director, Genre veya Poster bilgisi eksik olan filmlerin Letterboxd sayfasını BeautifulSoup ile ziyaret eder. Sayfadaki `<script type="application/ld+json">` etiketinden yapılandırılmış JSON verisi çeker: yönetmen, tür, süre, yıl, poster ve Letterboxd topluluk puanı (`aggregateRating`). Her istek arasında 1 saniye bekleme yapılır.

**Aşama 3 — `enrich_extra_data()`**
Backdrop görseli, orijinal dil, IMDb puanı ve Oscar istatistikleri için daha önce zenginleştirilmemiş (`Enrichment_Tried = 0`) filmleri işler:
- **TMDB API** → Backdrop URL ve orijinal dil
- **OMDB API** → IMDb puanı ve Oscar ödül/adaylık sayısı (Awards alanı regex ile parse edilir)

### 3. Otomatik Deploy (`.github/workflows/main.yml`)

GitHub Actions iş akışı şu adımları izler:

```
Her gece 03:00 UTC
        │
        ▼
  Checkout repo
        │
        ▼
  Python 3.12 kur
        │
        ▼
  pip install bağımlılıklar
        │
        ▼
  python web_scraper.py
  (TMDB_API_KEY ve OMDB_API_KEY secret olarak aktarılır)
        │
        ▼
  git add letterboxd_master.db
  git commit "Auto-sync from RSS: <tarih>"
  git pull --rebase && git push
        │
        ▼
  Değişiklik varsa → Render Deploy Hook tetiklenir (curl POST)
```

Değişiklik yoksa commit atılmaz, Render tetiklenmez.

### 4. Backend API (`backend/main.py` + `backend/data_core.py`)

FastAPI uygulaması Render üzerinde `uvicorn main:app --host 0.0.0.0 --port $PORT` komutuyla çalışır.

`data_core.py` veritabanını okuyup DataFrame'e dönüştürür. Gereksiz disk okumalarını önlemek için **thread-safe double-checked locking** ile 1 saatlik TTL önbellek kullanır. Birden fazla eşzamanlı istek aynı anda önbelleği yenilemeye çalışırsa `threading.Lock()` ile sadece biri çalışır.

Mevcut API endpoint'leri:

| Endpoint | Açıklama |
|---|---|
| `GET /api/kpis` | Toplam film, saat, ortalama puan, en iyi yönetmen/tür |
| `GET /api/latest` | En son izlenen film |
| `GET /api/movies` | Filtreleme/sıralama destekli film listesi |
| `GET /api/genres` | Tür dağılımı ve ortalama puanlar |
| `GET /api/directors` | En çok film izlenen yönetmenler |
| `GET /api/ratings` | Puan dağılımı histogramı |
| `GET /api/years` | Yıla göre izleme sayısı |
| `GET /api/goal` | Yıllık izleme hedefi ve ilerleme |
| `GET /api/week` | Bu haftaki izlemeler ve istatistikler |
| `GET /api/hall_of_fame` | En yüksek puanlı filmler |
| `GET /api/insights` | Marathon, boşa harcanan saat, zirve ay, favori gün |
| `GET /api/decades` | On yıllara göre izleme dağılımı |
| `GET /api/languages` | Orijinal dil dağılımı |
| `GET /api/community` | Letterboxd topluluk puanı karşılaştırması |
| `GET /api/imdb` | IMDb puanı karşılaştırması |
| `GET /api/oscar` | Oscar uyumu ve en çok ödüllü filmler |
| `GET /api/health` | Uptime kontrolü için sağlık endpoint'i |

CORS, Vercel frontend URL'ine ve `localhost:3000`'e izin verecek şekilde yapılandırılmıştır.

### 5. Frontend (`frontend/`)

Next.js 16 + TypeScript ile yazılmış, Vercel üzerinde çalışan tek sayfalık dashboard.

`frontend/lib/api.ts` tüm API çağrılarını merkezi olarak yönetir. Her istek 25 saniyelik `AbortSignal.timeout(25000)` ile korunur. Render'ın ücretsiz tier'ı soğuk başlatma yaptığında sayfa çökmemesi için tüm 11 veri çağrısı `Promise.all` içinde `.catch()` fallback'leriyle sarılmıştır.

`frontend/app/page.tsx` tek bir React Server Component olarak tüm verileri paralel olarak çeker ve şu bölümleri render eder: Hero / Şu An İzlediğim, KPI'lar, Bu Hafta, Yıllık Hedef, Hall of Fame, On Yıllar, Haftalık Insights, Sinema Dili, Community vs You, IMDb vs You, Academy Alignment.

`frontend/components/` içindeki 12 bileşen: animasyonlu sayılar, hedef barı, mosaic arka plan, film listesi, poster tilt efekti, özel cursor, scroll ilerleme çubuğu, intersection observer ile reveal animasyonu, on yıllar slider'ı ve açılış sekansı.

### 6. Manuel Film Ekleme

Letterboxd diary'sine loglanmayan (sadece "izledim" olarak işaretlenen) filmler için `manual_watched.csv` dosyasına `Name, Year, Letterboxd URI` kolonlarıyla satır eklenir, ardından lokalde çalıştırılır:

```bash
python add_watched.py
```

Bu filmler veritabanına eklenir, `web_scraper.py`'nin bir sonraki çalışmasında metadata ile zenginleştirilir.

### 7. Uptime

Render ücretsiz tier 15 dakika hareketsizlikte uyuya geçer. UptimeRobot, `/api/health` endpoint'ini her 5 dakikada bir ping ederek sunucunun sürekli uyanık kalmasını sağlar.

---

## Teknoloji Stack'i

| Katman | Teknoloji |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript |
| Backend | FastAPI, Python 3.12, uvicorn |
| Veritabanı | SQLite (git'e commit edilir) |
| Veri İşleme | Pandas |
| Web Scraping | BeautifulSoup4, feedparser, requests |
| Harici API | TMDB API, OMDB API |
| Otomasyon | GitHub Actions (günlük cron) |
| Frontend Deploy | Vercel |
| Backend Deploy | Render |
| Uptime | UptimeRobot |

---

## Ortam Değişkenleri

| Değişken | Kullanıldığı Yer | Açıklama |
|---|---|---|
| `TMDB_API_KEY` | GitHub Actions secret, web_scraper.py | TMDB film metadata'sı |
| `OMDB_API_KEY` | GitHub Actions secret, web_scraper.py | IMDb puanı ve Oscar verisi |
| `RENDER_DEPLOY_HOOK` | GitHub Actions secret | Render yeniden deploy tetikleyicisi |
| `FRONTEND_URL` | Render ortam değişkeni | CORS için Vercel URL'i |
| `NEXT_PUBLIC_API_URL` | Vercel ortam değişkeni | Frontend'in backend API adresi |

---

*Kişisel veri mühendisliği ve full-stack geliştirme projesi.*

---

**************

---

# Letterboxd Analytics Dashboard

**Live:** https://letterboxd-analytics-3s9w.vercel.app

A full-stack data engineering project that automatically syncs, enriches, and visualizes my Letterboxd watch history.

---

## Project Overview

The project is built on three main layers:

1. **Data Layer** — SQLite database + automated nightly sync via GitHub Actions
2. **Backend Layer** — REST API written with FastAPI, running on Render
3. **Frontend Layer** — Dashboard written with Next.js, running on Vercel

Every night at 03:00 UTC, GitHub Actions kicks in, pulls new films from the Letterboxd RSS feed, enriches metadata from TMDB/OMDB, updates the database, and triggers an automatic deploy.

---

## Folder & File Structure

```
letterboxdbot/
│
├── web_scraper.py           ← Main data pipeline (RSS + scraping + enrichment)
├── database_builder.py      ← One-time database setup script
├── add_watched.py           ← Helper script to insert manual_watched.csv into DB
├── manual_watched.csv       ← Films watched but not diary-logged, added manually
├── letterboxd_master.db     ← Master SQLite database (committed to git)
│
├── letterboxd_data/         ← Raw CSV exports downloaded from Letterboxd
│   ├── watched.csv
│   ├── diary.csv
│   ├── ratings.csv
│   └── reviews.csv
│
├── .github/workflows/
│   └── main.yml             ← GitHub Actions: nightly automated sync
│
├── backend/
│   ├── main.py              ← FastAPI app, all API endpoints
│   ├── data_core.py         ← Data processing layer, thread-safe 1h TTL cache
│   ├── requirements.txt     ← Python dependencies
│   ├── render.yaml          ← Render deployment configuration
│   └── Procfile             ← uvicorn start command
│
└── frontend/
    ├── app/
    │   └── page.tsx         ← Main dashboard page (single-page application)
    ├── components/          ← 12 React components
    │   ├── WeekFilmList.tsx
    │   ├── HofMosaic.tsx
    │   ├── CustomCursor.tsx
    │   ├── OpeningSequence.tsx
    │   ├── AnimatedNumber.tsx
    │   ├── AnimatedGoalBar.tsx
    │   ├── DecadesSlider.tsx
    │   ├── PosterTilt.tsx
    │   ├── ScrollReveal.tsx
    │   ├── ScrollProgress.tsx
    │   ├── HeroParallexImage.tsx
    │   └── KeepAlive.tsx
    ├── lib/
    │   └── api.ts           ← API client, all fetch calls
    └── package.json         ← Next.js 16, React 19, TypeScript
```

---

## Data Flow — Step by Step

### 1. Initial Setup (One-Time)

On first setup, a manual CSV export is downloaded from Letterboxd and placed in `letterboxd_data/`. Then `database_builder.py` is run to merge these CSVs and create the `letterboxd_master.db` SQLite database.

```bash
python database_builder.py
```

The database contains these columns: `Name`, `Rating`, `Watched Date`, `Letterboxd URI`, `Runtime`, `Director`, `Genre`, `Year`, `Poster_URL`, `Community_Rating`, `Community_Votes`, `Backdrop_URL`, `Original_Language`, `TMDB_ID`, `IMDb_ID`, `IMDb_Rating`, `Oscar_Wins`, `Oscar_Noms`, `Enrichment_Tried`

### 2. Nightly Automated Sync (`web_scraper.py`)

`web_scraper.py` is run every night by GitHub Actions and processes these 4 stages in order:

**Stage 0 — `migrate_db()`**
Safely adds new columns to the database. Skips if a column already exists, adds it if not. This ensures schema changes never corrupt existing data.

**Stage 1 — `sync_rss_to_db()`**
Reads the Letterboxd RSS feed (`/rss/`) with feedparser. For each entry, it extracts the film name, watch date, year, and rating. Films already in the database are skipped; new ones are inserted. This stage only captures diary-logged films.

**Stage 2 — `enrich_movie_data()`**
Visits the Letterboxd page of any film missing Runtime, Director, Genre, or Poster data using BeautifulSoup. Extracts structured JSON data from the `<script type="application/ld+json">` tag: director, genre, runtime, year, poster, and Letterboxd community rating (`aggregateRating`). A 1-second delay is applied between each request.

**Stage 3 — `enrich_extra_data()`**
Processes films not yet enriched (`Enrichment_Tried = 0`) for backdrop image, original language, IMDb rating, and Oscar statistics:
- **TMDB API** → Backdrop URL and original language
- **OMDB API** → IMDb rating and Oscar win/nomination counts (Awards field is parsed with regex)

### 3. Automated Deploy (`.github/workflows/main.yml`)

The GitHub Actions workflow follows these steps:

```
Every night at 03:00 UTC
        │
        ▼
  Checkout repo
        │
        ▼
  Set up Python 3.12
        │
        ▼
  pip install dependencies
        │
        ▼
  python web_scraper.py
  (TMDB_API_KEY and OMDB_API_KEY passed as secrets)
        │
        ▼
  git add letterboxd_master.db
  git commit "Auto-sync from RSS: <date>"
  git pull --rebase && git push
        │
        ▼
  If changes exist → Render Deploy Hook triggered (curl POST)
```

If there are no changes, no commit is made and Render is not triggered.

### 4. Backend API (`backend/main.py` + `backend/data_core.py`)

The FastAPI application runs on Render via `uvicorn main:app --host 0.0.0.0 --port $PORT`.

`data_core.py` reads the database and converts it to a DataFrame. To avoid unnecessary disk reads, it uses a **thread-safe double-checked locking** pattern with a 1-hour TTL cache. If multiple concurrent requests try to refresh the cache simultaneously, `threading.Lock()` ensures only one runs.

Available API endpoints:

| Endpoint | Description |
|---|---|
| `GET /api/kpis` | Total films, hours, average rating, best director/genre |
| `GET /api/latest` | Most recently watched film |
| `GET /api/movies` | Film list with filtering and sorting support |
| `GET /api/genres` | Genre distribution and average ratings |
| `GET /api/directors` | Most-watched directors |
| `GET /api/ratings` | Rating distribution histogram |
| `GET /api/years` | Watch count by year |
| `GET /api/goal` | Annual watch goal and progress |
| `GET /api/week` | This week's watches and stats |
| `GET /api/hall_of_fame` | Highest-rated films |
| `GET /api/insights` | Marathon, wasted hours, peak month, favorite day |
| `GET /api/decades` | Watch distribution by decade |
| `GET /api/languages` | Original language distribution |
| `GET /api/community` | Letterboxd community rating comparison |
| `GET /api/imdb` | IMDb rating comparison |
| `GET /api/oscar` | Oscar alignment and most-decorated films |
| `GET /api/health` | Health check endpoint for uptime monitoring |

CORS is configured to allow the Vercel frontend URL and `localhost:3000`.

### 5. Frontend (`frontend/`)

A single-page dashboard written in Next.js 16 + TypeScript, running on Vercel.

`frontend/lib/api.ts` centrally manages all API calls. Each request is protected with a 25-second `AbortSignal.timeout(25000)`. To prevent the page from crashing when Render does a cold start, all 11 data calls are wrapped inside `Promise.all` with `.catch()` fallbacks.

`frontend/app/page.tsx` is a single React Server Component that fetches all data in parallel and renders the following sections: Hero / Currently Watching, KPIs, This Week, Annual Goal, Hall of Fame, Decades, Weekly Insights, Cinema Language, Community vs You, IMDb vs You, Academy Alignment.

The 12 components in `frontend/components/`: animated numbers, goal bar, mosaic background, film list, poster tilt effect, custom cursor, scroll progress bar, intersection observer reveal animations, decades slider, and opening sequence.

### 6. Manual Film Entry

For films not diary-logged on Letterboxd (only marked as "watched"), a row is added to `manual_watched.csv` with `Name, Year, Letterboxd URI` columns, then run locally:

```bash
python add_watched.py
```

These films are inserted into the database and enriched with metadata on the next `web_scraper.py` run.

### 7. Uptime

Render's free tier sleeps after 15 minutes of inactivity. UptimeRobot pings the `/api/health` endpoint every 5 minutes to keep the server continuously awake.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript |
| Backend | FastAPI, Python 3.12, uvicorn |
| Database | SQLite (committed to git) |
| Data Processing | Pandas |
| Web Scraping | BeautifulSoup4, feedparser, requests |
| External APIs | TMDB API, OMDB API |
| Automation | GitHub Actions (daily cron) |
| Frontend Deploy | Vercel |
| Backend Deploy | Render |
| Uptime | UptimeRobot |

---

## Environment Variables

| Variable | Used In | Description |
|---|---|---|
| `TMDB_API_KEY` | GitHub Actions secret, web_scraper.py | TMDB film metadata |
| `OMDB_API_KEY` | GitHub Actions secret, web_scraper.py | IMDb rating and Oscar data |
| `RENDER_DEPLOY_HOOK` | GitHub Actions secret | Render redeploy trigger |
| `FRONTEND_URL` | Render environment variable | Vercel URL for CORS |
| `NEXT_PUBLIC_API_URL` | Vercel environment variable | Frontend's backend API address |

---

*Personal data engineering and full-stack development project.*
