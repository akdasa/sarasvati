import logging
import traceback


def show(ex):
    logging.exception(ex)
    print(traceback.format_exc())
