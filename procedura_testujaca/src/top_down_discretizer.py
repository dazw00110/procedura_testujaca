import os
from collections import deque
import numpy as np
import pandas as pd


# Główna funkcja dyskretyzacji zstępującej
def top_down_discretization(data_path, min_samples = 5):
    data = load_data(data_path)
    attributes = data.columns[:-1]
    decision_col = data.columns[-1]
    y = data[decision_col].values

    cuts_dict = {}
    for col in attributes:
        x = data[col].values
        cuts = top_down_cuts(x, y, min_samples)
        cuts_dict[col] = cuts

    disc_data = pd.DataFrame()
    for col in attributes:
        col_cuts = cuts_dict[col]
        if col_cuts:
            disc_data[col] = apply_cuts(data[col].values, col_cuts)
        else:
            disc_data[col] = ["(-inf; inf)" for _ in range(len(data))]
    disc_data[decision_col] = data[decision_col]

    # Zapis do pliku
    save_result(data_path, disc_data)


# Funkcja znajdująca punkty cięcia przedziałów
def top_down_cuts(x, y, min_samples = 5):
    # Kryterium podstawowe - liczba odseparowanych par (Oblicza liczbę różnych klas w lewym i prawym segmencie)
    def separated_pairs(left_counts, right_counts):
        total_left = left_counts.sum()
        total_right = right_counts.sum()
        # Wszystkie pary poza tymi w których klasa jest ta sama
        same_class_pairs = np.sum(left_counts * right_counts)
        return total_left * total_right - same_class_pairs

    # Kryterium dodatkowe - entropia (Oblicza entropię z tablicy counts (liczba próbek dla każdej klasy) i całkowitej liczby próbek)
    def entropy(counts, total):
        # Prawdopodobieństwa klas
        probs = counts / total
        # Tylko elementy > 0 żeby uniknąć log2(0)
        mask = probs > 0
        return -np.sum(probs[mask] * np.log2(probs[mask]))


    # Sortowanie wartości x oraz y
    order = np.argsort(x)
    x_sorted = x[order]
    y_sorted = y[order]

    n = len(x_sorted)
    # Kodowanie klas jako 0 ... K-1
    unique_classes, y_codes = np.unique(y_sorted, return_inverse=True)
    n_classes = unique_classes.shape[0]

    # Macierz one-hot i prefixowe sumy liczebności klas
    Y = np.eye(n_classes, dtype=int)[y_codes]
    prefix_counts = np.vstack([
        np.zeros(n_classes, dtype=int),
        np.cumsum(Y, axis=0)
    ])

    # Indeksy w których zmienia się klasa (Ograniczenie liczby kandydatów do cięcia)
    changes = np.where(y_codes[1:] != y_codes[:-1])[0] + 1

    cuts = []
    queue = deque([(0, n)])  # Segmenty jako (start, end)

    while queue:
        start, end = queue.popleft()
        length = end - start
        # Odrzucenie krótkich segmentów
        if length < 2 * min_samples:
            continue

        # Entropia oraz odseparowane pary segmentu bazowego
        total_counts_seg = prefix_counts[end] - prefix_counts[start]
        total_sep_pairs = separated_pairs(total_counts_seg, total_counts_seg)
        base_ent = entropy(total_counts_seg, length)

        best_score = 0.0
        best_i = None

        # Przegląd kandydatów
        for i in changes:
            if i <= start or i >= end:
                continue
            left_n = i - start
            right_n = end - i
            if left_n < min_samples or right_n < min_samples:
                continue

            left_counts = prefix_counts[i] - prefix_counts[start]
            right_counts = total_counts_seg - left_counts

            # Obliczenie kryterium podstawowego - Liczba odseparowanych klas
            sep_score = separated_pairs(left_counts, right_counts) / total_sep_pairs if total_sep_pairs > 0 else 0

            # Obliczenie kryterium dodatkowego - Entropia
            entropy_left = entropy(left_counts, left_n)
            entropy_right = entropy(right_counts, right_n)
            info_gain = base_ent - (left_n / length * entropy_left + right_n / length * entropy_right)

            combined_score = info_gain + sep_score

            if combined_score > best_score:
                best_score = combined_score
                best_i = i

        # Podział i rekurencja jeśli znaleziono dobry punkt cięcia
        if best_i is not None and best_score > 0:
            cut_val = round((x_sorted[best_i - 1] + x_sorted[best_i]) / 2.0, 2)
            cuts.append(cut_val)
            queue.append((start, best_i))
            queue.append((best_i, end))

    return sorted(set(cuts))


# Funkcja przypisująca przedział tekstowy każdej wartości x
def apply_cuts(x, cuts):
    bins = np.array([-np.inf] + cuts + [np.inf])
    # np.digitize zwraca indeksy przedziałów od 1 do len(bins)-1 (poza -inf i inf)
    bin_idx = np.digitize(x, bins[1:-1], right=True)
    labels = []
    for i in range(len(bins) - 1):
        left = "-inf" if i == 0 else f"{bins[i]:.2f}"
        right = "inf)" if i == len(bins) - 2 else f"{bins[i + 1]:.2f}]"
        labels.append(f"({left}; {right}")

    return [labels[i] for i in bin_idx]

# Funkcja wczytująca dane z pliku
def load_data(file_path: str) -> pd.DataFrame:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Plik {file_path} nie istnieje.")

    with open(file_path, 'r') as f:
        first_line = f.readline().strip().split(',')

    is_header = any(not val.replace(',', '').replace('.', '').isdigit() for val in first_line)

    skip_rows_option = 1 if is_header else 0

    df = pd.read_csv(file_path, sep=',', decimal='.', engine='python', header = None, skiprows = skip_rows_option)

    return df

# Funkcja zapisu do pliku
def save_result(data_path, disc_data):
    folder, file_name = os.path.split(data_path)
    result_path = os.path.join(folder, f"DISC{file_name}")
    disc_data.to_csv(result_path, index=False, header=False)
