import logging

# Configure the logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

# Create a file handler (logs will be saved to 'app.log')
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)  # Set the file handler to capture DEBUG level logs

# Create a formatter for the log entries
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Optionally, prevent log messages from being duplicated by other loggers
logger.propagate = False
