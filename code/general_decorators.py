import time
from datetime import datetime
from rich import pretty, print
import dotenv
import os

dotenv.load_dotenv()
DEBUG = os.getenv('DEBUG')

def printer(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result)
        return result
    return wrapper

def logger(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        if DEBUG == 'True':
            inicio = time.time()
            print(f'[{datetime.today().replace(microsecond=0)}] Starting function "{func.__name__}"...')
            result = func(*args, **kwargs)
            print(f'[{datetime.today().replace(microsecond=0)}] Function "{func.__name__}" execution time: {round(time.time()-inicio, 1)} seconds')
            return result

        else:
            result = func(*args, **kwargs)
            return result
            
    return wrapper