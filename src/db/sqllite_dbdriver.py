import os
import shutil
import sqlite3
import datetime


class SQLLiteDBDriver:
    def __init__(self, queue_length=500, path_to_db="./data"):
        self.__clear_db(path_to_db)
        os.mkdir(path_to_db)
        self.path_to_logs = path_to_db + '/main.db'
        self.queue_length = queue_length

    def setup_table(self, table_name, keys):
        db_connection = sqlite3.connect(self.path_to_logs)
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

    def __prune_records(self):
        db_connection = sqlite3.connect(self.path_to_logs)
        cur = db_connection.cursor()
        rowsQuery = "SELECT Count() FROM %s" % "logs"
        cur.execute(rowsQuery)
        numberOfRows = cur.fetchone()[0]
        if numberOfRows > self.queue_length:
            cur.execute("SELECT * FROM {} ORDER BY {} ASC LIMIT {};".format("logs", "id", numberOfRows - self.queue_length))
            row_ids = cur.fetchall()
            for row in row_ids:
                cur.execute("DELETE FROM {} WHERE id = {}".format("logs", row[0]))
        db_connection.commit()
        db_connection.close()

    def add_record(self, table_name, data, caller, Log_level):
        db_connection = sqlite3.connect(self.path_to_logs)
        cur = db_connection.cursor()
        db_string = "INSERT INTO {}(date, data, caller, log_level) VALUES (?,?,?,?)".format(table_name)
        cur.execute(db_string, (str(datetime.datetime.now()), str(data), str(caller), str(Log_level)))
        db_connection.commit()
        db_connection.close()
        self.__prune_records()

    def get_records(self, table_name, log_level=1):
        ret = []
        db_connection = sqlite3.connect(self.path_to_logs)
        cur = db_connection.cursor()
        for itm in cur.execute('SELECT * FROM {}'.format(table_name)):
            ret.append(itm)
        db_connection.commit()
        db_connection.close()
        return ret
