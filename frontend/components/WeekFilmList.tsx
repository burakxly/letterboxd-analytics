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

  return (
    <div ref={ref} style={{ flex: 1, borderTop: "1px solid rgba(255,255,255,0.05)", paddingTop: "16px" }}>
      {shown.map((m, i) => (
        <p
          key={i}
          className={visible ? "film-item-visible" : "film-item-hidden"}
          style={{
            margin: "0 0 6px 0",
            fontSize: "0.8rem",
            animationDelay: visible ? `${i * 45}ms` : "0ms",
          }}
        >
          <span style={{ color: "#445566", marginRight: "6px" }}>▪</span>
          <a href={m.letterboxd_url} target="_blank" rel="noopener noreferrer" style={{ color: "#a0b0c0" }}>
            {m.name.length > 32 ? m.name.slice(0, 29) + "…" : m.name}
            {m.year > 0 && <span style={{ color: "#5a6b7c", fontSize: "0.73rem", marginLeft: "5px" }}>({m.year})</span>}
          </a>
        </p>
      ))}
      {rest > 0 && (
        <p style={{ color: "#5a6b7c", fontSize: "0.7rem", fontStyle: "italic", margin: "6px 0 0 0" }}>
          + {rest} more films…
        </p>
      )}
    </div>
  );
}
