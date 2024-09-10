""" This logger was created is an improvement
on the default logger that comes with flask"""

import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(app):

    """ The function  implements improvements on flask's default logger.
    its sets the logging level,specifiesthe format of log
    the log messages,ensures that log file size don't
     exceed 10kb and stores upto 10 log files  """

    # Ensuring log directory exists
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Setting the logging level
    app.logger.setLevel(logging.INFO)

    # Creating a rotating file handler
    file_handler = RotatingFileHandler('logs/shortit.log', maxBytes=10240, backupCount=10)

    # Creating a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Added handlers to the logger
    app.logger.addHandler(file_handler)

    # Log
    app.logger.info('Logger setup completed')
