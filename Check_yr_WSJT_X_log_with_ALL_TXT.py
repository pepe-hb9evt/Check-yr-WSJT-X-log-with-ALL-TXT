from compress_data import filter_lines_with_callsign

# Variablen fuer Rufzeichen und Dateipfade
callsign = "HB9EVT"
input_file = "Excerpt_from_ALL-TXT.txt"
output_file = "filtered_lines.txt"


# Durch Aufruf der Funktion werden
# -- die Zeilen gefiltert,
# -- das Ergebnis in die Output-Datei geschrieben
# -- und zusätzlich in einem Navigator-Objekt gespeichert,
#    das ein kuenftiges zeilenweises Auslesen ermoeglicht.

navigator = filter_lines_with_callsign(
    callsign,
    input_file,
    output_file,
)

# Beispielnutzung:
print("Erste Zeile:", navigator.first())
print("Naechste Zeile:", navigator.next_forward())
print("Letzte Zeile:", navigator.last())
print("Vorherige Zeile:", navigator.next_backward())
print("3. Zeile:", navigator.at(2))

# Bestaetigungsnachricht
print("Filtering completed. Check 'filtered_lines.txt' for results.")