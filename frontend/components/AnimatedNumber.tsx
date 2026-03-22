"use client";

import { useEffect, useRef, useState } from "react";

interface Props {
  value: number;
  duration?: number;
  decimals?: number;
  suffix?: string;
}

export default function AnimatedNumber({ value, duration = 1400, decimals = 0, suffix }: Props) {
  const [display, setDisplay] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const started = useRef(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !started.current) {
          started.current = true;
          const start = performance.now();
          function tick(now: number) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            // ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            setDisplay(eased * value);
            if (progress < 1) requestAnimationFrame(tick);
            else setDisplay(value);
          }
          requestAnimationFrame(tick);
          observer.unobserve(el);
        }
      },
      { threshold: 0.3 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [value, duration]);

  const formatted = display.toLocaleString("en", {
    maximumFractionDigits: decimals,
    minimumFractionDigits: decimals,
  });

  return (
    <span ref={ref}>
      {formatted}
      {suffix && <span style={{ fontSize: "1rem", color: "#5a6b7c", fontWeight: 500, marginLeft: 6 }}>{suffix}</span>}
    </span>
  );
}
