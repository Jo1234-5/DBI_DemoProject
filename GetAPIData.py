import psycopg2
import csv
from psycopg2 import sql
from sqlalchemy import create_engine
from Visualisierung import engine
from config import DB_CONFIG


def get_db_connection():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}"
        )
        print("Erfolgreich mit Docker PostgreSQL verbunden")
        return engine
    except Exception as e:
        print(f"Verbindungsfehler: {e}")
        raise


def create_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
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
            """)
        conn.commit()
    except Exception as e:
        print(f"Fehler bei Tabellenerstellung: {e}")
        raise


def import_from_csv(conn, csv_file):
    try:
        with conn.cursor() as cur, open(csv_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig für BOM
            # Erste 5 Zeilen zur Diagnose anzeigen
            head = [next(f) for _ in range(5)]
            print("CSV-Header und erste Datenzeilen:")
            print(''.join(head))
            f.seek(0)

            # Trennzeichen automatisch erkennen
            dialect = csv.Sniffer().sniff(head[0])
            reader = csv.DictReader(f, dialect=dialect)

            # Spaltennamen normalisieren (Kleinschreibung, Trimmen)
            reader.fieldnames = [fname.strip().lower() for fname in reader.fieldnames]
            print("Erkannte Spalten:", reader.fieldnames)

            required = {'id', 'datum', 'uhrzeit', 'ort', 'latitude',
                        'longitude', 'verletzte', 'todesfaelle', 'wetter'}

            if not required.issubset(reader.fieldnames):
                missing = required - set(reader.fieldnames)
                raise ValueError(
                    f"Fehlende Spalten: {missing}\n"
                    f"Vorhandene Spalten: {reader.fieldnames}\n"
                    f"Erste Datenzeile: {next(reader)}"
                )

            # Zurücksetzen für den eigentlichen Import
            f.seek(0)
            next(reader)  # Header überspringen

            for row in reader:
                try:
                    cur.execute("""
                    INSERT INTO unfaelle VALUES (
                        %(id)s, %(datum)s, %(uhrzeit)s, %(ort)s, 
                        %(latitude)s, %(longitude)s, %(verletzte)s, 
                        %(todesfaelle)s, %(wetter)s
                    ) ON CONFLICT (id) DO NOTHING;
                    """, {
                        'id': int(row['id']),
                        'datum': row['datum'],
                        'uhrzeit': row['uhrzeit'],
                        'ort': row['ort'],
                        'latitude': float(row['latitude']),
                        'longitude': float(row['longitude']),
                        'verletzte': int(row['verletzte']),
                        'todesfaelle': int(row['todesfaelle']),
                        'wetter': row['wetter']
                    })
                except Exception as e:
                    print(f"Fehler in Zeile {reader.line_num}: {e}")
                    continue

            conn.commit()
            print(f"Erfolgreich importiert: {reader.line_num - 1} Zeilen")

    except Exception as e:
        conn.rollback()
        print(f"Importfehler: {str(e)}")
        raise

def main():
    conn = None
    try:
        conn = get_db_connection()
        create_table(conn)
        import_from_csv(conn, 'verkehrsunfaelle_oesterreich.csv')
    except Exception as e:
        print(f"Programmfehler: {e}")
    finally:
        if conn:
            conn.close()
        engine.close()

if __name__ == "__main__":
    main()