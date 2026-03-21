"use client";

import { useEffect } from "react";

export default function KeepAlive() {
  useEffect(() => {
    const url = process.env.NEXT_PUBLIC_API_URL;
    if (!url) return;
    const interval = setInterval(() => {
      fetch(url + "/health").catch(() => {});
    }, 4 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  return null;
}
