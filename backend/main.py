import os
import threading
import time
import requests as _requests
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import pandas as pd

from data_core import (
    load_data,
    get_latest_movie,
    get_kpis,
    get_genre_distribution,
    get_top_directors,
    get_rating_distribution,
    get_movies_by_year,
    get_goal,
    get_week_activity,
    get_hall_of_fame,
    get_insights,
    get_decades,
    get_language_stats,
    get_community_comparison,
    get_imdb_comparison,
    get_oscar_stats,
)

app = FastAPI(title="Letterboxd Analytics API", version="1.0.0")


def _keep_alive():
    port = os.environ.get("PORT", "8000")
    url = f"http://localhost:{port}/api/health"
    while True:
        time.sleep(60)
        try:
            _requests.get(url, timeout=5)
        except Exception:
            pass

_t = threading.Thread(target=_keep_alive, daemon=True)
_t.start()

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
FRONTEND_URL = os.environ.get("FRONTEND_URL", "")
if FRONTEND_URL:
    ALLOWED_ORIGINS.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────
# /api/kpis
# ──────────────────────────────────────────
@app.get("/api/kpis")
def kpis():
    df = load_data()
    df_rated = df[df["Rating"] > 0]
    return get_kpis(df, df_rated)


# ──────────────────────────────────────────
# /api/latest
# ──────────────────────────────────────────
@app.get("/api/latest")
def latest():
    return get_latest_movie()


# ──────────────────────────────────────────
# /api/movies
# query params: limit, offset, sort_by, order, genre, min_rating
# ──────────────────────────────────────────
@app.get("/api/movies")
def movies(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("watched_date", enum=["watched_date", "rating", "year", "name", "runtime"]),
    order: str = Query("desc", enum=["asc", "desc"]),
    genre: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
):
    df = load_data()

    if genre:
        df = df[df["Genre"].str.contains(genre, case=False, na=False)]
    if min_rating is not None:
        df = df[df["Rating"] >= min_rating]

    col_map = {
        "watched_date": "Watched Date",
        "rating": "Rating",
        "year": "Year",
        "name": "Name",
        "runtime": "Runtime",
    }
    sort_col = col_map[sort_by]
    ascending = order == "asc"

    df = df.sort_values(by=sort_col, ascending=ascending, na_position="last")
    total = len(df)
    df = df.iloc[offset : offset + limit]

    records = []
    for _, row in df.iterrows():
        records.append({
            "name": str(row.get("Name", "")),
            "year": int(row.get("Year", 0) or 0),
            "rating": float(row.get("Rating", 0) or 0),
            "director": str(row.get("Director", "") or ""),
            "genre": str(row.get("Genre", "") or ""),
            "runtime": int(row.get("Runtime", 0) or 0),
            "watched_date": str(row.get("Watched Date", "") or ""),
            "poster_url": str(row.get("Poster_URL", "") or ""),
            "letterboxd_url": str(row.get("Letterboxd URI", "") or ""),
        })

    return {"total": total, "offset": offset, "limit": limit, "data": records}


# ──────────────────────────────────────────
# /api/genres
# ──────────────────────────────────────────
@app.get("/api/genres")
def genres():
    df = load_data()
    df_rated = df[df["Rating"] > 0]
    return get_genre_distribution(df_rated)


# ──────────────────────────────────────────
# /api/directors
# ──────────────────────────────────────────
@app.get("/api/directors")
def directors(min_films: int = Query(3, ge=1)):
    df = load_data()
    df_rated = df[df["Rating"] > 0]
    return get_top_directors(df_rated, min_films=min_films)


# ──────────────────────────────────────────
# /api/ratings
# ──────────────────────────────────────────
@app.get("/api/ratings")
def rating_dist():
    df = load_data()
    df_rated = df[df["Rating"] > 0]
    return get_rating_distribution(df_rated)


# ──────────────────────────────────────────
# /api/years
# ──────────────────────────────────────────
@app.get("/api/years")
def years():
    df = load_data()
    return get_movies_by_year(df)


# ──────────────────────────────────────────
# /api/goal
# ──────────────────────────────────────────
@app.get("/api/goal")
def goal():
    df = load_data()
    return get_goal(df)


# ──────────────────────────────────────────
# /api/week
# ──────────────────────────────────────────
@app.get("/api/week")
def week():
    df = load_data()
    return get_week_activity(df)


# ──────────────────────────────────────────
# /api/hall_of_fame
# ──────────────────────────────────────────
@app.get("/api/hall_of_fame")
def hall_of_fame():
    df = load_data()
    return get_hall_of_fame(df)


# ──────────────────────────────────────────
# /api/insights
# ──────────────────────────────────────────
@app.get("/api/insights")
def insights():
    df = load_data()
    return get_insights(df)


# ──────────────────────────────────────────
# /api/decades
# ──────────────────────────────────────────
@app.get("/api/decades")
def decades():
    df = load_data()
    return get_decades(df)


# ──────────────────────────────────────────
# /api/languages
# ──────────────────────────────────────────
@app.get("/api/languages")
def languages():
    df = load_data()
    return get_language_stats(df)


# ──────────────────────────────────────────
# /api/community
# ──────────────────────────────────────────
@app.get("/api/community")
def community():
    df = load_data()
    return get_community_comparison(df)


# ──────────────────────────────────────────
# /api/imdb
# ──────────────────────────────────────────
@app.get("/api/imdb")
def imdb():
    df = load_data()
    return get_imdb_comparison(df)


# ──────────────────────────────────────────
# /api/oscar
# ──────────────────────────────────────────
@app.get("/api/oscar")
def oscar():
    df = load_data()
    return get_oscar_stats(df)


# ──────────────────────────────────────────
# /api/health
# ──────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok"}
