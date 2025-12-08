# lines_viewer.py
# Modul zum Anzeigen von Zeilen mit Hilfe eines LineNavigator-Objekts
# Hinweise:
# - Keine Umlaute oder landesspezifische Buchstaben in Code und Kommentaren
# - Erwartet ein Objekt mit Attribut:
#     navigator._lines -> Liste von Strings

import tkinter as tk
from typing import Optional, List


class LinesViewer:
    def __init__(self, navigator) -> None:
        self.navigator = navigator
        self.current_start_index: int = 0

        self.root = tk.Tk()
        self.root.title("Lines Viewer")

        # Text widget fuer die Anzeige der Zeilen
        self.text = tk.Text(self.root, width=100, height=22)
        self.text.grid(row=0, column=0, columnspan=8, padx=5, pady=5)

        # Eingabefeld fuer "Zeilen ab Zeile x"
        tk.Label(self.root, text="Start line (1-based):").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.entry_start = tk.Entry(self.root, width=10)
        self.entry_start.grid(row=1, column=1, padx=5, pady=2)

        # Buttons Grundfunktionen
        btn_first = tk.Button(
            self.root,
            text="Show first 20",
            command=self.show_first_20,
        )
        btn_first.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        btn_last = tk.Button(
            self.root,
            text="Show last 20",
            command=self.show_last_20,
        )
        btn_last.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        btn_from_x = tk.Button(
            self.root,
            text="Show from x",
            command=self.show_from_x,
        )
        btn_from_x.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        btn_prev_block = tk.Button(
            self.root,
            text="Shift -1 line",
            command=self.shift_minus_one,
        )
        btn_prev_block.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        btn_next_block = tk.Button(
            self.root,
            text="Shift +1 line",
            command=self.shift_plus_one,
        )
        btn_next_block.grid(row=2, column=4, padx=5, pady=5, sticky="ew")

        # Neue Buttons fuer RR73-Spruenge
        btn_rr73_next = tk.Button(
            self.root,
            text="Next RR73",
            command=self.jump_next_rr73,
        )
        btn_rr73_next.grid(row=2, column=5, padx=5, pady=5, sticky="ew")

        btn_rr73_prev = tk.Button(
            self.root,
            text="Prev RR73",
            command=self.jump_prev_rr73,
        )
        btn_rr73_prev.grid(row=2, column=6, padx=5, pady=5, sticky="ew")

        btn_quit = tk.Button(
            self.root,
            text="Quit",
            command=self.root.destroy,
        )
        btn_quit.grid(row=2, column=7, padx=5, pady=5, sticky="ew")

        # Initial: erste 20 Zeilen anzeigen
        self.show_first_20()

    def run(self) -> None:
        self.root.mainloop()

    def get_total_lines(self) -> int:
        return len(getattr(self.navigator, "_lines", []))

    def get_block(self, start_index: int, count: int = 20) -> List[str]:
        """
        Liefert einen Block von Zeilen ab start_index (0-basiert).
        """
        lines = getattr(self.navigator, "_lines", [])
        if start_index < 0:
            start_index = 0
        if start_index >= len(lines):
            return []
        end_index = min(start_index + count, len(lines))
        return lines[start_index:end_index]

    def show_lines(self, start_index: int) -> None:
        """
        Zeigt 20 Zeilen ab start_index an und aktualisiert current_start_index.
        """
        total = self.get_total_lines()
        if total == 0:
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", "No lines available.")
            self.current_start_index = 0
            return

        if start_index < 0:
            start_index = 0
        if start_index >= total:
            start_index = max(0, total - 20)

        block = self.get_block(start_index, 20)
        self.current_start_index = start_index

        self.text.delete("1.0", tk.END)
        for line in block:
            self.text.insert(tk.END, line)

    def show_first_20(self) -> None:
        self.show_lines(0)

    def show_last_20(self) -> None:
        total = self.get_total_lines()
        if total <= 20:
            start = 0
        else:
            start = total - 20
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

    # ---- RR73-Funktionen ----

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

    def jump_next_rr73(self) -> None:
        """
        Springt zur naechsten RR73-Zeile vorwaerts.
        Die gefundene RR73-Zeile wird als 5-unterste Zeile angezeigt,
        sofern moeglich, insgesamt 20 Zeilen.
        """
        current_rr_index = self.current_start_index + 15
        total = self.get_total_lines()
        if total == 0:
            return

        if current_rr_index >= total:
            current_rr_index = total - 1

        target_index = self.find_next_rr73_index(current_rr_index)
        if target_index is None:
            return

        # RR73-Zeile soll an Position "total_visible - 5" (0-basiert) liegen
        total_visible = 20
        offset_from_top = total_visible - 5  # 15 bei 20 Zeilen
        start_index = target_index - offset_from_top

        if start_index < 0:
            start_index = 0
        if start_index > total - total_visible:
            start_index = max(0, total - total_visible)

        self.show_lines(start_index)

    def jump_prev_rr73(self) -> None:
        """
        Springt zur vorherigen RR73-Zeile rueckwaerts.
        Die gefundene RR73-Zeile wird als 5-unterste Zeile angezeigt,
        sofern moeglich, insgesamt 20 Zeilen.
        """
        current_rr_index = self.current_start_index + 15
        total = self.get_total_lines()
        if total == 0:
            return

        if current_rr_index >= total:
            current_rr_index = total - 1

        target_index = self.find_prev_rr73_index(current_rr_index)
        if target_index is None:
            return

        total_visible = 20
        offset_from_top = total_visible - 5  # 15
        start_index = target_index - offset_from_top

        if start_index < 0:
            start_index = 0
        if start_index > total - total_visible:
            start_index = max(0, total - total_visible)

        self.show_lines(start_index)


# Beispiel, wie dieses Modul mit deinem Navigator verwendet werden koennte:
if __name__ == "__main__":
    class DummyNavigator:
        def __init__(self) -> None:
            self._lines = []
            for i in range(1, 101):
                if i % 17 == 0:
                    self._lines.append(f"Line {i}: RR73 example\n")
                else:
                    self._lines.append(f"Line {i}\n")

    navigator = DummyNavigator()
    viewer = LinesViewer(navigator)
    viewer.run()
