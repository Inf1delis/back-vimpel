# -*- coding: utf-8 -*-

import logging
import logging.handlers
from logging.config import dictConfig

from telegram_bot.bot import bot

logger = logging.getLogger(__name__)


def new_exception(msg, *args, exc_info=True, **kwargs):
    logger.error(msg, *args, exc_info=exc_info, **kwargs)
    text = 'New error found: ' + str(msg)
    bot.send_message(chat_id=197079657, text=text)


logger.exception = new_exception

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}


def configure_logging(logfile_path):
    """
    Initialize logging defaults for Project.

    :param logfile_path: logfile used to the logfile
    :type logfile_path: string

    This function does:

    - Assign INFO and DEBUG level to logger file handler and console handler

    """
    dictConfig(DEFAULT_LOGGING)

    default_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

    file_handler = logging.handlers.RotatingFileHandler(logfile_path, maxBytes=10485760, backupCount=300,
                                                        encoding='utf-8')
    file_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)

    file_handler.setFormatter(default_formatter)
    console_handler.setFormatter(default_formatter)

    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)
