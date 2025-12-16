# task2_binary_search.py
# ДЗ4 — Завдання 2: двійковий пошук для відсортованого масиву дробових чисел

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0

    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        # якщо x більше за значення посередині списку — шукаємо праворуч
        if arr[mid] < x:
            low = mid + 1
        else:
            # arr[mid] >= x — це кандидат на upper_bound, пробуємо знайти ще менший ліворуч
            upper_bound = arr[mid]
            high = mid - 1

    return iterations, upper_bound


def main():
    numbers = [0.5, 1.2, 2.4, 3.3, 4.4, 6.8, 10.1]

    print(binary_search(numbers, 4.4))   # (ітерації, 4.4)
    print(binary_search(numbers, 4.5))   # (ітерації, 6.8)
    print(binary_search(numbers, 0.1))   # (ітерації, 0.5)
    print(binary_search(numbers, 999))   # (ітерації, None)

    # прості перевірки
    assert binary_search(numbers, 4.4)[1] == 4.4
    assert binary_search(numbers, 4.5)[1] == 6.8
    assert binary_search(numbers, 0.1)[1] == 0.5
    assert binary_search(numbers, 999)[1] is None

if __name__ == "__main__":
    main()
