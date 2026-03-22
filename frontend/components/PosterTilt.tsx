"use client";

import { useRef } from "react";
import type { MouseEvent } from "react";

interface Props {
  href: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}

export default function PosterTilt({ href, children, style }: Props) {
  const ref = useRef<HTMLAnchorElement>(null);

  function onMouseMove(e: MouseEvent<HTMLAnchorElement>) {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    el.style.transform = `perspective(900px) rotateY(${x * 11}deg) rotateX(${-y * 11}deg) scale3d(1.03,1.03,1.03)`;
  }

  function onMouseLeave() {
    const el = ref.current;
    if (!el) return;
    el.style.transform = "perspective(900px) rotateY(0deg) rotateX(0deg) scale3d(1,1,1)";
  }

  return (
    <a
      ref={ref}
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      onMouseMove={onMouseMove}
      onMouseLeave={onMouseLeave}
      style={{
        display: "block",
        transformStyle: "preserve-3d",
        transition: "transform 0.35s ease",
        willChange: "transform",
        ...style,
      }}
    >
      {children}
    </a>
  );
}
