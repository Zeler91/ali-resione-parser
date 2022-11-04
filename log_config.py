import logging

log_file_name = 'app.log'
with open(log_file_name, 'w') as log_file:
    log_file.write('Log file for Resione parser \n \n')
log_file.close()

logging.basicConfig(datefmt='%a, %d %b %Y %H:%M:%S', level=logging.INFO, filename=log_file_name, format='%(levelname)s: %(name)s - %(asctime)s -  %(message)s')