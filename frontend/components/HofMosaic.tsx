"use client";

import type { HallOfFameEntry } from "@/lib/api";

interface Props {
  films: HallOfFameEntry[];
}

export default function HofMosaic({ films }: Props) {
  if (!films.length) return null;
  // pick 4 spread across the list for variety
  const picks = [0, 1, 2, 3].map((i) => films[i % films.length]).filter(Boolean);

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
