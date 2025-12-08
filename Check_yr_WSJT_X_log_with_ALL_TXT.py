from pathlib import Path


def filter_hb9evt_lines(
    input_path: str | Path,
    output_path: str | Path,
    callsign: str = "HB9EVT",
    cq_pattern: str = "CQ HB9EVT",
) -> None:
    """
    Liest eine Textdatei zeilenweise ein, filtert nur Zeilen mit `callsign`
    und reduziert anschließend Folgen aufeinander folgender Zeilen, die
    `cq_pattern` enthalten, auf jeweils die letzte Zeile der Folge.
    Das Ergebnis wird in `output_path` geschrieben.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    last_cq_line = None
    last_was_cq = False
    result_lines: list[str] = []

    with input_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            # Schritt 1: Nur Zeilen mit dem Rufzeichen behalten
            if callsign not in line:
                continue

            # Schritt 2: Folgen von "CQ HB9EVT" auf jeweils die letzte Zeile reduzieren
            if cq_pattern in line:
                # Merke die (aktuell letzte) CQ-Zeile
                last_cq_line = line
                last_was_cq = True
            else:
                # Wenn vorher eine CQ-Folge war, letzte CQ-Zeile zuerst übernehmen
                if last_was_cq and last_cq_line is not None:
                    result_lines.append(last_cq_line)
                    last_cq_line = None
                    last_was_cq = False

                # Diese Nicht-CQ-Zeile direkt übernehmen
                result_lines.append(line)

    # Falls die Datei mit einer CQ-Folge endet, die letzte CQ-Zeile noch anhängen
    if last_was_cq and last_cq_line is not None:
        result_lines.append(last_cq_line)

    # Ergebnis schreiben
    with output_path.open("w", encoding="utf-8") as out:
        out.writelines(result_lines)


if __name__ == "__main__":
    # Beispielaufruf:
    # python hb9evt_filter.py
    filter_hb9evt_lines("Ausschnitt-aus-all.txt", "hb9evt-gefiltert.txt")

