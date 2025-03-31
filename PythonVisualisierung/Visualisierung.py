# Import der notwendigen Bibliotheken
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Stil für die Visualisierungen
sns.set(style="whitegrid")


# Funktion 1: Generieren und Speichern von Testdaten
def generiere_testdaten(dateiname='testdaten.csv', n=100):

    np.random.seed(42)  # Für Reproduzierbarkeit
    data = {
        'Alter': np.random.randint(18, 65, size=n),
        'Einkommen': np.random.randint(20000, 100000, size=n),
        'Bildungsjahre': np.random.randint(10, 20, size=n),
        'Geschlecht': np.random.choice(['Männlich', 'Weiblich'], size=n),
        'Zufriedenheit': np.random.randint(1, 10, size=n)
    }
    df = pd.DataFrame(data)
    df.to_csv(dateiname, index=False)
    print(f"Testdaten wurden in '{dateiname}' gespeichert.")


# Funktion 2: Laden der Testdaten
def lade_testdaten(dateiname='testdaten.csv'):

    if os.path.exists(dateiname):
        df = pd.read_csv(dateiname)
        print(f"Daten aus '{dateiname}' erfolgreich geladen.")
        return df
    else:
        raise FileNotFoundError(f"Die Datei '{dateiname}' existiert nicht.")


# Funktion 3: Visualisierung 1 – Histogramm des Alters
def plot_alter_histogramm(df, speichern=False, dateiname='alter_histogramm.png'):

    plt.figure(figsize=(10, 6))
    plt.hist(df['Alter'], bins=15, color='skyblue', edgecolor='black')
    plt.title('Verteilung des Alters')
    plt.xlabel('Alter')
    plt.ylabel('Häufigkeit')
    if speichern:
        plt.savefig(dateiname)
        print(f"Histogramm wurde als '{dateiname}' gespeichert.")
    plt.show()


# Funktion 4: Visualisierung 2 – Streudiagramm von Einkommen vs. Bildungsjahre
def plot_einkommen_bildungsjahre(df, speichern=False, dateiname='einkommen_bildungsjahre.png'):

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Bildungsjahre', y='Einkommen', hue='Geschlecht', data=df, palette='viridis', s=100)
    plt.title('Einkommen vs. Bildungsjahre')
    plt.xlabel('Bildungsjahre')
    plt.ylabel('Einkommen')
    if speichern:
        plt.savefig(dateiname)
        print(f"Streudiagramm wurde als '{dateiname}' gespeichert.")
    plt.show()


# Funktion 5: Visualisierung 3 – Boxplot der Zufriedenheit nach Geschlecht
def plot_zufriedenheit_boxplot(df, speichern=False, dateiname='zufriedenheit_boxplot.png'):

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Geschlecht', y='Zufriedenheit', data=df, palette='pastel')
    plt.title('Zufriedenheit nach Geschlecht')
    plt.xlabel('Geschlecht')
    plt.ylabel('Zufriedenheit')
    if speichern:
        plt.savefig(dateiname)
        print(f"Boxplot wurde als '{dateiname}' gespeichert.")
    plt.show()


# Funktion 6: Visualisierung 4 – Korrelationsmatrix
def plot_korrelationsmatrix(df, speichern=False, dateiname='korrelationsmatrix.png'):

    plt.figure(figsize=(10, 6))
    corr = df.corr(numeric_only=True)  # Nur numerische Spalten berücksichtigen
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Korrelationsmatrix')
    if speichern:
        plt.savefig(dateiname)
        print(f"Korrelationsmatrix wurde als '{dateiname}' gespeichert.")
    plt.show()


# Funktion 7: Visualisierung 5 – Pairplot
def plot_pairplot(df, speichern=False, dateiname='pairplot.png'):

    pairplot = sns.pairplot(df, hue='Geschlecht', palette='viridis', height=2.5)
    pairplot.fig.suptitle('Pairplot der numerischen Variablen', y=1.02)
    if speichern:
        pairplot.savefig(dateiname)
        print(f"Pairplot wurde als '{dateiname}' gespeichert.")
    plt.show()


# Funktion 8: Visualisierung 6 – Violinplot der Zufriedenheit nach Geschlecht
def plot_zufriedenheit_violinplot(df, speichern=False, dateiname='zufriedenheit_violinplot.png'):

    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Geschlecht', y='Zufriedenheit', data=df, palette='pastel', inner='quartile')
    plt.title('Zufriedenheit nach Geschlecht')
    plt.xlabel('Geschlecht')
    plt.ylabel('Zufriedenheit')
    if speichern:
        plt.savefig(dateiname)
        print(f"Violinplot wurde als '{dateiname}' gespeichert.")
    plt.show()


# Hauptprogramm
if __name__ == "__main__":
    # Schritt 1: Testdaten generieren und speichern
    generiere_testdaten()

    # Schritt 2: Testdaten laden
    df = lade_testdaten()

    # Schritt 3: Visualisierungen erstellen und anzeigen
    plot_alter_histogramm(df, speichern=True)
    plot_einkommen_bildungsjahre(df, speichern=True)
    plot_zufriedenheit_boxplot(df, speichern=True)
    plot_korrelationsmatrix(df, speichern=True)
    plot_pairplot(df, speichern=True)
    plot_zufriedenheit_violinplot(df, speichern=True)

    print("Alle Visualisierungen wurden erfolgreich erstellt und gespeichert.")