from src.logger import Logger
import shutil


def test_logs_length():
    test_cleanup()
    test_logger = Logger(5, "./test_logs")
    for t in range(5):
        test_logger.info("TEST-{}".format(t), 123)
    test_logger.print_logs()
    print("---------------")
    test_logger.info("TEST-{}".format("test"), 123)
    test_logger.info("TEST-{}".format("test"), 123)
    test_logger.print_logs()


def test_cleanup():
    shutil.rmtree('./test_logs')