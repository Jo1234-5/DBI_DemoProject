-- init.sql
CREATE TABLE IF NOT EXISTS unfaelle (
    id INTEGER PRIMARY KEY,
    datum DATE NOT NULL,
    uhrzeit TIME NOT NULL,
    ort VARCHAR(100) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    verletzte INTEGER DEFAULT 0,
    todesfaelle INTEGER DEFAULT 0,
    wetter VARCHAR(50)
);

-- Berechtigungen setzen
GRANT ALL PRIVILEGES ON TABLE unfaelle TO postgres;