# -*- coding: utf-8 -*-
"""
@Author     : Dr Prashant Aparajeya
                Founder & Director @AISimply Ltd
                Computer Vision Scientist
                London, United Kingdom
                
@Copyright  : Copyright 2024 - present
@Project    : Dispersive Flies Optimization (DFO) Algorithm
"""

import logging
import logging.handlers as handlers
import os

from core.config import settings

class PackagePathFilter(logging.Filter):
    def filter(self, record):
        record.relativePath = os.path.relpath(record.pathname, os.getcwd())
        return True


os.makedirs(settings.LOG_DIR, exist_ok=True)

log_level = settings.LOG_MODE

FORMAT = "[%(asctime)s] %(levelname)s {%(relativePath)s:%(lineno)d} - %(message)s"
formatter = logging.Formatter(FORMAT)

logHandler = handlers.TimedRotatingFileHandler(
    f"{settings.LOG_DIR}{settings.LOG_FILE}", when=settings.LOG_INTERVAL, interval=1, backupCount=settings.BACKUP_COUNT
)
logHandler.setFormatter(formatter)
logHandler.setLevel(log_level)
logHandler.addFilter(PackagePathFilter())

warning_log_handler = handlers.TimedRotatingFileHandler(
    f"{settings.LOG_DIR}{settings.ISSUE_FILE}", when=settings.LOG_INTERVAL, interval=1, backupCount=settings.BACKUP_COUNT
)
warning_log_handler.setFormatter(formatter)
warning_log_handler.setLevel(logging.WARNING)


def get_logger():
    logger = logging.getLogger(__name__)

    logger.setLevel(log_level)
    logger.addHandler(logHandler)
    logger.addHandler(warning_log_handler)

    logger.propagate = False

    return logger


logger = get_logger()