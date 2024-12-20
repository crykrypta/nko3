import logging


class CustomFormatter(logging.Formatter):
    # ЦВЕТОКОДЫ (ANSI-escape codes)
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    # ФОРМАТ ДАТЫ
    DATEFMORMAT = "%m-%d %H:%M:%S"
    # СТРУКТУРА СООБЩЕНИЯ
    FORMAT = "[%(asctime)s.%(msecs)03d] %(levelname)-7s - %(module)10s:%(lineno)3d|%(funcName)-24s - %(message)s" # noqa
    # СОБРАННЫЙ ФОРМАТ (ЦВЕТОКОДЫ + СТРУКТУРА СООБЩЕНИЯ)
    FORMATS = {
        logging.DEBUG: GREY + FORMAT + RESET,
        logging.INFO: GREY + FORMAT + RESET,
        logging.WARNING: YELLOW + FORMAT + RESET,
        logging.ERROR: RED + FORMAT + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT + RESET
    }

    # Переопределяем встроенный метод format()
    # record - обьект содержащий информацию о сообщении
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.DATEFMORMAT)
        return formatter.format(record)


class LogConfig:
    """Класс конфигурации логирования
    setup_logging() - метод для настройки логирования
    """
    @staticmethod
    def setup_logging():
        """Настраивает логирование"""
        #  Получаем корневой логгер
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Handler для STDOUT (Stream Handler SH)
        sh = logging.StreamHandler()
        sh.setFormatter(CustomFormatter())

        # # Handler для записи в logfile.log
        # fh = logging.FileHandler('logfile.log', 'w', encoding='utf-8')
        # fh.setFormatter(CustomFormatter())

        # Добавляем оба Handler's
        root_logger.addHandler(sh)
        # root_logger.addHandler(fh)

        # Отключаем логирование от sqlalchemy и aiogram
        logging.getLogger('sqlalchemy.engine.Engine').disabled = True
        logging.getLogger('aiogram').setLevel(logging.WARNING)

        return logging.getLogger(__name__)
