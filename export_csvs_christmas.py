import sqlite3
import csv
import os

DB_PATH = "/home/claude/christmas_boxoffice/christmas_boxoffice.db"
OUT_DIR = "/home/claude/christmas_boxoffice/csv"
os.makedirs(OUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

def write_csv(filename, rows, fieldnames):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([dict(r) for r in rows])
    print(f"  ✅ {filename}  ({len(rows)} rows)")

print("\n📁 Exporting Christmas Box Office CSVs...\n")

# ── CSV 1: Annual totals ──────────────────────────────────────
rows = c.execute("SELECT * FROM annual_totals ORDER BY year").fetchall()
write_csv("01_annual_totals.csv", rows,
    ["year","total_gross_mil","pct_change","releases","top_film",
     "top_film_gross","day_of_week","era","bryce_carmike","data_quality","source_note"])

# ── CSV 2: Notable films ──────────────────────────────────────
rows = c.execute("SELECT * FROM notable_films ORDER BY year, christmas_gross DESC").fetchall()
write_csv("02_notable_films.csv", rows,
    ["id","year","film","studio","christmas_gross","total_gross",
     "genre","is_number_one","notes"])

# ── CSV 3: Era summary ────────────────────────────────────────
rows = c.execute("SELECT * FROM era_summary ORDER BY start_year").fetchall()
write_csv("03_era_summary.csv", rows,
    ["era","start_year","end_year","avg_total_gross","max_total_gross","min_total_gross","notes"])

# ── CSV 4: Top film vs total gross comparison ─────────────────
rows = c.execute("""
    SELECT year, total_gross_mil, top_film, top_film_gross, era,
           ROUND(top_film_gross / total_gross_mil * 100, 1) AS top_film_pct_of_total,
           bryce_carmike
    FROM annual_totals
    ORDER BY year
""").fetchall()
write_csv("04_top_film_share.csv", rows,
    ["year","total_gross_mil","top_film","top_film_gross",
     "era","top_film_pct_of_total","bryce_carmike"])

# ── CSV 5: Day of week analysis ───────────────────────────────
rows = c.execute("""
    SELECT day_of_week,
           COUNT(*) as occurrences,
           ROUND(AVG(total_gross_mil),1) as avg_gross,
           MAX(total_gross_mil) as max_gross,
           MIN(total_gross_mil) as min_gross,
           GROUP_CONCAT(year, ', ') as years
    FROM annual_totals
    GROUP BY day_of_week
    ORDER BY avg_gross DESC
""").fetchall()
write_csv("05_day_of_week.csv", rows,
    ["day_of_week","occurrences","avg_gross","max_gross","min_gross","years"])

conn.close()
print("\n✅ All CSVs exported to:", OUT_DIR)
