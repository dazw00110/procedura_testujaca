'''
Tworzy raport tekstowy na podstawie wyników.
'''
def generate(stats, errors):
    with open("reports/raport.txt", "w", encoding="utf-8") as f:
        f.write("=== RAPORT ===\n")
        f.write(f"Czas działania: {stats['czas']} s\n")
        f.write(f"Liczba wierszy: {stats['wiersze']}\n")
        f.write(f"Liczba błędów: {stats['błędy']}\n\n")
        f.write("Błędne wiersze:\n")
        for idx, row in errors:
            f.write(f"{idx}: {row}\n")
