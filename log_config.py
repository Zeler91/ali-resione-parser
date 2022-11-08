import logging

with open('./data/app.log', 'w') as log_file:
    log_file.write('Log file for Resione parser \n \n')
log_file.close()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('./data/app.log', 'a')
formatter = logging.Formatter(datefmt='%a, %d %b %Y %H:%M:%S', 
                              fmt='%(levelname)s: %(name)s - %(asctime)s -  %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)