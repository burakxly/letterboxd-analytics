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

    const targets = Array.from(document.querySelectorAll("a, button"));

    document.addEventListener("mousemove", onMove);
    targets.forEach((n) => {
      n.addEventListener("mouseenter", onEnter);
      n.addEventListener("mouseleave", onLeave);
    });

    return () => {
      document.removeEventListener("mousemove", onMove);
      targets.forEach((n) => {
        n.removeEventListener("mouseenter", onEnter);
        n.removeEventListener("mouseleave", onLeave);
      });
    };
  }, []);

  return <div ref={ref} className="cursor-dot" />;
}
