const API_BASE = process.env.API_URL ?? "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    next: { revalidate: 3600 },
  });
  if (!res.ok) throw new Error(`API ${path} → ${res.status}`);
  return res.json();
}

// ── Types ──────────────────────────────────────────────────

export interface KPIs {
  total_films: number;
  total_hours: number;
  avg_rating: number;
  best_director: string;
  best_director_avg: number;
  best_genre: string;
  best_genre_avg: number;
  best_genre_count: number;
}

export interface LatestMovie {
  name: string;
  director: string;
  runtime: number;
  rating: number;
  genre: string;
  year: number;
  poster_url: string;
  letterboxd_url: string;
}

export interface WeekMovie {
  name: string;
  year: number;
  rating: number;
  runtime: number;
  letterboxd_url: string;
  poster_url: string;
}

export interface WeekActivity {
  count: number;
  avg_rating: number;
  runtime_mins: number;
  start_date: string;
  end_date: string;
  movies: WeekMovie[];
}

export interface Goal {
  year: number;
  goal: number;
  count: number;
  progress_pct: number;
}

export interface HallOfFameEntry {
  name: string;
  year: number;
  director: string;
  runtime: number;
  poster_url: string;
  letterboxd_url: string;
  watched_date: string;
}

export interface InsightFilm {
  name: string;
  runtime?: number;
  rating?: number;
  year?: number;
  letterboxd_url: string;
}

export interface Marathon {
  date: string;
  film_count: number;
  total_runtime_mins: number;
  bg_poster: string;
  films: InsightFilm[];
}

export interface TimeWasted {
  total_mins: number;
  films: InsightFilm[];
}

export interface PeakMonth {
  month: string;
  year: string;
  avg_rating: number;
  film_count: number;
  bg_poster: string;
  top_films: InsightFilm[];
}

export interface BestDecade {
  decade: number;
  avg_rating: number;
  film_count: number;
  bg_poster: string;
  top_films: InsightFilm[];
}

export interface Insights {
  marathon: Marathon | null;
  time_wasted: TimeWasted;
  peak_month: PeakMonth | null;
  best_decade: BestDecade | null;
  favorite_day: string | null;
}

export interface DecadeEntry {
  decade: number;
  name: string;
  year: number;
  rating: number;
  director: string;
  poster_url: string;
  letterboxd_url: string;
}

// ── Fetchers ───────────────────────────────────────────────

export const fetchKPIs = () => get<KPIs>("/api/kpis");
export const fetchLatest = () => get<LatestMovie>("/api/latest");
export const fetchWeek = () => get<WeekActivity>("/api/week");
export const fetchGoal = () => get<Goal>("/api/goal");
export const fetchHallOfFame = () => get<HallOfFameEntry[]>("/api/hall_of_fame");
export const fetchInsights = () => get<Insights>("/api/insights");
export const fetchDecades = () => get<DecadeEntry[]>("/api/decades");
