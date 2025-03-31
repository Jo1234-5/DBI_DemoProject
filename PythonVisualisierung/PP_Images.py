import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Beispiel-Daten erstellen
df = pd.DataFrame({
    'Feature1': np.random.randn(5),  # Zufällige Werte für Feature 1
    'Feature2': np.random.randn(5),  # Zufällige Werte für Feature 2
    'Feature3': np.random.randn(5),  # Zufällige Werte für Feature 3
    'Feature4': np.random.randn(5)   # Zufällige Werte für Feature 4
})

# Korrelationsmatrix erstellen
# Die .corr()-Methode berechnet die Pearson-Korrelation zwischen allen Spalten im DataFrame
corr = df.corr()

# Heatmap erstellen
# sns.heatmap() visualisiert die Korrelationsmatrix als farbkodierte Heatmap
sns.heatmap(
    corr,                # Die Korrelationsmatrix, die visualisiert werden soll
    annot=True,          # Zeigt die numerischen Werte in den Zellen an
    cmap='coolwarm',     # Farbpalette: Blau (negativ) bis Rot (positiv)
    fmt='.2f',           # Formatierung der annotierten Werte auf 2 Dezimalstellen
    vmin=-1,             # Untere Grenze der Farbskala (vollständige negative Korrelation)
    vmax=1               # Obere Grenze der Farbskala (vollständige positive Korrelation)
)

# Titel hinzufügen
plt.title('Korrelationsmatrix der Beispiel-Daten', fontsize=16, pad=20)

# Heatmap anzeigen
plt.show()