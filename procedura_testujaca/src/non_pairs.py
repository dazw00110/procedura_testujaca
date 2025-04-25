'''
Funkcja sprawdzająca ile w zdyskretyzowanym systemie jest par obiektów niedeterministycznych
'''

def count_nondeterministic_pairs(disc) -> int:
    cond_cols = list(disc.columns[:-1])
    dec_col = disc.columns[-1]
    nondet_pairs = 0

    for _, group in disc.groupby(cond_cols):
        n = len(group)
        if n < 2:
            continue
        total_pairs = n * (n - 1) // 2
        same_pairs = sum(cnt * (cnt - 1) // 2 for cnt in group[dec_col].value_counts())
        nondet_pairs += (total_pairs - same_pairs)

    print(f"Liczba par niedeterministycznych: {nondet_pairs}")
    return nondet_pairs