# Letterboxd Analytics Dashboard

A fully automated personal movie analytics dashboard built on my Letterboxd watch history.

**Live:** https://letterboxd-analytics-3s9w.vercel.app

---

## What it does

- Syncs my Letterboxd diary every night via GitHub Actions
- Enriches each film with metadata from TMDB, OMDB, and Letterboxd itself
- Stores everything in a SQLite database committed to the repo
- Serves stats through a FastAPI backend deployed on Render
- Displays them in a Next.js frontend deployed on Vercel

## Stats tracked

Hall of Fame, weekly recap, yearly goal progress, top directors/genres, language breakdown, decade distribution, community rating comparisons, IMDb divergence, Oscar alignment, marathon detection, and more.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, TypeScript, deployed on Vercel |
| Backend | FastAPI (Python), deployed on Render |
| Database | SQLite, committed to git |
| Sync | GitHub Actions (daily cron at 03:00 UTC) |
| Scraping | BeautifulSoup4, Feedparser, Requests |
| Enrichment | TMDB API, OMDB API |

## How the pipeline works

1. GitHub Actions triggers `web_scraper.py` nightly
2. Script reads my Letterboxd RSS feed for new diary entries
3. Missing metadata is fetched from TMDB/OMDB and scraped from Letterboxd
4. SQLite DB is updated and committed back to the repo
5. Render redeploys the backend; Vercel serves the updated frontend

---

*Personal data engineering & full-stack project.*
