# task3_substring_search.py
# ДЗ4 — Завдання 3: Boyer–Moore, KMP, Rabin–Karp + timeit (без partial)

from pathlib import Path
import timeit


# ---------------- Boyer–Moore (bad character rule) ----------------
def boyer_moore(text: str, pattern: str) -> int:
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0

    last = {}
    for i, ch in enumerate(pattern):
        last[ch] = i

    shift = 0
    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            return shift

        bad_i = last.get(text[shift + j], -1)
        shift += max(1, j - bad_i)

    return -1


# ---------------- KMP ----------------
def compute_lps(pattern: str) -> list[int]:
    lps = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    return lps


def kmp_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0

    lps = compute_lps(pattern)
    j = 0

    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
            if j == len(pattern):
                return i - j + 1

    return -1


# ---------------- Rabin–Karp (base=256, mod=101) ----------------
def polynomial_hash(s: str, base=256, modulus=101) -> int:
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % modulus
    return h


def rabin_karp_search(text: str, pattern: str) -> int:
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    base = 256
    mod = 101

    p_hash = polynomial_hash(pattern, base, mod)
    w_hash = polynomial_hash(text[:m], base, mod)

    h = pow(base, m - 1, mod)

    for i in range(n - m + 1):
        if p_hash == w_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            w_hash = (w_hash - ord(text[i]) * h) % mod
            w_hash = (w_hash * base + ord(text[i + m])) % mod
            w_hash %= mod

    return -1


# ---------------- helpers ----------------
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1251", errors="ignore")


def measure(func, text: str, pattern: str, number: int) -> float:
    timer = timeit.Timer(lambda: func(text, pattern))
    return timer.timeit(number=number)


def main():
    base_dir = Path(__file__).parent

    file1 = base_dir / "стаття 1.txt"
    file2 = base_dir / "стаття 2 (1).txt"

    if not file1.exists() or not file2.exists():
        print("Не знайдено потрібні файли поруч зі скриптом:")
        print("- стаття 1.txt")
        print("- стаття 2 (1).txt")
        return

    text1 = read_text(file1)
    text2 = read_text(file2)

    existing = "бінарний пошук"
    fake = "суперсекретнийпідрядок12345"

    # Перевірки умов (щоб не було фейлу в звіті)
    if existing not in text1 or existing not in text2:
        print("Помилка: підрядок 'бінарний пошук' має бути в обох текстах, але його не знайдено.")
        print("Перевір файли або підрядок.")
        return

    if fake in text1 or fake in text2:
        print("Помилка: 'вигаданий' підрядок знайшовся в тексті(ах). Заміни fake.")
        return

    algos = [
        ("Boyer–Moore", boyer_moore),
        ("KMP", kmp_search),
        ("Rabin–Karp", rabin_karp_search),
    ]

    number = 50  # можна змінити

    results = []
    for label, text in [("Стаття 1", text1), ("Стаття 2", text2)]:
        row = {"label": label, "times_exist": {}, "times_fake": {}}

        # sanity-check
        for _, f in algos:
            assert f(text, existing) != -1
            assert f(text, fake) == -1

        for name, f in algos:
            row["times_exist"][name] = measure(f, text, existing, number)
            row["times_fake"][name] = measure(f, text, fake, number)

        results.append(row)

    # Console output
    for r in results:
        print(f"\n=== {r['label']} ===")
        for name in r["times_exist"]:
            print(f"{name}: існуючий={r['times_exist'][name]:.6f}s, вигаданий={r['times_fake'][name]:.6f}s")

        fastest_exist = min(r["times_exist"], key=r["times_exist"].get)
        fastest_fake = min(r["times_fake"], key=r["times_fake"].get)
        print("Найшвидший (існуючий):", fastest_exist)
        print("Найшвидший (вигаданий):", fastest_fake)

    # report.md
    lines = []
    lines.append("# ДЗ4 — Завдання 3 (порівняння пошуку підрядка)")
    lines.append("")
    lines.append(f"Тексти: `стаття 1.txt`, `стаття 2 (1).txt`.")
    lines.append("Підрядки:")
    lines.append(f"- **існуючий**: `{existing}`")
    lines.append(f"- **вигаданий**: `{fake}`")
    lines.append("")
    lines.append(f"Вимірювання через `timeit`, number={number}.")
    lines.append("")

    for r in results:
        lines.append(f"## {r['label']}")
        lines.append("")
        lines.append("| Алгоритм | існуючий (s) | вигаданий (s) |")
        lines.append("|---|---:|---:|")
        for name in r["times_exist"]:
            lines.append(f"| {name} | {r['times_exist'][name]:.6f} | {r['times_fake'][name]:.6f} |")
        lines.append("")
        fastest_exist = min(r["times_exist"], key=r["times_exist"].get)
        fastest_fake = min(r["times_fake"], key=r["times_fake"].get)
        lines.append(f"Найшвидший для **існуючого**: **{fastest_exist}**.")
        lines.append(f"Найшвидший для **вигаданого**: **{fastest_fake}**.")
        lines.append("")

    (base_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("\nreport.md створено.")


if __name__ == "__main__":
    main()
