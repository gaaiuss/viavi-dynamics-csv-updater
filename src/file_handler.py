import csv

import openpyxl

from path_vars import COUNTER, NT_FND_CNTR, ROOT_CSV, TARGET_CSV, TARGET_XLSX


class FileHandler:
    def __init__(self) -> None:
        self.counter = 0
        self.setup()

    def setup(self) -> None:
        if not TARGET_CSV.exists():
            self.set_header()  # Setup csv target file header
        if not COUNTER.exists():
            self.set_counter()  # Set counter.csv file
        if not NT_FND_CNTR.exists():
            self.set_not_found_counter()  # Setup csv target file header
        else:
            # If already set up, counts the csv lines
            self.counter = self.count()

    def get_pn_list(self) -> list[str]:
        pn_list: list[str] = []
        with open(ROOT_CSV) as f:
            r = csv.reader(f, delimiter=",")
            next(r)
            for row in r:
                pn_list.append(row[0])

        return pn_list

    def set_header(self) -> None:
        with open(ROOT_CSV) as file:
            reader = csv.reader(file)
            with open(TARGET_CSV, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(next(reader)[:3])

    def update_csv(self, row_data: list[str]) -> None:
        with open(TARGET_CSV, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row_data)

    def set_counter(self) -> None:
        with open(COUNTER, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["PN"])

    def set_not_found_counter(self) -> None:
        with open(NT_FND_CNTR, "w", newline=""):
            ...

    def count(self) -> int:
        with open(COUNTER, newline="") as file:
            reader = csv.reader(file)
            return sum(1 for row in reader) - 1  # type: ignore

    def add_count(self, content: int) -> None:
        with open(COUNTER, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([content])

    def add_not_found_count(self, content: int) -> None:
        with open(NT_FND_CNTR, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([content])

    def csv_to_excel(self) -> None:
        wb = openpyxl.Workbook()
        ws = wb.active

        with open(TARGET_CSV, newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if ws is not None:
                    ws.append(row)

        if ws is not None:
            for row in range(2, ws.max_row + 1):
                cell = ws.cell(row=row, column=3)
                cell.value = float(cell.value)  # type: ignore

        wb.save(TARGET_XLSX)
