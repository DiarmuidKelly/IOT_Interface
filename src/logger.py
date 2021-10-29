import datetime
import os
import shutil
import sqlite3
import time


class Logger:
    def __init__(self, queue_length=500, path_to_logs="./logs"):
        self.__clear_logs("./logs")
        os.mkdir(path_to_logs)
        self.path_to_logs = path_to_logs + '/main.db'
        self.__setup_db()
        self.queue_length = queue_length

    def __setup_db(self):
        time.sleep(2)
        db_connection = sqlite3.connect(self.path_to_logs)
        cur = db_connection.cursor()
        cur.execute('''CREATE TABLE logs
                       (date text, data text, caller text, log_level text)''')

        db_connection.commit()
        db_connection.close()

    def __clear_logs(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)

    def __add_to_log(self, data, caller, Log_level):
        db_connection = sqlite3.connect(self.path_to_logs)
        cur = db_connection.cursor()
        db_string = "INSERT INTO logs(date, data, caller, log_level) VALUES (?,?,?,?)"
        vals = [str(datetime.datetime.now()), str(data), str(caller), str(Log_level)]
        cur.execute(db_string, vals)
        db_connection.commit()
        db_connection.close()

    def print_logs(self, log_level=1):
        ret = []
        db_connection = sqlite3.connect(self.path_to_logs)
        cur = db_connection.cursor()
        for itm in cur.execute('SELECT * FROM logs'):
            ret.append(itm)
        db_connection.commit()
        db_connection.close()
        return ret

    def debug(self, data, caller):
        self.__add_to_log(data, caller, "DEBUG")

    def info(self, data, caller):
        self.__add_to_log(data, caller, "INFO")

    def warn(self, data, caller):
        self.__add_to_log(data, caller, "WARN")

    def error(self, data, caller):
        self.__add_to_log(data, caller, "ERROR")


