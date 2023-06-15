# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
from operator import inv
import os
import random
import re
import threading
import time
from multiprocessing import Process

import os
import numpy as np
import pandas as pd
import yaml
from scipy import stats
from Metrics import FunctionCount
# from DataCollect import FunctionCount
import uuid
import requests
import json

result_col = ['action_name', 'invokeTime', 'startTime',
              'endTime', 'req_mod', 'schedule_latency/ms', 'qps', 'config', 'platform']


reqest_col = ['time', 'req', 'platform']


result_col = ['actionName', 'invokeTime', 'startTime',
              'endTime', 'schedule_latency', 'req', 'config', 'platform']

exp_platforms = ['OpenFaas']
# exp_platforms = ['OpenFaas']

openfaas_base_url = 'http://serverless.siat.ac.cn:31112/function/{function_name}.openfaas-fn'
result_col = ["uuid","platform","function", "invokeTime", "startTime","endTime",'ip','node_name']
result_col = ["function", "invokeTime", "startTime","endTime",'ip','node_name','value']
result_col = ["function", "invokeTime", "startTime","endTime",'node_name', "excutionTime",'pid']



# %%
def handler(action_name, qps, config):
    uuidstring = config['uuidstring']
    cwd = config['cwd']
    threads = []
    # print('starting  request")
    platform_name = config['platform_name']
    for i in range(qps):
        t = threading.Thread(target=client_net, args=( action_name, platform_name,uuidstring,cwd))
        threads.append(t)

    # start the clients
    start_time = time.time()
    config['first_req'] = start_time
    for i in range(qps):
        threads[i].start()


## UUIDstring 用于标记一次请求一次函数请求
def client_1(action_name, platform_name,uuidstring,cwd):
    command = "bash {cwd}/{platform_name}/executor.sh -a {action_name}  -P {platform_name} -u {uuidstring}"
    command = command.format(cwd=cwd,action_name=action_name,platform_name=platform_name,uuidstring=uuidstring)
    os.system(command)

def client_requests(action_name, p_name, uuid, cwd ):
    from DataCollect import Prometheus
    prom = Prometheus()
    invoke_time = time.time()
    url = openfaas_base_url.format(function_name=action_name)
    res = requests.get(url)
    if res.status_code == 200:
        start_time = res.json()['startTime']
        ip= res.json()['ip']
        ip_split =ip.split(".")
        ip_3 = ip_split[0] + "." + ip_split[1]+ "."  + ip_split[2]
        file = open('node_ip.csv', 'r')
        js = file.read()
        node_dict = json.loads(js)
        node_name = node_dict[ip_3]
        # print(node_name)
    else:
        start_time = ''
        ip = ''
        node_name ='null'
    end_time = time.time()

    if start_time == '':
        print("start_tiem:", start_time)
        return

    value = prom.run_net_perf(start=start_time, end=end_time)
    value = value['value']
    df = pd.DataFrame(columns=result_col)
    value = value.tolist()
    df.loc[0] = [action_name, invoke_time, start_time, end_time, ip, node_name,value]
    df.to_csv(cwd+'/result.csv', mode='a', header=False, index=False)



def client_net(action_name, p_name, uuid, cwd ):
    from DataCollect import Prometheus
    prom = Prometheus()
    invoke_time = time.time()
    url = openfaas_base_url.format(function_name=action_name)
    res = requests.get(url)
    if res.status_code == 200:
        start_time = res.json()['startTime']
        ip= res.json()['ip']
        ip_split =ip.split(".")
        ip_3 = ip_split[0] + "." + ip_split[1]+ "."  + ip_split[2]
        file = open('node_ip.csv', 'r')
        js = file.read()
        node_dict = json.loads(js)
        node_name = node_dict[ip_3]
        # print(node_name)
    else:
        start_time = ''
        ip = ''
        node_name ='null'
    end_time = time.time()

    if start_time == '':
        print("start_time:", start_time)
        return

    excutionTime =end_time - start_time
    df = pd.DataFrame(columns=result_col)

    # Metric_val = prom.run_net_perf(metrics='node_netstat_Tcp_MetricsSegs',start=start_time, end=end_time)
    # Metric_val = Metric_val['value']
    # Metric_val = Metric_val.tolist()

    pid = os.getpid()
    df.loc[0] = [action_name, invoke_time, start_time, end_time, node_name, pid, excutionTime]
    df.to_csv(cwd+'/ee.csv', mode='a', header=False, index=False)
    return
     
# %%


# %%
def multi_process(actions, qps, config):
    request_threads = []
    action_name_list = ['stream-net']
    if config['uuidstring'] == '':
        config['uuidstring']=uuid.uuid1()
    else:
        config['uuidstring'] = 'max-'+ str(uuid.uuid1())
    for action_name in action_name_list:
        t = threading.Thread(target=handler, args=(action_name, qps, config))
        request_threads.append(t)

    random.shuffle(request_threads)
    total = len(request_threads)
    for i in range(total):
        request_threads[i].start()
    
    # for i in range(total):
    #     request_threads[i].join()


# %%
def run(qps=5, mode='normal', platform_name='OpenFaas',last_state=False,uuids=''):
    start_time = time.time()
    cwd = os.getcwd()
    config = {"qps": qps, "first_req": '', "platform_name": platform_name, "last_state":last_state,"uuidstring":uuids,"cwd":cwd}

    with open("../DIC/envs/actions.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        stream_action = data_loaded.get("Stream")
    try:

        p_stream = Process(target=multi_process, args=(
            stream_action, qps, config))
        p_stream.start()

    except Exception:
        print('error...')
    end_time = time.time()
    record = 'start_time: ' + str(start_time) + \
         'end_time: ' + str(end_time) +'\n'

    with open('record'+platform_name+'.log', 'a+') as s:
        s.write(record)


# %%
def runner(namespace, platform_name, workload, period):
    last_state = False
    # start function_instance counting
    fc = FunctionCount(namespace)
    print('start counting function instance')
    fc.get_pod_in_platform(platform_name, namespace)

    max_workload=int(max(workload)) 

    # start recording request.
    for i in range(len(workload)):
        qps = int(workload[i])
        if i == len(workload):
            last_state = True
        print('qps...', qps)
        time_now = time.time()
        df_req = pd.DataFrame({"time": [time_now], "req": [qps], "platform": [platform_name]})
        df_req.to_csv("request_"+platform_name+'.csv',header=False, index=False)
        if qps < 1:
            print('skiping')
            time.sleep(period)
            continue
        if qps ==max_workload:
            uuids='max'
        else:
            uuids=''
        t = threading.Thread(target=run, args=(qps,  'normal', platform_name,last_state,uuids))
        t.start()
        
        time.sleep(period)

    return
    
# %%
def entry():
    from DataCollect import Prometheus
    period = 5
    # 工作个数
    y = [8]
    print(y)
    prom = Prometheus()

    platf = {
        "OpenFaas": 'openfaas-fn',
        "OpenWhisk": 'openwhisk',
        "Kubeless": 'kl'
    }

    for platform_name in exp_platforms:
        start = time.time()
        try:
            namespace = platf[platform_name]
            runner(namespace, platform_name, y, period)
        except Exception:
            end = time.time()
        end = time.time()
        # prom.get_netstat(start=start, end=end,
        #                          platform=platform_name, namespace=namespace)

        # with open('runTime.log','w') as f:
        #     string = 'platform:'+ platform_name, '+ start:'+ str(start), '+ end:'+ str(end)
        #     f.write(string)
        #     f.write("---")

# %%
# os.chdir(os.path.dirname(__file__))
os.chdir(os.getcwd())
print(os.getcwd()) 
entry()