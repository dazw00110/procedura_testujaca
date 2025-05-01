import csv
import pandas as pd
import re
import os

# Regex na '(a; b]', '(a; b)', '[a; b)' itp.
_interval_re = re.compile(
    r'^\s*([\(\[])\s*'        # '(' lub '['
    r'([^;]+?)\s*;\s*'         # lewa wartość
    r'([^\)\]]+?)\s*'         # prawa wartość
    r'([\)\]])\s*$'           # ')' lub ']'
)

'''
Detekcja separatora na podstawie pierwszej niepustej linii.
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

'''
Sprawdza, czy pierwszy wiersz to nagłówek:
- Jeśli co najmniej jeden token nie jest ani liczbą, ani przedziałem, to traktujemy nagłówek.
- W przeciwnym wypadku to dane.
'''
def has_header(path: str, delimiter: str, decimal_comma: bool) -> bool:
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter if delimiter!=' ' else None, skipinitialspace=True)
        first = next(reader, [])
    for token in first:
        token = token.strip()
        # Spróbuj sparsować liczbę
        try:
            # zamiana przecinka na kropkę, jeśli decimal_comma=True
            val = token.replace(',', '.') if decimal_comma else token
            float(val)
            continue
        except ValueError:
            # Jeśli token to przedział, to też traktujemy jako dane
            if _interval_re.match(token):
                continue
            # W przeciwnym razie: to nagłówek
            return True
    return False

'''
Wczytuje plik .csv i zwraca dane jako DataFrame,
uwzględniając detekcję nagłówka i separatora.
'''
def load_dataframe(path: str, decimal_comma: bool) -> pd.DataFrame:
    # Jeśli to plik dyskretyzowany (pola w formacie '(a; b]'), wymuś przecinek jako separator kolumn
    if not decimal_comma:
        sep = ','
        engine = 'c'
        header = None
    else:
        # oryginalne dane: wykryj separator i nagłówek
        sep = detect_delimiter(path)
        if sep == ' ':
            sep, engine = r'\s+', 'python'
        else:
            engine = 'c'
        # Detekcja nagłówka tylko dla oryginalnych danych
        header = 0 if has_header(path, sep if sep != r'\s+' else ' ', decimal_comma) else None

    kwargs = {
        'sep': sep,
        'engine': engine,
        'header': header,
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
