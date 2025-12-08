from pathlib import Path
from typing import List, Optional


class LineNavigator:
    def __init__(self, lines: List[str]) -> None:
        self._lines = lines
        self._index: Optional[int] = 0 if lines else None

    def first(self) -> Optional[str]:
        if not self._lines:
            self._index = None
            return None
        self._index = 0
        return self._lines[self._index]

    def last(self) -> Optional[str]:
        if not self._lines:
            self._index = None
            return None
        self._index = len(self._lines) - 1
        return self._lines[self._index]

    def next_forward(self) -> Optional[str]:
        if self._index is None or not self._lines:
            return None
        if self._index + 1 >= len(self._lines):
            return None
        self._index += 1
        return self._lines[self._index]

    def next_backward(self) -> Optional[str]:
        if self._index is None or not self._lines:
            return None
        if self._index - 1 < 0:
            return None
        self._index -= 1
        return self._lines[self._index]

    def at(self, n: int) -> Optional[str]:
        """0-basierter Index; fuer 'x-te Zeile' ggf. n-1 verwenden."""
        if n < 0 or n >= len(self._lines):
            return None
        self._index = n
        return self._lines[self._index]

    def __len__(self) -> int:
        return len(self._lines)


def filter_lines_with_callsign(
    callsign: str,
    input_path: str | Path,
    output_path: str | Path,
) -> LineNavigator:
    """
    liefert zusaetzlich einen LineNavigator mit allen Ergebniszeilen.
    """
    
    cq_pattern = "CQ " + callsign  # Suchmuster für CQ-Zeilen

    input_path = Path(input_path)
    output_path = Path(output_path)

    last_cq_line = None
    last_was_cq = False
    result_lines: list[str] = []

    with input_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if callsign not in line:
                continue

            if cq_pattern in line:
                last_cq_line = line
                last_was_cq = True
            else:
                if last_was_cq and last_cq_line is not None:
                    result_lines.append(last_cq_line)
                    last_cq_line = None
                    last_was_cq = False

                result_lines.append(line)

    if last_was_cq and last_cq_line is not None:
        result_lines.append(last_cq_line)

    with output_path.open("w", encoding="utf-8") as out:
        out.writelines(result_lines)

    # Ergebnis zusaetzlich in einem Navigator-Objekt zurückgeben
    return LineNavigator(result_lines)


if __name__ == "__main__":

    # Beispielaufruf:
    navigator = filter_lines_with_callsign(
        "HB9EVT",
        "Excerpt_from_ALL-TXT.txt",
        "filtered_lines.txt",
    )

    # Beispielnutzung:
    print("Erste Zeile:", navigator.first())
    print("Naechste Zeile:", navigator.next_forward())
    print("Letzte Zeile:", navigator.last())
    print("Vorherige Zeile:", navigator.next_backward())
    print("3. Zeile:", navigator.at(2))
