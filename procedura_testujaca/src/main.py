'''
To punkt startowy programu. Łączy wszystkie pozostałe moduły.
'''
import csv_reader, verifier, performance, report, non_pairs

def main():

    # path = input("Podaj ścieżkę do pliku CSV z oryginalnymi danymi: ")
    # orig = csv_reader.load_dataframe(path, decimal_comma=True).astype(float)
    # path = input("Podaj ścieżkę do pliku CSV z danymi zdyskretyzowanymi: ")
    # disc = csv_reader.load_dataframe(path, decimal_comma=False)

    # valid_data, errors = verifier.check_data(data)
    # stats = performance.evaluate(data, errors)
    # report.generate(stats, errors)
    # print("Gotowe. Raport zapisano.")

    # STAŁA ŚCIEŻKA DO PLIKÓW - do testów porgramu, odkomentować w razie potrzeby
    orig = csv_reader.load_dataframe('test_data/data1.csv', decimal_comma=True).astype(float)
    disc = csv_reader.load_dataframe('test_data/DISCdata1.csv', decimal_comma=False)

    verifier.check_shape(orig, disc)
    verifier.check_intervals(orig, disc)
    non_pairs.count_nondeterministic_pairs(disc)

if __name__ == "__main__":
    main()

