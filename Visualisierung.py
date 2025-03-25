import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from config import DB_CONFIG
from datetime import datetime

# Verbindung zur PostgreSQL-Datenbank
engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}"
)

# Daten abfragen und vorbereiten
query_all = "SELECT * FROM unfaelle"
df_all = pd.read_sql(query_all, engine)

# Datums- und Zeitfeatures erstellen
df_all['datum'] = pd.to_datetime(df_all['datum'])
df_all['wochentag'] = df_all['datum'].dt.day_name()
df_all['monat'] = df_all['datum'].dt.month_name()
df_all['uhrzeit'] = pd.to_datetime(df_all['uhrzeit'].astype(str)).dt.time
df_all['stunde'] = pd.to_datetime(df_all['uhrzeit'].astype(str)).dt.hour

# Spezielle Datensätze erstellen
df_injured = df_all[df_all['verletzte'] > 0]
df_fatal = df_all[df_all['todesfaelle'] > 0]
df_high_injuries = df_all[df_all['verletzte'] >= 3]
df_wien = df_all[df_all['ort'].str.contains('Wien', case=False)]

# 1. Unfälle pro Wochentag (korrigiert)
plt.figure(figsize=(12, 6))
sns.countplot(x='wochentag', data=df_all,
             order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
             hue='wochentag', palette='coolwarm', legend=False)
plt.title('Unfälle pro Wochentag', fontsize=16)
plt.xlabel('Wochentag', fontsize=12)
plt.ylabel('Anzahl der Unfälle', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 2. Unfälle pro Monat (korrigiert)
plt.figure(figsize=(12, 6))
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
sns.countplot(x='monat', data=df_all, order=month_order,
             hue='monat', palette='viridis', legend=False)
plt.title('Unfälle pro Monat', fontsize=16)
plt.xlabel('Monat', fontsize=12)
plt.ylabel('Anzahl der Unfälle', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 5. Boxplot der Verletzten (korrigiert)
plt.figure(figsize=(12, 6))
sns.boxplot(x=df_all['verletzte'], hue=df_all['verletzte'], palette='magma', legend=False)
plt.title('Verteilung der Verletzten', fontsize=16)
plt.xlabel('Anzahl der Verletzten', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 10. Unfälle mit hohem Verletzungsgrad (korrigiert)
plt.figure(figsize=(12, 6))
sns.countplot(x='wochentag', data=df_high_injuries,
             order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
             hue='wochentag', palette='coolwarm', legend=False)
plt.title('Unfälle mit hohem Verletzungsgrad (3+ Verletzte)', fontsize=16)
plt.xlabel('Wochentag', fontsize=12)
plt.ylabel('Anzahl der Unfälle', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 12. Heatmap korrigiert
plt.figure(figsize=(14, 8))
heat_data = pd.pivot_table(df_all, values='id',
                          index='wochentag',
                          columns='stunde',
                          aggfunc='count').fillna(0)

# Sicherstellen, dass die Werte ganzzahlig sind
heat_data = heat_data.astype(int)

sns.heatmap(heat_data, annot=True, fmt="d", cmap="YlGnBu",
           cbar_kws={'label': 'Anzahl der Unfälle'})
plt.title('Unfälle nach Wochentag und Uhrzeit', fontsize=16)
plt.xlabel('Stunde des Tages', fontsize=12)
plt.ylabel('Wochentag', fontsize=12)
plt.tight_layout()
plt.show()

# 15. Verletzte pro Monat (korrigiert)
plt.figure(figsize=(12, 6))
sns.boxplot(x='monat', y='verletzte', data=df_all,
           order=month_order,
           hue='monat', palette='coolwarm', legend=False)
plt.title('Verletzte pro Monat', fontsize=16)
plt.xlabel('Monat', fontsize=12)
plt.ylabel('Anzahl der Verletzten', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 16. Unfälle in Wien
plt.figure(figsize=(12, 6));
sns.countplot(x='wochentag', data=df_wien,order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],palette='coolwarm');
plt.title('Unfälle in Wien nach Wochentag', fontsize=16);
plt.xlabel('Wochentag', fontsize=12);
plt.ylabel('Anzahl der Unfälle', fontsize=12);
plt.xticks(rotation=45);
plt.grid(axis='y', linestyle='--', alpha=0.7);
plt.tight_layout();
plt.show();



# 19. Hohe Verletzungen nach Monat
plt.figure(figsize=(12, 6));
sns.countplot(x='monat', data=df_high_injuries, order=month_order, palette='Blues');
plt.title('Unfälle mit hohem Verletzungsgrad nach Monat', fontsize=16);
plt.xlabel('Monat', fontsize=12);
plt.ylabel('Anzahl der Unfälle', fontsize=12);
plt.xticks(rotation=45);
plt.grid(axis='y', linestyle='--', alpha=0.7);
plt.tight_layout();
plt.show();

# 20. Unfälle nach Wochentag und Wetter
plt.figure(figsize=(14, 8));
sns.countplot(x='wochentag', hue='wetter', data=df_all, order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],   palette='coolwarm');
plt.title('Unfälle nach Wochentag und Wetter', fontsize=16);
plt.xlabel('Wochentag', fontsize=12);
plt.ylabel('Anzahl der Unfälle', fontsize=12);
plt.xticks(rotation=45);
plt.grid(axis='y', linestyle='--', alpha=0.7);
plt.legend(title='Wetter', bbox_to_anchor=(1.05, 1), loc='upper left');
plt.tight_layout();
plt.show();

# Datenbankverbindung schließen
engine.dispose()