"use client";

import { useState, useTransition } from "react";
import { fetchWeek, type WeekActivity } from "@/lib/api";
import WeekFilmList from "@/components/WeekFilmList";

interface Props {
  initialWeek: WeekActivity;
}

function formatDateRange(start: string, end: string): string {
  if (!start || !end) return "No Activity";
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const s = new Date(start + "T00:00:00");
  const e = new Date(end + "T00:00:00");
  const sm = months[s.getMonth()];
  const em = months[e.getMonth()];
  if (sm === em) {
    return `${sm} ${s.getDate()} — ${e.getDate()}`;
  }
  return `${sm} ${s.getDate()} — ${em} ${e.getDate()}`;
}

function getChipLabel(offset: number, baseStart: string): string {
  const base = baseStart ? new Date(baseStart + "T00:00:00") : null;
  let s: Date;
  if (base && !isNaN(base.getTime())) {
    s = new Date(base);
    s.setDate(base.getDate() - offset * 7);
  } else {
    const today = new Date();
    const dow = today.getDay() === 0 ? 6 : today.getDay() - 1;
    s = new Date(today);
    s.setDate(today.getDate() - dow - offset * 7);
  }
  const e = new Date(s);
  e.setDate(s.getDate() + 6);
  return formatDateRange(
    s.toISOString().slice(0, 10),
    e.toISOString().slice(0, 10)
  );
}

export default function WeekSection({ initialWeek }: Props) {
  const [selected, setSelected] = useState(0);
  const [week, setWeek] = useState(initialWeek);
  const [isPending, startTransition] = useTransition();

  const currentStart = initialWeek.start_date;

  function handleSelect(offset: number) {
    if (offset === selected) return;
    setSelected(offset);
    startTransition(async () => {
      try {
        const data = await fetchWeek(offset);
        setWeek(data);
      } catch {
        // keep current data on error
      }
    });
  }

  const stripZero = (d: string) => d.replace(/ 0(\d)$/, " $1");
  const title = week.start_date && week.end_date
    ? `${stripZero(week.start_date)} — ${stripZero(week.end_date)}`
    : "No Activity";

  return (
    <div style={{ display: "flex", flexDirection: "column", minHeight: "360px" }}>

      {/* Header: pulse dot + "RECORDING" label */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        marginBottom: "20px", flexWrap: "wrap", gap: "8px",
      }}>
        <p style={{
          fontFamily: "var(--font-headline)",
          fontSize: "11px", fontWeight: 400,
          letterSpacing: "0.15em", textTransform: "uppercase",
          color: "var(--color-muted-text)", margin: 0,
        }}>
          <span className="pulse-dot" />Recording
        </p>

        {/* Week nav — flat buttons, 2px radius */}
        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
          {[0, 1, 2, 3].map((offset) => (
            <button
              key={offset}
              onClick={() => handleSelect(offset)}
              style={{
                background: "none",
                border: `1px solid ${selected === offset ? "var(--color-film-gold)" : "var(--color-border-whisper)"}`,
                color: selected === offset ? "var(--color-film-gold)" : "var(--color-muted-text)",
                borderRadius: "2px",
                padding: "4px 10px",
                fontSize: "11px",
                fontFamily: "var(--font-headline)",
                fontWeight: 400,
                letterSpacing: "0.08em",
                cursor: "pointer",
                transition: "border-color 0.15s, color 0.15s",
                whiteSpace: "nowrap",
              }}
            >
              {offset === 0 ? "This week" : getChipLabel(offset, currentStart)}
            </button>
          ))}
        </div>
      </div>

      {/* Date range — Playfair Display */}
      <h3 style={{
        fontFamily: "var(--font-display)",
        fontSize: "32px",
        fontWeight: 400,
        letterSpacing: "-0.02em",
        lineHeight: 1.05,
        color: "var(--color-primary-text)",
        margin: "0 0 8px 0",
        opacity: isPending ? 0.35 : 1,
        transition: "opacity 0.2s",
      }}>
        {title}
      </h3>

      {/* Single metadata line */}
      <p style={{
        fontFamily: "var(--font-body)",
        fontSize: "12px",
        fontWeight: 400,
        color: "var(--color-muted-text)",
        letterSpacing: "0.03em",
        margin: "0 0 24px 0",
        opacity: isPending ? 0.35 : 1,
        transition: "opacity 0.2s",
      }}>
        {week.count} {week.count === 1 ? "film" : "films"}
        {week.avg_rating > 0 && ` · ${week.avg_rating.toFixed(2)} avg`}
        {week.runtime_mins > 0 && ` · ${week.runtime_mins.toLocaleString()} min`}
      </p>

      {/* Film list */}
      <div style={{ opacity: isPending ? 0.35 : 1, transition: "opacity 0.2s", flex: 1 }}>
        <WeekFilmList movies={week.movies} />
      </div>
    </div>
  );
}
