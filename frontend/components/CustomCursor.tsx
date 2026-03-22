"use client";

import { useEffect, useRef } from "react";

export default function CustomCursor() {
  const dotRef = useRef<HTMLDivElement>(null);
  const ringRef = useRef<HTMLDivElement>(null);
  const mouse = useRef({ x: 0, y: 0 });
  const ring = useRef({ x: 0, y: 0 });
  const raf = useRef<number>(0);

  useEffect(() => {
    const dot = dotRef.current;
    const ringEl = ringRef.current;
    if (!dot || !ringEl) return;

    function onMove(e: MouseEvent) {
      mouse.current = { x: e.clientX, y: e.clientY };
      dot!.style.left = e.clientX + "px";
      dot!.style.top = e.clientY + "px";
    }

    function onEnterLink() { ringEl!.classList.add("hovering"); }
    function onLeaveLink() { ringEl!.classList.remove("hovering"); }

    function loop() {
      ring.current.x += (mouse.current.x - ring.current.x) * 0.12;
      ring.current.y += (mouse.current.y - ring.current.y) * 0.12;
      ringEl!.style.left = ring.current.x + "px";
      ringEl!.style.top = ring.current.y + "px";
      raf.current = requestAnimationFrame(loop);
    }

    document.addEventListener("mousemove", onMove);

    const interactives = document.querySelectorAll("a, button");
    interactives.forEach((el) => {
      el.addEventListener("mouseenter", onEnterLink);
      el.addEventListener("mouseleave", onLeaveLink);
    });

    raf.current = requestAnimationFrame(loop);

    return () => {
      document.removeEventListener("mousemove", onMove);
      interactives.forEach((el) => {
        el.removeEventListener("mouseenter", onEnterLink);
        el.removeEventListener("mouseleave", onLeaveLink);
      });
      cancelAnimationFrame(raf.current);
    };
  }, []);

  return (
    <>
      <div ref={dotRef} className="cursor-dot" />
      <div ref={ringRef} className="cursor-ring" />
    </>
  );
}
