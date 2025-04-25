import csv
import pandas as pd
import re

'''
Wczytuje plik .csv i zwraca dane jako data frame.
'''
def detect_delimiter(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        for raw in f:
            line = raw.strip('\n\r')
            if line.strip():
                break
    candidates = ['\t', ';', ',', ' ']
    counts = {d: line.count(d) for d in candidates}
    return max(counts, key=counts.get)

def load_dataframe(path: str, decimal_comma: bool) -> pd.DataFrame:
    sep = detect_delimiter(path)
    if sep == ' ':
        sep, engine = r'\s+', 'python'
    else:
        engine = 'c'
    kwargs = {
        'sep': sep,
        'engine': engine,
        'header': None,
        'skip_blank_lines': True
    }
    if decimal_comma:
        kwargs['decimal'] = ','

    df = pd.read_csv(path, **kwargs)

    # Sprawdzenie na puste wartości i zgłoszenie, gdzie są
    if df.isnull().values.any():
        nan_locs = df.isnull()
        for row_idx, row in nan_locs.iterrows():
            for col_idx, is_nan in enumerate(row):
                if is_nan:
                    raise ValueError(
                        f"W pliku '{path}' znaleziono puste pole w wierszu {row_idx + 1}, kolumna {col_idx + 1}."
                    )

    return df

# Regex na '(a; b]', '(a; b)', '[a; b)' itp.
_interval_re = re.compile(
    r'^([\(\[])\s*'        # '(' lub '['
    r'([^;]+?)\s*;\s*'     # lewa wartość
    r'([^\)\]]+?)\s*'      # prawa wartość
    r'([\)\]])$'           # ')' lub ']'
)
