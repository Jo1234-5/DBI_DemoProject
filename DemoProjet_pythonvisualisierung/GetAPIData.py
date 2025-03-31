import psycopg2
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_CONFIG


def get_db_connection():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}"
        )
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Erfolgreich mit Docker PostgreSQL verbunden")
        return engine, session
    except Exception as e:
        print(f"Verbindungsfehler: {e}")
        raise


def create_table(engine):
    from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date, Time

    metadata = MetaData()

    unfaelle = Table(
        'unfaelle', metadata,
        Column('id', Integer, primary_key=True),
        Column('datum', Date),
        Column('uhrzeit', Time),
        Column('ort', String(100)),
        Column('latitude', Float),
        Column('longitude', Float),
        Column('verletzte', Integer),
        Column('todesfaelle', Integer),
        Column('wetter', String(50)))

    metadata.create_all(engine);
    print("Tabelle 'unfaelle' wurde erstellt/überprüft")


def import_from_csv(engine, csv_file, unfaelle=None):
    from sqlalchemy import insert
    from sqlalchemy.orm import Session

    try:
        with Session(engine) as session, open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            # Batch-Insert für bessere Performance
            batch = []
            batch_size = 1000

            for row in reader:
                batch.append({
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

                if len(batch) >= batch_size:
                    session.execute(insert(unfaelle), batch)
                    session.commit()
                    batch = []

            if batch:  # Restliche Einträge
                session.execute(insert(unfaelle), batch)
                session.commit()

            print(f"Erfolgreich importiert: {reader.line_num - 1} Zeilen")

    except Exception as e:
        session.rollback()
        print(f"Importfehler: {str(e)}")
        raise


def main():
    engine = None
    try:
        engine, session = get_db_connection()
        create_table(engine)
        import_from_csv(engine, 'verkehrsunfaelle_oesterreich.csv')
    except Exception as e:
        print(f"Programmfehler: {e}")
    finally:
        if engine:
            engine.dispose()
        if session:
            session.close()


if __name__ == "__main__":
    main()