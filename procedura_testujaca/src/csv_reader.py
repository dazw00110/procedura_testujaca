'''
Wczytuje plik .csv i zwraca dane jako listę słowników.
'''
import csv

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
