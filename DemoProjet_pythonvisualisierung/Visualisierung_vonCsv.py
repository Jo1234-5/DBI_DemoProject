import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

# Data preparation
df = pd.read_csv('verkehrsunfaelle_oesterreich.csv', parse_dates=['datum'], dayfirst=True)
df['uhrzeit'] = pd.to_datetime(df['uhrzeit'], format='%H:%M', errors='coerce').dt.time
df['wochentag'] = df['datum'].dt.day_name()
df['monat'] = df['datum'].dt.month_name()
df['stunde'] = pd.to_datetime(df['uhrzeit'].astype(str), format='%H:%M:%S', errors='coerce').dt.hour
df['jahr'] = df['datum'].dt.year

# Create season column
season_map = {
    'December': 'Winter', 'January': 'Winter', 'February': 'Winter',
    'March': 'Frühling', 'April': 'Frühling', 'May': 'Frühling',
    'June': 'Sommer', 'July': 'Sommer', 'August': 'Sommer',
    'September': 'Herbst', 'October': 'Herbst', 'November': 'Herbst'
}
df['saison'] = df['monat'].map(season_map)

# Set visual style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

# ================= KORRIGIERTE DIAGRAMME ================= #

# 1. Weekly accident distribution (korrigiert)
plt.figure(figsize=(12,6))
sns.countplot(x='wochentag', data=df, order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
              hue='wochentag', palette='coolwarm', legend=False)
plt.title('Unfälle pro Wochentag', fontsize=16)
plt.xlabel('Wochentag', fontsize=12)
plt.ylabel('Anzahl der Unfälle', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Monthly accident pattern (korrigiert)
month_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]
plt.figure(figsize=(12,6))
sns.countplot(x='monat', data=df, order=month_order,
              hue='monat', palette='viridis', legend=False)
plt.title('Unfälle pro Monat', fontsize=16)
plt.xlabel('Monat', fontsize=12)
plt.ylabel('Anzahl der Unfälle', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Hourly accident distribution (korrigiert)
plt.figure(figsize=(12,6))
sns.histplot(df['stunde'].dropna(), bins=24, kde=True, color='royalblue')
plt.title('Unfälle nach Tageszeit', fontsize=16)
plt.xlabel('Stunde des Tages', fontsize=12)
plt.ylabel('Anzahl der Unfälle', fontsize=12)
plt.xticks(range(0,24))
plt.tight_layout()
plt.show()

# 4. Injury severity distribution (korrigiert)
plt.figure(figsize=(12,6))
sns.boxplot(x=df['verletzte'], hue=df['verletzte'], palette='magma', legend=False)
plt.title('Verletztenverteilung pro Unfall', fontsize=16)
plt.xlabel('Anzahl der Verletzten', fontsize=12)
plt.tight_layout()
plt.show()

# 5. Weather condition analysis (korrigiert)
plt.figure(figsize=(12,6))
weather_order = df['wetter'].value_counts().index
sns.countplot(x='wetter', data=df, palette='coolwarm', order=weather_order)
plt.title('Unfälle nach Wetterbedingungen', fontsize=16)
plt.xlabel('Wetterbedingungen', fontsize=12)
plt.ylabel('Anzahl der Unfälle', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. Top accident locations (korrigiert)
plt.figure(figsize=(12,6))
top_locations = df['ort'].value_counts().head(10)
sns.barplot(x=top_locations.values, y=top_locations.index, palette='rocket_r')
plt.title('Top 10 Unfallorte', fontsize=16)
plt.xlabel('Anzahl der Unfälle', fontsize=12)
plt.ylabel('Ort', fontsize=12)
plt.tight_layout()
plt.show()

# 7. Fatal accidents analysis (korrigiert)
plt.figure(figsize=(12,6))
sns.countplot(x='monat', data=df[df['todesfaelle'] > 0], order=month_order,
              hue='monat', palette='Reds', legend=False)
plt.title('Tödliche Unfälle nach Monat', fontsize=16)
plt.xlabel('Monat', fontsize=12)
plt.ylabel('Anzahl der tödlichen Unfälle', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 8. Vienna-specific analysis (korrigiert)
if df['ort'].str.contains('Wien').any():
    plt.figure(figsize=(12,6))
    sns.countplot(x='wochentag', data=df[df['ort'].str.contains('Wien')],
                  order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                  hue='wochentag', palette='coolwarm', legend=False)
    plt.title('Wiener Unfälle nach Wochentag', fontsize=16)
    plt.xlabel('Wochentag', fontsize=12)
    plt.ylabel('Anzahl der Unfälle', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 9. Injury-fatality comparison (korrigiert)
plt.figure(figsize=(14,6))
df.groupby('monat')[['verletzte','todesfaelle']].sum().loc[month_order].plot(kind='bar')
plt.title('Verletzte vs. Todesfälle nach Monat', fontsize=16)
plt.xlabel('Monat', fontsize=12)
plt.ylabel('Anzahl', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Art')
plt.tight_layout()
plt.show()

# 10. Correlation analysis (korrigiert)
plt.figure(figsize=(10,6))
corr_matrix = df[['verletzte','todesfaelle','latitude','longitude','stunde']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
plt.title('Korrelationsmatrix', fontsize=16)
plt.tight_layout()
plt.show()

# 11. Seasonal accident distribution (korrigiert)
plt.figure(figsize=(12,6))
sns.countplot(x='saison', data=df, order=['Winter','Frühling','Sommer','Herbst'],
              hue='saison', palette='pastel', legend=False)
plt.title('Unfälle nach Jahreszeiten', fontsize=16)
plt.xlabel('Jahreszeit', fontsize=12)
plt.ylabel('Anzahl der Unfälle', fontsize=12)
plt.tight_layout()
plt.show()

# 12. Fatal vs non-fatal accidents (korrigiert)
plt.figure(figsize=(8,6))
df['tödlich'] = df['todesfaelle'] > 0
sns.countplot(x='tödlich', data=df, palette=['#2ecc71','#e74c3c'])
plt.title('Tödliche vs. nicht-tödliche Unfälle', fontsize=16)
plt.xlabel('Tödlicher Unfall', fontsize=12)
plt.ylabel('Anzahl', fontsize=12)
plt.xticks([0,1], ['Nein', 'Ja'])
plt.tight_layout()
plt.show()

# 13. Injury severity by weather (korrigiert)
plt.figure(figsize=(12,6))
sns.boxplot(x='wetter', y='verletzte', data=df, palette='Set2', showfliers=False)
plt.title('Verletzungsschwere nach Wetter', fontsize=16)
plt.xlabel('Wetterbedingungen', fontsize=12)
plt.ylabel('Anzahl der Verletzten', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 14. Accident time distribution (korrigiert)
plt.figure(figsize=(12,6))
sns.kdeplot(df['stunde'].dropna(), fill=True, color='purple')
plt.title('Unfallzeitenverteilung', fontsize=16)
plt.xlabel('Stunde des Tages', fontsize=12)
plt.ylabel('Dichte', fontsize=12)
plt.xticks(range(0,24))
plt.tight_layout()
plt.show()

# 15. Geospatial heatmap (korrigiert)
plt.figure(figsize=(12,8))
sns.kdeplot(x=df['longitude'], y=df['latitude'], fill=True, cmap='Reds', alpha=0.6)
plt.title('Geografische Unfallverteilung', fontsize=16)
plt.xlabel('Längengrad', fontsize=12)
plt.ylabel('Breitengrad', fontsize=12)
plt.tight_layout()
plt.show()

# 16. Coordinates scatter plot (korrigiert)
plt.figure(figsize=(12,8))
sns.scatterplot(x='longitude', y='latitude', size='verletzte', hue='todesfaelle',
                data=df, palette='viridis', sizes=(20, 200))
plt.title('Unfallorte mit Schweregrad', fontsize=16)
plt.xlabel('Längengrad', fontsize=12)
plt.ylabel('Breitengrad', fontsize=12)
plt.tight_layout()
plt.show()

# 17. Fatal accidents by hour (korrigiert)
plt.figure(figsize=(12,6))
sns.countplot(x='stunde', data=df[df['todesfaelle'] > 0],
              hue='stunde', palette='coolwarm', legend=False)
plt.title('Tödliche Unfälle nach Uhrzeit', fontsize=16)
plt.xlabel('Stunde des Tages', fontsize=12)
plt.ylabel('Anzahl der tödlichen Unfälle', fontsize=12)
plt.tight_layout()
plt.show()

# 18. Weather impact analysis (korrigiert)
plt.figure(figsize=(12,6))
sns.violinplot(x='wetter', y='verletzte', data=df, palette='Set3')
plt.title('Wettereinfluss auf Verletzungsschwere', fontsize=16)
plt.xlabel('Wetterbedingungen', fontsize=12)
plt.ylabel('Anzahl der Verletzten', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 19. Monthly injury trends (korrigiert)
plt.figure(figsize=(12,6))
df.groupby('monat')['verletzte'].sum().loc[month_order].plot(kind='line', marker='o', color='green')
plt.title('Monatliche Verletzungstrends', fontsize=16)
plt.xlabel('Monat', fontsize=12)
plt.ylabel('Anzahl der Verletzten', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# 20. Time-weather combination heatmap (korrigiert)
plt.figure(figsize=(14,8))
weather_hour = pd.crosstab(df['stunde'], df['wetter'])
sns.heatmap(weather_hour, cmap='YlGnBu', cbar_kws={'label': 'Anzahl der Unfälle'}, fmt='d')
plt.title('Unfallhäufigkeit nach Uhrzeit und Wetter', fontsize=16)
plt.xlabel('Wetter', fontsize=12)
plt.ylabel('Stunde des Tages', fontsize=12)
plt.tight_layout()
plt.show()