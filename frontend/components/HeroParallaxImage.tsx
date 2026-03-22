"use client";

import { useEffect, useRef } from "react";

export default function HeroParallaxImage() {
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const img = imgRef.current;
    if (!img) return;

    function onScroll() {
      const y = window.scrollY;
      img!.style.transform = `translateX(-65%) translateY(${y * 0.28}px)`;
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      ref={imgRef}
      src="/another.jpeg"
      alt="The Face of Another"
      className="hero-img"
    />
  );
}
