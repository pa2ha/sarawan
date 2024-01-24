def unique_numbers_in_sequence(n):
    result = []
    for i in range(1, n + 1):
        result.extend([i] * i)
    return result[:n]


# Пример вызова функции с n = 22
n = 22
unique_numbers = unique_numbers_in_sequence(n)
print(f" {n} первых элементов последовательности это: {(unique_numbers)}")
print(f"уникальных чисел до позиции {n}: {(set(unique_numbers))}")
