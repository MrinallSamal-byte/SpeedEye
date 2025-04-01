import logging

def setup_logger(log_file="speedeye.log", log_level=logging.INFO):
    """
    Set up a logger for the project with console and file handlers.
    """
    logger = logging.getLogger("SpeedEyeLogger")
    logger.setLevel(log_level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

# Example usage:
# logger = setup_logger(log_level=logging.DEBUG)
# logger.info("This is an info message.")
# logger.error("This is an error message.")
