import sqlite3

class DataBase:
    def cur_Main_DB(self):
        base_main = sqlite3.connect('group_main.db')
        cursor_main = base_main.cursor()
        base_main.execute('CREATE TABLE IF NOT EXISTS data(login PRIMARY KEY, class VARCHAR)')
        base_main.commit()
        return cursor_main

    def get_Main_DB(self):
        base_main = sqlite3.connect('group_main.db')
        return base_main

    def cur_Zamena_DB(self):
        base_zamena = sqlite3.connect('group_zamena.db')
        cursor_db = base_zamena.cursor()
        base_zamena.execute('CREATE TABLE IF NOT EXISTS data(login text, class text)')
        base_zamena.commit()
        return cursor_db

    def get_Zamena_DB(self):
        base_zamena = sqlite3.connect('group_zamena.db')
        return base_zamena