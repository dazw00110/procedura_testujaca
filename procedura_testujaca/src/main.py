import os
import time
import sys
import glob
import subprocess
import pandas as pd
from csv_reader import load_dataframe
from verifier import check_shape, check_intervals, count_cuts
from non_pairs import count_nondeterministic_pairs

dys_algoritm_name = 'top_down_discretizer.py'


def run_md_algorithm(orig_path: str, disc_path: str) -> float:
    if os.path.exists(disc_path):
        os.remove(disc_path)

    start_time = time.time()
    subprocess.run(
        [sys.executable, dys_algoritm_name, orig_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    return time.time() - start_time

'''
Testuje wynik dyskretyzacji:
- Wczytuje dane oryginalne i zdyskretyzowane,
- sprawdza zgodność rozmiarów i poprawność przedziałów,
- liczy niedeterministyczne pary i cięcia,
- zwraca ocenę na podstawie det, cuts i czasu.
'''
def test_algorithm(orig_path: str, disc_path: str, md_time: float) -> dict:
    orig = load_dataframe(orig_path, decimal_comma=True).astype(float)
    disc = load_dataframe(disc_path, decimal_comma=False)
    check_shape(orig, disc)
    check_intervals(orig, disc)

    det = count_nondeterministic_pairs(disc)  # Oblicz det raz
    cuts = count_cuts(disc)

    return {
        'det': det,
        'cuts': cuts,
        'time': round(md_time, 4),
        'ocena': round(0.5 * det + 0.25 * cuts + md_time, 2)
    }


def main():
    data_dir = "test_data"
    test_cases = [
        ('data1.csv', 'DISCdata1.csv'),
        ('data2.csv', 'DISCdata2.csv'),
        ('data3.csv', 'DISCdata3.csv'),
    ]

    for old in glob.glob(os.path.join(data_dir, 'DISC*.csv')):
        os.remove(old)

    results = []
    for orig_file, disc_file in test_cases:
        orig_path = os.path.join(data_dir, orig_file)
        disc_path = os.path.join(data_dir, disc_file)

        md_time = run_md_algorithm(orig_path, disc_path)
        result = test_algorithm(orig_path, disc_path, md_time)

        results.append({
            'Plik': orig_file,
            'det': result['det'],
            'cuts': result['cuts'],
            'time': result['time'],
            'ocena': result['ocena']
        })

    df = pd.DataFrame(results)
    total = df[['det', 'cuts', 'time', 'ocena']].sum()
    df.loc['Σ'] = ['Razem'] + total.tolist()

    print("\n=== RAPORT TESTOWY ===")
    print(df.to_string(index=False))
    df.to_csv(os.path.join(data_dir, 'raport.csv'), index=False)


if __name__ == "__main__":
    main()