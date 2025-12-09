import React, { useState } from "react";
import useEmissions from "../hooks/useEmissions";
import KPICards from "../components/KPICards";
import TimeSeriesChart from "../components/TimeSeriesChart";
import ChatPanel from "../components/ChatPanel";

export default function DashboardPage() {
  const [filters, setFilters] = useState({
    startYear: 2015,
    endYear: 2025,
  });

  const { time_series, loading, error } = useEmissions(filters);

  return (
    <div className="app-container">
      {/* LEFT SIDEBAR */}
      <aside className="sidebar">
        <h3>Filters</h3>

        <div className="filter-group">
          <label>Start Year</label>
          <input
            type="number"
            value={filters.startYear}
            onChange={(e) =>
              setFilters((prev) => ({ ...prev, startYear: Number(e.target.value) }))
            }
          />
        </div>

        <div className="filter-group">
          <label>End Year</label>
          <input
            type="number"
            value={filters.endYear}
            onChange={(e) =>
              setFilters((prev) => ({ ...prev, endYear: Number(e.target.value) }))
            }
          />
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-column">
        <h1>Emissions Dashboard</h1>

        <KPICards timeSeries={time_series} />

        {loading ? (
          <div>Loading...</div>
        ) : (
          <TimeSeriesChart timeSeries={time_series} />
        )}

        {error && <div style={{ color: "red" }}>Error: {error}</div>}
      </main>

      {/* RIGHT COLUMN */}
      <aside className="right-column">
        <div className="chat-container-wrapper" style={{ display: "flex", flexDirection: "column", height: "100%" }}>
          <ChatPanel filters={filters} />
        </div>
      </aside>
    </div>
  );
}
