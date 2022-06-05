import openpyxl
import datetime

book = openpyxl.open("Четность.xlsx", read_only=True)
sheet = book.active

now = datetime.datetime.now()

# text = input(": ")
#sheet[f'{chr(j)}3'].value
# print("Предмет: "+sheet[text].value[:-4]+"\nКласс: "+sheet[text].value[-3:])

# print(sheet['A1'].value)

# print(chr(65)) --- A



def Parity():
    now = datetime.datetime.now()
    try:
        for i in range(2, 9):
            if now.day - 1 <= sheet[f'{chr(66)}{i}'].value and now.month == sheet[f'{chr(65)}{i}'].value:
                return sheet[f'{chr(67)}{i}'].value
    except:
        pass

print(Parity())










