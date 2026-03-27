"use client";

import type { HallOfFameEntry } from "@/lib/api";

interface Props {
  films: HallOfFameEntry[];
}

export default function HofMosaic({ films }: Props) {
  if (!films.length) return null;
  // pick up to 4 distinct films spread across the list for variety
  const step = Math.max(1, Math.floor(films.length / 4));
  const picks = Array.from({ length: Math.min(4, films.length) }, (_, i) => films[i * step]);

  return (
    <div
      aria-hidden
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 1,
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gridTemplateRows: "1fr 1fr",
        overflow: "hidden",
        pointerEvents: "none",
      }}
    >
      {picks.map((film, i) => (
        <div
          key={i}
          style={{
            backgroundImage: `url('${film.poster_url}')`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            filter: "blur(90px) grayscale(100%) brightness(0.12)",
            transform: "scale(1.15)",
          }}
        />
      ))}
    </div>
  );
}
