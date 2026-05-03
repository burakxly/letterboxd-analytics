export const revalidate = 3600; // 1 saatte bir Vercel cache'i yenile (veri günlük 1 kez güncelleniyor)

import Image from "next/image";
import {
  fetchKPIs,
  fetchLatest,
  fetchWeek,
  fetchGoal,
  fetchHallOfFame,
  fetchInsights,
  fetchDecades,
  type KPIs,
  type LatestMovie,
  type WeekActivity,
  type HallOfFameEntry,
  type Insights,
  type DecadeEntry,
} from "@/lib/api";
import DecadesSlider from "@/components/DecadesSlider";
import ScrollReveal from "@/components/ScrollReveal";
import AnimatedNumber from "@/components/AnimatedNumber";
import HeroParallaxImage from "@/components/HeroParallaxImage";
import AnimatedGoalBar from "@/components/AnimatedGoalBar";
import PosterTilt from "@/components/PosterTilt";
import WeekSection from "@/components/WeekSection";
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

const labelStyle: React.CSSProperties = {
  fontFamily: "var(--font-headline)",
  fontSize: "11px",
  fontWeight: 400,
  letterSpacing: "0.15em",
  textTransform: "uppercase",
  color: "var(--color-muted-text)",
  margin: "0 0 12px 0",
  lineHeight: 1,
};

const numberStyle: React.CSSProperties = {
  fontFamily: "var(--font-display)",
  fontSize: "48px",
  fontWeight: 400,
  letterSpacing: "-0.02em",
  lineHeight: 1,
  color: "var(--color-white)",
  margin: 0,
};

const goldNameStyle: React.CSSProperties = {
  fontFamily: "var(--font-display)",
  fontSize: "32px",
  fontWeight: 400,
  letterSpacing: "-0.01em",
  lineHeight: 1.1,
  color: "var(--color-film-gold)",
  margin: 0,
};

const subStyle: React.CSSProperties = {
  fontFamily: "var(--font-body)",
  fontSize: "12px",
  fontWeight: 400,
  color: "var(--color-muted-text)",
  margin: "8px 0 0 0",
  letterSpacing: "0.03em",
};

function KPIStrip({ kpis }: { kpis: KPIs }) {
  const dirSlug = kpis.best_director.toLowerCase().replace(/ /g, "-");
  return (
    <div className="kpi-strip">
      {/* Total Films */}
      <div className="kpi-item" style={{ flex: 1 }}>
        <p style={labelStyle}>Total Films</p>
        <p style={numberStyle}>
          <AnimatedNumber value={kpis.total_films} />
        </p>
      </div>

      {/* Total Hours */}
      <div className="kpi-item" style={{ flex: 1 }}>
        <p style={labelStyle}>Total Hours</p>
        <p style={numberStyle}>
          <AnimatedNumber value={kpis.total_hours} suffix="h" />
        </p>
      </div>

      {/* Top Director */}
      <div className="kpi-item" style={{ flex: 1.8 }}>
        <p style={labelStyle}>Top Director</p>
        <a
          href={`https://letterboxd.com/director/${dirSlug}/`}
          target="_blank"
          rel="noopener noreferrer"
          style={{ ...goldNameStyle, display: "block", textDecoration: "none" }}
        >
          {kpis.best_director}
        </a>
        <p style={subStyle}>{kpis.best_director_avg.toFixed(2)} avg rating</p>
      </div>

      {/* Top Genre */}
      <div className="kpi-item" style={{ flex: 1.8 }}>
        <p style={labelStyle}>Top Genre</p>
        <p style={goldNameStyle}>{kpis.best_genre}</p>
        <p style={subStyle}>
          {kpis.best_genre_avg.toFixed(2)} avg · {kpis.best_genre_count} films
        </p>
      </div>
    </div>
  );
}

// GoalBar → AnimatedGoalBar (client component, see components/AnimatedGoalBar.tsx)

// WeekActivity → WeekSection (client component, see components/WeekSection.tsx)

// ─── Latest Movie ─────────────────────────────────────────────────────────

function LatestMovieCard({ latest }: { latest: LatestMovie }) {
  return (
    <div style={{ alignSelf: "flex-start" }}>
      <p style={{
        fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
        letterSpacing: "0.15em", textTransform: "uppercase",
        color: "var(--color-muted-text)", margin: "0 0 16px 0", lineHeight: 1,
      }}>
        Most Recent Watch
      </p>
      <PosterTilt href={latest.letterboxd_url} style={{
        position: "relative",
        width: "260px", height: "390px",
        flexShrink: 0,
        borderRadius: "2px", overflow: "hidden",
      }}>
        {latest.poster_url && (
          <Image
            src={latest.poster_url} alt={latest.name} fill
            style={{ objectFit: "cover", objectPosition: "center top" }}
          />
        )}
        <div style={{
          position: "absolute", bottom: 0, left: 0, right: 0,
          background: "linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.6) 50%, transparent 100%)",
          padding: "16px", zIndex: 10,
        }}>
          <h2 style={{
            fontFamily: "var(--font-body)", fontSize: "13px", fontWeight: 400,
            textTransform: "uppercase", letterSpacing: "0.08em",
            color: "var(--color-white)", margin: "0 0 4px 0", lineHeight: 1.3,
          }}>
            {latest.name}
          </h2>
          <p style={{
            fontFamily: "var(--font-body)", fontSize: "13px", fontWeight: 400,
            color: "var(--color-muted-text)", margin: "0 0 8px 0",
          }}>
            {latest.director}
          </p>
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
    <div style={{
      marginBottom: "48px",
      height: "260px",
      display: "flex", flexDirection: "column", justifyContent: "center",
      overflow: "hidden",
    }}>
      <p style={{
        fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
        letterSpacing: "0.15em", textTransform: "uppercase",
        color: "var(--color-muted-text)", margin: "0 0 20px 0", lineHeight: 1,
      }}>
        Hall of Fame
      </p>
      <div className="marquee-wrapper">
        <div className="marquee-track">
          {doubled.map((film, i) => (
            <a key={i} href={film.letterboxd_url} target="_blank" rel="noopener noreferrer"
              className="hof-poster">
              <div style={{
                width: "110px", height: "165px",
                borderRadius: "2px", overflow: "hidden",
                position: "relative",
              }}>
                <Image
                  src={film.poster_url || "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"}
                  alt={film.name} fill
                  style={{ objectFit: "cover" }}
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
    <div style={{ position: "relative" }}>

      {/* Watermark — film count as enormous background number */}
      {marathon && (
        <div style={{
          position: "absolute", top: "-16px", right: "0",
          fontFamily: "var(--font-display)",
          fontSize: "18rem", fontWeight: 700,
          color: "var(--color-border-whisper)",
          opacity: 0.3,
          lineHeight: 1, pointerEvents: "none",
          userSelect: "none", zIndex: 0,
        }}>
          {marathon.film_count}
        </div>
      )}

      <div style={{ position: "relative", zIndex: 1 }}>

        {/* Section label */}
        <p style={{
          fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
          letterSpacing: "0.15em", textTransform: "uppercase",
          color: "var(--color-muted-text)", margin: "0 0 24px 0", lineHeight: 1,
        }}>
          Longest Marathon
        </p>

        {marathon ? (
          <>
            {/* Runtime — display 72px gold */}
            <p style={{
              fontFamily: "var(--font-display)",
              fontSize: "72px", fontWeight: 400,
              letterSpacing: "-0.025em", lineHeight: 1,
              color: "var(--color-film-gold)",
              margin: "0 0 8px 0",
            }}>
              {Math.floor(marathon.total_runtime_mins / 60)}H {marathon.total_runtime_mins % 60}M
            </p>

            {/* Film count */}
            <p style={{
              fontFamily: "var(--font-body)", fontSize: "15px", fontWeight: 400,
              color: "var(--color-muted-text)", margin: "0 0 4px 0",
            }}>
              {marathon.film_count} films
            </p>

            {/* Date — headline style */}
            <p style={{
              fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
              letterSpacing: "0.12em", textTransform: "uppercase",
              color: "var(--color-muted-text)", margin: "0 0 32px 0",
            }}>
              {new Date(marathon.date + "T12:00:00").toLocaleDateString("en-US", {
                month: "long", day: "numeric", year: "numeric",
              })}
            </p>

            {/* Film list — editorial, no dividers */}
            <div>
              {marathon.films.map((f, i) => (
                <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
                  style={{ display: "block", textDecoration: "none", lineHeight: 2.3 }}>
                  <span style={{
                    fontFamily: "var(--font-body)", fontSize: "15px", fontWeight: 400,
                    color: "var(--color-body-text)",
                  }}>
                    {f.name && f.name.length > 45 ? f.name.slice(0, 42) + "…" : f.name}
                    {f.runtime ? (
                      <span style={{ color: "var(--color-muted-text)" }}>
                        {" "}— {f.runtime} min
                      </span>
                    ) : null}
                  </span>
                </a>
              ))}
            </div>
          </>
        ) : (
          <p style={{ fontFamily: "var(--font-body)", fontSize: "15px", color: "var(--color-muted-text)" }}>
            No marathon data available
          </p>
        )}

        {/* Time Wasted */}
        {time_wasted.total_mins > 0 && (
          <div style={{ marginTop: "64px" }}>
            <p style={{
              fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
              letterSpacing: "0.15em", textTransform: "uppercase",
              color: "var(--color-negative)", margin: "0 0 16px 0", lineHeight: 1,
              opacity: 0.7,
            }}>
              &ldquo;Time Wasted&rdquo; Index
            </p>
            <p style={{
              fontFamily: "var(--font-display)",
              fontSize: "48px", fontWeight: 400,
              letterSpacing: "-0.02em", lineHeight: 1,
              color: "var(--color-negative)",
              margin: "0 0 6px 0",
            }}>
              {Math.floor(time_wasted.total_mins / 60)}h {time_wasted.total_mins % 60}m
            </p>
            <p style={{
              fontFamily: "var(--font-body)", fontSize: "13px",
              color: "var(--color-muted-text)", margin: "0 0 20px 0",
            }}>
              on films rated below 2.0 stars
            </p>
            {time_wasted.films.map((f, i) => (
              <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
                style={{ display: "block", textDecoration: "none", lineHeight: 2.3 }}>
                <span style={{
                  fontFamily: "var(--font-body)", fontSize: "15px", fontWeight: 400,
                  color: "var(--color-body-text)",
                }}>
                  {f.name && f.name.length > 36 ? f.name.slice(0, 33) + "…" : f.name}
                  {f.rating ? (
                    <span style={{ color: "var(--color-negative)" }}>
                      {" "}— {f.rating}★
                    </span>
                  ) : null}
                </span>
              </a>
            ))}
          </div>
        )}

      </div>
    </div>
  );
}

// ─── Insights: Peak Month + Best Decade + Fav Day ─────────────────────────

function InsightsRight({ insights }: { insights: Insights }) {
  const { peak_month, best_decade, favorite_day } = insights;

  const sectionLabel: React.CSSProperties = {
    fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
    letterSpacing: "0.15em", textTransform: "uppercase",
    color: "var(--color-muted-text)", margin: "0 0 24px 0", lineHeight: 1,
  };

  const filmRow: React.CSSProperties = {
    display: "block",
    fontFamily: "var(--font-body)", fontSize: "15px", fontWeight: 400,
    color: "var(--color-body-text)",
    lineHeight: 2.3,
    textDecoration: "none",
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "64px" }}>

      {/* ── Peak Cinema Month ── */}
      {peak_month && (
        <div>
          <p style={sectionLabel}>Peak Cinema Month</p>

          {/* Month — 96px display */}
          <p style={{
            fontFamily: "var(--font-display)",
            fontSize: "96px", fontWeight: 400,
            letterSpacing: "-0.03em", lineHeight: 0.95,
            color: "var(--color-white)",
            margin: "0 0 12px 0",
          }}>
            {peak_month.month}
          </p>

          {/* Year — headline uppercase */}
          <p style={{
            fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
            letterSpacing: "0.15em", textTransform: "uppercase",
            color: "var(--color-muted-text)", margin: "0 0 16px 0",
          }}>
            {peak_month.year}
          </p>

          {/* Stats — plain gold text, no badge */}
          <p style={{
            fontFamily: "var(--font-body)", fontSize: "15px", fontWeight: 400,
            color: "var(--color-film-gold)", margin: "0 0 24px 0",
          }}>
            {peak_month.avg_rating.toFixed(2)} avg · {peak_month.film_count} films
          </p>

          {/* Film list — plain lines */}
          <div>
            {peak_month.top_films.map((f, i) => (
              <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
                style={filmRow}>
                {f.name && f.name.length > 45 ? f.name.slice(0, 42) + "…" : f.name}
              </a>
            ))}
          </div>
        </div>
      )}

      {/* ── Most Generous Era ── */}
      {best_decade && (
        <div>
          <p style={sectionLabel}>Most Generous Era</p>

          {/* Decade — 72px display */}
          <div style={{ display: "flex", alignItems: "baseline", gap: "24px", marginBottom: "16px" }}>
            <p style={{
              fontFamily: "var(--font-display)",
              fontSize: "72px", fontWeight: 400,
              letterSpacing: "-0.025em", lineHeight: 1,
              color: "var(--color-white)", margin: 0,
            }}>
              {best_decade.decade}s
            </p>
            <div>
              <p style={{
                fontFamily: "var(--font-display)",
                fontSize: "24px", fontWeight: 400,
                color: "var(--color-film-gold)", margin: 0, lineHeight: 1,
              }}>
                {best_decade.avg_rating.toFixed(2)}
              </p>
              <p style={{
                fontFamily: "var(--font-body)", fontSize: "12px",
                color: "var(--color-muted-text)", margin: "4px 0 0 0",
              }}>
                {best_decade.film_count} films
              </p>
            </div>
          </div>

          {/* Film list */}
          <div>
            {best_decade.top_films.map((f, i) => (
              <a key={i} href={f.letterboxd_url} target="_blank" rel="noopener noreferrer"
                style={{ display: "block", textDecoration: "none", lineHeight: 2.3 }}>
                <span style={{
                  fontFamily: "var(--font-body)", fontSize: "15px", fontWeight: 400,
                  color: "var(--color-body-text)",
                }}>
                  {f.name && f.name.length > 42 ? f.name.slice(0, 39) + "…" : f.name}
                  {f.year ? (
                    <span style={{ color: "var(--color-muted-text)" }}>
                      {" "}— {f.year}
                    </span>
                  ) : null}
                </span>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* ── Favorite Day ── */}
      {favorite_day && (
        <div>
          <p style={sectionLabel}>Favorite Recent Day</p>
          <p style={{
            fontFamily: "var(--font-display)",
            fontSize: "48px", fontWeight: 400,
            letterSpacing: "-0.02em", lineHeight: 1,
            color: "var(--color-film-gold)", margin: 0,
          }}>
            {favorite_day}s
          </p>
        </div>
      )}

    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────

export default async function HomePage() {
  const [kpis, latest, week, goal, hallOfFame, insights, decades] = await Promise.all([
    fetchKPIs().catch(() => ({ total_films: 0, total_hours: 0, avg_rating: 0, best_director: "N/A", best_director_avg: 0, best_genre: "N/A", best_genre_avg: 0, best_genre_count: 0 })),
    fetchLatest().catch(() => ({ name: "—", director: "—", runtime: 0, rating: 0, genre: "—", year: 0, poster_url: "", letterboxd_url: "#" })),
    fetchWeek().catch(() => ({ count: 0, avg_rating: 0, runtime_mins: 0, start_date: "", end_date: "", movies: [] })),
    fetchGoal().catch(() => ({ year: new Date().getFullYear(), goal: 200, count: 0, progress_pct: 0 })),
    fetchHallOfFame().catch(() => [] as import("@/lib/api").HallOfFameEntry[]),
    fetchInsights().catch(() => ({ marathon: null, time_wasted: { total_mins: 0, films: [] }, peak_month: null, best_decade: null, favorite_day: null })),
    fetchDecades().catch(() => [] as import("@/lib/api").DecadeEntry[]),
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
          <WeekSection initialWeek={week} />
          <LatestMovieCard latest={latest} />
        </div>
      </ScrollReveal>

      <ScrollReveal>
        <HallOfFame films={hallOfFame} />
      </ScrollReveal>

      <hr className="section-sep" />

      <ScrollReveal>
        <div style={{ marginBottom: "48px" }}>
          <p style={{
            fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
            letterSpacing: "0.15em", textTransform: "uppercase",
            color: "var(--color-muted-text)", margin: "0 0 48px 0", lineHeight: 1,
          }}>
            Deep Insights
          </p>
          <div className="grid-insights">
            <MarathonCard insights={insights} />
            <div className="grid-insights-divider" />
            <InsightsRight insights={insights} />
          </div>
        </div>
      </ScrollReveal>

      <hr className="section-sep" />

      <ScrollReveal>
        <div>
          <p style={{
            fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
            letterSpacing: "0.15em", textTransform: "uppercase",
            color: "var(--color-muted-text)", margin: "0 0 48px 0", lineHeight: 1,
          }}>
            Decades of Cinema
          </p>
          <DecadesSlider decades={decades} />
        </div>
      </ScrollReveal>

    </main>
    </>
  );
}
