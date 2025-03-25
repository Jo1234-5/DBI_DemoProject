import csv

# Header der CSV-Datei
header = ['id', 'datum', 'uhrzeit', 'ort', 'latitude', 'longitude', 'verletzte', 'todesfaelle', 'wetter']

# Testdaten für Verkehrsunfälle in Österreich
data = [
    [1, '2023-01-05', '07:45', 'Wien', 48.2082, 16.3738, 2, 0, 'Nebel'],
    [2, '2023-01-12', '08:30', 'Graz', 47.0707, 15.4395, 1, 0, 'Regen'],
    [3, '2023-01-18', '14:15', 'Linz', 48.3069, 14.2858, 3, 0, 'Bewölkt'],
    [4, '2023-01-22', '17:50', 'Salzburg', 47.8095, 13.0550, 0, 0, 'Schnee'],
    [5, '2023-01-28', '22:10', 'Innsbruck', 47.2682, 11.3923, 1, 1, 'Eisglätte'],
    [6, '2023-02-03', '09:20', 'Klagenfurt', 46.6249, 14.3050, 2, 0, 'Sonnig'],
    [7, '2023-02-09', '13:40', 'Villach', 46.6111, 13.8558, 0, 0, 'Regen'],
    [8, '2023-02-15', '18:25', 'Wels', 48.1575, 14.0289, 1, 0, 'Bewölkt'],
    [9, '2023-02-21', '06:15', 'St. Pölten', 48.2047, 15.6256, 3, 0, 'Nebel'],
    [10, '2023-02-27', '16:30', 'Dornbirn', 47.4125, 9.7416, 0, 0, 'Sonnig'],
    [11, '2023-03-05', '11:10', 'Steyr', 48.0425, 14.4211, 2, 0, 'Regen'],
    [12, '2023-03-11', '15:20', 'Feldkirch', 47.2371, 9.5969, 0, 0, 'Bewölkt'],
    [13, '2023-03-17', '21:05', 'Bregenz', 47.5031, 9.7471, 1, 0, 'Nebel'],
    [14, '2023-03-23', '07:55', 'Leonding', 48.2605, 14.2406, 0, 0, 'Frost'],
    [15, '2023-03-29', '12:40', 'Kapfenberg', 47.4444, 15.2933, 3, 0, 'Sonnig'],
    [16, '2023-04-04', '18:15', 'Baden', 48.0061, 16.2308, 1, 0, 'Regen'],
    [17, '2023-04-10', '09:30', 'Klosterneuburg', 48.3052, 16.3252, 2, 0, 'Bewölkt'],
    [18, '2023-04-16', '14:50', 'Leoben', 47.3829, 15.0925, 0, 0, 'Sonnig'],
    [19, '2023-04-22', '20:25', 'Traun', 48.2203, 14.2403, 1, 0, 'Regen'],
    [20, '2023-04-28', '06:40', 'Amstetten', 48.1229, 14.8740, 0, 0, 'Nebel'],
    [21, '2023-05-04', '13:15', 'Lustenau', 47.4264, 9.6587, 2, 0, 'Sonnig'],
    [22, '2023-05-10', '17:30', 'Hallein', 47.6837, 13.0957, 1, 0, 'Bewölkt'],
    [23, '2023-05-16', '22:05', 'Bludenz', 47.1547, 9.8225, 0, 0, 'Regen'],
    [24, '2023-05-22', '08:50', 'Spittal an der Drau', 46.8006, 13.4896, 3, 0, 'Sonnig'],
    [25, '2023-05-28', '11:20', 'Schwechat', 48.1409, 16.4718, 1, 0, 'Bewölkt'],
    [26, '2023-06-03', '15:45', 'Ternitz', 47.7273, 16.0359, 0, 0, 'Regen'],
    [27, '2023-06-09', '19:10', 'Perchtoldsdorf', 48.1194, 16.2631, 2, 0, 'Sonnig'],
    [28, '2023-06-15', '23:30', 'Wolfsberg', 46.8406, 14.8442, 1, 0, 'Bewölkt'],
    [29, '2023-06-21', '10:15', 'Kufstein', 47.5848, 12.1699, 0, 0, 'Regen'],
    [30, '2023-06-27', '14:50', 'Brunn am Gebirge', 48.1070, 16.2847, 1, 0, 'Sonnig'],
    [31, '2023-07-03', '18:25', 'Schwaz', 47.3466, 11.7073, 3, 0, 'Gewitter'],
    [32, '2023-07-09', '21:40', 'Lienz', 46.8312, 12.7597, 0, 0, 'Regen'],
    [33, '2023-07-15', '09:55', 'Vöcklabruck', 48.0033, 13.6567, 2, 0, 'Sonnig'],
    [34, '2023-07-21', '12:30', 'Knittelfeld', 47.2167, 14.8167, 1, 0, 'Bewölkt'],
    [35, '2023-07-27', '16:05', 'Saalfelden', 47.4266, 12.8480, 0, 0, 'Regen'],
    [36, '2023-08-02', '20:20', 'Ansfelden', 48.2096, 14.2904, 1, 0, 'Sonnig'],
    [37, '2023-08-08', '07:35', 'Stockerau', 48.3833, 16.2167, 3, 0, 'Bewölkt'],
    [38, '2023-08-14', '11:50', 'Hollabrunn', 48.5619, 16.0814, 0, 0, 'Regen'],
    [39, '2023-08-20', '15:15', 'Tulln', 48.3319, 16.0556, 2, 0, 'Sonnig'],
    [40, '2023-08-26', '19:40', 'Mistelbach', 48.5700, 16.5767, 1, 0, 'Bewölkt'],
    [41, '2023-09-01', '22:55', 'Neunkirchen', 47.7206, 16.0811, 0, 0, 'Regen'],
    [42, '2023-09-07', '06:10', 'Hard', 47.4833, 9.6833, 1, 0, 'Nebel'],
    [43, '2023-09-13', '10:25', 'Gmunden', 47.9189, 13.7997, 3, 0, 'Sonnig'],
    [44, '2023-09-19', '13:40', 'Traiskirchen', 48.0167, 16.3000, 0, 0, 'Bewölkt'],
    [45, '2023-09-25', '17:05', 'Bruck an der Mur', 47.4167, 15.2833, 2, 0, 'Regen'],
    [46, '2023-10-01', '21:20', 'Sankt Veit an der Glan', 46.7667, 14.3667, 1, 0, 'Bewölkt'],
    [47, '2023-10-07', '08:45', 'Deutschlandsberg', 46.8167, 15.2167, 0, 0, 'Nebel'],
    [48, '2023-10-13', '12:00', 'Voitsberg', 47.0500, 15.1500, 1, 0, 'Regen'],
    [49, '2023-10-19', '15:35', 'Weiz', 47.2167, 15.6167, 3, 0, 'Sonnig'],
    [50, '2023-10-25', '18:50', 'Gänserndorf', 48.3392, 16.7222, 0, 0, 'Bewölkt'],
    [51, '2023-10-31', '23:15', 'Gerasdorf', 48.2947, 16.4667, 2, 0, 'Regen'],
    [52, '2023-11-06', '07:30', 'Enns', 48.2136, 14.4761, 1, 0, 'Nebel'],
    [53, '2023-11-12', '11:45', 'Bischofshofen', 47.4167, 13.2167, 0, 0, 'Schnee'],
    [54, '2023-11-18', '14:20', 'Lauterach', 47.4833, 9.7333, 1, 0, 'Regen'],
    [55, '2023-11-24', '17:55', 'Rankweil', 47.2833, 9.6500, 3, 0, 'Bewölkt'],
    [56, '2023-11-30', '20:10', 'Neusiedl am See', 47.9500, 16.8333, 0, 0, 'Nebel'],
    [57, '2023-12-06', '09:25', 'Marchtrenk', 48.1917, 14.1167, 2, 0, 'Frost'],
    [58, '2023-12-12', '13:40', 'Sierning', 48.0434, 14.3093, 1, 0, 'Schnee'],
    [59, '2023-12-18', '16:15', 'Seekirchen', 47.9000, 13.1333, 0, 0, 'Regen'],
    [60, '2023-12-24', '19:50', 'St. Johann im Pongau', 47.3500, 13.2000, 1, 0, 'Schnee'],
    [61, '2023-01-07', '08:15', 'Melk', 48.2167, 15.3167, 2, 0, 'Nebel'],
    [62, '2023-01-13', '12:30', 'Haag', 48.1167, 14.5667, 0, 0, 'Frost'],
    [63, '2023-01-19', '16:45', 'Gmünd', 48.7667, 14.9833, 1, 0, 'Schnee'],
    [64, '2023-01-25', '21:00', 'Zell am See', 47.3167, 12.7833, 3, 0, 'Eisglätte'],
    [65, '2023-01-31', '06:20', 'Lilienfeld', 48.0167, 15.6000, 0, 0, 'Nebel'],
    [66, '2023-02-06', '10:35', 'Neulengbach', 48.1833, 15.9000, 2, 0, 'Bewölkt'],
    [67, '2023-02-12', '14:50', 'Herzogenburg', 48.2833, 15.6833, 1, 0, 'Regen'],
    [68, '2023-02-18', '18:05', 'St. Andrä', 46.7667, 14.8167, 0, 0, 'Schnee'],
    [69, '2023-02-24', '23:20', 'St. Valentin', 48.1667, 14.5167, 1, 0, 'Nebel'],
    [70, '2023-03-02', '07:45', 'Altheim', 48.2500, 13.2333, 3, 0, 'Frost'],
    [71, '2023-03-08', '11:10', 'Grein', 48.2167, 14.8500, 0, 0, 'Bewölkt'],
    [72, '2023-03-14', '15:25', 'Peuerbach', 48.3500, 13.7667, 2, 0, 'Regen'],
    [73, '2023-03-20', '19:40', 'Schärding', 48.4500, 13.4333, 1, 0, 'Sonnig'],
    [74, '2023-03-26', '22:55', 'Ried', 48.2167, 13.5000, 0, 0, 'Bewölkt'],
    [75, '2023-04-01', '05:10', 'Mauerkirchen', 48.1833, 13.1333, 1, 0, 'Nebel'],
    [76, '2023-04-07', '09:25', 'Oberndorf', 47.9500, 12.9333, 3, 0, 'Regen'],
    [77, '2023-04-13', '13:40', 'Mattighofen', 48.1000, 13.1500, 0, 0, 'Sonnig'],
    [78, '2023-04-19', '17:55', 'Lofer', 47.5833, 12.6833, 2, 0, 'Bewölkt'],
    [79, '2023-04-25', '20:10', 'St. Johann in Tirol', 47.5167, 12.4333, 1, 0, 'Regen'],
    [80, '2023-05-01', '23:25', 'Kitzbühel', 47.4500, 12.3833, 0, 0, 'Sonnig'],
    [81, '2023-05-08', '06:40', 'Rattenberg', 47.4333, 11.8833, 1, 0, 'Bewölkt'],
    [82, '2023-05-14', '10:55', 'Schwaz', 47.3500, 11.7000, 3, 0, 'Regen'],
    [83, '2023-05-20', '14:10', 'Rum', 47.2833, 11.4500, 0, 0, 'Sonnig'],
    [84, '2023-05-26', '18:25', 'Wattens', 47.2833, 11.6000, 2, 0, 'Bewölkt'],
    [85, '2023-06-01', '21:40', 'Vomp', 47.3333, 11.6833, 1, 0, 'Regen'],
    [86, '2023-06-07', '03:55', 'Telfs', 47.3000, 11.0667, 0, 0, 'Nebel'],
    [87, '2023-06-13', '08:10', 'Imst', 47.2333, 10.7333, 1, 0, 'Sonnig'],
    [88, '2023-06-19', '12:25', 'Landeck', 47.1333, 10.5667, 3, 0, 'Bewölkt'],
    [89, '2023-06-25', '16:40', 'Reutte', 47.4833, 10.7167, 0, 0, 'Regen'],
    [90, '2023-07-01', '19:55', 'Ehrenberg', 47.5000, 10.7000, 2, 0, 'Sonnig'],
    [91, '2023-07-07', '23:10', 'Scharnitz', 47.3833, 11.2667, 1, 0, 'Bewölkt'],
    [92, '2023-07-14', '04:25', 'Seefeld', 47.3333, 11.1833, 0, 0, 'Regen'],
    [93, '2023-07-20', '08:40', 'Mieming', 47.3000, 10.9833, 1, 0, 'Sonnig'],
    [94, '2023-07-26', '12:55', 'Haiming', 47.2500, 10.8833, 3, 0, 'Bewölkt'],
    [95, '2023-08-01', '16:10', 'Ötztal', 47.1333, 10.9333, 0, 0, 'Regen'],
    [96, '2023-08-07', '20:25', 'Pitztal', 47.1833, 10.7500, 2, 0, 'Sonnig'],
    [97, '2023-08-13', '23:40', 'Kaunertal', 47.0333, 10.7500, 1, 0, 'Bewölkt'],
    [98, '2023-08-20', '05:55', 'St. Anton am Arlberg', 47.1167, 10.2667, 0, 0, 'Regen'],
    [99, '2023-08-26', '09:10', 'Ischgl', 47.0167, 10.2833, 1, 0, 'Sonnig'],
    [100, '2023-09-01', '13:25', 'Galtür', 46.9667, 10.1833, 3, 0, 'Bewölkt']
]

# CSV-Datei erstellen
# Für bessere Kompatibilität mit Excel:
with open('verkehrsunfaelle_oesterreich.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')  # Semikolon für europäische Excel-Versionen
    writer.writerow(header)
    writer.writerows(data)

print("CSV-Datei 'verkehrsunfaelle_oesterreich.csv' wurde erfolgreich erstellt!")