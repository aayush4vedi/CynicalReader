import time

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

RETRIES_STATUS_CODES = [429, 500, 502, 503, 504]  # not used rn

"""
    Used self-retry logic. but check this package:: Read about requests.retries here: [doc](https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure), [stkofw](https://stackoverflow.com/questions/23267409/how-to-implement-retry-mechanism-into-python-requests-library?rq=1)
"""
def hitGetWithRetry(url, HEADER='',VERIFY=False ,retry_count=2,sleep_seconds=15,TIMEOUT=None):
    if(retry_count == 0):
        return -1
    else:
        data = requests.get(url, verify=VERIFY,headers= HEADER, timeout=TIMEOUT)
        if(data.status_code==200):
            return data
        else:
            print(" \txxxxxx------------ Found Status Code: {} sleeping for {} sec.Retries remaining = {} --------------xxxxx".format(data.status_code,sleep_seconds,retry_count-1))
            time.sleep(sleep_seconds) 
    return hitGetWithRetry(url, HEADER,retry_count-1,sleep_seconds)
