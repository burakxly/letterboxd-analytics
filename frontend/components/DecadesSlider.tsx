"use client";

import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import type { DecadeEntry } from "@/lib/api";

export default function DecadesSlider({ decades }: { decades: DecadeEntry[] }) {
  const [active, setActive] = useState(0);
  const [prev, setPrev] = useState(0);
  const btnRefs = useRef<(HTMLButtonElement | null)[]>([]);
  const contentRef = useRef<HTMLDivElement>(null);

  if (!decades.length) return null;

  const current = decades[active];

  useEffect(() => {
    const el = contentRef.current;
    if (!el || active === prev) return;
    el.classList.add("transitioning");
    const t = setTimeout(() => el.classList.remove("transitioning"), 260);
    return () => clearTimeout(t);
  }, [active, prev]);

  function handleTabClick(i: number) {
    if (i === active) return;
    setPrev(active);
    setActive(i);
    btnRefs.current[i]?.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
  }

  return (
    <div>
      {/* Tab bar — thin gold underline on active, whisper line on container */}
      <div style={{
        display: "flex",
        overflowX: "auto",
        overflowY: "hidden",
        borderBottom: "1px solid var(--color-border-whisper)",
        marginBottom: "40px",
        scrollbarWidth: "none",
        gap: "0",
      }}>
        {decades.map((d, i) => (
          <button
            key={d.decade}
            ref={(el) => { btnRefs.current[i] = el; }}
            onClick={() => handleTabClick(i)}
            style={{
              background: "none",
              border: "none",
              borderBottom: i === active
                ? "1px solid var(--color-film-gold)"
                : "1px solid transparent",
              marginBottom: "-1px",
              position: "relative",
              zIndex: i === active ? 1 : 0,
              cursor: "pointer",
              padding: "12px 24px 14px",
              fontFamily: "var(--font-display)",
              fontSize: "1rem",
              fontWeight: 400,
              letterSpacing: "0.02em",
              color: i === active ? "var(--color-primary-text)" : "var(--color-muted-text)",
              transition: "color 0.15s",
              whiteSpace: "nowrap",
              flexShrink: 0,
            }}
          >
            &apos;{String(d.decade).slice(-2)}s
          </button>
        ))}
      </div>

      {/* Content — poster left, text right */}
      <div
        ref={contentRef}
        className="decades-content-inner"
        style={{ display: "flex", gap: "40px", alignItems: "flex-start", padding: "0" }}
      >
        {/* Poster — 2px radius, no shadow */}
        <a
          href={current.letterboxd_url}
          target="_blank"
          rel="noopener noreferrer"
          style={{ flexShrink: 0, display: "block" }}
        >
          <div style={{
            width: "160px", height: "240px",
            borderRadius: "2px", overflow: "hidden",
            position: "relative",
          }}>
            <Image
              src={current.poster_url || "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"}
              alt={current.name}
              fill
              style={{ objectFit: "cover" }}
            />
          </div>
        </a>

        {/* Info */}
        <div>
          {/* Decade label */}
          <p style={{
            fontFamily: "var(--font-headline)", fontSize: "11px", fontWeight: 400,
            letterSpacing: "0.15em", textTransform: "uppercase",
            color: "var(--color-muted-text)", margin: "0 0 20px 0", lineHeight: 1,
          }}>
            The {current.decade}s
          </p>

          {/* Film title — display serif */}
          <a href={current.letterboxd_url} target="_blank" rel="noopener noreferrer"
            style={{ textDecoration: "none" }}>
            <h2 style={{
              fontFamily: "var(--font-display)",
              fontSize: "32px", fontWeight: 400,
              letterSpacing: "-0.02em", lineHeight: 1.05,
              color: "var(--color-primary-text)",
              margin: "0 0 12px 0",
            }}>
              {current.name}
            </h2>
          </a>

          {/* Director */}
          {current.director && (
            <p style={{
              fontFamily: "var(--font-body)", fontSize: "15px", fontWeight: 400,
              color: "var(--color-muted-text)", margin: "0 0 4px 0",
            }}>
              {current.director}
            </p>
          )}

          {/* Year */}
          {current.year > 0 && (
            <p style={{
              fontFamily: "var(--font-body)", fontSize: "13px",
              color: "var(--color-muted-text)", margin: "0 0 24px 0",
            }}>
              {current.year}
            </p>
          )}

          {/* Rating — plain text fraction, no star, no pill */}
          <p style={{
            fontFamily: "var(--font-display)",
            fontSize: "24px", fontWeight: 400,
            letterSpacing: "-0.01em", lineHeight: 1,
            color: "var(--color-film-gold)", margin: 0,
          }}>
            {current.rating} / 5
          </p>
        </div>
      </div>
    </div>
  );
}
