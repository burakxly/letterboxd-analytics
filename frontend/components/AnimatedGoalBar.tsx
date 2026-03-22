"use client";

import { useEffect, useRef, useState } from "react";
import type { Goal } from "@/lib/api";
import AnimatedNumber from "@/components/AnimatedNumber";

export default function AnimatedGoalBar({ goal }: { goal: Goal }) {
  const ref = useRef<HTMLDivElement>(null);
  const fillRef = useRef<HTMLDivElement>(null);
  const dotRef = useRef<HTMLDivElement>(null);
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
          const dot = dotRef.current;
          if (!fill || !dot) return;
          const start = performance.now();
          const duration = 1200;
          function tick(now: number) {
            const p = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - p, 3);
            const w = eased * pct;
            fill!.style.width = `${w}%`;
            dot!.style.left = `${w}%`;
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
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "16px" }}>
        <div>
          <p style={{ color: "#8E8E93", fontSize: "0.72rem", fontWeight: 600, letterSpacing: "0.15em", textTransform: "uppercase", margin: "0 0 8px 0" }}>
            {goal.year} Campaign
          </p>
          <p style={{ color: "#F2F2F7", fontSize: "2.2rem", fontWeight: 300, letterSpacing: "0.02em", lineHeight: 1, margin: 0, fontFamily: "var(--font-cormorant), Georgia, serif" }}>
            Annual Goal
          </p>
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: "6px" }}>
          <span style={{ color: "#FFFFFF", fontSize: "4rem", fontWeight: 200, letterSpacing: "-0.05em", lineHeight: 0.8 }}>
            {triggered ? <AnimatedNumber value={goal.count} duration={1200} /> : 0}
          </span>
          <span style={{ color: "#636366", fontSize: "1.2rem", fontWeight: 500 }}>/ {goal.goal}</span>
        </div>
      </div>
      <div style={{ position: "relative", width: "100%", height: "4px", background: "rgba(255,255,255,0.06)", borderRadius: "4px" }}>
        <div ref={fillRef} style={{
          position: "absolute", top: 0, left: 0, width: "0%", height: "100%",
          background: "linear-gradient(90deg, #D4AF37, #FDE08B)",
          borderRadius: "4px",
          boxShadow: "0 0 12px rgba(253,224,139,0.4)",
        }} />
        <div ref={dotRef} style={{
          position: "absolute", top: "50%", left: "0%",
          transform: "translate(-50%, -50%)",
          width: "10px", height: "10px",
          background: "#FFFFFF", borderRadius: "50%",
          boxShadow: "0 0 8px rgba(255,255,255,0.8)",
        }} />
      </div>
      <p style={{ color: "#5a6b7c", fontSize: "0.7rem", marginTop: "10px", textAlign: "right", letterSpacing: "1px" }}>
        {pct.toFixed(1)}% complete
      </p>
    </div>
  );
}
