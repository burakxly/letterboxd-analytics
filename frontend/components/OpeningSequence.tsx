"use client";

import { useEffect, useState } from "react";

export default function OpeningSequence() {
  const [phase, setPhase] = useState<"hold" | "fade" | "done">("hold");

  useEffect(() => {
    const t1 = setTimeout(() => setPhase("fade"), 700);
    const t2 = setTimeout(() => setPhase("done"), 2100);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, []);

  if (phase === "done") return null;

  return (
    <div style={{
      position: "fixed",
      inset: 0,
      zIndex: 200000,
      background: "#0a0c0f",
      opacity: phase === "fade" ? 0 : 1,
      transition: "opacity 1.2s ease",
      pointerEvents: phase === "fade" ? "none" : "all",
    }}>
      <div style={{
        position: "absolute", inset: 0, pointerEvents: "none",
        backgroundImage: "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")",
        backgroundSize: "128px 128px",
        opacity: 0.07,
      }} />
    </div>
  );
}
