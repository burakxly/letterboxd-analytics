\#  Letterboxd Auto-Sync Dashboard bot



This is a custom-built, fully automated data pipeline and web dashboard designed exclusively to track, enrich, and visualize my personal Letterboxd movie logs. By utilizing a daily cron job that reads my RSS feed and scrapes missing metadata, this system completely eliminates manual data entry and serves as a hands-on data engineering project. It runs 24/7 in the cloud, maintaining my movie history on autopilot.



\##  Features



\* \*\*Personalized Auto-Sync:\*\* A GitHub Actions cron job runs every night to check my specific Letterboxd RSS feed for newly logged movies.

\* \*\*Data Enrichment:\*\* Automatically visits movie pages to scrape missing metadata (Director, Genre, Runtime, Release Year) using `BeautifulSoup` and JSON-LD parsing.

\* \*\*Database Management:\*\* Maintains a clean, up-to-date `SQLite` database without duplicating my historical entries.

\* \*\*Interactive Dashboard:\*\* A dynamic and responsive UI built with `Streamlit` to visualize my movie stats, longest marathons, and favorite genres/directors.

\* \*\*Set \& Forget:\*\* Fully cloud-based automation. The pipeline updates the live Streamlit dashboard instantly without any local execution.



\##  Tech Stack



\* \*\*Language:\*\* Python 3.12

\* \*\*Data Processing \& Storage:\*\* Pandas, SQLite3

\* \*\*Web Scraping:\*\* BeautifulSoup4, Feedparser, Requests

\* \*\*Frontend / UI:\*\* Streamlit, Plotly

\* \*\*Automation / CI-CD:\*\* GitHub Actions



\##  How It Works



1\. \*\*Trigger:\*\* A GitHub Action (`Daily Sync`) wakes up every day at 03:00 UTC.

2\. \*\*Fetch:\*\* `web\_scraper.py` reads my Letterboxd RSS feed to detect newly logged movies.

3\. \*\*Enrich:\*\* The script visits the specific movie URIs to scrape additional details (Runtime, Director, Genre, etc.).

4\. \*\*Update:\*\* The new, enriched data is inserted into the master `SQLite` database.

5\. \*\*Deploy:\*\* Changes are committed and pushed back to the repository automatically, triggering Streamlit Cloud to update the live dashboard seamlessly.



\---

\*Built as a personal Data Engineering \& Automation project.\*

