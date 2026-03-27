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
    <div className="decades-outer">
      {/* Main content */}
      <div style={{ position: "relative", overflow: "hidden", flex: 1 }}>
        {/* Background backdrop/poster blur */}
        {(current.backdrop_url || current.poster_url) && (
          <div style={{
            position: "absolute", inset: 0,
            backgroundImage: `url('${current.backdrop_url || current.poster_url}')`,
            backgroundSize: "cover", backgroundPosition: "center",
            filter: "blur(18px) brightness(0.42)",
            zIndex: 0,
          }} />
        )}

        <div className="decades-content-inner" ref={contentRef}>
          {/* Poster */}
          <a href={current.letterboxd_url} target="_blank" rel="noopener noreferrer"
            style={{ flexShrink: 0, display: "block" }}>
            <div style={{
              width: "200px", height: "300px",
              borderRadius: "8px", overflow: "hidden",
              position: "relative",
              boxShadow: "0 20px 60px rgba(0,0,0,0.7)",
              border: "1px solid rgba(255,255,255,0.1)",
            }}>
              <Image
                src={current.poster_url || "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"}
                alt={current.name}
                fill
                style={{ objectFit: "cover" }}
                unoptimized
              />
            </div>
          </a>

          {/* Info */}
          <div>
            <p style={{ color: "#5a6b7c", fontSize: "0.78rem", letterSpacing: "3px", fontWeight: 600, textTransform: "uppercase", margin: "0 0 16px 0", fontFamily: "var(--font-cormorant), Georgia, serif" }}>
              The {current.decade}s
            </p>
            <a href={current.letterboxd_url} target="_blank" rel="noopener noreferrer">
              <h2 style={{
                color: "#F2F2F7", fontSize: "2.2rem", fontWeight: 800,
                lineHeight: 1.1, margin: "0 0 12px 0",
                letterSpacing: "-0.03em",
              }}>
                {current.name}
              </h2>
            </a>
            {current.year > 0 && (
              <p style={{ color: "#7a8b99", fontSize: "0.9rem", margin: "0 0 6px 0" }}>{current.year}</p>
            )}
            {current.director && (
              <p style={{ color: "#a0b0c0", fontSize: "0.9rem", fontStyle: "italic", margin: "0 0 20px 0" }}>{current.director}</p>
            )}
            <p style={{ color: "#e0e6ed", fontSize: "1.5rem", fontWeight: 300, margin: "0 0 8px 0" }}>
              <span style={{ color: "#c5a059" }}>★</span> {current.rating} / 5.0
            </p>
            <span style={{
              background: "rgba(197,160,89,0.1)",
              border: "1px solid rgba(197,160,89,0.25)",
              color: "#c5a059",
              padding: "4px 12px",
              borderRadius: "20px",
              fontSize: "0.7rem",
              fontWeight: 700,
              letterSpacing: "1.5px",
              textTransform: "uppercase",
            }}>
              Rated by Burak
            </span>
          </div>
        </div>
      </div>

      {/* Nav tabs — bottom */}
      <div className="decades-nav">
        {decades.map((d, i) => (
          <button
            key={d.decade}
            ref={(el) => { btnRefs.current[i] = el; }}
            onClick={() => handleTabClick(i)}
            className={`decades-nav-btn${i === active ? " decades-nav-btn--active" : ""}`}
          >
            <span style={{
              color: i === active ? "#F2F2F7" : "#5a6b7c",
              fontSize: i === active ? "1.35rem" : "1.1rem",
              fontWeight: i === active ? 700 : 400,
              fontFamily: "var(--font-cormorant), Georgia, serif",
              letterSpacing: "0.02em",
              transition: "all 0.2s",
            }}>
              &apos;{String(d.decade).slice(-2)}s
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
