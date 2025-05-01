import pandas as pd
from csv_reader import _interval_re  # Import z Twojego istniejącego kodu

def count_cuts(disc: pd.DataFrame) -> int:
    total_cuts = 0
    for col in disc.columns[:-1]:
        unique_intervals = disc[col].nunique()
        total_cuts += (unique_intervals - 1) if unique_intervals > 1 else 0
    return total_cuts


def parse_interval(s: str):
    m = _interval_re.match(s.strip())
    if not m:
        raise ValueError(f"Niepoprawny format przedziału: {s!r}")
    _, left_s, right_s, _ = m.groups()
    a = float('-inf') if left_s.strip() in ('-inf','-∞') else float(left_s)
    b = float('inf') if right_s.strip() in ('inf','∞') else float(right_s)
    return a, b


def check_shape(orig, disc) -> None:
    if orig.shape != disc.shape:
        raise ValueError(
            f"Rozmiar niezgodny!\n"
            f"Oryginalny: {orig.shape}\nZdyskretyzowany: {disc.shape}"
        )


def check_intervals(orig, disc) -> None:
    for i in range(orig.shape[0]):
        for j in range(orig.shape[1]-1):
            val = orig.iat[i, j]
            interval = str(disc.iat[i, j])
            a, b = parse_interval(interval)
            if not (a < val <= b):
                raise ValueError(
                    f"Błąd w wierszu {i+1}, kolumna {j+1}: "
                    f"{val} ∉ {interval}"
                )


def count_cuts(disc: pd.DataFrame) -> int:
    total_cuts = 0
    for col in disc.columns[:-1]:
        unique_intervals = disc[col].nunique()
        total_cuts += (unique_intervals - 1) if unique_intervals > 1 else 0
    return total_cuts