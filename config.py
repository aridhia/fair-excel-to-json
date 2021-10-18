import logging, datetime

def log_message(statement):
    logging.info(statement)
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print(date_time + "\t" + str(statement))