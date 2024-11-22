import logging

def createLogger():
    # Create a logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)  # Set the logging level for the logger

    # Create a file handler
    file_handler = logging.FileHandler('app.log')  # Log messages to a file
    file_handler.setLevel(logging.INFO)  # Set the logging level for the file handler

    # Create a console handler
    console_handler = logging.StreamHandler()  # Log messages to the console
    console_handler.setLevel(logging.INFO)  # Set the logging level for the console handler

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Add the formatter to both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

