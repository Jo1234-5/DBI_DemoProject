import pandas as pd
import psycopg2

from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
query = "SELECT * FROM unfaelle"
df = pd.read_sql(query, conn)
print(df.head());
conn.close();

# Daten anzeigen
print(df.head())