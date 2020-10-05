import logging
import logging.handlers
import datetime

path_root = 'H:/'
file_name = 'fa.log'
file_path = path_root + file_name

if __name__ == '__main__':
    logger = logging.getLogger('falogger')
    logger.setLevel(logging.DEBUG)

    #  0 o'clock rotating everyday
    # rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7,
    #                                                        atTime=datetime.time(0, 0, 0, 0))
    # rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # f_handler = logging.FileHandler(file_path)
    # backup-size 1M
    f_handler = logging.handlers.RotatingFileHandler(file_path, maxBytes=1*1024*1024, backupCount=10)
    f_handler.setLevel(logging.DEBUG)

    # f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # logger.addHandler(rf_handler)
    logger.addHandler(f_handler)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')