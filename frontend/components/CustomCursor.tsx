"use client";

import { useEffect, useRef } from "react";

export default function CustomCursor() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    function onMove(e: MouseEvent) {
      el!.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
    }
    function onEnter() { el!.classList.add("hovering"); }
    function onLeave() { el!.classList.remove("hovering"); }

    document.addEventListener("mousemove", onMove);
    document.querySelectorAll("a, button").forEach((n) => {
      n.addEventListener("mouseenter", onEnter);
      n.addEventListener("mouseleave", onLeave);
    });

    return () => document.removeEventListener("mousemove", onMove);
  }, []);

  return <div ref={ref} className="cursor-dot" />;
}
