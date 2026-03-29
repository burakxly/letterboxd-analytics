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

  const colTemplate = hasCommunity ? "1fr 36px 80px" : "1fr 36px";

  return (
    <div ref={ref} style={{ flex: 1, borderTop: "1px solid rgba(255,255,255,0.05)", paddingTop: "14px" }}>

      {/* Column header */}
      <div style={{ display: "grid", gridTemplateColumns: colTemplate, alignItems: "center", marginBottom: "10px", paddingBottom: "8px", borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
        <span style={{ color: "#445566", fontSize: "0.6rem", letterSpacing: "1.5px", textTransform: "uppercase", fontWeight: 600 }}>Film</span>
        <span style={{ color: "#c5a059", fontSize: "0.6rem", letterSpacing: "1.5px", textTransform: "uppercase", fontWeight: 600, textAlign: "right" }}>Mine</span>
        {hasCommunity && (
          <span style={{ color: "#5a6b7c", fontSize: "0.6rem", letterSpacing: "1.5px", textTransform: "uppercase", fontWeight: 600, textAlign: "right" }}>Community</span>
        )}
      </div>

      {shown.map((m, i) => {
        const hasBoth = m.community_rating > 0 && m.rating > 0;
        const diff = hasBoth ? m.rating - m.community_rating : null;
        const diffColor = diff === null ? "transparent" : diff > 0.3 ? "#6db86d" : diff < -0.3 ? "#c06060" : "#6a7a8a";

        return (
          <div
            key={i}
            className={visible ? "film-item-visible" : "film-item-hidden"}
            style={{
              display: "grid",
              gridTemplateColumns: colTemplate,
              alignItems: "center",
              gap: "0",
              padding: "5px 0",
              borderBottom: "1px solid rgba(255,255,255,0.03)",
              animationDelay: visible ? `${i * 45}ms` : "0ms",
            }}
          >
            {/* Film name */}
            <a href={m.letterboxd_url} target="_blank" rel="noopener noreferrer"
              style={{ color: "#a0b0c0", fontSize: "0.82rem", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", paddingRight: "8px" }}>
              {m.name.length > 28 ? m.name.slice(0, 25) + "…" : m.name}
              {m.year > 0 && <span style={{ color: "#445566", fontSize: "0.7rem", marginLeft: "5px" }}>({m.year})</span>}
            </a>

            {/* Mine rating */}
            <span style={{ color: m.rating > 0 ? "#c5a059" : "#2a3a4a", fontSize: "0.85rem", fontWeight: 700, textAlign: "right" }}>
              {m.rating > 0 ? m.rating : "—"}
            </span>

            {/* Community rating + diff */}
            {hasCommunity && (
              <span style={{ textAlign: "right", fontSize: "0.82rem", color: "#5a6b7c", whiteSpace: "nowrap" }}>
                {hasBoth ? (
                  <>
                    {m.community_rating.toFixed(1)}
                    {diff !== null && (
                      <span style={{ color: diffColor, fontSize: "0.65rem", fontWeight: 700, marginLeft: "4px" }}>
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
        <p style={{ color: "#5a6b7c", fontSize: "0.7rem", fontStyle: "italic", margin: "8px 0 0 0" }}>
          +{rest} more this week
        </p>
      )}
    </div>
  );
}
