"""
Configure root logger.
"""

import logging


def setup_root_logger(log_file):
    """
    Function configure logging handlers.
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    log_file_all = log_file.replace(".log", "_all.log")
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_file, encoding="utf-8")
    f_handler_all = logging.FileHandler(log_file_all, encoding="utf-8")

    # Set severity level for each handler
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.INFO)
    f_handler_all.setLevel(logging.DEBUG)

    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)
    f_handler_all.setFormatter(log_format)

    root.addHandler(c_handler)
    root.addHandler(f_handler)
    root.addHandler(f_handler_all)
    return root
