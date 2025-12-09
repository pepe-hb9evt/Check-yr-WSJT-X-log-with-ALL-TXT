"""
LICENSE
==========
This file is part of <Check_yr_WSJT_X_log_with_ALL_TXT>
Licensed under the MIT License - see the LICENSE file for details.

Developed by Pepe HB9EVT
with support from my lovely auntie A.I. Perplexity, 2025

I would appreciate a short email if you use this software:
github2025  -at-  pepemail.ch
"""


"""
lines_viewer.py
=================
GUI-Anwendung zur Anzeige von Zeilen aus einem LineNavigator-Objekt.    


Aufruf im Hauptprogramm:
========================

viewer = LinesViewer(navigator, own_callsign)
viewer.run()
"""


# IMPORTS
import tkinter as tk
from typing import Optional, List


# KONSTANTEN
BREITE_TEXTFELD = 80                # Breite des Textfelds in Zeichen
VISIBLE_LINES = 20                  # Anzahl der sichtbaren Zeilen im Fenster
RR73_POS_INDEX = VISIBLE_LINES - 5  # RR73-Zeile wird auf Position 15 gesetzt
OTHER_MARK_SUFFIX = "     ***"      # Kennzeichnung fuer Zeilen mit anderem Rufzeichen


# KLASSE LinesViewer
class LinesViewer:
    def __init__(self, navigator, own_callsign: str) -> None:
        self.navigator = navigator
        self.own_callsign = own_callsign
        # Darf auch negativ sein, wenn vor Listenanfang mit Leerzeilen aufgefuellt wird
        self.current_start_index: int = 0
        # Das aktuell ermittelte andere Rufzeichen
        self.other_callsign: Optional[str] = None

        self.root = tk.Tk()
        self.root.title("Lines Viewer")

        # Text widget fuer die Anzeige der Zeilen
        self.text = tk.Text(self.root, width=BREITE_TEXTFELD, height=VISIBLE_LINES)
        self.text.grid(row=0, column=0, columnspan=6, padx=5, pady=5)

        # Tags fuer Hervorhebung im Text-Widget
        self.text.tag_config("other_cs", foreground="red")
        self.text.tag_config("mark_suffix", foreground="red")

        # Labels fuer Pfeile / Zaehler
        self.label_above = tk.Label(self.root, text="", fg="red")
        self.label_above.grid(row=0, column=6, padx=5, pady=2, sticky="n")

        self.label_below = tk.Label(self.root, text="", fg="red")
        self.label_below.grid(row=0, column=6, padx=5, pady=2, sticky="s")

        # Eingabefeld fuer "Zeilen ab Zeile x"
        tk.Label(self.root, text="Start line (1-based):").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.entry_start = tk.Entry(self.root, width=10)
        self.entry_start.grid(row=1, column=1, padx=5, pady=2)

        # Buttons Grundfunktionen
        tk.Button(
            self.root,
            text="Show first 20",
            command=self.show_first_20,
        ).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        tk.Button(
            self.root,
            text="Show last 20",
            command=self.show_last_20,
        ).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Button(
            self.root,
            text="Show from x",
            command=self.show_from_x,
        ).grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        # Shift-Buttons als Attribute, damit ihr state spaeter geaendert werden kann
        self.btn_shift_minus = tk.Button(
            self.root,
            text="Shift -1 line",
            command=self.shift_minus_one,
        )
        self.btn_shift_minus.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        self.btn_shift_plus = tk.Button(
            self.root,
            text="Shift +1 line",
            command=self.shift_plus_one,
        )
        self.btn_shift_plus.grid(row=2, column=4, padx=5, pady=5, sticky="ew")

        # RR73-Spruenge
        tk.Button(
            self.root,
            text="Next RR73",
            command=self.jump_next_rr73,
        ).grid(row=2, column=5, padx=5, pady=5, sticky="ew")

        tk.Button(
            self.root,
            text="Prev RR73",
            command=self.jump_prev_rr73,
        ).grid(row=2, column=6, padx=5, pady=5, sticky="ew")

        tk.Button(
            self.root,
            text="Quit",
            command=self.root.destroy,
        ).grid(row=2, column=7, padx=5, pady=5, sticky="ew")

        # Initial: erste 20 Zeilen anzeigen
        self.show_first_20()

    def run(self) -> None:
        self.root.mainloop()

    def get_total_lines(self) -> int:
        return len(getattr(self.navigator, "_lines", []))

    # ------------------------------------------------------------------
    # Block-Erzeugung und Anzeige
    # ------------------------------------------------------------------

    def get_block_with_padding(self, start_index: int, count: int = VISIBLE_LINES) -> List[str]:
        """
        Liefert genau 'count' Zeilen ab start_index (0-basiert).
        Negative Bereiche vor Index 0 und Bereiche hinter dem Listenende
        werden als leere Zeilen dargestellt.
        """
        lines = getattr(self.navigator, "_lines", [])
        total = len(lines)
        result: List[str] = []

        for offset in range(count):
            idx = start_index + offset
            if 0 <= idx < total:
                result.append(lines[idx])
            else:
                # Zeile existiert nicht -> Leerzeile
                result.append("\n")
        return result

    def highlight_other_callsign_and_suffix(self, block: List[str]) -> None:
        """
        Markiert alle Vorkommen von self.other_callsign in den
        aktuell im Text-Widget eingefuegten Zeilen mit roter Schrift
        und haengt bei Zeilen mit other_callsign den visuellen Suffix an.
        """
        # Tags entfernen
        self.text.tag_remove("other_cs", "1.0", tk.END)
        self.text.tag_remove("mark_suffix", "1.0", tk.END)

        if not self.other_callsign:
            return

        cs = self.other_callsign
        cs_len = len(cs)

        # Jede sichtbare Zeile durchsuchen
        for i, line in enumerate(block):
            if not line.strip():
                continue

            # Position der Zeile im Widget
            line_no = i + 1
            # Wir holen uns den Text genau dieser Zeile aus dem Widget,
            # damit auch vorherige Suffixe sicher beruecksichtigt werden.
            current_line_text = self.text.get(f"{line_no}.0", f"{line_no}.end")

            # 1) other_callsign markieren
            start_pos = 0
            while True:
                idx = current_line_text.find(cs, start_pos)
                if idx == -1:
                    break
                start_index = f"{line_no}.{idx}"
                end_index = f"{line_no}.{idx + cs_len}"
                self.text.tag_add("other_cs", start_index, end_index)
                start_pos = idx + cs_len

            # 2) Nur wenn other_callsign in dieser Zeile vorkommt,
            #    visualen Suffix "     ***" anhaengen (reine Anzeige).
            if cs in current_line_text:
                # An das Ende der Zeile (nicht ganze Zeile loeschen)
                self.text.insert(f"{line_no}.end", OTHER_MARK_SUFFIX)
                # Neu eingefuegten Suffix als rot taggen
                start_index = f"{line_no}.{len(current_line_text)}"
                end_index = f"{line_no}.{len(current_line_text) + len(OTHER_MARK_SUFFIX)}"
                self.text.tag_add("mark_suffix", start_index, end_index)

    def update_arrow_labels(self) -> None:
        """
        Zaehlt in den nicht sichtbaren Zeilen oberhalb und unterhalb des aktuellen Fensters,
        wie oft other_callsign vorkommt, und zeigt ggf. rote Pfeile mit Anzahl an.
        """
        if not self.other_callsign:
            # Keine Pfeile anzeigen
            self.label_above.config(text="")
            self.label_below.config(text="")
            return

        lines = getattr(self.navigator, "_lines", [])
        total = len(lines)
        cs = self.other_callsign

        # Bereich des aktuellen Fensters in der Datenliste
        start = self.current_start_index
        end = self.current_start_index + VISIBLE_LINES - 1

        # Oberer Bereich: 0 .. start-1
        count_above = 0
        if total > 0:
            for i in range(0, max(0, start)):
                if cs in lines[i]:
                    count_above += 1

        # Unterer Bereich: end+1 .. total-1
        count_below = 0
        if total > 0:
            for i in range(min(total, end + 1), total):
                if cs in lines[i]:
                    count_below += 1

        # Pfeile aktualisieren
        if count_above > 0:
            # Unicode Pfeil nach oben
            self.label_above.config(text=f"\u25B2 {count_above}")
        else:
            self.label_above.config(text="")

        if count_below > 0:
            # Unicode Pfeil nach unten
            self.label_below.config(text=f"\u25BC {count_below}")
        else:
            self.label_below.config(text="")

    def update_shift_buttons_state(self) -> None:
        """
        Aktiviert/Deaktiviert die Shift-Buttons, so dass kein Shift
        ausgefuehrt werden kann, der weniger als 2 sichtbare reale
        Zeilen uebrig lassen wuerde.
        """
        total = self.get_total_lines()

        # Standard: beide aktiviert
        state_prev = tk.NORMAL
        state_next = tk.NORMAL

        if total <= 2:
            # Insgesamt zu wenig Zeilen fuer sinnvolles Shiften
            state_prev = tk.DISABLED
            state_next = tk.DISABLED
        else:
            start = self.current_start_index
            lines = getattr(self.navigator, "_lines", [])

            # Zaehle reale Zeilen im aktuellen Fenster
            visible_real = 0
            for offset in range(VISIBLE_LINES):
                idx = start + offset
                if 0 <= idx < total:
                    visible_real += 1

            # Wenn im aktuellen Fenster nur noch 2 oder weniger reale Zeilen
            # sichtbar sind, kein weiteres Shiften erlauben
            if visible_real <= 2:
                state_prev = tk.DISABLED
                state_next = tk.DISABLED

            # Feintuning: kein Rueckwaerts-Shift am absoluten Anfang
            if start <= 0:
                state_prev = tk.DISABLED

            # Kein Vorwaerts-Shift, wenn das Fenster am Ende anliegt
            if start + VISIBLE_LINES >= total and visible_real <= VISIBLE_LINES:
                state_next = tk.DISABLED

        self.btn_shift_minus.config(state=state_prev)
        self.btn_shift_plus.config(state=state_next)

    def show_lines(self, start_index: int) -> None:
        """
        Zeigt genau VISIBLE_LINES Zeilen an.
        Zeilen vor Listenanfang / nach Listenende werden als Leerzeilen dargestellt.
        Hebt sofern gesetzt das andere Rufzeichen in rot hervor, erweitert
        die betreffenden Zeilen in der Anzeige um "     ***" und aktualisiert
        die Pfeil-Labels fuer Vorkommen oberhalb/unterhalb sowie die Shift-Buttons.
        """
        total = self.get_total_lines()

        self.text.delete("1.0", tk.END)

        if total == 0:
            for _ in range(VISIBLE_LINES):
                self.text.insert(tk.END, "\n")
            self.current_start_index = 0
            self.text.tag_remove("other_cs", "1.0", tk.END)
            self.text.tag_remove("mark_suffix", "1.0", tk.END)
            self.label_above.config(text="")
            self.label_below.config(text="")
            self.update_shift_buttons_state()
            return

        block = self.get_block_with_padding(start_index, VISIBLE_LINES)
        self.current_start_index = start_index

        for line in block:
            self.text.insert(tk.END, line)

        # Anderes Rufzeichen hervorheben und Suffix anhaengen
        self.highlight_other_callsign_and_suffix(block)

        # Pfeile / Anzahlen aktualisieren
        self.update_arrow_labels()

        # Shift-Buttons aktivieren/deaktivieren
        self.update_shift_buttons_state()

    def show_first_20(self) -> None:
        self.show_lines(0)

    def show_last_20(self) -> None:
        total = self.get_total_lines()
        if total <= VISIBLE_LINES:
            start = 0
        else:
            start = total - VISIBLE_LINES
        self.show_lines(start)

    def show_from_x(self) -> None:
        """
        Liest eine 1-basierte Zeilennummer aus dem Entry
        und zeigt ab dort 20 Zeilen an.
        """
        value = self.entry_start.get().strip()
        try:
            line_num = int(value)
        except ValueError:
            return

        index_0 = line_num - 1
        self.show_lines(index_0)

    def shift_minus_one(self) -> None:
        """
        Verschiebt den angezeigten Block um 1 Zeile nach oben (Rueckwaerts).
        """
        new_start = self.current_start_index - 1
        self.show_lines(new_start)

    def shift_plus_one(self) -> None:
        """
        Verschiebt den angezeigten Block um 1 Zeile nach unten (Vorwaerts).
        """
        new_start = self.current_start_index + 1
        self.show_lines(new_start)

    # ------------------------------------------------------------------
    # RR73-Funktionen und Rufzeichen-Erkennung
    # ------------------------------------------------------------------

    def find_next_rr73_index(self, start_from: int) -> Optional[int]:
        """
        Sucht vorwaerts ab start_from (exklusive) die naechste Zeile mit "RR73".
        """
        lines = getattr(self.navigator, "_lines", [])
        for i in range(start_from + 1, len(lines)):
            if "RR73" in lines[i]:
                return i
        return None

    def find_prev_rr73_index(self, start_from: int) -> Optional[int]:
        """
        Sucht rueckwaerts ab start_from (exklusive) die vorherige Zeile mit "RR73".
        """
        lines = getattr(self.navigator, "_lines", [])
        for i in range(start_from - 1, -1, -1):
            if "RR73" in lines[i]:
                return i
        return None

    def get_current_rr73_ref_index(self) -> int:
        """
        Liefert den Index der aktuell als RR73-Referenz angenommenen Zeile.
        Liegt das Fenster ausserhalb der Listengroesse, wird an den gueltigen Bereich geclippt.
        """
        total = self.get_total_lines()
        if total == 0:
            return 0
        idx = self.current_start_index + RR73_POS_INDEX
        if idx < 0:
            idx = 0
        if idx >= total:
            idx = total - 1
        return idx

    def extract_other_callsign_from_rr73_line(self, line: str) -> Optional[str]:
        """
        Erwartete Struktur am Ende:
        ' ... <cs1> <cs2> RR73'
        own_callsign ist eines von cs1 oder cs2.
        Rueckgabe: das andere Rufzeichen oder None.
        """
        parts = line.strip().split()
        if len(parts) < 3:
            return None
        if parts[-1] != "RR73":
            return None
        cs1 = parts[-3]
        cs2 = parts[-2]

        if cs1.upper() == self.own_callsign.upper():
            return cs2
        if cs2.upper() == self.own_callsign.upper():
            return cs1
        return None

    def update_other_callsign_from_index(self, rr73_index: int) -> None:
        """
        Ermittelt aus der RR73-Zeile an rr73_index das andere Rufzeichen
        und speichert es in self.other_callsign.
        """
        lines = getattr(self.navigator, "_lines", [])
        if 0 <= rr73_index < len(lines):
            line = lines[rr73_index]
            other = self.extract_other_callsign_from_rr73_line(line)
            if other:
                self.other_callsign = other

    def jump_next_rr73(self) -> None:
        """
        Springt zur naechsten RR73-Zeile vorwaerts.
        Die gefundene RR73-Zeile wird immer auf RR73_POS_INDEX gesetzt;
        nicht benoetigte Zeilen werden als Leerzeilen angezeigt.
        Ermittelt dabei das andere Rufzeichen und hebt es in allen 20 Zeilen rot hervor,
        inklusive visueller Markierung '     ***' und Pfeil-Anzeigen.
        """
        total = self.get_total_lines()
        if total == 0:
            return

        current_rr_index = self.get_current_rr73_ref_index()
        target_index = self.find_next_rr73_index(current_rr_index)
        if target_index is None:
            return

        self.update_other_callsign_from_index(target_index)

        start_index = target_index - RR73_POS_INDEX
        self.show_lines(start_index)

    def jump_prev_rr73(self) -> None:
        """
        Springt zur vorherigen RR73-Zeile rueckwaerts.
        Die gefundene RR73-Zeile wird immer auf RR73_POS_INDEX gesetzt;
        nicht benoetigte Zeilen werden als Leerzeilen angezeigt.
        Ermittelt dabei das andere Rufzeichen und hebt es in allen 20 Zeilen rot hervor,
        inklusive visueller Markierung '     ***' und Pfeil-Anzeigen.
        """
        total = self.get_total_lines()
        if total == 0:
            return

        current_rr_index = self.get_current_rr73_ref_index()
        target_index = self.find_prev_rr73_index(current_rr_index)
        if target_index is None:
            return

        self.update_other_callsign_from_index(target_index)

        start_index = target_index - RR73_POS_INDEX
        self.show_lines(start_index)
# Ende der Klasse LinesViewer -----------------------------


# Beispiel, wie dieses Modul mit einem Navigator verwendet werden kann
if __name__ == "__main__":
    class DummyNavigator:
        def __init__(self) -> None:
            self._lines = []
            # Kuenstliche Daten mit own_callsign = "HB9EVT"
            for i in range(1, 60):
                if i in (7, 15, 25, 33, 48):
                    self._lines.append(
                        f"251208_0414{i:02d}     3.573 Rx FT8    -12  0.4 1030 HB9EVT DJ2MS RR73\n"
                    )
                else:
                    self._lines.append(
                        f"251208_0414{i:02d}     3.573 Rx FT8    -10  0.4 1030 HB9EVT DJ2MS {i}\n"
                    )

    navigator = DummyNavigator()
    viewer = LinesViewer(navigator, own_callsign="HB9EVT")
    viewer.run()
