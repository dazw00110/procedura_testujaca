import os
import time
import sys
import glob
import subprocess
import pandas as pd
from csv_reader import load_dataframe
from verifier import check_shape, check_intervals, count_cuts
from non_pairs import count_nondeterministic_pairs


# Tutaj wpisujemy ścieżkę algorytmu
dys_algoritm_name = 'top_down_discretizer.py'


def run_md_algorithm(orig_path: str, disc_path: str) -> float:
    """Uruchamia algorytm dyskretyzacji i mierzy czas"""
    # Usuń stary plik wynikowy, jeśli istnieje
    if os.path.exists(disc_path):
        os.remove(disc_path)

    start_time = time.time()
    # Wywołujemy Pythona z odpowiednim skryptem i argumentami
    result = subprocess.run(
        [sys.executable, dys_algoritm_name, orig_path, disc_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    elapsed = time.time() - start_time

    # Sprawdź, czy plik wynikowy powstał
    if not os.path.exists(disc_path):
        raise FileNotFoundError(
            f"Algorytm dyskretyzacji nie wygenerował pliku {disc_path}\n"
            f"stdout:\n{result.stdout.decode()}\n"
            f"stderr:\n{result.stderr.decode()}"
        )

    return elapsed


def test_algorithm(orig_path: str, disc_path: str) -> dict:
    start_time = time.time()

    # Wczytaj dane
    orig = load_dataframe(orig_path, decimal_comma=True).astype(float)
    disc = load_dataframe(disc_path, decimal_comma=False)

    # Weryfikacja
    check_shape(orig, disc)
    check_intervals(orig, disc)

    # Obliczenia
    det = count_nondeterministic_pairs(disc)
    cuts = count_cuts(disc)
    time_spent = time.time() - start_time

    return {
        'det': det,
        'cuts': cuts,
        'time': round(time_spent, 4),
        'ocena': round(0.5 * det + 0.25 * cuts + time_spent, 2)
    }


def main():
    # Konfiguracja ścieżek
    data_dir = "test_data"
    test_cases = [
        ('data1.csv', 'DISCdata1.csv'),
        ('data2.csv', 'DISCdata2.csv'),
        ('data3.csv', 'DISCdata3.csv'),
    ]

    # 0) Usuń stare pliki wynikowe DISC*.csv
    pattern = os.path.join(data_dir, 'DISC*.csv')
    for old in glob.glob(pattern):
        try:
            os.remove(old)
            print(f"Usunięto stary plik: {old}")
        except OSError as e:
            print(f"Nie udało się usunąć {old}: {e}")

    results = []
    for orig_file, disc_file in test_cases:
        orig_path = os.path.join(data_dir, orig_file)
        disc_path = os.path.join(data_dir, disc_file)

        # 1) Sprawdź plik oryginalny
        if not os.path.exists(orig_path):
            raise FileNotFoundError(f"Brak pliku: {orig_path}")

        # 2) Wygeneruj plik dyskretyzowany
        print(f"==> Dyskretyzacja: {orig_file} -> {disc_file}")
        md_time = run_md_algorithm(orig_path, disc_path)
        print(f"    Czas dyskretyzacji: {md_time:.3f} s")

        # 3) Teraz testuj wynik
        result = test_algorithm(orig_path, disc_path)
        result.update({'md_time': round(md_time, 4)})
        results.append({
            'Plik': orig_file,
            **result
        })

    # Generuj raport
    df = pd.DataFrame(results)
    total = df[['det', 'cuts', 'time', 'md_time', 'ocena']].sum()
    df.loc['Σ'] = ['Razem'] + total.tolist()

    print("\n=== RAPORT TESTOWY ===")
    print(df.to_string(index=False))
    df.to_csv(os.path.join(data_dir, 'raport.csv'), index=False)


if __name__ == "__main__":
    main()

