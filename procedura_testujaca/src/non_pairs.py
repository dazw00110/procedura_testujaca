#funkcja do policzenia par niedeterministycznych
def count_nondeterministic_pairs(disc) -> int:
    cond_cols = list(disc.columns[:-1]) #atrybuty warunkowe
    dec_col = disc.columns[-1] #atrybuty decyzyjne
    nondet_pairs = 0
    for _, group in disc.groupby(cond_cols):
        n = len(group)
        if n < 2:
            continue
        class_counts = group[dec_col].value_counts()
        same_pairs = sum(cnt * (cnt - 1) // 2 for cnt in class_counts)
        total_pairs = n * (n - 1) // 2
        nondet_pairs += (total_pairs - same_pairs)
    return nondet_pairs