from concurrent.futures import thread
import json
import aiohttp
import asyncio
import nest_asyncio
import time
import pandas as pd
import kubernetes as k8s
import threading as th

# 实验配置，每次修改
Stream_req = [1]
interface = 'wired' # wired
type = 'single' # concurrent，single
tag = 'local_images' # remote_images, local_images
data_path = '/home/tinker/workspace/Euler-Serverless/Platform-Testing/version0826/{}-{}.csv'
sleeptime = 10

# action_functions = ['resnet34']
action_functions = ['lstm-cloud', 'mnist-cloud', 'resnet18-cloud', 'resnet34-cloud','mobilenet-cloud', 'shufflenet-cloud']
action_functions = ['resnet34','resnet50']

# action_functions = ['mobilenet-cloud']


k8s.config.load_kube_config()
k8sclient = k8s.client.CoreV1Api()
loopctl = True




openfaas_base_url = 'http://serverless.siat.ac.cn:31112/function/{function_name}.openfaas-fn'
res_col = ["function", "invoke_time", "time_model_load", "startTime", "endTime", "runtime","ip","response_time","request_vol","interface","type"]

record_col= ["function","start","end","request","type"]
nest_asyncio.apply()


class Kubernetes:
    def __init__(self):
        self.loop = asyncio.new_event_loop()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

    async def _countClass(self):
        while True:
            pod_count = pd.DataFrame(columns=['time','function', 'pod_count','tag'])
            pods = k8sclient.list_namespaced_pod('openfaas-fn')
            instance_count = {}
            for action in action_functions:
                for pod in pods.items:
                    if pod.metadata.name.startswith(action):
                        instance_count[action] = instance_count.get(action, 0) + 1
            for action in action_functions:
                pod_count = pod_count.append({'time': time.time(), 'function': action, 'pod_count': instance_count[action],'tag':tag}, ignore_index=True)
            pod_count.to_csv(data_path.format(tag,'pod_count'), mode='a', header=False, index=False)
            await asyncio.sleep(2)
    def countClass(self):
        asyncio.ensure_future(self._countClass())


async def invoke_function(session,fname):
    url = openfaas_base_url.format(function_name=fname)
    invoke_time = time.time()
    res = await session.request('GET', url)
    res = await res.text()
    return res, fname, invoke_time,time.time()

async def main(vol,fname):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(vol):
            tasks.append(invoke_function(session=session,fname=fname))
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

k8spod = Kubernetes()

thread = th.Thread(target=asyncio.run, args=(k8spod.countClass()))  
thread.start()
thread.join()

for i in Stream_req:
    starttime = time.time()
    avg_vol = i
    for fname in action_functions:
        function_starttime = time.time()
        data = asyncio.run(main(avg_vol,fname))
        df_res = pd.DataFrame(columns=res_col)
        for item in data:
            if isinstance(item, Exception):
                print(item)
            else:
                res, fname, invoke_time, response_time = item
                # exclude the line not contain "token" of the response
                token = res.split("\n")
                for line in token:
                    if "token" in line:
                        token = json.loads(line)
                        break
                df = pd.json_normalize(token)
                # df.drop(['token'], axis=1, inplace=True)
                df['function'] = fname
                df['invoke_time'] = invoke_time
                df['response_time'] = response_time
                df['request_vol'] = avg_vol
                df['interface'] = interface
                df['type'] = type
                df_res = pd.concat([df_res, df], axis=0)
        function_end = time.time()
        dp = {'function':fname,'start':function_starttime,'end':function_end,'request':avg_vol,'type':type}
        df_function_record = pd.json_normalize(dp)
        df_function_record.to_csv(data_path.format(tag,"run_record"), mode='a', header=False, index=False)
        df_res.to_csv(data_path.format(tag,'result'), mode='a', header=False, index=False)
    endtime = time.time()
    if endtime - starttime < sleeptime:
        time.sleep(sleeptime - (endtime - starttime))
k8spod.stop()

