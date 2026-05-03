"use client";

import { useEffect, useRef, useState } from "react";
import type { WeekMovie } from "@/lib/api";

interface Props {
  movies: WeekMovie[];
}

export default function WeekFilmList({ movies }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.unobserve(el); } },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const shown = movies.slice(0, 10);
  const rest = movies.length - 10;
  const hasCommunity = shown.some(m => m.community_rating > 0 && m.rating > 0);

  const colTemplate = hasCommunity ? "1fr 40px 72px" : "1fr 40px";

  const colHeaderStyle: React.CSSProperties = {
    fontFamily: "var(--font-headline)",
    fontSize: "11px",
    fontWeight: 400,
    letterSpacing: "0.15em",
    textTransform: "uppercase",
    lineHeight: 1,
  };

  return (
    <div ref={ref} style={{ flex: 1 }}>

      {/* Column headers */}
      <div style={{
        display: "grid", gridTemplateColumns: colTemplate, columnGap: "32px", alignItems: "center",
        paddingBottom: "10px",
        borderBottom: "1px solid var(--color-border-whisper)",
        marginBottom: "0",
      }}>
        <span style={{ ...colHeaderStyle, color: "var(--color-muted-text)" }}>Film</span>
        <span style={{ ...colHeaderStyle, color: "var(--color-film-gold)", textAlign: "right" }}>Mine</span>
        {hasCommunity && (
          <span style={{ ...colHeaderStyle, color: "var(--color-muted-text)", textAlign: "right" }}>Community</span>
        )}
      </div>

      {shown.map((m, i) => {
        const hasBoth = m.community_rating > 0 && m.rating > 0;
        const diff = hasBoth ? m.rating - m.community_rating : null;

        return (
          <div
            key={i}
            className={visible ? "film-item-visible" : "film-item-hidden"}
            style={{
              display: "grid",
              gridTemplateColumns: colTemplate,
              columnGap: "32px",
              alignItems: "center",
              padding: "10px 0",
              borderBottom: "1px solid var(--color-border-whisper)",
              animationDelay: visible ? `${i * 45}ms` : "0ms",
            }}
          >
            {/* Film name + year */}
            <a
              href={m.letterboxd_url}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                fontFamily: "var(--font-body)",
                fontSize: "15px",
                fontWeight: 400,
                color: "var(--color-body-text)",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                paddingRight: "8px",
                textDecoration: "none",
              }}
            >
              {m.name.length > 30 ? m.name.slice(0, 27) + "…" : m.name}
              {m.year > 0 && (
                <span style={{
                  color: "var(--color-muted-text)",
                  fontSize: "12px",
                  marginLeft: "6px",
                }}>
                  {m.year}
                </span>
              )}
            </a>

            {/* Mine rating */}
            <span style={{
              fontFamily: "var(--font-body)",
              fontSize: "15px",
              fontWeight: 400,
              color: m.rating > 0 ? "var(--color-film-gold)" : "var(--color-border-whisper)",
              textAlign: "right",
            }}>
              {m.rating > 0 ? m.rating : "—"}
            </span>

            {/* Community rating */}
            {hasCommunity && (
              <span style={{
                fontFamily: "var(--font-body)",
                fontSize: "13px",
                fontWeight: 400,
                color: "var(--color-muted-text)",
                textAlign: "right",
                whiteSpace: "nowrap",
              }}>
                {hasBoth ? (
                  <>
                    {m.community_rating.toFixed(1)}
                    {diff !== null && Math.abs(diff) > 0.3 && (
                      <span style={{
                        fontSize: "11px",
                        marginLeft: "4px",
                        color: diff > 0 ? "var(--color-positive)" : "var(--color-negative)",
                      }}>
                        {diff > 0 ? `+${diff.toFixed(1)}` : diff.toFixed(1)}
                      </span>
                    )}
                  </>
                ) : "—"}
              </span>
            )}
          </div>
        );
      })}

      {rest > 0 && (
        <p style={{
          fontFamily: "var(--font-body)",
          fontSize: "12px",
          color: "var(--color-muted-text)",
          margin: "12px 0 0 0",
          letterSpacing: "0.03em",
        }}>
          +{rest} more this week
        </p>
      )}
    </div>
  );
}
