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

  const title = formatDateRange(week.start_date, week.end_date);

  return (
    <div className="glass-card card-hover" style={{
      padding: "24px",
      display: "flex", flexDirection: "column", minHeight: "360px",
    }}>
      {/* Header: pulse dot + chips */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px", flexWrap: "wrap", gap: "8px" }}>
        <p style={{ color: "#a0b0c0", fontSize: "0.75rem", fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", margin: 0 }}>
          <span className="pulse-dot" />Recording
        </p>
        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
          {[0, 1, 2, 3].map((offset) => (
            <button
              key={offset}
              onClick={() => handleSelect(offset)}
              style={{
                background: selected === offset ? "rgba(197,160,89,0.15)" : "rgba(255,255,255,0.04)",
                border: `1px solid ${selected === offset ? "rgba(197,160,89,0.4)" : "rgba(255,255,255,0.08)"}`,
                color: selected === offset ? "#c5a059" : "#5a6b7c",
                borderRadius: "20px",
                padding: "3px 10px",
                fontSize: "0.65rem",
                fontWeight: selected === offset ? 700 : 400,
                letterSpacing: "0.5px",
                cursor: "pointer",
                transition: "all 0.2s",
                whiteSpace: "nowrap",
              }}
            >
              {offset === 0 ? "This week" : getChipLabel(offset, currentStart)}
            </button>
          ))}
        </div>
      </div>

      {/* Big bold date heading */}
      <h3 style={{
        color: "#F2F2F7",
        fontSize: "1.75rem",
        fontWeight: 800,
        letterSpacing: "-0.03em",
        lineHeight: 1.1,
        margin: "0 0 20px 0",
        opacity: isPending ? 0.4 : 1,
        transition: "opacity 0.2s",
        fontFamily: "var(--font-geist-sans), sans-serif",
      }}>
        {title}
      </h3>

      {/* Stats row */}
      <div style={{ display: "flex", gap: "24px", marginBottom: "20px", opacity: isPending ? 0.4 : 1, transition: "opacity 0.2s" }}>
        {[
          { label: "Films", val: week.count },
          { label: "Avg Rating", val: week.avg_rating > 0 ? week.avg_rating.toFixed(2) : "—" },
          { label: "Total Mins", val: week.runtime_mins.toLocaleString() },
        ].map((s) => (
          <div key={s.label}>
            <p style={{ color: "#5a6b7c", fontSize: "0.65rem", fontWeight: 600, letterSpacing: "1px", textTransform: "uppercase", margin: "0 0 4px 0" }}>{s.label}</p>
            <p style={{ color: "#e0e6ed", fontSize: "1.6rem", fontWeight: 700, margin: 0, lineHeight: 1 }}>{s.val}</p>
          </div>
        ))}
      </div>

      {/* Film list */}
      <div style={{ opacity: isPending ? 0.4 : 1, transition: "opacity 0.2s", flex: 1 }}>
        <WeekFilmList movies={week.movies} />
      </div>
    </div>
  );
}
