"use client";

import { useState } from "react";
import type { Marathon, TimeWasted, InsightFilm } from "@/lib/api";

interface Props {
  marathon: Marathon | null;
  time_wasted: TimeWasted;
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

function ExpandableFilmList({ films, firstCount = 1 }: { films: InsightFilm[]; firstCount?: number }) {
  const [expanded, setExpanded] = useState(false);
  const first = films.slice(0, firstCount);
  const rest = films.slice(firstCount);

  return (
    <div>
      {/* First film — italic, slightly larger */}
      {first.map((f, i) => (
        <a
          key={i}
          href={f.letterboxd_url}
          target="_blank"
          rel="noopener noreferrer"
          style={{ display: "block", textDecoration: "none" }}
        >
          <span style={{
            fontFamily: "var(--font-body)",
            fontSize: "17px",
            fontStyle: "italic",
            fontWeight: 400,
            color: "var(--color-body-text)",
            lineHeight: 1.6,
          }}>
            {f.name}
            {f.runtime ? (
              <span style={{ fontStyle: "normal", color: "var(--color-muted-text)", fontSize: "13px", marginLeft: "8px" }}>
                {f.runtime} min
              </span>
            ) : null}
          </span>
        </a>
      ))}

      {/* Expand toggle — only if there are more films */}
      {rest.length > 0 && (
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
            {f.runtime ? (
              <span style={{ color: "var(--color-muted-text)", marginLeft: "8px" }}>
                {f.runtime} min
              </span>
            ) : null}
          </span>
        </a>
      ))}
    </div>
  );
}

export default function InsightsLeft({ marathon, time_wasted }: Props) {
  return (
    <div style={{ position: "relative" }}>

      {/* Watermark */}
      {marathon && (
        <div aria-hidden style={{
          position: "absolute",
          top: "-16px",
          right: "0",
          fontFamily: "var(--font-display)",
          fontSize: "18rem",
          fontWeight: 700,
          color: "var(--color-border-whisper)",
          opacity: 0.3,
          lineHeight: 1,
          pointerEvents: "none",
          userSelect: "none",
          zIndex: 0,
        }}>
          {marathon.film_count}
        </div>
      )}

      <div style={{ position: "relative", zIndex: 1 }}>

        {/* ── Longest Marathon ── */}
        <p style={sectionLabel}>Longest Marathon</p>

        {marathon ? (
          <>
            {/* Runtime — 72px gold display */}
            <p style={{
              fontFamily: "var(--font-display)",
              fontSize: "72px",
              fontWeight: 400,
              letterSpacing: "-0.025em",
              lineHeight: 1,
              color: "var(--color-film-gold)",
              margin: "0 0 12px 0",
            }}>
              {Math.floor(marathon.total_runtime_mins / 60)}H {marathon.total_runtime_mins % 60}M
            </p>

            {/* Film count · Date — single headline line */}
            <p style={{
              fontFamily: "var(--font-headline)",
              fontSize: "11px",
              fontWeight: 400,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "var(--color-muted-text)",
              margin: "0 0 28px 0",
              lineHeight: 1,
            }}>
              {marathon.film_count} films &middot;{" "}
              {new Date(marathon.date + "T12:00:00").toLocaleDateString("en-US", {
                month: "long",
                day: "numeric",
                year: "numeric",
              })}
            </p>

            {/* Film list — first film italic, rest expandable */}
            {marathon.films.length > 0 && (
              <ExpandableFilmList films={marathon.films} firstCount={1} />
            )}
          </>
        ) : (
          <p style={{
            fontFamily: "var(--font-body)",
            fontSize: "15px",
            color: "var(--color-muted-text)",
          }}>
            No marathon data available
          </p>
        )}

        {/* ── Time Wasted ── */}
        {time_wasted.total_mins > 0 && (
          <div style={{ marginTop: "64px" }}>
            <p style={{
              ...sectionLabel,
              color: "var(--color-negative)",
              opacity: 0.7,
              margin: "0 0 16px 0",
            }}>
              &ldquo;Time Wasted&rdquo; Index
            </p>

            {/* Hours — 72px negative display */}
            <p style={{
              fontFamily: "var(--font-display)",
              fontSize: "72px",
              fontWeight: 400,
              letterSpacing: "-0.025em",
              lineHeight: 1,
              color: "var(--color-negative)",
              margin: "0 0 12px 0",
            }}>
              {Math.floor(time_wasted.total_mins / 60)}h
            </p>

            {/* Single subtitle line */}
            <p style={{
              fontFamily: "var(--font-headline)",
              fontSize: "11px",
              fontWeight: 400,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "var(--color-muted-text)",
              margin: 0,
              lineHeight: 1,
              opacity: 0.7,
            }}>
              on films rated below 2.0 stars
            </p>
          </div>
        )}

      </div>
    </div>
  );
}
