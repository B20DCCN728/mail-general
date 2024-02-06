import colorlog
import logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s:%(levelname)s: %(message)s'))

logger = logging.getLogger('ЧВК «Вагнер»')
logger.addHandler(handler)

# Set the log level to INFO
logger.setLevel(logging.INFO)

# Example usage of the logger
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')