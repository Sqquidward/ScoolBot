# s=  "('10m2',)"
import datetime
# s=s[:-4][-3:]
# import sqlite3
#
## cursor = base.cursor()
#
# base.execute('CREATE TABLE IF NOT EXISTS data(login PRIMARY KEY, class text)')
# base.commit()
#
# r = cursor.execute('SELECT class FROM data WHERE login == ?', ('816550783',)).fetchone()
#
# print(r)

today = datetime.datetime.today().weekday()


# 1 урок 08.45-9.30
# 2 урок 09.45-10.30
# 3 урок 10.40-11.25'
# 4 урок 11.35-12.20
# 5 урок 12.45-13.30
# 6 урок 13.55-14.40'
# 7 урок 14.50-15.35
# 8 урок 15.45-16.30'

def Time(digit):
    # now = datetime.datetime.now()
    #
    # digit = now.hour*100+now.minute

    count = int(str(digit)[-2:])

    if digit >= 845 and digit<= 930:
        # 1 урок
        lesson = '1 урок'
        if digit<=860:
            time = 60-count+30
        else:
            time = 30-count
        return lesson, time

    elif digit >= 945 and digit <= 1030:
        # 2 урок
        lesson = '2 урок'
        if digit<=960:
            time = 60-count+30
        else:
            time = 30-count
        return lesson, time

    elif digit >= 1040 and digit <= 1125:
        # 3 урок
        lesson = '3 урок'
        if digit<=1060:
            time = 60-count+25
        else:
            time = 25-count
        return lesson, time

    elif digit >= 1135 and digit <= 1220:
        # 4 урок
        lesson = '4 урок'
        if digit<1160:
            time = 60-count+20
        else:
            time = 20-count
        return lesson, time

    elif digit >= 1245 and digit <= 1330:
        # 5 урок
        lesson = '5 урок'
        if digit<=1260:
            time = 60-count+30
        else:
            time = 30-count
        return lesson, time

    elif digit >= 1355 and digit <= 1440:
        # 6 урок
        lesson = '6 урок'
        if digit<=1360:
            time = 60-count+40
        else:
            time = 40-digit[-2:]
        return lesson, time

    elif digit >= 1450 and digit <= 1535:
        # 7 урок
        lesson = '7 урок'
        if digit<=1460:
            time = 60-count+35
        else:
            time = 35-count
        return lesson, time

    elif digit >= 1545 and digit <= 1630:
        # 8 урок
        lesson = '8 урок'
        if digit<=1560:
            time = 60-count+30
        else:
            time = 30-count
        return lesson, time

    elif digit>1630:
        return 'Уроки кончились'

    else:
        return 'Сейчас перемена'



print(Time(int(input())))




