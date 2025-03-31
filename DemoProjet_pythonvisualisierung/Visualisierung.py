import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_CONFIG
from datetime import datetime


def get_db_connection():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}",
            pool_pre_ping=True
        )
        Session = sessionmaker(bind=engine)
        print("Erfolgreich mit Docker PostgreSQL verbunden")
        return engine
    except Exception as e:
        print(f"Verbindungsfehler: {e}")
        raise


def main():
    engine = None
    try:
        engine = get_db_connection()
        query_all = "SELECT * FROM unfaelle"
        df_all = pd.read_sql(query_all, engine)

        # Datenaufbereitung mit expliziten Formaten
        df_all['datum'] = pd.to_datetime(df_all['datum'], format='%Y-%m-%d')  # Format explizit angeben
        df_all['uhrzeit'] = pd.to_datetime(df_all['uhrzeit'].astype(str), format='%H:%M:%S').dt.time

        # Abgeleitete Spalten
        df_all['wochentag'] = df_all['datum'].dt.day_name()
        df_all['monat'] = df_all['datum'].dt.month_name()
        df_all['stunde'] = df_all['uhrzeit'].apply(lambda x: x.hour)
        df_all['jahr'] = df_all['datum'].dt.year

        # Numerische Spalten sicher konvertieren
        df_all['verletzte'] = pd.to_numeric(df_all['verletzte'], errors='coerce').fillna(0)
        df_all['todesfaelle'] = pd.to_numeric(df_all['todesfaelle'], errors='coerce').fillna(0)

        # Gefilterte Datensätze
        df_injured = df_all[df_all['verletzte'] > 0]
        df_fatal = df_all[df_all['todesfaelle'] > 0]
        df_high_injuries = df_all[df_all['verletzte'] >= 3]
        df_wien = df_all[df_all['ort'].str.contains('Wien', case=False, na=False)]

        # Stil-Einstellungen
        sns.set_style("whitegrid")
        plt.rcParams['figure.autolayout'] = True

        #Unfallverteilung nach Wochentag (Balkendiagramm)
        plt.figure(figsize=(14, 7))
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        ax = sns.countplot(x='wochentag', data=df_all, order=weekday_order,
                           palette="coolwarm", hue='wochentag', legend=False)
        plt.title('Unfallverteilung nach Wochentag', fontsize=16)
        plt.xlabel('Wochentag', fontsize=12)
        plt.ylabel('Anzahl der Unfälle', fontsize=12)
        plt.xticks(rotation=45)

        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        xytext=(0, 5),
                        textcoords='offset points')
        plt.show()

        #Unfälle nach Monat und Jahr (Heatmap)
        plt.figure(figsize=(12, 8))
        month_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]

        heatmap_data = df_all.groupby(['jahr', 'monat']).size().unstack()
        heatmap_data = heatmap_data[month_order].fillna(0).astype(int)

        sns.heatmap(heatmap_data, cmap="YlOrRd", annot=True, fmt="d", linewidths=.5)
        plt.title('Unfälle nach Monat und Jahr', fontsize=16)
        plt.xlabel('Monat', fontsize=12)
        plt.ylabel('Jahr', fontsize=12)
        plt.show()

        #Verletzte vs. Todesfälle (Streudiagramm mit Regression)
        plt.figure(figsize=(12, 7))
        sns.regplot(x='verletzte', y='todesfaelle', data=df_all,
                    scatter_kws={'alpha': 0.4, 'color': 'blue'},
                    line_kws={'color': 'red'})
        plt.title('Zusammenhang zwischen Verletzten und Todesfällen', fontsize=16)
        plt.xlabel('Anzahl Verletzte', fontsize=12)
        plt.ylabel('Anzahl Todesfälle', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()

        #Unfallverteilung nach Uhrzeit (KDE-Plot)
        plt.figure(figsize=(12, 6))
        sns.kdeplot(data=df_all, x='stunde', fill=True, color='purple', alpha=0.3)
        plt.title('Unfallverteilung über den Tag', fontsize=16)
        plt.xlabel('Uhrzeit (Stunde)', fontsize=12)
        plt.ylabel('Dichte', fontsize=12)
        plt.xticks(range(0, 24, 2))
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()

        #3D-Plot: Unfälle nach Wochentag, Uhrzeit und Anzahl (Matplotlib)
        fig = plt.figure(figsize=(16, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Daten vorbereiten mit Integer-Werten
        grouped = df_all.groupby(['wochentag', 'stunde']).size().reset_index(name='count')
        weekday_map = {day: i for i, day in enumerate(weekday_order)}
        grouped['weekday_num'] = grouped['wochentag'].map(weekday_map)

        # Surface Plot mit Integer-Werten
        X = grouped['weekday_num'].values
        Y = grouped['stunde'].values
        Z = grouped['count'].values

        ax.plot_trisurf(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.8)

        ax.set_xlabel('Wochentag', fontsize=12, labelpad=10)
        ax.set_ylabel('Uhrzeit (Stunde)', fontsize=12, labelpad=10)
        ax.set_zlabel('Anzahl Unfälle', fontsize=12, labelpad=10)

        ax.set_xticks(list(weekday_map.values()))
        ax.set_xticklabels(list(weekday_map.keys()), rotation=45)
        ax.set_yticks(range(0, 24, 3))

        plt.title('3D-Darstellung der Unfallhäufigkeit', fontsize=16)
        plt.tight_layout()
        plt.show()

        # Unfälle pro Wochentag
        plt.figure(figsize=(12, 6))
        sns.countplot(x='wochentag', data=df_all,
                      order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                      hue='wochentag', palette='coolwarm', legend=False)
        plt.title('Unfälle pro Wochentag', fontsize=16)
        plt.xlabel('Wochentag', fontsize=12)
        plt.ylabel('Anzahl der Unfälle', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Unfälle pro Monat
        plt.figure(figsize=(12, 6))
        month_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        sns.countplot(x='monat', data=df_all, order=month_order,
                      hue='monat', palette='viridis', legend=False)
        plt.title('Unfälle pro Monat', fontsize=16)
        plt.xlabel('Monat', fontsize=12)
        plt.ylabel('Anzahl der Unfälle', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Boxplot der Verletzten
        plt.figure(figsize=(12, 6))
        sns.boxplot(x=df_all['verletzte'], hue=df_all['verletzte'],
                    palette='magma', legend=False)
        plt.title('Verteilung der Verletzten', fontsize=16)
        plt.xlabel('Anzahl der Verletzten', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Unfälle mit hohem Verletzungsgrad
        plt.figure(figsize=(12, 6))
        sns.countplot(x='wochentag', data=df_high_injuries,
                      order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                      hue='wochentag', palette='coolwarm', legend=False)
        plt.title('Unfälle mit hohem Verletzungsgrad (3+ Verletzte)', fontsize=16)
        plt.xlabel('Wochentag', fontsize=12)
        plt.ylabel('Anzahl der Unfälle', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Heatmap Wochentag vs. Uhrzeit
        plt.figure(figsize=(14, 8))
        heat_data = pd.pivot_table(df_all, values='id',
                                   index='wochentag',
                                   columns='stunde',
                                   aggfunc='count').fillna(0).astype(int)

        sns.heatmap(heat_data, annot=True, fmt="d", cmap="YlGnBu",
                    cbar_kws={'label': 'Anzahl der Unfälle'})
        plt.title('Unfälle nach Wochentag und Uhrzeit', fontsize=16)
        plt.xlabel('Stunde des Tages', fontsize=12)
        plt.ylabel('Wochentag', fontsize=12)
        plt.tight_layout()
        plt.show()

        # Verletzte pro Monat
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

        # Unfälle in Wien
        plt.figure(figsize=(12, 6))
        sns.countplot(x='wochentag', data=df_wien,
                      order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                      hue='wochentag', palette='coolwarm', legend=False)
        plt.title('Unfälle in Wien nach Wochentag', fontsize=16)
        plt.xlabel('Wochentag', fontsize=12)
        plt.ylabel('Anzahl der Unfälle', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Hohe Verletzungen nach Monat
        plt.figure(figsize=(12, 6))
        sns.countplot(x='monat', data=df_high_injuries,
                      order=month_order, palette='Blues')
        plt.title('Unfälle mit hohem Verletzungsgrad nach Monat', fontsize=16)
        plt.xlabel('Monat', fontsize=12)
        plt.ylabel('Anzahl der Unfälle', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Unfälle nach Wochentag und Wetter
        plt.figure(figsize=(14, 8))
        sns.countplot(x='wochentag', hue='wetter', data=df_all,
                      order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                      palette='coolwarm')
        plt.title('Unfälle nach Wochentag und Wetter', fontsize=16)
        plt.xlabel('Wochentag', fontsize=12)
        plt.ylabel('Anzahl der Unfälle', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Wetter', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"✗ Programmfehler: {str(e)}")
    finally:
        if engine:
            engine.dispose()
            print("✓ Datenbankverbindung geschlossen")


if __name__ == "__main__":
    main()