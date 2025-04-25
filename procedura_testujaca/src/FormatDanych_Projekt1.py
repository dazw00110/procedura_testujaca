# Zespol przygotowujacy algorytm dyskretyzacji danych otrzyma dane w formacie plików csv.
# Każdy plik będzie zawierał ustaloną liczbę wierszy i kolumn (w każdym wierszu tyle samo, bez wartości brakujących). 
# Ostatnia kolumna to decyzja, pozostałe kolumny to atrybuty warunkowe, wszystkie nadające się do dyskretyzacji.
# Do algorytmu dyskretyzującego należy przekazać ścieżkę do pliku z danymi w formacie csv jako argument metody.
# Dane wyjściowe z algorytmu powinny być zapisane na dysku, w tym samym folderze, co plik wejściowy, w formacie csv.
# Zespół testujący wczytuje zdyskretyzowane dane z csv z dysku.

# Dla przykładowych danych:
# TO NIE JEST FORMAT W JAKIM DANE ZOSTANĄ DOSTARCZONE DO ALGORYTMU TNĄCEGO
#  x1 |  x2 | Decyzja
# 0.9 | 6.2 | 3
# 2.7 | 6.2 | 2
# 2.7 | 2.1 | 1
# 1.2 | 4.5 | 2
# 3.3 | 6.8 | 2
# 4.3 | 4.5 | 1
# 1.2 | 6.2 | 3

# TAK WYGLĄDAJĄ DANE ZDYSKRETYZOWANE KTÓRE POWINNY SIĘ ZNALEŹĆ W ZWRACANYM PLIKU CSV:
# (-inf; 1.95],(5.35; inf),3
# (1.95; inf),(5.35; inf),2
# (1.95; inf),(-inf; 5.35],1
# (-inf; 1.95],(-inf; 5.35],2
# (1.95; inf),(5.35; inf),2
# (1.95; inf),(-inf; 5.35],1
# (-inf; 1.95],(5.35; inf),3

# Interpretacja: W każdym wierszu każda wartość każdego atrybutu jest przedziałem pomiędzy lewym cięciem i prawym cięciem. 
# (Jeśli w prawo lub w lewo nie ma cięcia to podawana jest wartość inf lub -inf). Jeśli na jakimś atrybucie nie zostało wybrane 
# żadne cięcie, to cała kolumna odpowiadająca temu atrybutowi będzie mieć następującą postać w zwracanym pliku: (-inf; inf)
# Przedziały są oznaczone w formacie (a, b] co oznacza że a nie należy do przedziału natomiast b należy do przedziału
# W ostatniej kolumnie znajdują się oryginalne wartości decyzji.

# Zespół testujący otrzyma dane oryginalne oraz zdyskretyzowane. Zadaniem zespołu testującego będzie:
# -sprawdzić czy rozmiar danych zdyskretyzowanych jest taki sam jak oryginalnych (tzn. czy nie dodano lub nie usunięto danych). Jeśli nie - STOP
# -sprawdzić, czy dla każdego obiektu i-tego w oryginalnym systemie decyzyjnym i dla jego wartości na każdym j-ym atrybucie, wartość ta  należy do j-ego przedziału 
#  w danych zdyskretyzowanych (tzn. czy dyskretyzacja jest prawidłowa). Jeśli nie - STOP
# -wyliczyć i zwrócić ile w zdyskretyzowanym systemie jest par obiektów niedeterministycznych (Liczba par obiektów niedeterministycznych w oryginalnych danych będzie znana)
# -wyznaczyć i zwrócić czas dyskretyzacji
# -wyliczyć i zwrócić liczbę cięć użytych do dyskretyzacji (łącznie na wszystkich atrybutach warunkowych).

# Pliki z danymi powinny nazywać się: data1.csv, data2.csv, data3.csv, ...
# Pliki ze zdyskretyzowanymi danymi powinny nazywać się: DISCdata1.csv, DISCdata2.csv, DISCdata3.csv, ...

# Przykładowa sesja testowa:

data_paths = ['data1.csv', 'data2.csv', 'data3.csv']
desc_data_paths = ['DISCdata1.csv', 'DISCdata2.csv', 'DISCdata3.csv']

# Przed testem każdego algorytmu należy pamiętać o wyczyszczeniu poprzednich plików DISCdata

timer.start()
for data in data_paths:
    Algorithm.example_algorithm(data) # Do algorytmu dyskretyzującego podana jest ścieżka do pliku z danymi w formacie csv
                                      # Algorytm dyskretyzujący niczego nie zwraca, tylko zapisuje dane na dysku w formacie csv
timer.stop()

for disc_data in disc_data_paths:
    Tests.test_algorithm(disc_data)