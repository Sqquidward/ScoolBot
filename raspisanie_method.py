from datetime import datetime


class Raspisanie:
    def do_Smt(text, i):
        try:
            for page_Num in range(0, 9):
                for char in range(66, 79):
                    if book.worksheets[page_Num][f'{chr(char)}9'].value == text:
                        print(' Я нашел')
                        return Raspisanie.Subject_today(page_Num, char, i)

        except Exception as ex:
            return 'Произошла ошибка', ex


    def Subject_today(page_Num, char, i):
        if Raspisanie.Parity() == 'ч':
            page_Num+=1
        integer = [11, 21, 31, 42, 52, 62]
        today = datetime.datetime.today().weekday()
        if today == 5 and i == 1:
            today = 0; i = 0
        tod = Days(today, i)
        print('Hey')
        try:
            print('Bro')
            les = ''
            les += '1. '+book.worksheets[page_Num][f'{chr(char)}{integer[tod+i]}'].value + '\n'
            print(les+'1')
            les += '2. '+book.worksheets[page_Num][f'{chr(char)}{integer[tod+i] + 2}'].value + '\n'
            print(les+'2')
            les += '3. '+book.worksheets[page_Num][f'{chr(char)}{integer[tod+i] + 5}'].value + '\n'
            print(les)
            les += '4. '+book.worksheets[page_Num][f'{chr(char)}{integer[tod+i] + 7}'].value + '\n'
            print('Hey bro')
            print(les)
        except Exception as ex:
            pass
        return les

    def Parity(self):
        now = datetime.datetime.now()
        try:
            for i in range(2, 9):
                if now.day - 1 <= sheet[f'{chr(66)}{i}'].value and now.month == sheet[f'{chr(65)}{i}'].value:
                    return sheet[f'{chr(67)}{i}'].value
        except:
            pass
