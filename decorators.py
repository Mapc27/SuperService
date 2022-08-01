import time

import requests
import urllib3
from colorama import Fore


def bad_connection(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except (ConnectionRefusedError, requests.exceptions.ProxyError, urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.NewConnectionError, requests.exceptions.ConnectTimeout,
                    requests.exceptions.ProxyError, urllib3.exceptions.ConnectTimeoutError, TimeoutError,
                    requests.exceptions.ReadTimeout, urllib3.exceptions.ReadTimeoutError) as error:
                print()
                print(Fore.RED + error)
                print("Wait for 5s")
                time.sleep(5)

    return wrapper


def bad_response(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        bad_response_number = 0
        while not response.json()['done'] and "база" in str(response.json()['message']).lower():
            if bad_response_number > 20:
                break
            bad_response_number += 1
            print("Bad response:", response.json())
            print("Waiting for 20s ...")
            time.sleep(20)
            print("Trying again: ")
            response = func(*args, **kwargs)
        return response

    return wrapper
