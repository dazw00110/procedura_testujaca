'''
Sprawdza poprawność danych, np. czy wymagane pola nie są puste.
'''
import csv
import pandas as pd
import re
import math
import csv_reader

# Parsowanie przedziałów danych zdyskretyzowanych
def parse_interval(s: str):
    m = csv_reader._interval_re.match(s.strip())
    if not m:
        raise ValueError(f"Niepoprawny format przedziału: {s!r}")
    _, left_s, right_s, _ = m.groups()
    a = float('-inf') if left_s.strip() in ('-inf','-∞') else float(left_s)
    b = float('inf')  if right_s.strip() in ('inf','∞')   else float(right_s)
    return a, b

# Funkcja sprawdzająca, czy rozmiar danych zdyskretyzowanych jest taki sam jak oryginalnych
def check_shape(orig, disc) -> None:
    print(f"Odczytane kształty: ORYGINAŁ = {orig.shape}, DISC = {disc.shape}")
    if orig.shape != disc.shape:
        raise ValueError(
            f"Rozmiar niezgodny!\n"
            f"Oryginalny:       {orig.shape[0]} wierszy × {orig.shape[1]} kolumn\n"
            f"Zdyskretyzowany:  {disc.shape[0]} wierszy × {disc.shape[1]} kolumn"
        )
    print(f"OK: oba pliki mają {orig.shape[0]} wierszy i {orig.shape[1]} kolumn.")

# Funkcja sprawdzająca, czy dyskretyzacja jest prawidłowa
def check_intervals(orig, disc) -> None:
    rows, cols = orig.shape
    for i in range(rows):
        for j in range(cols - 1):  # ostatnia kolumna to decyzja
            val = orig.iat[i, j]
            interval = str(disc.iat[i, j])
            a, b = parse_interval(interval)
            if not (val > a and val <= b):
                raise ValueError(
                    f"Niepoprawna dyskretyzacja w wierszu {i+1}, kolumnie {j+1}:\n"
                    f"  oryginał = {val}\n"
                    f"  przedział = {interval!r}\n"
                    f"  (spodziewano: {a} < {val} ≤ {b})"
                )
    print("OK: wszystkie wartości mieszczą się w deklarowanych przedziałach.")



