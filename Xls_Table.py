import openpyxl


class Table:
    def Get_Raspisanie(self):
        book = openpyxl.open("Raspisanie.xlsx", read_only=True)
        return book

    def Get_Chetnost(self):
        table = openpyxl.open("Четность.xlsx", read_only=True)
        sheet = table.active
        return sheet
