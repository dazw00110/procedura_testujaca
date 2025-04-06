'''
To punkt startowy programu. Łączy wszystkie pozostałe moduły.
'''
import csv_reader, verifier, performance, report

def main():
    path = input("Podaj ścieżkę do pliku CSV: ")
    data = csv_reader.read_csv(path)

    valid_data, errors = verifier.check_data(data)
    stats = performance.evaluate(data, errors)

    report.generate(stats, errors)
    print("Gotowe. Raport zapisano.")

if __name__ == "__main__":
    main()
