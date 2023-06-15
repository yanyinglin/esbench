import time
from collections import Counter
from urllib import request
import random
import json

def handle(c):
    start_time = time.time()
    url = 'http://10.10.1.121:10000/files/stream_data/600KB/{i}'.format(i=random.randint(1, 10))
    filedata = request.urlopen(url)
    net_time =time.time()
    Counter(filedata.read().strip().split())
    execution_time= time.time()
    # for key, value in count.most_common(100):
    #     print(key + " - " + str(value))
    result = {"token": "inference finished", "start_time": start_time,"net_time":net_time,"execution_time":execution_time}
    print(result)
    return json.dumps(result)
