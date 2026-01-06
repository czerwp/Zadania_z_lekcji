import sys
import csv
import json
import pickle
import os


class plik:
    def __init__(self):
        self.data = []

    def load(self, file_path):
        raise NotImplementedError("Metoda load musi być zaimplementowana w klasie pochodnej")

    def save(self, file_path, data):
        raise NotImplementedError("Metoda save musi być zaimplementowana w klasie pochodnej")

    def modify(self, changes):
        for change in changes:
            try:
                x, y, value = change.split(',')
                x, y = int(x), int(y)
                if y < len(self.data) and x < len(self.data[y]):
                    self.data[y][x] = str(value)
                else:
                    print(f"Ostrzeżenie: Współrzędne {x},{y} poza zakresem.")
            except ValueError:
                print(f"Błąd: Niepoprawny format zmiany '{change}'.")

    def display(self):
        for row in self.data:
            print(",".join(map(str, row)))


class CSV_plik(plik):
    def load(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as f:
            self.data = list(csv.reader(f))

    def save(self, file_path, data):
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)


class JSON_plik(plik):
    def load(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def save(self, file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)


class TXT_plik(plik):
    def load(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = [line.strip().split(',') for line in f]

    def save(self, file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            for row in data:
                f.write(",".join(map(str, row)) + "\n")


class Pickle_plik(plik):
    def load(self, file_path):
        with open(file_path, 'rb') as f:
            self.data = pickle.load(f)

    def save(self, file_path, data):
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)


def typy(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    handlers = {
        '.csv': CSV_plik(),
        '.json': JSON_plik(),
        '.txt': TXT_plik(),
        '.pickle': Pickle_plik()
    }
    return handlers.get(extension)


def main():
    if len(sys.argv) < 3:
        print(r"Błąd: Za mało argumentów. Wpis w konsoli powinien wyglądać w następujący sposób: python .\{ścieżka w której znajduje się plik z kodem programu}\'nazwa pliku z programem' in.csv out.csv x,y,wartość")
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    changes = sys.argv[3:]

    input_handler = typy(input_path)
    output_handler = typy(output_path)

    if not input_handler or not output_handler:
        print("Błąd: Nieobsługiwany format pliku.")
        return

    if not os.path.exists(input_path):
        print(f"Błąd: Plik {input_path} nie istnieje.")
        return

    input_handler.load(input_path)
    input_handler.modify(changes)
    input_handler.display()

    output_handler.save(output_path, input_handler.data)
    print(f"\n Zapisano do {output_path}")


if __name__ == "__main__":
    main()