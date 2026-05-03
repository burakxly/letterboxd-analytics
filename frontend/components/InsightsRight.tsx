"use client";

import { useState } from "react";
import type { PeakMonth, BestDecade, InsightFilm } from "@/lib/api";

interface Props {
  peak_month: PeakMonth | null;
  best_decade: BestDecade | null;
  favorite_day: string | null;
}

const sectionLabel: React.CSSProperties = {
  fontFamily: "var(--font-headline)",
  fontSize: "11px",
  fontWeight: 400,
  letterSpacing: "0.15em",
  textTransform: "uppercase",
  color: "var(--color-muted-text)",
  margin: "0 0 24px 0",
  lineHeight: 1,
};

function ExpandableProseList({ films, showCount = 3 }: { films: InsightFilm[]; showCount?: number }) {
  const [expanded, setExpanded] = useState(false);
  const displayed = expanded ? films : films.slice(0, showCount);
  const hasMore = films.length > showCount;

  // Render as comma-separated prose italic paragraph
  const prose = displayed.map(f => f.name).join(", ");

  return (
    <div>
      <p style={{
        fontFamily: "var(--font-body)",
        fontSize: "15px",
        fontStyle: "italic",
        fontWeight: 400,
        color: "var(--color-body-text)",
        lineHeight: 1.7,
        margin: 0,
      }}>
        {prose}
        {!expanded && hasMore && (
          <span style={{ color: "var(--color-muted-text)", fontStyle: "normal" }}>…</span>
        )}
      </p>
      {hasMore && (
        <button
          onClick={() => setExpanded(e => !e)}
          style={{
            background: "none",
            border: "none",
            padding: "8px 0 0 0",
            cursor: "pointer",
            fontFamily: "var(--font-headline)",
            fontSize: "11px",
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--color-muted-text)",
            display: "flex",
            alignItems: "center",
            gap: "6px",
          }}
        >
          <span style={{ fontSize: "14px", lineHeight: 1 }}>{expanded ? "↑" : "+"}</span>
          {expanded ? "collapse" : `${films.length - showCount} more`}
        </button>
      )}
    </div>
  );
}

function ExpandableFilmLines({ films, showCount = 1 }: { films: InsightFilm[]; showCount?: number }) {
  const [expanded, setExpanded] = useState(false);
  const first = films[0];
  const rest = films.slice(1);

  if (!first) return null;

  return (
    <div>
      {/* Standout film — Playfair 32px italic */}
      <a
        href={first.letterboxd_url}
        target="_blank"
        rel="noopener noreferrer"
        style={{ display: "block", textDecoration: "none", marginBottom: rest.length > 0 ? "0" : "0" }}
      >
        <span style={{
          fontFamily: "var(--font-display)",
          fontSize: "32px",
          fontStyle: "italic",
          fontWeight: 400,
          letterSpacing: "-0.01em",
          lineHeight: 1.1,
          color: "var(--color-primary-text)",
        }}>
          {first.name}
          {first.year ? (
            <span style={{
              fontFamily: "var(--font-body)",
              fontStyle: "normal",
              fontSize: "13px",
              color: "var(--color-muted-text)",
              marginLeft: "10px",
              letterSpacing: "normal",
            }}>
              {first.year}
            </span>
          ) : null}
        </span>
      </a>

      {/* Expand toggle */}
      {rest.length > 0 && (
        <button
          onClick={() => setExpanded(e => !e)}
          style={{
            background: "none",
            border: "none",
            padding: "10px 0 0 0",
            cursor: "pointer",
            fontFamily: "var(--font-headline)",
            fontSize: "11px",
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--color-muted-text)",
            display: "flex",
            alignItems: "center",
            gap: "6px",
          }}
        >
          <span style={{ fontSize: "14px", lineHeight: 1 }}>{expanded ? "↑" : "+"}</span>
          {expanded ? "collapse" : `${rest.length} more`}
        </button>
      )}

      {/* Remaining films */}
      {expanded && rest.map((f, i) => (
        <a
          key={i}
          href={f.letterboxd_url}
          target="_blank"
          rel="noopener noreferrer"
          style={{ display: "block", textDecoration: "none" }}
        >
          <span style={{
            fontFamily: "var(--font-body)",
            fontSize: "15px",
            fontWeight: 400,
            color: "var(--color-body-text)",
            lineHeight: 2.2,
          }}>
            {f.name}
            {f.year ? (
              <span style={{ color: "var(--color-muted-text)", marginLeft: "8px" }}>
                {f.year}
              </span>
            ) : null}
          </span>
        </a>
      ))}
    </div>
  );
}

export default function InsightsRight({ peak_month, best_decade, favorite_day }: Props) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "72px" }}>

      {/* ── Peak Cinema Month ── */}
      {peak_month && (
        <div>
          <p style={sectionLabel}>Peak Cinema Month</p>

          {/* Month — 96px white display */}
          <p style={{
            fontFamily: "var(--font-display)",
            fontSize: "96px",
            fontWeight: 400,
            letterSpacing: "-0.03em",
            lineHeight: 0.95,
            color: "var(--color-white)",
            margin: "0 0 10px 0",
          }}>
            {peak_month.month}
          </p>

          {/* Year — 11px headline uppercase */}
          <p style={{
            fontFamily: "var(--font-headline)",
            fontSize: "11px",
            fontWeight: 400,
            letterSpacing: "0.15em",
            textTransform: "uppercase",
            color: "var(--color-muted-text)",
            margin: "0 0 18px 0",
            lineHeight: 1,
          }}>
            {peak_month.year}
          </p>

          {/* Stats — plain gold text */}
          <p style={{
            fontFamily: "var(--font-body)",
            fontSize: "15px",
            fontWeight: 400,
            color: "var(--color-film-gold)",
            margin: "0 0 20px 0",
          }}>
            {peak_month.avg_rating.toFixed(2)} avg &middot; {peak_month.film_count} films
          </p>

          {/* Films — comma-separated prose italic, expandable */}
          {peak_month.top_films.length > 0 && (
            <ExpandableProseList films={peak_month.top_films} showCount={3} />
          )}
        </div>
      )}

      {/* ── Most Generous Era ── */}
      {best_decade && (
        <div>
          <p style={sectionLabel}>Most Generous Era</p>

          {/* Decade — 96px white display */}
          <p style={{
            fontFamily: "var(--font-display)",
            fontSize: "96px",
            fontWeight: 400,
            letterSpacing: "-0.03em",
            lineHeight: 0.95,
            color: "var(--color-white)",
            margin: "0 0 10px 0",
          }}>
            {best_decade.decade}s
          </p>

          {/* Stats — gold body text */}
          <p style={{
            fontFamily: "var(--font-body)",
            fontSize: "15px",
            fontWeight: 400,
            color: "var(--color-film-gold)",
            margin: "0 0 24px 0",
          }}>
            {best_decade.avg_rating.toFixed(2)} avg &middot; {best_decade.film_count} films
          </p>

          {/* Standout film — Playfair 32px italic, rest expandable */}
          {best_decade.top_films.length > 0 && (
            <ExpandableFilmLines films={best_decade.top_films} />
          )}
        </div>
      )}

      {/* ── Favorite Day ── */}
      {favorite_day && (
        <div>
          <p style={sectionLabel}>Best Day to Watch</p>
          <p style={{
            fontFamily: "var(--font-display)",
            fontSize: "48px",
            fontWeight: 400,
            letterSpacing: "-0.02em",
            lineHeight: 1,
            color: "var(--color-film-gold)",
            margin: "0 0 8px 0",
          }}>
            {favorite_day}s
          </p>
          <p style={{
            fontFamily: "var(--font-headline)",
            fontSize: "11px",
            fontWeight: 400,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--color-muted-text)",
            margin: 0,
            lineHeight: 1,
          }}>
            highest avg rating by weekday
          </p>
        </div>
      )}

    </div>
  );
}
