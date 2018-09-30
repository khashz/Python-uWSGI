import logging

def get_logger(logger_name):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)03d  %(name)-10s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='server_logs.log',
                        filemode='w')
    logger = logging.getLogger(logger_name)
    return logger
