export const dynamic = 'force-dynamic';

import Image from "next/image";
import {
  fetchKPIs,
  fetchLatest,
  fetchWeek,
  fetchGoal,
  fetchHallOfFame,
  fetchInsights,
  fetchDecades,
  fetchLanguages,
  fetchCommunity,
  fetchImdb,
  fetchOscar,
  type KPIs,
  type LatestMovie,
  type WeekActivity,
  type HallOfFameEntry,
  type Insights,
  type DecadeEntry,
  type LanguageStat,
  type CommunityComparison,
  type ImdbComparison,
  type OscarStats,
} from "@/lib/api";
import DecadesSlider from "@/components/DecadesSlider";
import ScrollReveal from "@/components/ScrollReveal";
import AnimatedNumber from "@/components/AnimatedNumber";
import HeroParallaxImage from "@/components/HeroParallaxImage";
import AnimatedGoalBar from "@/components/AnimatedGoalBar";
import PosterTilt from "@/components/PosterTilt";
import WeekFilmList from "@/components/WeekFilmList";
import HofMosaic from "@/components/HofMosaic";

// ─── helpers ──────────────────────────────────────────────────────────────

function Stars({ rating }: { rating: number }) {
  if (!rating) return <span style={{ color: "#5a6b7c", fontSize: "0.85rem" }}>No Rating</span>;
  const full = Math.floor(rating);
  const half = rating % 1 !== 0;
  const empty = 5 - full - (half ? 1 : 0);
  return (
    <span style={{ color: "#c5a059", fontSize: "1.25rem", letterSpacing: "3px" }}>
      {"★".repeat(full)}
      {half ? "½" : ""}
      {"☆".repeat(empty)}
    </span>
  );
}

// ─── Hero ─────────────────────────────────────────────────────────────────

function HeroSection() {
  return (
    <>
      <p style={{
        color: "rgba(255,255,255,0.45)",
        fontSize: "1.1rem",
        fontStyle: "italic",
        fontFamily: "var(--font-cormorant), Georgia, serif",
        letterSpacing: "0.06em",
        fontWeight: 400,
        marginBottom: "14px",
      }}>
        some masks come off, some don&rsquo;t
      </p>

      <div className="hero-banner">
        <HeroParallaxImage />
        {/* mobile only — bottom-up overlay (desktop: mask-image on .hero-img) */}
        <div className="hero-overlay" style={{
          position: "absolute", inset: 0,
          background: "transparent",
          pointerEvents: "none",
          zIndex: 2,
        }} />
        {/* top vignette */}
        <div style={{
          position: "absolute", inset: 0,
          background: "linear-gradient(to bottom, rgba(10,12,15,0.6) 0%, transparent 20%, transparent 75%, rgba(10,12,15,0.4) 100%)",
          pointerEvents: "none",
          zIndex: 3,
        }} />
        <div className="hero-text-panel">
          <p className="hero-manifesto hero-text-enter" style={{
            color: "rgba(235,242,248,0.96)", fontSize: "1.12rem",
            lineHeight: 1.85, fontFamily: "var(--font-cormorant), Georgia, serif",
            fontWeight: 500, margin: "0 0 20px 0",
            animationDelay: "0.3s",
            fontFeatureSettings: '"liga" 1, "kern" 1',
          }}>
            This project was born from a mix of pure boredom and absolute freedom.
            I built this system as a direct response to the absurdity of Letterboxd
            processing my own data just to sell it back to me. Now, fueled by a 24/7
            GitHub automation, I construct my archive exactly how I want it —
            visualizing and tracking my cinematic history strictly on my own terms.
          </p>
          <p className="hero-byline hero-text-enter" style={{
            color: "rgba(235,242,248,0.95)", fontSize: "0.82rem", fontWeight: 600,
            letterSpacing: "5px", textTransform: "uppercase", fontStyle: "italic",
            fontFamily: "var(--font-cormorant), Georgia, serif",
            animationDelay: "0.7s",
          }}>
            created by burak
          </p>
        </div>
      </div>
    </>
  );
}

// ─── KPI Strip ────────────────────────────────────────────────────────────

function KPIStrip({ kpis }: { kpis: KPIs }) {
  const dirSlug = kpis.best_director.toLowerCase().replace(/ /g, "-");
  return (
    <div className="kpi-strip">
      {/* Total Films */}
      <div className="kpi-item" style={{ flex: 1, borderRight: "1px solid rgba(255,255,255,0.05)" }}>
        <p style={{ color: "#7a8b99", fontSize: "0.68rem", fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", margin: "0 0 6px 0" }}>Total Films</p>
        <p style={{ color: "#e0e6ed", fontSize: "2.2rem", fontWeight: 700, lineHeight: 1, margin: 0 }}>
          <AnimatedNumber value={kpis.total_films} />
        </p>
      </div>
      {/* Total Hours */}
      <div className="kpi-item" style={{ flex: 1, borderRight: "1px solid rgba(255,255,255,0.05)" }}>
        <p style={{ color: "#7a8b99", fontSize: "0.68rem", fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", margin: "0 0 6px 0" }}>Total Hours</p>
        <p style={{ color: "#e0e6ed", fontSize: "2.2rem", fontWeight: 700, lineHeight: 1, margin: 0 }}>
          <AnimatedNumber value={kpis.total_hours} suffix="hrs" />
        </p>
      </div>
      {/* Top Director */}
      <div className="kpi-item" style={{ flex: 1.8, borderRight: "1px solid rgba(255,255,255,0.05)" }}>
        <p style={{ color: "#7a8b99", fontSize: "0.68rem", fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", margin: "0 0 6px 0" }}>
          Top Director <span style={{ color: "#445566", fontWeight: 400 }}>(min 6 watched films)</span>
        </p>
        <a href={`https://letterboxd.com/director/${dirSlug}/`} target="_blank" rel="noopener noreferrer"
          className="gold-gradient"
          style={{ fontSize: "1.35rem", fontWeight: 700, lineHeight: 1.2, display: "block" }}>
          {kpis.best_director}
        </a>
        <p style={{ color: "#a0b0c0", fontSize: "0.78rem", margin: "4px 0 0 0", fontStyle: "italic" }}>
          {kpis.best_director_avg.toFixed(2)} Avg Rating
        </p>
      </div>
      {/* Top Genre */}
      <div className="kpi-item" style={{ flex: 1.8 }}>
        <p style={{ color: "#7a8b99", fontSize: "0.68rem", fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", margin: "0 0 6px 0" }}>
          Top Genre <span style={{ color: "#445566", fontWeight: 400 }}>(Weighted)</span>
        </p>
        <p className="gold-gradient" style={{ fontSize: "1.35rem", fontWeight: 700, lineHeight: 1.2, margin: 0 }}>{kpis.best_genre}</p>
        <p style={{ color: "#a0b0c0", fontSize: "0.78rem", margin: "4px 0 0 0", fontStyle: "italic" }}>
          {kpis.best_genre_avg.toFixed(2)} Avg • {kpis.best_genre_count} Films
        </p>
      </div>
    </div>
  );
}

// GoalBar → AnimatedGoalBar (client component, see components/AnimatedGoalBar.tsx)

// ─── Week Activity ────────────────────────────────────────────────────────

function WeekActivity({ week }: { week: WeekActivity }) {
  return (
    <div className="glass-card card-hover" style={{
      padding: "24px",
      display: "flex", flexDirection: "column", minHeight: "360px",
    }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "20px" }}>
        <p style={{ color: "#a0b0c0", fontSize: "0.75rem", fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", margin: 0 }}>
          <span className="pulse-dot" />Recording
        </p>
        <p style={{ color: "#5a6b7c", fontSize: "0.75rem", margin: 0 }}>
          [{week.start_date} — {week.end_date}]
        </p>
      </div>

      <div style={{ display: "flex", gap: "24px", marginBottom: "20px" }}>
        {[
          { label: "Films", val: week.count },
          { label: "Avg Rating", val: week.avg_rating > 0 ? week.avg_rating.toFixed(2) : "—" },
          { label: "Total Mins", val: week.runtime_mins.toLocaleString() },
        ].map((s) => (
          <div key={s.label}>
            <p style={{ color: "#5a6b7c", fontSize: "0.65rem", fontWeight: 600, letterSpacing: "1px", textTransform: "uppercase", margin: "0 0 4px 0" }}>{s.label}</p>
            <p style={{ color: "#e0e6ed", fontSize: "1.6rem", fontWeight: 700, margin: 0, lineHeight: 1 }}>{s.val}</p>
          </div>
        ))}
      </div>

      <WeekFilmList movies={week.movies} />
    </div>
  );
}

// ─── Latest Movie ─────────────────────────────────────────────────────────

function LatestMovieCard({ latest }: { latest: LatestMovie }) {
  return (
    <div style={{ alignSelf: "flex-start" }}>
      <p style={{ color: "#a0b0c0", fontSize: "0.75rem", fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", margin: "0 0 12px 0" }}>
        Most Recent Watch
      </p>
      <PosterTilt href={latest.letterboxd_url} style={{
        position: "relative",
        width: "260px", height: "390px",
        flexShrink: 0,
        borderRadius: "10px", overflow: "hidden",
        border: "1px solid rgba(255,255,255,0.1)",
        boxShadow: "0 12px 40px rgba(0,0,0,0.6)",
      }}>
        {latest.poster_url && (
          <Image
            src={latest.poster_url} alt={latest.name} fill
            style={{ objectFit: "cover", objectPosition: "center top" }}
            unoptimized
          />
        )}
        <div style={{
          position: "absolute", bottom: 0, left: 0, right: 0,
          background: "linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.6) 50%, transparent 100%)",
          padding: "16px", zIndex: 10,
        }}>
          <h2 style={{ color: "#f0f0f0", fontSize: "0.85rem", fontWeight: 800, textTransform: "uppercase", margin: "0 0 4px 0", lineHeight: 1.3 }}>{latest.name}</h2>
          <p style={{ color: "#ccd6dd", fontSize: "0.7rem", fontStyle: "italic", margin: "0 0 8px 0" }}>{latest.director}</p>
          <Stars rating={latest.rating} />
        </div>
      </PosterTilt>
    </div>
  );
}

// ─── Hall of Fame ─────────────────────────────────────────────────────────

function HallOfFame({ films }: { films: HallOfFameEntry[] }) {
  if (!films.length) return null;
  const doubled = [...films, ...films];

  return (
    <div className="glass-card" style={{
      padding: "24px 24px 24px 28px",
      marginBottom: "48px",
      height: "260px",
      display: "flex", flexDirection: "column", justifyContent: "center",
      overflow: "hidden",
    }}>
      <h4 style={{ color: "#a0b0c0", fontSize: "0.78rem", letterSpacing: "2px", fontWeight: 800, textTransform: "uppercase", margin: "0 0 16px 0" }}>
        Hall of Fame <span style={{ color: "#5a6b7c", fontWeight: 400, fontSize: "0.68rem" }}>(Masterpieces)</span>
      </h4>
      <div className="marquee-wrapper">
        <div className="marquee-track">
          {doubled.map((film, i) => (
            <a key={i} href={film.letterboxd_url} target="_blank" rel="noopener noreferrer"
              className="hof-poster">
              <div style={{
                width: "110px", height: "165px",
                borderRadius: "6px", overflow: "hidden",
                position: "relative",
                border: "1px solid rgba(255,255,255,0.08)",
              }}>
                <Image
                  src={film.poster_url || "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"}
                  alt={film.name} fill
                  style={{ objectFit: "cover" }}
                  unoptimized
                />
              </div>
              <div className="hof-overlay">
                <p style={{ color: "#f0f0f0", fontSize: "0.6rem", fontWeight: 700, margin: 0, lineHeight: 1.3, textTransform: "uppercase", letterSpacing: "0.5px" }}>
                  {film.name.length > 18 ? film.name.slice(0, 16) + "…" : film.name}
                </p>
                {film.year > 0 && (
                  <p style={{ color: "#c5a059", fontSize: "0.58rem", margin: "2px 0 0 0", fontWeight: 600 }}>{film.year}</p>
                )}
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Insights: Marathon + Time Wasted ─────────────────────────────────────

function MarathonCard({ insights }: { insights: Insights }) {
  const { marathon, time_wasted } = insights;

  return (
    <div className="glass-card card-hover" style={{
      borderLeft: "3px solid rgba(224,230,237,0.4)",
      padding: "32px",
      position: "relative", overflow: "hidden",
    }}>
      {marathon?.bg_poster && (
        <div style={{
          position: "absolute", inset: 0,
          backgroundImage: `url('${marathon.bg_poster}')`,
          backgroundSize: "cover", backgroundPosition: "center",
          filter: "blur(55px) brightness(0.1)", zIndex: 0,
        }} />
      )}
      <div style={{ position: "relative", zIndex: 1 }}>
        {marathon && (
          <div style={{
            position: "absolute", top: "-30px", right: "-10px",
            fontSize: "13rem", fontWeight: 700, color: "rgba(255,255,255,0.04)",
            lineHeight: 1, pointerEvents: "none", fontFamily: "var(--font-cormorant), Georgia, serif",
          }}>
            {marathon.film_count}
          </div>
        )}

        <p style={{ color: "#5a6b7c", fontSize: "0.62rem", letterSpacing: "3px", fontWeight: 800, textTransform: "uppercase", margin: "0 0 20px 0" }}>
          Longest Marathon
        </p>

        {marathon ? (
          <>
            <div style={{ display: "flex", alignItems: "flex-end", gap: "24px", marginBottom: "8px" }}>
              <div>
                <span style={{ fontSize: "7rem", fontWeight: 900, color: "#f0f0f0", lineHeight: 1, letterSpacing: "-5px" }}>{marathon.film_count}</span>
                <span style={{ fontSize: "1.4rem", color: "#7a8b99", fontWeight: 400, marginLeft: "8px" }}>films</span>
              </div>
              <div style={{ paddingBottom: "12px" }}>
                <p style={{ fontSize: "2.4rem", fontWeight: 700, color: "#c5a059", margin: 0, lineHeight: 1 }}>
                  {Math.floor(marathon.total_runtime_mins / 60)}H {marathon.total_runtime_mins % 60}M
                </p>
                <p style={{ color: "#445566", fontSize: "0.68rem", letterSpacing: "1px", margin: "4px 0 0 0", textTransform: "uppercase" }}>total runtime</p>
              </div>
            </div>
            <p style={{ color: "#556677", fontSize: "0.82rem", margin: "0 0 24px 0", fontFamily: "monospace" }}>
              {new Date(marathon.date + "T12:00:00").toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
            </p>
            <div style={{ borderTop: "1px solid rgba(255,255,255,0.07)", paddingTop: "16px" }}>
              <p style={{ color: "#445566", fontSize: "0.62rem", letterSpacing: "2px", textTransform: "uppercase", margin: "0 0 8px 0" }}>Films watched</p>
              {marathon.films.map((f, i) => (
                <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
                  style={{ display: "flex", justifyContent: "space-between", alignItems: "center", color: "#8090a0", fontSize: "0.82rem", padding: "8px 0", borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
                  <span>{f.name && f.name.length > 45 ? f.name.slice(0, 42) + "…" : f.name}</span>
                  <span style={{ color: "#5a6b7c", fontSize: "0.7rem" }}>{f.runtime ? `${f.runtime} min` : ""}</span>
                </a>
              ))}
            </div>
          </>
        ) : (
          <p style={{ color: "#5a6b7c" }}>No marathon data available</p>
        )}

        {/* Time Wasted */}
        <div style={{ marginTop: "24px", paddingTop: "20px", borderTop: "1px solid rgba(139,42,42,0.2)" }}>
          <p style={{ color: "#6a3333", fontSize: "0.6rem", letterSpacing: "3px", fontWeight: 800, textTransform: "uppercase", margin: "0 0 4px 0" }}>
            &ldquo;Time Wasted&rdquo; Index
          </p>
          <p style={{ fontSize: "1.8rem", fontWeight: 800, color: "#a53838", margin: "0 0 4px 0", fontFamily: "'Courier New', monospace", letterSpacing: "-1px", lineHeight: 1 }}>
            {Math.floor(time_wasted.total_mins / 60)}h {time_wasted.total_mins % 60}m
          </p>
          <p style={{ color: "#4a3333", fontSize: "0.68rem", margin: "0 0 10px 0" }}>on films rated below 2.0 stars</p>
          {time_wasted.films.map((f, i) => (
            <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
              style={{ display: "flex", justifyContent: "space-between", alignItems: "center", color: "#7a5555", fontSize: "0.75rem", padding: "4px 0", borderBottom: "1px solid rgba(139,42,42,0.12)" }}>
              <span>{f.name && f.name.length > 36 ? f.name.slice(0, 33) + "…" : f.name}</span>
              <span style={{ fontWeight: 700, color: "#a53838", marginLeft: "8px" }}>{f.rating}★</span>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Insights: Peak Month + Best Decade + Fav Day ─────────────────────────

function InsightsRight({ insights }: { insights: Insights }) {
  const { peak_month, best_decade, favorite_day } = insights;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {peak_month && (
        <div className="glass-card card-hover" style={{
          border: "1px solid rgba(197,160,89,0.2)",
          borderBottom: "2px solid #c5a059",
          borderRadius: "6px", padding: "20px",
          textAlign: "center", position: "relative", overflow: "hidden",
        }}>
          {peak_month.bg_poster && (
            <div style={{
              position: "absolute", inset: 0,
              backgroundImage: `url('${peak_month.bg_poster}')`,
              backgroundSize: "cover", backgroundPosition: "center",
              filter: "blur(50px) brightness(0.08)", zIndex: 0,
            }} />
          )}
          <div style={{ position: "relative", zIndex: 1 }}>
            <p style={{ color: "#5a4a20", fontSize: "0.62rem", letterSpacing: "3px", fontWeight: 800, textTransform: "uppercase", margin: "0 0 4px 0" }}>Peak Cinema Month</p>
            <p style={{ color: "#4a3a18", fontSize: "0.92rem", fontStyle: "italic", fontFamily: "var(--font-cormorant), Georgia, serif", margin: "0 0 10px 0" }}>
              The month you were most in tune with cinema
            </p>
            <p style={{ fontSize: "2rem", fontWeight: 800, color: "#e8d090", margin: 0, lineHeight: 1.1 }}>{peak_month.month}</p>
            <p style={{ fontSize: "1rem", fontWeight: 500, color: "#7a6a30", margin: "0 0 8px 0" }}>{peak_month.year}</p>
            <span style={{ background: "rgba(197,160,89,0.12)", border: "1px solid rgba(197,160,89,0.3)", color: "#c5a059", padding: "3px 12px", borderRadius: "20px", fontWeight: 800, fontSize: "0.9rem" }}>
              {peak_month.avg_rating.toFixed(2)} AVG · {peak_month.film_count} films
            </span>
            <div style={{ borderTop: "1px solid rgba(197,160,89,0.12)", paddingTop: "12px", marginTop: "14px", textAlign: "left" }}>
              {peak_month.top_films.map((f, i) => (
                <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
                  style={{ display: "block", color: "#7a6a30", fontSize: "0.78rem", padding: "5px 0", borderBottom: "1px solid rgba(197,160,89,0.1)" }}>
                  {f.name && f.name.length > 45 ? f.name.slice(0, 42) + "…" : f.name}
                </a>
              ))}
            </div>
          </div>
        </div>
      )}

      {best_decade && (
        <div className="glass-card card-hover" style={{
          borderRadius: "8px", padding: "24px",
          position: "relative", overflow: "hidden",
        }}>
          {best_decade.bg_poster && (
            <div style={{
              position: "absolute", inset: 0,
              backgroundImage: `url('${best_decade.bg_poster}')`,
              backgroundSize: "cover", backgroundPosition: "center",
              filter: "blur(50px) brightness(0.1)", zIndex: 0,
            }} />
          )}
          <div style={{ position: "relative", zIndex: 1 }}>
            <p style={{ color: "#5a6b7c", fontSize: "0.72rem", letterSpacing: "3px", fontWeight: 600, textTransform: "uppercase", margin: "0 0 12px 0", fontFamily: "var(--font-cormorant), Georgia, serif" }}>Most Generous Era</p>
            <div style={{ display: "flex", alignItems: "baseline", gap: "16px", marginBottom: "16px", paddingBottom: "16px", borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
              <p style={{ fontSize: "5rem", fontWeight: 300, color: "#e0e6ed", lineHeight: 1, margin: 0, letterSpacing: "-1px", fontFamily: "var(--font-cormorant), Georgia, serif" }}>
                {best_decade.decade}s
              </p>
              <div>
                <p style={{ fontSize: "1.2rem", fontWeight: 700, color: "#c5a059", margin: 0, lineHeight: 1 }}>{best_decade.avg_rating.toFixed(2)}</p>
                <p style={{ fontSize: "0.7rem", color: "#5a6b7c", margin: "2px 0 0 0", letterSpacing: "1px", textTransform: "uppercase" }}>avg rating</p>
                <p style={{ fontSize: "0.7rem", color: "#5a6b7c", margin: "2px 0 0 0", letterSpacing: "1px", textTransform: "uppercase" }}>{best_decade.film_count} films watched</p>
              </div>
            </div>
            <p style={{ color: "#445566", fontSize: "0.62rem", letterSpacing: "2px", textTransform: "uppercase", margin: "0 0 4px 0" }}>Top Films</p>
            {best_decade.top_films.map((f, i) => (
              <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
                style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", padding: "7px 0", borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                <span style={{ color: "#c8d4dc", fontSize: "0.9rem", fontStyle: "italic", fontFamily: "var(--font-cormorant), Georgia, serif" }}>
                  {f.name && f.name.length > 42 ? f.name.slice(0, 39) + "…" : f.name}
                </span>
                <span style={{ color: "#c5a059", fontSize: "0.75rem", fontWeight: 700, marginLeft: "10px", whiteSpace: "nowrap" }}>{f.year}</span>
              </a>
            ))}
          </div>
        </div>
      )}

      {favorite_day && (
        <div className="glass-card" style={{
          borderRadius: "8px", padding: "18px 24px",
          display: "flex", alignItems: "center", justifyContent: "space-between",
        }}>
          <p style={{ color: "#5a6b7c", fontSize: "0.7rem", letterSpacing: "2px", textTransform: "uppercase", margin: 0 }}>Favorite Recent Day</p>
          <p className="gold-gradient" style={{ fontSize: "1.4rem", fontWeight: 700, margin: 0 }}>{favorite_day}s</p>
        </div>
      )}
    </div>
  );
}

// ─── Language Stats ───────────────────────────────────────────────────────

function LanguageSection({ languages }: { languages: LanguageStat[] }) {
  if (!languages.length) return null;
  const total = languages.reduce((s, l) => s + l.count, 0);
  // Visual max: 2nd language * 2.5 so English doesn't crush everyone
  const visualMax = languages.length > 1 ? languages[1].count * 2.5 : languages[0].count;

  return (
    <div className="glass-card card-hover" style={{ padding: "28px 32px" }}>
      <p className="section-label" style={{ margin: "0 0 4px 0" }}>Cinema Language</p>
      <p style={{ color: "#445566", fontSize: "0.82rem", fontStyle: "italic", fontFamily: "var(--font-cormorant), Georgia, serif", margin: "0 0 20px 0" }}>
        Original language distribution across {total} films
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        {languages.map((l) => {
          const pct = Math.round((l.count / total) * 100);
          const barW = Math.min((l.count / visualMax) * 100, 100);
          return (
            <div key={l.language}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "5px" }}>
                <span style={{ color: "#c8d4dc", fontSize: "1.05rem", fontFamily: "var(--font-cormorant), Georgia, serif", fontStyle: "italic" }}>
                  {l.label}
                </span>
                <span style={{ color: "#5a6b7c", fontSize: "0.8rem", display: "flex", gap: "10px", alignItems: "center" }}>
                  <span style={{ color: "#a0b0c0", fontWeight: 600 }}>{pct}%</span>
                  <span>{l.count} film</span>
                  <span style={{ color: "#c5a059", fontWeight: 700 }}>{l.avg_rating.toFixed(2)} avg.</span>
                </span>
              </div>
              <div style={{ height: "3px", background: "rgba(255,255,255,0.05)", borderRadius: "2px", overflow: "hidden" }}>
                <div style={{
                  height: "100%",
                  width: `${barW}%`,
                  background: "linear-gradient(90deg, #b8924a, #e8cc80)",
                  borderRadius: "2px",
                }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── Community Comparison ─────────────────────────────────────────────────
// Full-width, two-column editorial. Max 4 films per side.

function CommunitySection({ data }: { data: CommunityComparison }) {
  if (!data.total_compared) return null;
  const diffLabel = data.avg_diff > 0 ? `+${data.avg_diff.toFixed(2)}` : data.avg_diff.toFixed(2);
  const diffColor = data.avg_diff > 0 ? "#6db86d" : "#c06060";
  const serif = "var(--font-cormorant), Georgia, serif";

  return (
    <div className="glass-card card-hover" style={{ padding: "32px 36px", gridColumn: "1 / -1" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", marginBottom: "28px", paddingBottom: "20px", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div>
          <p className="section-label" style={{ margin: "0 0 6px 0" }}>Community vs You</p>
          <p style={{ color: "#8090a0", fontSize: "1.2rem", fontStyle: "italic", fontFamily: serif, margin: 0, lineHeight: 1.3 }}>
            {data.total_compared} films compared against Letterboxd average
          </p>
        </div>
        <div style={{ textAlign: "right" }}>
          <span style={{ fontSize: "4rem", fontWeight: 400, color: diffColor, lineHeight: 1, fontFamily: "var(--font-cormorant), Georgia, serif", fontVariantNumeric: "lining-nums", letterSpacing: "-0.01em" }}>{diffLabel}</span>
          <p style={{ color: "#5a6b7c", fontSize: "0.86rem", margin: "4px 0 0 0", fontFamily: "var(--font-cormorant), Georgia, serif", fontStyle: "italic" }}>
            {data.avg_diff < 0 ? "Community generally rates higher than you" : "You generally rate higher than the community"}
          </p>
        </div>
      </div>

      {/* Two columns — max 4 films each */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "40px" }}>
        <div>
          <p className="section-label" style={{ color: "#6db86d", margin: "0 0 2px 0" }}>Your Hidden Gems</p>
          <p style={{ color: "#556677", fontSize: "0.97rem", fontStyle: "italic", fontFamily: serif, margin: "0 0 16px 0" }}>
            Films the community underrated
          </p>
          {data.underrated.slice(0, 4).map((f, i) => (
            <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
              style={{ display: "block", padding: "14px 0", borderBottom: "1px solid rgba(255,255,255,0.04)", textDecoration: "none" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "5px" }}>
                <span style={{ color: "#d0dce6", fontSize: "1.15rem", fontFamily: serif, fontStyle: "italic", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: "72%" }}>
                  {f.name}
                </span>
                <span style={{ color: "#6db86d", fontSize: "1.2rem", fontWeight: 700, fontFamily: serif, flexShrink: 0 }}>
                  +{f.diff.toFixed(1)}
                </span>
              </div>
              <div style={{ display: "flex", gap: "14px" }}>
                <span style={{ color: "#6db86d", fontSize: "0.9rem" }}>You {f.user_rating}</span>
                <span style={{ color: "#334455", fontSize: "0.9rem" }}>·</span>
                <span style={{ color: "#5a6b7c", fontSize: "0.9rem" }}>Community {f.community_rating?.toFixed(1)}</span>
                <span style={{ color: "#4a5a68", fontSize: "0.84rem", marginLeft: "auto" }}>{f.year}</span>
              </div>
            </a>
          ))}
        </div>

        <div>
          <p className="section-label" style={{ color: "#c06060", margin: "0 0 2px 0" }}>Overrated by Community</p>
          <p style={{ color: "#556677", fontSize: "0.97rem", fontStyle: "italic", fontFamily: serif, margin: "0 0 16px 0" }}>
            Films the community rated above you
          </p>
          {data.overrated.slice(0, 4).map((f, i) => (
            <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
              style={{ display: "block", padding: "14px 0", borderBottom: "1px solid rgba(255,255,255,0.04)", textDecoration: "none" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "5px" }}>
                <span style={{ color: "#d0dce6", fontSize: "1.15rem", fontFamily: serif, fontStyle: "italic", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: "72%" }}>
                  {f.name}
                </span>
                <span style={{ color: "#c06060", fontSize: "1.2rem", fontWeight: 700, fontFamily: serif, flexShrink: 0 }}>
                  {f.diff.toFixed(1)}
                </span>
              </div>
              <div style={{ display: "flex", gap: "14px" }}>
                <span style={{ color: "#c06060", fontSize: "0.9rem" }}>You {f.user_rating}</span>
                <span style={{ color: "#334455", fontSize: "0.9rem" }}>·</span>
                <span style={{ color: "#5a6b7c", fontSize: "0.9rem" }}>Community {f.community_rating?.toFixed(1)}</span>
                <span style={{ color: "#4a5a68", fontSize: "0.84rem", marginLeft: "auto" }}>{f.year}</span>
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── IMDb Comparison ──────────────────────────────────────────────────────
// Half-width. Featured #1 disagreement as hero card, then compact list.

function ImdbSection({ data }: { data: ImdbComparison }) {
  if (!data.total_compared) return null;
  const diffLabel = data.avg_diff > 0 ? `+${data.avg_diff.toFixed(2)}` : data.avg_diff.toFixed(2);
  const serif = "var(--font-cormorant), Georgia, serif";
  const [top, ...rest] = data.disagreements;

  return (
    <div className="glass-card card-hover" style={{ padding: "28px 32px" }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "20px" }}>
        <div>
          <p className="section-label" style={{ margin: "0 0 4px 0" }}>IMDb vs You</p>
          <p style={{ color: "#8090a0", fontSize: "1.1rem", fontStyle: "italic", fontFamily: serif, margin: 0, lineHeight: 1.3 }}>
            Biggest gaps across {data.total_compared} films
          </p>
        </div>
        <div style={{ textAlign: "right", flexShrink: 0, marginLeft: "16px" }}>
          <span style={{ fontSize: "2.8rem", fontWeight: 400, color: "#c5a059", lineHeight: 1, fontFamily: "var(--font-cormorant), Georgia, serif", fontVariantNumeric: "lining-nums", letterSpacing: "-0.01em", display: "block" }}>{diffLabel}</span>
          <span style={{ color: "#5a6b7c", fontSize: "0.7rem", fontFamily: "var(--font-cormorant), Georgia, serif", fontStyle: "italic" }}>
            {data.avg_diff < 0 ? "IMDb rates higher than you" : "You rate higher than IMDb"}
          </span>
        </div>
      </div>

      {/* Featured #1 disagreement */}
      {top && (() => {
        const myScore = top.user_rating;
        const imdbNorm = (top.imdb_rating ?? 0) / 2;
        const iLikedMore = top.diff > 0;
        return (
          <a href={top.letterboxd_url} target="_blank" rel="noopener noreferrer"
            style={{ display: "block", background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: "10px", padding: "18px 20px", marginBottom: "14px", textDecoration: "none" }}>
            <p style={{ color: "#445566", fontSize: "0.58rem", letterSpacing: "2.5px", textTransform: "uppercase", fontWeight: 700, margin: "0 0 10px 0" }}>
              Biggest Gap
            </p>
            <p style={{ color: "#d0dce6", fontSize: "1.6rem", fontFamily: serif, fontStyle: "italic", margin: "0 0 14px 0", lineHeight: 1.2 }}>
              {top.name}
              <span style={{ color: "#3a4a58", fontSize: "0.94rem", marginLeft: "10px" }}>{top.year}</span>
            </p>
            <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "2rem", fontWeight: 700, color: iLikedMore ? "#c5a059" : "#8090a0", fontFamily: serif, lineHeight: 1 }}>{myScore}</div>
                <div style={{ fontSize: "0.56rem", letterSpacing: "1.5px", color: "#445566", marginTop: "3px" }}>YOU</div>
              </div>
              <div style={{ color: "#2a3a48", fontSize: "1rem", fontWeight: 300 }}>vs</div>
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "2rem", fontWeight: 300, color: "#4a5a6a", fontFamily: serif, lineHeight: 1 }}>{imdbNorm.toFixed(1)}</div>
                <div style={{ fontSize: "0.56rem", letterSpacing: "1.5px", color: "#445566", marginTop: "3px" }}>IMDb</div>
              </div>
              <span style={{
                marginLeft: "auto", fontSize: "0.85rem", fontWeight: 700, padding: "4px 14px", borderRadius: "20px",
                color: iLikedMore ? "#c5a059" : "#8090a0",
                background: iLikedMore ? "rgba(197,160,89,0.12)" : "rgba(128,144,160,0.12)",
                border: `1px solid ${iLikedMore ? "rgba(197,160,89,0.3)" : "rgba(128,144,160,0.2)"}`,
              }}>
                {iLikedMore ? `+${top.diff.toFixed(1)}` : top.diff.toFixed(1)}
              </span>
            </div>
          </a>
        );
      })()}

      {/* Compact list for the rest */}
      {rest.slice(0, 4).map((f, i) => {
        const myScore = f.user_rating;
        const imdbNorm = ((f.imdb_rating ?? 0) / 2);
        const iLikedMore = f.diff > 0;
        return (
          <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
            style={{ display: "flex", alignItems: "center", gap: "10px", padding: "9px 0", borderBottom: "1px solid rgba(255,255,255,0.04)", textDecoration: "none" }}>
            <span style={{ color: iLikedMore ? "#c5a059" : "#7a8b99", fontSize: "1.2rem", fontWeight: 700, fontFamily: serif, minWidth: "24px", textAlign: "center" }}>{myScore}</span>
            <span style={{ color: "#2a3a48", fontSize: "0.75rem" }}>vs</span>
            <span style={{ color: "#445566", fontSize: "1.1rem", fontWeight: 300, fontFamily: serif, minWidth: "28px", textAlign: "center" }}>{imdbNorm.toFixed(1)}</span>
            <span style={{ flex: 1, color: "#c0ccd8", fontSize: "1.12rem", fontFamily: serif, fontStyle: "italic", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {f.name}
            </span>
            <span style={{ flexShrink: 0, fontSize: "0.82rem", fontWeight: 700, color: iLikedMore ? "#c5a059" : "#7a8b99" }}>
              {iLikedMore ? `+${f.diff.toFixed(1)}` : f.diff.toFixed(1)}
            </span>
          </a>
        );
      })}
    </div>
  );
}

// ─── Oscar Stats ──────────────────────────────────────────────────────────

function OscarSection({ data }: { data: OscarStats }) {
  if (!data.total_oscar_films) return null;
  return (
    <div className="glass-card card-hover" style={{ padding: "28px 32px" }}>
      <p style={{ color: "#5a6b7c", fontSize: "0.68rem", letterSpacing: "3px", fontWeight: 800, textTransform: "uppercase", margin: "0 0 16px 0" }}>
        Academy Alignment
      </p>
      <div style={{ display: "flex", gap: "28px", marginBottom: "20px" }}>
        {[
          { label: "Oscar Films", val: data.total_oscar_films },
          { label: "Total Wins", val: data.total_wins },
          { label: "Nominations", val: data.total_noms },
        ].map((s) => (
          <div key={s.label}>
            <p style={{ color: "#5a6b7c", fontSize: "0.68rem", fontWeight: 600, letterSpacing: "1px", textTransform: "uppercase", margin: "0 0 4px 0" }}>{s.label}</p>
            <p style={{ color: "#e8d090", fontSize: "2rem", fontWeight: 700, margin: 0, lineHeight: 1 }}>{s.val}</p>
          </div>
        ))}
      </div>
      <p className="section-label" style={{ margin: "0 0 4px 0" }}>Most Decorated</p>
      <p style={{ color: "#556677", fontSize: "0.82rem", fontStyle: "italic", margin: "0 0 10px 0" }}>Oscar films you&apos;ve watched</p>
      <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px", marginBottom: "4px" }}>
        <span style={{ color: "#5a6b7c", fontSize: "0.68rem", minWidth: "48px", textAlign: "center" }}>Awards</span>
        <span style={{ color: "#5a6b7c", fontSize: "0.68rem", minWidth: "32px", textAlign: "right" }}>Score</span>
      </div>
      {data.top_winners.map((f, i) => (
        <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
          style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: "12px", alignItems: "center", padding: "9px 0", borderBottom: "1px solid rgba(255,255,255,0.05)", textDecoration: "none" }}>
          <span style={{ minWidth: 0 }}>
            <span style={{ color: "#c8d4dc", fontSize: "1.05rem", fontFamily: "var(--font-cormorant), Georgia, serif", fontStyle: "italic", display: "block", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {f.name}
            </span>
            <span style={{ color: "#556677", fontSize: "0.75rem" }}>{f.year}</span>
          </span>
          <span style={{ display: "flex", gap: "10px", alignItems: "center", flexShrink: 0 }}>
            <span style={{ color: "#e8d090", fontWeight: 700, fontSize: "0.85rem", minWidth: "48px", textAlign: "center" }}>
              {f.oscar_wins}W {f.oscar_noms > 0 ? `/ ${f.oscar_noms}N` : ""}
            </span>
            <span style={{ color: "#c5a059", fontSize: "0.85rem", fontWeight: 700, minWidth: "32px", textAlign: "right" }}>
              {f.user_rating > 0 ? f.user_rating : "—"}
            </span>
          </span>
        </a>
      ))}
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────

export default async function HomePage() {
  const [kpis, latest, week, goal, hallOfFame, insights, decades, languages, community, imdb, oscar] = await Promise.all([
    fetchKPIs().catch(() => ({ total_films: 0, total_hours: 0, avg_rating: 0, best_director: "N/A", best_director_avg: 0, best_genre: "N/A", best_genre_avg: 0, best_genre_count: 0 })),
    fetchLatest().catch(() => ({ name: "—", director: "—", runtime: 0, rating: 0, genre: "—", year: 0, poster_url: "", letterboxd_url: "#" })),
    fetchWeek().catch(() => ({ count: 0, avg_rating: 0, runtime_mins: 0, start_date: "—", end_date: "—", movies: [] })),
    fetchGoal().catch(() => ({ year: new Date().getFullYear(), goal: 200, count: 0, progress_pct: 0 })),
    fetchHallOfFame().catch(() => [] as import("@/lib/api").HallOfFameEntry[]),
    fetchInsights().catch(() => ({ marathon: null, time_wasted: { total_mins: 0, films: [] }, peak_month: null, best_decade: null, favorite_day: null })),
    fetchDecades().catch(() => [] as import("@/lib/api").DecadeEntry[]),
    fetchLanguages().catch(() => []),
    fetchCommunity().catch(() => ({ avg_diff: 0, total_compared: 0, underrated: [], overrated: [] })),
    fetchImdb().catch(() => ({ avg_diff: 0, total_compared: 0, agreements: [], disagreements: [] })),
    fetchOscar().catch(() => ({ total_oscar_films: 0, total_wins: 0, total_noms: 0, top_winners: [] })),
  ]);

  return (
    <>
      <HofMosaic films={hallOfFame} />
      <main className="page-main">
      <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "16px" }}>
        <a href="https://letterboxd.com/burakxly/" target="_blank" rel="noopener noreferrer"
          style={{
            color: "#8a9ab0", fontSize: "0.72rem", fontWeight: 500,
            letterSpacing: "2px", display: "flex", alignItems: "center", gap: "7px",
            borderBottom: "1px solid rgba(197,160,89,0.2)", paddingBottom: "2px",
          }}>
          <span style={{ color: "#c5a059", fontSize: "0.42rem", lineHeight: 1 }}>◆</span>
          @burakxly on Letterboxd
          <span style={{ color: "#c5a059", fontSize: "0.68rem" }}>↗</span>
        </a>
      </div>

      <HeroSection />

      <ScrollReveal>
        <KPIStrip kpis={kpis} />
      </ScrollReveal>

      <ScrollReveal delay={80}>
        <AnimatedGoalBar goal={goal} />
      </ScrollReveal>

      <ScrollReveal delay={60}>
        <div className="grid-week">
          <WeekActivity week={week} />
          <LatestMovieCard latest={latest} />
        </div>
      </ScrollReveal>

      <ScrollReveal>
        <HallOfFame films={hallOfFame} />
      </ScrollReveal>

      <hr className="section-sep" />

      <ScrollReveal>
        <div style={{ marginBottom: "48px" }}>
          <h4 style={{ color: "#a0b0c0", fontSize: "0.68rem", letterSpacing: "0.18em", textTransform: "uppercase", fontWeight: 500, margin: "0 0 28px 0", fontFamily: "var(--font-geist-sans), sans-serif" }}>
            Deep Insights
          </h4>
          <div className="grid-insights">
            <MarathonCard insights={insights} />
            <InsightsRight insights={insights} />
          </div>
        </div>
      </ScrollReveal>

      <hr className="section-sep" />

      <ScrollReveal>
        <div>
          <h4 style={{ color: "#a0b0c0", fontSize: "0.68rem", letterSpacing: "0.18em", textTransform: "uppercase", fontWeight: 500, margin: "0 0 28px 0", fontFamily: "var(--font-geist-sans), sans-serif" }}>
            Decades of Cinema
          </h4>
          <DecadesSlider decades={decades} />
        </div>
      </ScrollReveal>

      <hr className="section-sep" style={{ marginTop: "48px" }} />

      <ScrollReveal>
        <div style={{ marginBottom: "48px" }}>
          <h4 style={{ color: "#a0b0c0", fontSize: "0.68rem", letterSpacing: "0.18em", textTransform: "uppercase", fontWeight: 500, margin: "0 0 28px 0", fontFamily: "var(--font-geist-sans), sans-serif" }}>
            Data & Analytics
          </h4>
          <div className="grid-insights" style={{ rowGap: "28px" }}>
            <LanguageSection languages={languages} />
            <OscarSection data={oscar} />
            <CommunitySection data={community} />
            <ImdbSection data={imdb} />
          </div>
        </div>
      </ScrollReveal>
    </main>
    </>
  );
}
