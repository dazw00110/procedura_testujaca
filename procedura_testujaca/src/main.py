import os
import time
import glob
import pandas as pd
import top_down_discretizer
from csv_reader import load_dataframe
from verifier import check_shape, check_intervals, count_cuts
from non_pairs import count_nondeterministic_pairs

def run_md_algorithm(orig_path: str, disc_path: str) -> float:
    # usuń, jeśli już jest
    if os.path.exists(disc_path):
        os.remove(disc_path)
    start = time.time()
    top_down_discretizer.top_down_discretization(orig_path)
    return time.time() - start

def test_algorithm(orig_path: str, disc_path: str, md_time: float) -> dict:
    orig = load_dataframe(orig_path, decimal_comma=True).astype(float)
    disc = load_dataframe(disc_path, decimal_comma=False)
    check_shape(orig, disc)
    check_intervals(orig, disc)
    det = count_nondeterministic_pairs(disc)
    cuts = count_cuts(disc)
    return {
        'det': det,
        'cuts': cuts,
        'time': round(md_time, 4),
        'ocena': round(0.5*det + 0.25*cuts + md_time, 2)
    }

def main():
    data_dir = "test_data"
    cases = [
        ('data1.csv', 'DISCdata1.csv'),
        ('data2.csv', 'DISCdata2.csv'),
        ('data3.csv', 'DISCdata3.csv'),
    ]
    # czyść stare
    for old in glob.glob(os.path.join(data_dir, 'DISC*.csv')):
        os.remove(old)

    wyniki = []
    for orig_file, disc_file in cases:
        orig = os.path.join(data_dir, orig_file)
        disc = os.path.join(data_dir, disc_file)
        t = run_md_algorithm(orig, disc)
        res = test_algorithm(orig, disc, t)
        wyniki.append({
            'Plik': orig_file,
            'det': res['det'],
            'cuts': res['cuts'],
            'time': res['time'],
            'ocena': res['ocena']
        })

    df = pd.DataFrame(wyniki)
    suma = df[['det','cuts','time','ocena']].sum()
    df.loc['Σ'] = ['Razem'] + suma.tolist()

    print("\n=== RAPORT TESTOWY ===")
    print(df.to_string(index=False))
    df.to_csv(os.path.join(data_dir, 'raport.csv'), index=False)

if __name__ == "__main__":
    main()
