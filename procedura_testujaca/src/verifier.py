'''
Sprawdza poprawność danych, np. czy wymagane pola nie są puste.
'''
def check_data(data):
    errors = []
    valid_data = []

    for idx, row in enumerate(data):
        if not row["nazwa"] or not row["id"].isdigit():
            errors.append((idx + 1, row))
        else:
            valid_data.append(row)

    return valid_data, errors
