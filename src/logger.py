class Logger:
    def __init__(self, db_driver, queue_length=500):
        self.table_name = "logs"
        self.queue_length = queue_length
        self.sqllite_driver = db_driver
        self.sqllite_driver.setup_table(self.table_name, "data text, caller text, log_level text")

    def print_logs(self, log_level=1):
        return self.sqllite_driver.get_records(self.table_name, log_level=log_level)

    def debug(self, data, caller):
        self.sqllite_driver.add_record(self.table_name, data, caller, "DEBUG", self.queue_length)

    def info(self, data, caller):
        self.sqllite_driver.add_record(self.table_name, data, caller, "INFO", self.queue_length)

    def warn(self, data, caller):
        self.sqllite_driver.add_record(self.table_name, data, caller, "WARN", self.queue_length)

    def error(self, data, caller):
        self.sqllite_driver.add_record(self.table_name, data, caller, "ERROR", self.queue_length)
