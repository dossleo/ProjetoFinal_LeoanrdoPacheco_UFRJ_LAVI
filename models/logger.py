import time
from datetime import datetime
from rich import pretty, print

def logger(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        print(f'[{datetime.today().replace(microsecond=0)}] Starting function "{func.__name__}"...')
        result = func(*args, **kwargs)
        print(f'[{datetime.today().replace(microsecond=0)}] Function "{func.__name__}" execution time: {round(time.perf_counter()-inicio, 5)} seconds\n')
        return result            
    return wrapper