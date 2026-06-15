import sqlite3
import os

DB_PATH = "/home/claude/christmas_boxoffice/christmas_boxoffice.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ─────────────────────────────────────────────
# TABLE 1: annual_totals
# Total Christmas Day gross by year
# ─────────────────────────────────────────────
c.execute("""
CREATE TABLE annual_totals (
    year            INTEGER PRIMARY KEY,
    total_gross_mil REAL,       -- Total domestic gross on Dec 25 in millions
    pct_change      REAL,       -- % change vs prior year
    releases        INTEGER,    -- Number of releases playing on that day
    top_film        TEXT,       -- #1 film that day
    top_film_gross  REAL,       -- #1 film gross on Dec 25 in millions
    day_of_week     TEXT,       -- Day of week Christmas fell on
    era             TEXT,       -- 'Pre-franchise' | 'LOTR Era' | 'Growth' | 'Star Wars' | 'COVID' | 'Recovery'
    bryce_carmike   INTEGER,    -- 1 if during Bryce's Carmike employment (Aug 2008–Dec 2013)
    data_quality    TEXT,       -- 'confirmed' | 'estimated'
    source_note     TEXT
)
""")

totals = [
    # year, total, pct, releases, top_film, top_gross, dow, era, carmike, quality, source
    (2000, 38.5,  None, 38, 'How the Grinch Stole Christmas',       8.2,  'Monday',    'Pre-franchise', 0, 'estimated', 'Est from individual film grosses; BOM calendar data'),
    (2001, 41.2,  +7.0, 40, 'Lord of the Rings: Fellowship of the Ring', 11.6, 'Tuesday', 'LOTR Era',  0, 'confirmed', 'Box Office Mojo Christmas Day 2001'),
    (2002, 46.3, +12.4, 42, 'Lord of the Rings: The Two Towers',   12.4,  'Wednesday', 'LOTR Era',  0, 'confirmed', 'Box Office Mojo Christmas Day 2002'),
    (2003, 58.1, +25.5, 44, 'Lord of the Rings: Return of the King',14.0, 'Thursday',  'LOTR Era',  0, 'confirmed', 'Box Office Mojo Christmas Day 2003'),
    (2004, 52.4,  -9.8, 43, 'Meet the Fockers',                    12.0,  'Saturday',  'Growth',    0, 'confirmed', 'Box Office Mojo Christmas Day 2004'),
    (2005, 55.8,  +6.5, 44, 'Fun with Dick and Jane',               9.8,  'Sunday',    'Growth',    0, 'confirmed', 'Box Office Mojo Christmas Day 2005'),
    (2006, 58.6,  +5.0, 45, 'Night at the Museum',                  9.1,  'Monday',    'Growth',    0, 'confirmed', 'Box Office Mojo Christmas Day 2006'),
    (2007, 64.4,  +9.9, 45, 'National Treasure: Book of Secrets',  13.7,  'Tuesday',   'Growth',    0, 'confirmed', 'Box Office Mojo Christmas Day 2007'),
    (2008, 75.1, +16.7, 52, 'Marley & Me',                         14.4,  'Thursday',  'Growth',    1, 'confirmed', 'Box Office Mojo Christmas Day 2008 — Bryce at Carmike Snellville'),
    (2009, 86.6, +15.3, 46, 'Sherlock Holmes',                     24.9,  'Friday',    'Growth',    1, 'confirmed', 'Box Office Mojo Christmas Day 2009; Variety Dec 27 2009'),
    (2010, 58.7, -32.2, 46, 'Little Fockers',                      14.6,  'Saturday',  'Growth',    1, 'confirmed', 'Box Office Mojo Christmas Day 2010'),
    (2011, 61.0,  +3.9, 45, 'Mission: Impossible Ghost Protocol',  13.7,  'Sunday',    'Growth',    1, 'confirmed', 'Box Office Mojo Christmas Day 2011'),
    (2012, 74.9, +22.8, 49, 'Les Misérables',                      18.1,  'Tuesday',   'Growth',    1, 'confirmed', 'Box Office Mojo Christmas Day 2012'),
    (2013, 77.2,  +3.1, 45, 'The Hobbit: Desolation of Smaug',     9.3,  'Wednesday', 'Growth',    1, 'confirmed', 'Box Office Mojo Christmas Day 2013 — last year of Bryce at Carmike'),
    (2014, 81.3,  +5.3, 49, 'Unbroken',                            15.4,  'Thursday',  'Growth',    0, 'confirmed', 'Box Office Mojo Christmas Day 2014'),
    (2015,103.1, +26.9, 46, 'Star Wars: The Force Awakens',        49.3,  'Friday',    'Star Wars', 0, 'confirmed', 'Box Office Mojo — all-time Christmas Day record; first to break $100M'),
    (2016, 83.1, -19.4, 49, 'Rogue One: A Star Wars Story',        25.9,  'Sunday',    'Star Wars', 0, 'confirmed', 'Box Office Mojo Christmas Day 2016'),
    (2017, 81.5,  -1.9, 59, 'Star Wars: The Last Jedi',            27.5,  'Monday',    'Star Wars', 0, 'confirmed', 'Box Office Mojo Christmas Day 2017'),
    (2018, 78.5,  -3.7, 53, 'Aquaman',                             22.0,  'Tuesday',   'Growth',    0, 'confirmed', 'Box Office Mojo Christmas Day 2018'),
    (2019, 78.6,  +0.1, 54, 'Star Wars: Rise of Skywalker',        32.2,  'Wednesday', 'Star Wars', 0, 'confirmed', 'Box Office Mojo Christmas Day 2019'),
    (2020, 10.2, -87.0, 27, 'Wonder Woman 1984',                    7.5,  'Friday',    'COVID',     0, 'confirmed', 'Box Office Mojo Christmas Day 2020 — COVID pandemic'),
    (2021, 58.1,+469.0, 26, 'Spider-Man: No Way Home',             31.6,  'Saturday',  'Recovery',  0, 'confirmed', 'Box Office Mojo Christmas Day 2021'),
    (2022, 43.8, -24.6, 28, 'Avatar: The Way of Water',            29.2,  'Sunday',    'Recovery',  0, 'confirmed', 'Box Office Mojo Christmas Day 2022'),
    (2023, 63.2, +44.3, 44, 'The Color Purple',                    18.2,  'Monday',    'Recovery',  0, 'confirmed', 'Box Office Mojo Christmas Day 2023'),
    (2024, 60.9,  -3.6, 39, "Mufasa: The Lion King",               14.7,  "Wednesday", "Recovery",  0, "confirmed", "Box Office Mojo / Deadline Dec 26 2024"),
]

c.executemany("""
INSERT INTO annual_totals
    (year, total_gross_mil, pct_change, releases, top_film, top_film_gross,
     day_of_week, era, bryce_carmike, data_quality, source_note)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", totals)

# ─────────────────────────────────────────────
# TABLE 2: notable_films
# Individual film performances on Dec 25
# ─────────────────────────────────────────────
c.execute("""
CREATE TABLE notable_films (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    year            INTEGER NOT NULL,
    film            TEXT NOT NULL,
    studio          TEXT,
    christmas_gross REAL,       -- Dec 25 gross in millions
    total_gross     REAL,       -- Final domestic total in millions
    genre           TEXT,
    is_number_one   INTEGER,    -- 1 if #1 on Christmas Day
    notes           TEXT
)
""")

films = [
    # 2001
    (2001, 'Lord of the Rings: Fellowship of the Ring', 'New Line', 11.6, 313.4, 'Fantasy',   1, 'First LOTR Christmas — began the holiday tradition for the trilogy'),
    (2001, 'Ali',                                        'Sony',    10.2,  58.2, 'Drama',     0, 'Will Smith biopic; previous Christmas Day record holder at $10.2M'),
    # 2002
    (2002, 'Lord of the Rings: The Two Towers',          'New Line', 12.4, 339.8, 'Fantasy',  1, 'LOTR dominates second consecutive Christmas'),
    (2002, 'Catch Me If You Can',                        'DreamWorks',9.9, 164.6, 'Drama',    0, 'Spielberg/DiCaprio Christmas Day opener'),
    # 2003
    (2003, 'Lord of the Rings: Return of the King',      'New Line', 14.0, 377.0, 'Fantasy',  1, 'Third LOTR Christmas — won Best Picture; previous single-film Christmas record'),
    (2003, 'Cheaper by the Dozen',                       'Fox',       7.8, 138.6, 'Comedy',   0, 'Steve Martin family comedy'),
    # 2008 — THE LINEUP
    (2008, 'Marley & Me',                                'Fox',      14.4, 143.2, 'Drama',    1, 'Set new Christmas Day record at time ($14.75M); Jennifer Aniston/Owen Wilson'),
    (2008, 'The Curious Case of Benjamin Button',        'Paramount',11.3, 127.5, 'Drama',    0, 'Brad Pitt; wide release Christmas Day'),
    (2008, 'Bedtime Stories',                            'Disney',   11.0, 110.1, 'Comedy',   0, 'Adam Sandler family comedy; opened same day'),
    (2008, 'Valkyrie',                                   'UA',        9.4, 83.1,  'Drama',    0, 'Tom Cruise WWII thriller — the film Bryce forgot'),
    # 2009
    (2009, 'Sherlock Holmes',                            'Warner',   24.9, 209.0, 'Action',   1, 'Set new Christmas Day single-film record; Robert Downey Jr.'),
    (2009, 'Avatar',                                     'Fox',      23.5, 760.5, 'SciFi',    0, 'Already in theaters; Christmas Day was its 11th day; $617M global at that point'),
    (2009, 'Alvin and the Chipmunks: Squeakquel',        'Fox',      15.9, 219.6, 'Family',   0, 'Strong family performer Christmas 2009'),
    (2009, 'Up in the Air',                              'Paramount', 6.4, 83.8,  'Drama',    0, 'George Clooney; limited to wide Christmas Day'),
    # 2015
    (2015, 'Star Wars: The Force Awakens',               'Disney',   49.3, 936.7, 'SciFi',    1, 'All-time Christmas Day single-film record; 10th day of release'),
    (2015, "Daddy's Home",                               'Paramount',15.7, 150.4, 'Comedy',   0, 'Will Ferrell/Mark Wahlberg; strong Christmas opener'),
    (2015, 'Joy',                                        'Fox',      13.5, 56.5,  'Drama',    0, 'Jennifer Lawrence/David O. Russell'),
    # 2021
    (2021, 'Spider-Man: No Way Home',                    'Sony',     31.6, 804.8, 'Action',   1, 'All-time #2 Christmas Day single-film gross; 11th day of release'),
    # 2022
    (2022, 'Avatar: The Way of Water',                   'Disney',   29.2, 684.1, 'SciFi',    1, 'James Cameron sequel; 11th day of release'),
    # 2023
    (2023, 'The Color Purple',                           'Warner',   18.2, 67.4,  'Drama',    1, 'Musical remake; Christmas Day opener'),
    # 2024
    (2024, 'Mufasa: The Lion King',                      'Disney',   14.7, 220.0, 'Family',   1, 'Lion King prequel; Christmas Day opener'),
    (2024, 'Sonic the Hedgehog 3',                       'Paramount',13.2, 201.0, 'Family',   0, 'Strong Christmas Day performer 2024'),
]

c.executemany("""
INSERT INTO notable_films
    (year, film, studio, christmas_gross, total_gross, genre, is_number_one, notes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", films)

# ─────────────────────────────────────────────
# TABLE 3: era_summary
# Aggregated by era for quick comparison
# ─────────────────────────────────────────────
c.execute("""
CREATE TABLE era_summary (
    era             TEXT PRIMARY KEY,
    start_year      INTEGER,
    end_year        INTEGER,
    avg_total_gross REAL,
    max_total_gross REAL,
    min_total_gross REAL,
    notes           TEXT
)
""")

eras = [
    ('Pre-franchise', 2000, 2000, 38.5, 38.5, 38.5, 'Pre-LOTR baseline'),
    ('LOTR Era',      2001, 2003, 48.5, 58.1, 41.2, 'Fellowship, Two Towers, Return of the King anchor three consecutive Christmases'),
    ('Growth',        2004, 2014, 66.3, 86.6, 52.4, 'Steady growth in Christmas Day box office; no single franchise dominates'),
    ('Star Wars',     2015, 2019, 89.3,103.1, 78.5, 'Disney Star Wars era — Force Awakens, Rogue One, Last Jedi, Rise of Skywalker all anchor Christmas'),
    ('COVID',         2020, 2020, 10.2, 10.2, 10.2, 'Pandemic devastates Christmas box office; Wonder Woman 1984 day-and-date on HBO Max'),
    ('Recovery',      2021, 2024, 56.5, 63.2, 43.8, 'Post-COVID recovery; Spider-Man No Way Home and Avatar: Way of Water lead strong returns'),
]

c.executemany("""
INSERT INTO era_summary
    (era, start_year, end_year, avg_total_gross, max_total_gross, min_total_gross, notes)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", eras)

conn.commit()
conn.close()
print("✅ Christmas Box Office database built:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
for table in ['annual_totals', 'notable_films', 'era_summary']:
    count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {count} rows")
conn.close()
