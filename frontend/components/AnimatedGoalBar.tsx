"use client";

import { useEffect, useRef, useState } from "react";
import type { Goal } from "@/lib/api";
import AnimatedNumber from "@/components/AnimatedNumber";

export default function AnimatedGoalBar({ goal }: { goal: Goal }) {
  const ref = useRef<HTMLDivElement>(null);
  const fillRef = useRef<HTMLDivElement>(null);
  const [triggered, setTriggered] = useState(false);
  const pct = goal.progress_pct;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !triggered) {
          setTriggered(true);
          observer.unobserve(el);
          // animate fill bar
          const fill = fillRef.current;
          if (!fill) return;
          const start = performance.now();
          const duration = 1200;
          function tick(now: number) {
            const p = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - p, 3);
            const w = eased * pct;
            fill!.style.width = `${w}%`;
            if (p < 1) requestAnimationFrame(tick);
          }
          requestAnimationFrame(tick);
        }
      },
      { threshold: 0.3 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [pct, triggered]);

  return (
    <div ref={ref} style={{ marginBottom: "48px", paddingTop: "10px" }}>
      {/* Header row */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "24px" }}>
        <div>
          <p style={{
            fontFamily: "var(--font-headline)",
            fontSize: "11px",
            fontWeight: 400,
            letterSpacing: "0.15em",
            textTransform: "uppercase",
            color: "var(--color-muted-text)",
            margin: "0 0 10px 0",
            lineHeight: 1,
          }}>
            {goal.year} Annual Goal
          </p>
          {/* Large count */}
          <div style={{ display: "flex", alignItems: "baseline", gap: "12px" }}>
            <span style={{
              fontFamily: "var(--font-display)",
              fontSize: "72px",
              fontWeight: 400,
              letterSpacing: "-0.025em",
              lineHeight: 1,
              color: "var(--color-white)",
            }}>
              {triggered ? <AnimatedNumber value={goal.count} duration={1200} /> : 0}
            </span>
            <span style={{
              fontFamily: "var(--font-body)",
              fontSize: "17px",
              fontWeight: 400,
              color: "var(--color-muted-text)",
              letterSpacing: "0.02em",
            }}>
              / {goal.goal}
            </span>
          </div>
        </div>
        {/* Percent — top-right, aligned to number baseline area */}
        <p style={{
          fontFamily: "var(--font-body)",
          fontSize: "11px",
          fontWeight: 400,
          letterSpacing: "0.05em",
          color: "var(--color-muted-text)",
          margin: 0,
          alignSelf: "flex-end",
          paddingBottom: "6px",
        }}>
          {pct.toFixed(1)}% complete
        </p>
      </div>

      {/* 2px flat bar — no radius, no glow */}
      <div style={{ width: "100%", height: "2px", background: "var(--color-border-whisper)" }}>
        <div ref={fillRef} style={{
          width: "0%",
          height: "100%",
          background: "var(--color-film-gold)",
        }} />
      </div>
    </div>
  );
}
