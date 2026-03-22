"use client";

import { useEffect, useRef } from "react";

export default function CustomCursor() {
  const ringRef = useRef<HTMLDivElement>(null);
  const pos = useRef({ x: -100, y: -100 });
  const target = useRef({ x: -100, y: -100 });
  const raf = useRef<number>(0);

  useEffect(() => {
    const ring = ringRef.current;
    if (!ring) return;

    function onMove(e: MouseEvent) {
      target.current = { x: e.clientX, y: e.clientY };
    }

    function onEnter() { ring!.classList.add("hovering"); }
    function onLeave() { ring!.classList.remove("hovering"); }

    function loop() {
      pos.current.x += (target.current.x - pos.current.x) * 0.1;
      pos.current.y += (target.current.y - pos.current.y) * 0.1;
      const half = ring!.offsetWidth / 2;
      ring!.style.transform = `translate(${pos.current.x - half}px, ${pos.current.y - half}px)`;
      raf.current = requestAnimationFrame(loop);
    }

    document.addEventListener("mousemove", onMove);
    document.querySelectorAll("a, button").forEach((el) => {
      el.addEventListener("mouseenter", onEnter);
      el.addEventListener("mouseleave", onLeave);
    });

    raf.current = requestAnimationFrame(loop);

    return () => {
      document.removeEventListener("mousemove", onMove);
      cancelAnimationFrame(raf.current);
    };
  }, []);

  return <div ref={ringRef} className="cursor-ring" />;
}
