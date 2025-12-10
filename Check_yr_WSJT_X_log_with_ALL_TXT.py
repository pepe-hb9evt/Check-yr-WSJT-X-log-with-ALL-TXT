"""
LICENSE
==========
This file is part of the project <Check_yr_WSJT_X_log_with_ALL_TXT>
Licensed under the MIT License - see the LICENSE file for details.

Developed by Pepe HB9EVT
with support from my lovely auntie A.I. Perplexity, 2025

I would appreciate a short email if you use this software:
github2025  -at-  pepemail.ch
"""


"""
Check_yr_WSJT_X_log_with_ALL_TXT.py
===================================
Hauptskript
"""


# IMPORTS
from sub_compress_data import filter_lines_with_callsign
from sub_lines_viewer import LinesViewer


# Variablen fuer Rufzeichen und Dateipfade
own_callsign = "HB9EVT"
input_file = "Excerpt_from_ALL-TXT.txt"
output_file = "filtered_lines.txt"


# Durch Aufruf der Funktion werden
# -- die Zeilen gefiltert,
# -- das Ergebnis in die Output-Datei geschrieben
# -- und zusätzlich in einem Navigator-Objekt gespeichert,
#    das ein kuenftiges zeilenweises Auslesen ermoeglicht.

navigator = filter_lines_with_callsign(
    own_callsign,
    input_file,
    output_file,
)


viewer = LinesViewer(navigator, own_callsign)
viewer.run()


# Beispielnutzung:
# print("Erste Zeile:", navigator.first())
# print("Naechste Zeile:", navigator.next_forward())
# print("Letzte Zeile:", navigator.last())
# print("Vorherige Zeile:", navigator.next_backward())
# print("3. Zeile:", navigator.at(2))

# Bestaetigungsnachricht
print("Filtering completed. Check 'filtered_lines.txt' for results.")