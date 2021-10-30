from db.sqllite_dbdriver import SQLLiteDBDriver


class Logger:
    def __init__(self, db_driver, queue_length=500):
        self.table_name = "logs"
        self.sqllite_driver = db_driver
        self.sqllite_driver.setup_table(self.table_name, "data text, caller text, log_level text")

    def print_logs(self, log_level=1):
        return self.sqllite_driver.get_records(self.table_name, log_level=1)

    def debug(self, data, caller):
        self.sqllite_driver.add_record(self.table_name, data, caller, "DEBUG")

    def info(self, data, caller):
        self.sqllite_driver.add_record(self.table_name, data, caller, "INFO")

    def warn(self, data, caller):
        self.sqllite_driver.add_record(self.table_name, data, caller, "WARN")

    def error(self, data, caller):
        self.sqllite_driver.add_record(self.table_name, data, caller, "ERROR")
