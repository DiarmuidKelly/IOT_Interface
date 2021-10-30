import os
import shutil
import sqlite3
import datetime


class SQLLiteDBDriver:
    def __init__(self, path_to_db="./data", persistence=False):
        self.persistence = persistence
        if not persistence:
            self.__clear_db(path_to_db)
        if not os.path.exists(path_to_db):
            os.mkdir(path_to_db)
        self.path_to_db = path_to_db + '/main.db'

    def setup_table(self, table_name, keys):
        if not self.persistence:
            db_connection = sqlite3.connect(self.path_to_db)
            cur = db_connection.cursor()
            cur.execute('''CREATE TABLE {}
                           (id integer primary key autoincrement, 
                           date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                           {})'''.format(table_name, keys))

            db_connection.commit()
            db_connection.close()

    def __clear_db(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)

    def __prune_records(self, table_name, queue_length=50):
        db_connection = sqlite3.connect(self.path_to_db)
        cur = db_connection.cursor()
        cur.execute("SELECT Count() FROM {}".format(table_name))
        numberOfRows = cur.fetchone()[0]
        if numberOfRows > queue_length:
            cur.execute("SELECT * FROM {} ORDER BY {} ASC LIMIT {};".format(table_name, "id", numberOfRows - queue_length))
            row_ids = cur.fetchall()
            for row in row_ids:
                cur.execute("DELETE FROM {} WHERE id = {}".format(table_name, row[0]))
        db_connection.commit()
        db_connection.close()

    def add_record(self, table_name, data, caller, Log_level, queue_length=50):
        db_connection = sqlite3.connect(self.path_to_db)
        cur = db_connection.cursor()
        db_string = "INSERT INTO {}(date, data, caller, log_level) VALUES (?,?,?,?)".format(table_name)
        cur.execute(db_string, (str(datetime.datetime.now()), str(data), str(caller), str(Log_level)))
        db_connection.commit()
        db_connection.close()
        self.__prune_records(table_name, queue_length)

    def get_records(self, table_name, log_level=1):
        ret = []
        db_connection = sqlite3.connect(self.path_to_db)
        cur = db_connection.cursor()
        for itm in cur.execute('SELECT * FROM {}'.format(table_name)):
            ret.append(itm)
        db_connection.commit()
        db_connection.close()
        return ret
