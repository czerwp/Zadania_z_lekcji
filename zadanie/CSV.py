import sys
import csv
import os


def main():
    if len(sys.argv) < 3:
        print("Błąd: Za mało argumentów. Wpis w konsoli powinien wyglądać w następujący sposób:  python .\{ścieżka w której znajduje się plik z kodem programu}\CSV.py in.csv out.csv x,y,wartość")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    changes = sys.argv[3:]

    if not os.path.exists(input_file):
        print(f"Błąd! Plik wejściowy '{input_file}' nie istnieje.")
        return

    data = []
    try:
        with open(input_file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
    except Exception as wyjatek:
        print(f"Błąd podczas odczytu pliku: {wyjatek}")
        return

    for change in changes:
        try:
            parts = change.split(',')
            if len(parts) != 3:
                print(f"Pominięto błędną zmianę: {change} (wymagany format x,y,wartosc)")
                continue

            x = int(parts[0])
            y = int(parts[1])
            new_value = parts[2]

            if y < len(data) and x < len(data[y]):
                data[y][x] = new_value
            else:
                print(f"Błąd, współrzędne {x},{y} poza zakresem pliku.")
        except ValueError:
            print(f"Błąd, współrzędne w '{change}' muszą być liczbami całkowitymi.")

    print("\n Zawartość po modyfikacji:")
    for row in data:
        print(",".join(row))

    try:
        with open(output_file, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"\n Zmiany zapisane w '{output_file}'.")
    except Exception as e:
        print(f"Błąd podczas zapisu pliku: {e}")


if __name__ == "__main__":
    main()