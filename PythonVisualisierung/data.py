import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Stil für die Visualisierungen
sns.set(style="whitegrid")
# Anzahl der Datenpunkte
n = 100

# Generieren von Testdaten
np.random.seed(42)
data = {
    'Alter': np.random.randint(18, 65, size=n),
    'Einkommen': np.random.randint(20000, 100000, size=n),
    'Bildungsjahre': np.random.randint(10, 20, size=n),
    'Geschlecht': np.random.choice(['Männlich', 'Weiblich'], size=n),
    'Zufriedenheit': np.random.randint(1, 10, size=n)
}

# Erstellen eines DataFrames
df = pd.DataFrame(data)

# Speichern der Daten in einer CSV-Datei
df.to_csv('testdaten.csv', index=False)