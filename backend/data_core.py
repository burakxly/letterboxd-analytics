import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "letterboxd_master.db")


def fetch_poster_url(movie_page_url: str) -> str:
    if not movie_page_url:
        return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(movie_page_url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")  # lxml removed for Railway compat

        script_tag = soup.find("script", type="application/ld+json")
        if script_tag:
            raw_json = script_tag.text.replace("/* <![CDATA[ */", "").replace("/* ]]> */", "").strip()
            data = json.loads(raw_json)
            if "image" in data:
                return data["image"]

        og_image = soup.find("meta", property="og:image")
        if og_image:
            return og_image.get("content")
    except Exception:
        pass
    return "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"


def load_data() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT rowid, * FROM movies", conn)
    conn.close()

    if "Runtime" not in df.columns:
        df["Runtime"] = 0
    if "Year" not in df.columns:
        df["Year"] = 0
    if "Rating" not in df.columns:
        df["Rating"] = 0
    if "Director" not in df.columns:
        df["Director"] = "Unknown"
    if "Genre" not in df.columns:
        df["Genre"] = "Unknown"

    if "Watched_Date_Log" in df.columns:
        df["Watched_Date_Log"] = pd.to_datetime(df["Watched_Date_Log"], errors="coerce")
    if "Watched Date" in df.columns:
        df["Watched Date"] = pd.to_datetime(df["Watched Date"], errors="coerce")

    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0)
    df["Runtime"] = pd.to_numeric(df["Runtime"], errors="coerce").fillna(0)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(0)

    return df


def get_latest_movie() -> dict:
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT Name, Rating, Director, Runtime, Genre, Year, "Letterboxd URI", Poster_URL
        FROM movies
        WHERE "Watched Date" IS NOT NULL AND "Watched Date" != ''
        ORDER BY date("Watched Date") DESC, rowid DESC
        LIMIT 1
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return {
            "name": "VERI YOK",
            "director": "Unknown",
            "runtime": 0,
            "rating": 0.0,
            "genre": "Unknown",
            "year": 0,
            "poster_url": "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg",
            "letterboxd_url": "#",
        }

    row = df.iloc[0]
    return {
        "name": str(row["Name"]).upper(),
        "director": str(row["Director"]).split(",")[0].strip(),
        "runtime": int(row["Runtime"] or 0),
        "rating": float(row["Rating"] or 0.0),
        "genre": str(row["Genre"] or "Unknown"),
        "year": int(row["Year"] or 0),
        "poster_url": str(row["Poster_URL"]) or "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg",
        "letterboxd_url": str(row["Letterboxd URI"]),
    }


def get_kpis(df_all: pd.DataFrame, df_rated: pd.DataFrame) -> dict:
    total_films = len(df_all.drop_duplicates(subset=["Letterboxd URI"]))
    total_hours = int(df_all["Runtime"].sum()) / 60

    df_dir = df_rated.assign(Director=df_rated["Director"].str.split(", ")).explode("Director")
    df_dir = df_dir[~df_dir["Director"].isin(["Unknown", "", None])]
    dir_stats = df_dir.groupby("Director").agg(Film_Count=("Name", "count"), Avg_Rating=("Rating", "mean"))
    valid_dirs = dir_stats[dir_stats["Film_Count"] >= 5]

    if not valid_dirs.empty:
        best_dir_row = valid_dirs.sort_values(by="Avg_Rating", ascending=False).iloc[0]
        best_dir_name = best_dir_row.name
        best_dir_avg = round(float(best_dir_row["Avg_Rating"]), 2)
    else:
        best_dir_name, best_dir_avg = "N/A", 0.0

    df_genre = df_rated.assign(Genre=df_rated["Genre"].str.split(", ")).explode("Genre")
    df_genre = df_genre[~df_genre["Genre"].isin(["Unknown", "", None])]
    genre_stats = df_genre.groupby("Genre").agg(Film_Count=("Name", "count"), Avg_Rating=("Rating", "mean"))
    valid_genres = genre_stats[genre_stats["Film_Count"] >= 10].copy()

    if not valid_genres.empty:
        max_c, min_c = valid_genres["Film_Count"].max(), valid_genres["Film_Count"].min()
        max_r, min_r = valid_genres["Avg_Rating"].max(), valid_genres["Avg_Rating"].min()
        range_c = max_c - min_c if max_c > min_c else 1
        range_r = max_r - min_r if max_r > min_r else 1
        valid_genres["Combined_Score"] = (
            (valid_genres["Film_Count"] - min_c) / range_c
        ) + (
            (valid_genres["Avg_Rating"] - min_r) / range_r
        )
        best_genre = valid_genres.sort_values(by="Combined_Score", ascending=False).iloc[0]
        best_genre_name = best_genre.name
        best_genre_avg = round(float(best_genre["Avg_Rating"]), 2)
        best_genre_count = int(best_genre["Film_Count"])
    else:
        best_genre_name, best_genre_avg, best_genre_count = "N/A", 0.0, 0

    avg_rating = round(float(df_rated["Rating"].mean()), 2) if not df_rated.empty else 0.0

    return {
        "total_films": total_films,
        "total_hours": round(total_hours, 1),
        "avg_rating": avg_rating,
        "best_director": best_dir_name,
        "best_director_avg": best_dir_avg,
        "best_genre": best_genre_name,
        "best_genre_avg": best_genre_avg,
        "best_genre_count": best_genre_count,
    }


def get_genre_distribution(df_rated: pd.DataFrame) -> list[dict]:
    df_genre = df_rated.assign(Genre=df_rated["Genre"].str.split(", ")).explode("Genre")
    df_genre = df_genre[~df_genre["Genre"].isin(["Unknown", "", None])]
    genre_counts = (
        df_genre.groupby("Genre")
        .agg(count=("Name", "count"), avg_rating=("Rating", "mean"))
        .reset_index()
        .sort_values("count", ascending=False)
        .head(15)
    )
    return [
        {"genre": row["Genre"], "count": int(row["count"]), "avg_rating": round(float(row["avg_rating"]), 2)}
        for _, row in genre_counts.iterrows()
    ]


def get_top_directors(df_rated: pd.DataFrame, min_films: int = 3) -> list[dict]:
    df_dir = df_rated.assign(Director=df_rated["Director"].str.split(", ")).explode("Director")
    df_dir = df_dir[~df_dir["Director"].isin(["Unknown", "", None])]
    dir_stats = (
        df_dir.groupby("Director")
        .agg(film_count=("Name", "count"), avg_rating=("Rating", "mean"))
        .reset_index()
    )
    dir_stats = dir_stats[dir_stats["film_count"] >= min_films].sort_values("film_count", ascending=False).head(15)
    return [
        {"director": row["Director"], "film_count": int(row["film_count"]), "avg_rating": round(float(row["avg_rating"]), 2)}
        for _, row in dir_stats.iterrows()
    ]


def get_rating_distribution(df_rated: pd.DataFrame) -> list[dict]:
    counts = df_rated["Rating"].value_counts().sort_index()
    return [{"rating": float(r), "count": int(c)} for r, c in counts.items() if r > 0]


def get_movies_by_year(df_all: pd.DataFrame) -> list[dict]:
    df = df_all[df_all["Year"] > 1900].copy()
    year_counts = df.groupby("Year").size().reset_index(name="count").sort_values("Year")
    return [{"year": int(row["Year"]), "count": int(row["count"])} for _, row in year_counts.iterrows()]


def get_goal(df: pd.DataFrame) -> dict:
    goal = 200
    current_year = pd.Timestamp.now().year
    # "Watched Date" = gerçek izleme tarihi, bunu kullan
    df_year = df[df["Watched Date"].dt.year == current_year]
    count = len(df_year)
    progress_pct = min(100, round((count / goal) * 100, 1))
    return {"year": current_year, "goal": goal, "count": count, "progress_pct": progress_pct}


def get_week_activity(df: pd.DataFrame) -> dict:
    # "Watched Date" = gerçek izleme tarihi
    df_dates = df.dropna(subset=["Watched Date"]).copy()

    if df_dates.empty:
        return {"count": 0, "avg_rating": 0.0, "runtime_mins": 0, "start_date": "", "end_date": "", "movies": []}

    max_date = df_dates["Watched Date"].max()
    start_of_week = max_date - pd.Timedelta(days=max_date.weekday())
    end_of_week = start_of_week + pd.Timedelta(days=6)
    df_week = df_dates[
        (df_dates["Watched Date"] >= start_of_week) & (df_dates["Watched Date"] <= end_of_week)
    ]

    week_count = len(df_week)
    week_avg = round(float(df_week[df_week["Rating"] > 0]["Rating"].mean()), 2) if week_count > 0 else 0.0
    week_runtime = int(df_week["Runtime"].sum())

    movies = []
    for _, row in df_week.sort_values(["Watched Date", "rowid"], ascending=[False, False]).iterrows():
        movies.append({
            "name": str(row.get("Name", "")),
            "year": int(row.get("Year", 0) or 0),
            "rating": float(row.get("Rating", 0) or 0),
            "runtime": int(row.get("Runtime", 0) or 0),
            "letterboxd_url": str(row.get("Letterboxd URI", "") or ""),
            "poster_url": str(row.get("Poster_URL", "") or ""),
            "community_rating": float(row.get("Community_Rating", 0) or 0),
        })

    return {
        "count": week_count,
        "avg_rating": week_avg if not pd.isna(week_avg) else 0.0,
        "runtime_mins": week_runtime,
        "start_date": start_of_week.strftime("%b %d"),
        "end_date": end_of_week.strftime("%b %d"),
        "movies": movies,
    }


def get_hall_of_fame(df: pd.DataFrame) -> list[dict]:
    # Gerçek izleme tarihine göre sırala
    df_dates = df.dropna(subset=["Watched Date"]).copy()
    df_5star = df_dates[(df_dates["Rating"] == 5.0) & (df_dates["Runtime"] >= 35)].sort_values("Watched Date", ascending=False)

    result = []
    for _, row in df_5star.iterrows():
        result.append({
            "name": str(row.get("Name", "")),
            "year": int(row.get("Year", 0) or 0),
            "director": str(row.get("Director", "") or "").split(",")[0].strip(),
            "runtime": int(row.get("Runtime", 0) or 0),
            "poster_url": str(row.get("Poster_URL", "") or "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"),
            "letterboxd_url": str(row.get("Letterboxd URI", "") or ""),
            "watched_date": str(row.get("Watched Date", "") or ""),
        })
    return result


def get_insights(df: pd.DataFrame) -> dict:
    # "Watched Date" = gerçek izleme tarihi, tüm hesaplamalarda bunu kullan
    df_dates = df.dropna(subset=["Watched Date"]).copy()
    df_dates["DateOnly"] = df_dates["Watched Date"].dt.date

    # --- Marathon ---
    marathon_stats = (
        df_dates.groupby("DateOnly")
        .agg(film_count=("Name", "count"), total_runtime=("Runtime", "sum"))
        .reset_index()
    )
    valid_marathons = marathon_stats[marathon_stats["film_count"] <= 8]
    marathon = None
    if not valid_marathons.empty:
        best = valid_marathons.sort_values(by=["film_count", "total_runtime"], ascending=[False, False]).iloc[0]
        marathon_films_df = df_dates[df_dates["DateOnly"] == best["DateOnly"]].sort_values("Watched Date")
        bg_poster = ""
        for _, rf in marathon_films_df.iterrows():
            p = str(rf.get("Poster_URL", ""))
            if p and p not in ("nan", ""):
                bg_poster = p
                break
        marathon = {
            "date": str(best["DateOnly"]),
            "film_count": int(best["film_count"]),
            "total_runtime_mins": int(best["total_runtime"]),
            "bg_poster": bg_poster,
            "films": [
                {
                    "name": str(r.get("Name", "")),
                    "runtime": int(r.get("Runtime", 0) or 0),
                    "letterboxd_url": str(r.get("Letterboxd URI", "") or ""),
                }
                for _, r in marathon_films_df.iterrows()
            ],
        }

    # --- Time Wasted ---
    wasted_df = df[(df["Rating"] > 0) & (df["Rating"] < 2.0)].copy()
    wasted_runtime = int(wasted_df["Runtime"].sum())
    wasted_films = wasted_df.sort_values("Rating").head(5)
    time_wasted = {
        "total_mins": wasted_runtime,
        "films": [
            {
                "name": str(r.get("Name", "")),
                "rating": float(r.get("Rating", 0) or 0),
                "letterboxd_url": str(r.get("Letterboxd URI", "") or ""),
            }
            for _, r in wasted_films.iterrows()
        ],
    }

    # --- Peak Month (gerçek izleme tarihine göre) ---
    df_rated_months = df[(df["Rating"] > 0) & df["Watched Date"].notna()].copy()
    df_rated_months["YearMonth"] = df_rated_months["Watched Date"].dt.to_period("M")
    month_stats = df_rated_months.groupby("YearMonth").agg(film_count=("Name", "count"), avg_rating=("Rating", "mean")).reset_index()
    valid_months = month_stats[month_stats["film_count"] >= 10]
    peak_month = None
    if not valid_months.empty:
        best_month = valid_months.loc[valid_months["avg_rating"].idxmax()]
        peak_films_df = df_rated_months[df_rated_months["YearMonth"] == best_month["YearMonth"]].sort_values("Rating", ascending=False).head(5)
        peak_bg = str(peak_films_df.iloc[0].get("Poster_URL", "")) if not peak_films_df.empty else ""
        peak_bg = peak_bg if peak_bg and peak_bg != "nan" else ""
        peak_month = {
            "month": best_month["YearMonth"].strftime("%B"),
            "year": best_month["YearMonth"].strftime("%Y"),
            "avg_rating": round(float(best_month["avg_rating"]), 2),
            "film_count": int(best_month["film_count"]),
            "bg_poster": peak_bg,
            "top_films": [
                {
                    "name": str(r.get("Name", "")),
                    "letterboxd_url": str(r.get("Letterboxd URI", "") or ""),
                }
                for _, r in peak_films_df.iterrows()
            ],
        }

    # --- Best Decade ---
    df_generous = df[(df["Year"] > 1800) & (df["Rating"] > 0)].copy()
    df_generous["Decade"] = (df_generous["Year"] // 10) * 10
    decade_stats = df_generous.groupby("Decade").agg(avg_rating=("Rating", "mean"), film_count=("Name", "count")).reset_index()
    valid_decades = decade_stats[decade_stats["film_count"] >= 10]
    best_decade = None
    if not valid_decades.empty:
        best_dec_row = valid_decades.loc[valid_decades["avg_rating"].idxmax()]
        decade_val = int(best_dec_row["Decade"])
        decade_films_df = (
            df_generous[df_generous["Decade"] == decade_val]
            .sort_values("Rating", ascending=False)
            .drop_duplicates("Name")
            .head(5)
        )
        era_bg = str(decade_films_df.iloc[0].get("Poster_URL", "")) if not decade_films_df.empty else ""
        era_bg = era_bg if era_bg and era_bg != "nan" else ""
        best_decade = {
            "decade": decade_val,
            "avg_rating": round(float(best_dec_row["avg_rating"]), 2),
            "film_count": int(best_dec_row["film_count"]),
            "bg_poster": era_bg,
            "top_films": [
                {
                    "name": str(r.get("Name", "")),
                    "year": int(r.get("Year", 0) or 0),
                    "letterboxd_url": str(r.get("Letterboxd URI", "") or ""),
                }
                for _, r in decade_films_df.iterrows()
            ],
        }

    # --- Favorite Day (gerçek izleme tarihine göre, son 3 ay) ---
    favorite_day = None
    if not df_dates.empty:
        max_date = df_dates["Watched Date"].max()
        three_months_ago = max_date - pd.DateOffset(months=3)
        recent_df = df_dates[df_dates["Watched Date"] >= three_months_ago]
        if not recent_df.empty:
            favorite_day = recent_df["Watched Date"].dt.day_name().value_counts().idxmax()

    return {
        "marathon": marathon,
        "time_wasted": time_wasted,
        "peak_month": peak_month,
        "best_decade": best_decade,
        "favorite_day": favorite_day,
    }


def get_decades(df: pd.DataFrame) -> list[dict]:
    df_rated = df[df["Rating"] > 0].copy()
    df_decades = df_rated[(df_rated["Year"] >= 1900) & (df_rated["Runtime"] >= 35)].copy()
    df_decades["Decade"] = (df_decades["Year"] // 10 * 10).astype(int)

    # Her on yıl için: Rating DESC, eşit puanda en son izlenen (Watched Date DESC)
    sort_cols = ["Rating", "Watched Date"] if "Watched Date" in df_decades.columns else ["Rating"]
    ascending = [False, False][:len(sort_cols)]

    top_per_decade = (
        df_decades
        .sort_values(sort_cols, ascending=ascending)
        .groupby("Decade")
        .first()
        .reset_index()
        .sort_values("Decade", ascending=False)
    )

    result = []
    for _, row in top_per_decade.iterrows():
        result.append({
            "decade": int(row["Decade"]),
            "name": str(row.get("Name", "")),
            "year": int(row.get("Year", 0) or 0),
            "rating": float(row.get("Rating", 0) or 0),
            "director": str(row.get("Director", "") or "").split(",")[0].strip(),
            "poster_url": str(row.get("Poster_URL", "") or "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"),
            "backdrop_url": str(row.get("Backdrop_URL", "") or ""),
            "letterboxd_url": str(row.get("Letterboxd URI", "") or ""),
        })
    return result


# ─── Language → human-readable label ──────────────────────
_LANG_LABELS = {
    "en": "English", "fr": "French", "de": "German", "it": "Italian",
    "es": "Spanish", "ja": "Japanese", "ko": "Korean", "zh": "Chinese",
    "pt": "Portuguese", "ru": "Russian", "tr": "Turkish", "sv": "Swedish",
    "da": "Danish", "nl": "Dutch", "pl": "Polish", "fa": "Persian",
    "ar": "Arabic", "hi": "Hindi", "no": "Norwegian", "fi": "Finnish",
    "cs": "Czech", "hu": "Hungarian", "ro": "Romanian", "he": "Hebrew",
    "th": "Thai", "id": "Indonesian", "uk": "Ukrainian", "el": "Greek",
}


def get_language_stats(df: pd.DataFrame) -> list[dict]:
    if "Original_Language" not in df.columns:
        return []
    df_lang = df[df["Original_Language"].notna() & (df["Original_Language"] != "")].copy()
    if df_lang.empty:
        return []
    lang_stats = (
        df_lang.groupby("Original_Language")
        .agg(count=("Name", "count"), avg_rating=("Rating", "mean"))
        .reset_index()
        .sort_values("count", ascending=False)
        .head(12)
    )
    return [
        {
            "language": str(row["Original_Language"]),
            "label": _LANG_LABELS.get(str(row["Original_Language"]), str(row["Original_Language"]).upper()),
            "count": int(row["count"]),
            "avg_rating": round(float(row["avg_rating"]), 2),
        }
        for _, row in lang_stats.iterrows()
    ]


def get_community_comparison(df: pd.DataFrame) -> dict:
    if "Community_Rating" not in df.columns:
        return {"avg_diff": 0, "total_compared": 0, "underrated": [], "overrated": []}

    df_both = df[
        (df["Rating"] > 0) &
        (df["Community_Rating"] > 0)
    ].copy()

    if df_both.empty:
        return {"avg_diff": 0, "total_compared": 0, "underrated": [], "overrated": []}

    # Convert community rating from /5 scale (Letterboxd) to match user rating /5
    df_both["diff"] = df_both["Rating"] - df_both["Community_Rating"]
    avg_diff = round(float(df_both["diff"].mean()), 3)

    # Films you loved more than community (underrated by community)
    underrated = (
        df_both.sort_values("diff", ascending=False)
        .head(5)
    )
    # Films you liked less than community (overrated by community)
    overrated = (
        df_both.sort_values("diff", ascending=True)
        .head(5)
    )

    def film_row(row):
        return {
            "name": str(row.get("Name", "")),
            "year": int(row.get("Year", 0) or 0),
            "user_rating": float(row.get("Rating", 0) or 0),
            "community_rating": float(row.get("Community_Rating", 0) or 0),
            "diff": round(float(row.get("diff", 0)), 2),
            "letterboxd_url": str(row.get("Letterboxd URI", "") or ""),
            "poster_url": str(row.get("Poster_URL", "") or ""),
        }

    return {
        "avg_diff": avg_diff,
        "total_compared": len(df_both),
        "underrated": [film_row(r) for _, r in underrated.iterrows()],
        "overrated": [film_row(r) for _, r in overrated.iterrows()],
    }


def get_imdb_comparison(df: pd.DataFrame) -> dict:
    if "IMDb_Rating" not in df.columns:
        return {"avg_diff": 0, "total_compared": 0, "agreements": [], "disagreements": []}

    df_both = df[
        (df["Rating"] > 0) &
        (df["IMDb_Rating"] > 0)
    ].copy()

    if df_both.empty:
        return {"avg_diff": 0, "total_compared": 0, "agreements": [], "disagreements": []}

    # Normalize IMDb /10 → /5 scale for comparison
    df_both["imdb_norm"] = df_both["IMDb_Rating"] / 2.0
    df_both["diff"] = df_both["Rating"] - df_both["imdb_norm"]

    avg_diff = round(float(df_both["diff"].mean()), 3)

    # Biggest agreements (diff closest to 0)
    df_both["abs_diff"] = df_both["diff"].abs()
    agreements = df_both.sort_values("abs_diff").head(5)
    # Biggest disagreements
    disagreements = df_both.sort_values("abs_diff", ascending=False).head(5)

    def film_row(row):
        return {
            "name": str(row.get("Name", "")),
            "year": int(row.get("Year", 0) or 0),
            "user_rating": float(row.get("Rating", 0) or 0),
            "imdb_rating": float(row.get("IMDb_Rating", 0) or 0),
            "diff": round(float(row.get("diff", 0)), 2),
            "letterboxd_url": str(row.get("Letterboxd URI", "") or ""),
            "poster_url": str(row.get("Poster_URL", "") or ""),
        }

    return {
        "avg_diff": avg_diff,
        "total_compared": len(df_both),
        "agreements": [film_row(r) for _, r in agreements.iterrows()],
        "disagreements": [film_row(r) for _, r in disagreements.iterrows()],
    }


def get_oscar_stats(df: pd.DataFrame) -> dict:
    if "Oscar_Wins" not in df.columns:
        return {"total_oscar_films": 0, "total_wins": 0, "total_noms": 0, "top_winners": []}

    df_oscar = df[
        ((df["Oscar_Wins"] > 0) | (df["Oscar_Noms"] > 0))
    ].copy()

    if df_oscar.empty:
        return {"total_oscar_films": 0, "total_wins": 0, "total_noms": 0, "top_winners": []}

    total_wins = int(df_oscar["Oscar_Wins"].sum())
    total_noms = int(df_oscar["Oscar_Noms"].sum())

    top_winners = (
        df_oscar[df_oscar["Oscar_Wins"] > 0]
        .sort_values(["Oscar_Wins", "Oscar_Noms"], ascending=[False, False])
        .head(8)
    )

    return {
        "total_oscar_films": len(df_oscar),
        "total_wins": total_wins,
        "total_noms": total_noms,
        "top_winners": [
            {
                "name": str(r.get("Name", "")),
                "year": int(r.get("Year", 0) or 0),
                "oscar_wins": int(r.get("Oscar_Wins", 0) or 0),
                "oscar_noms": int(r.get("Oscar_Noms", 0) or 0),
                "user_rating": float(r.get("Rating", 0) or 0),
                "poster_url": str(r.get("Poster_URL", "") or ""),
                "letterboxd_url": str(r.get("Letterboxd URI", "") or ""),
            }
            for _, r in top_winners.iterrows()
        ],
    }
