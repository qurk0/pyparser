-- Таблица дисциплин
CREATE TABLE IF NOT EXISTS ra_disc (
    id SERIAL PRIMARY KEY,
    title TEXT,
    shorttitle TEXT,
    department_id INTEGER
);

-- Таблица учебных планов
CREATE TABLE IF NOT EXISTS ra_plan (
    id SERIAL PRIMARY KEY,
    level INTEGER,
    year INTEGER
);

-- Таблица форм контроля
CREATE TABLE IF NOT EXISTS ra_control (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES ra_plan(id),
    disc_id INTEGER REFERENCES ra_disc(id),
    sem INTEGER,
    form INTEGER,
    max_grade INTEGER
);

-- Таблица версий
CREATE TABLE IF NOT EXISTS ra_version (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP,
    comment TEXT
);

-- Таблица оценок
CREATE TABLE IF NOT EXISTS ra_mark (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES ra_version(id),
    stud_id INTEGER,
    control_id INTEGER REFERENCES ra_control(id),
    grade INTEGER
);

-- Таблица результатов
CREATE TABLE IF NOT EXISTS ra_results (
    id SERIAL PRIMARY KEY,
    position INTEGER,
    stud_id INTEGER UNIQUE,
    cur_sem INTEGER,
    open_sem INTEGER,
    session_score INTEGER,
    total_score INTEGER,
    diff_score INTEGER,
    vega INTEGER,
    vm INTEGER,
    other INTEGER,
    percent REAL,
    diff_percent REAL
);