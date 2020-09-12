import time

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

RETRIES_STATUS_CODES = [429, 500, 502, 503, 504]  # not used rn

"""
    Used self-retry logic. but check this package:: Read about requests.retries here: [doc](https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure), [stkofw](https://stackoverflow.com/questions/23267409/how-to-implement-retry-mechanism-into-python-requests-library?rq=1)
"""
def hitGetWithRetry(url, HEADER='',VERIFY=False ,retry_count=3,SLEEP_SECONDS=15,TIMEOUT=None):
    data = requests.get(url, verify=VERIFY,headers= HEADER, timeout=TIMEOUT)
    if(data.status_code==200):
        return data
    while (retry_count > 0 and data.status_code != 200):
        print(" \txxxxxx------------ Found Status Code: {} sleeping for {} sec.Retries remaining = {} --------------xxxxx".format(data.status_code,SLEEP_SECONDS,retry_count-1))
        data = requests.get(url, verify=VERIFY,headers= HEADER, timeout=TIMEOUT)
        retry_count -= 1
    if(data.status_code==200):
        return data
    else:
        return -1