import server_logger
import threading

class handler():
    def __init__(self):
        self.logger = server_logger.get_logger('handler')
        self.logger.info("Handler class instantiating")
        self.health_status = 200

    def get_greeting_message(self):
        return "Hello, World"

    def get_health_status(self):
        return self.health_status

    def shutdown(self):
        self.logger.info("Shutting down handler class")


class factory():
    instance = None
    lock = threading.RLock()

    @staticmethod
    def get_instance():
        if factory.instance is None:
            with factory.lock:
                if factory.instance is None:
                    factory.instance = handler()

        return factory.instance
