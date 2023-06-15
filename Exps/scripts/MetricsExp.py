import os
import pandas as pd
import requests
# from kubernetes import client, config

def str_return(str):
    return str


class TKPrometheus:
    columns_all=['requests','type','timestamp','value','metrics','node_ip','function','interface']
    headers = {"Authorization": "Bearer eyJrIjoiZUp5Y00xN3haaFF3N05ZcHAxU1AzZDBhOTVSZ05mNEwiLCJuIjoidGlua2VyIiwiaWQiOjF9"}
    # headers = {
    #     'Cookie':'grafana_session=68d36b7854b82d21e6558409044db86e'
    # }
    def __init__(self):
        # os.popen("kubectl get node -o wide|grep -v 'NAME'|awk '{print $1,$6}'> node.t>node.t")
        return

    def reset_time(self,x,s):
        return x-s


    def fetch_grafana(self, query='',start='1',end='1',step=0.5, name='cache_misses_rate', function='default', req = 1,type='single',node_ip='',interface=''):
        url = 'http://serverless.siat.ac.cn:30965/api/datasources/proxy/1/api/v1/query_range?query={metric}&start={start}&end={end}&step={step}'
        if 'function_name' in query:
            query = query.replace('{function_name}',function)
        
        if 'instance_ip' in query:
            query = query.replace('{instance_ip}',node_ip)

        url=url.format(metric=query,start=start,end=end,step=step)
        r = requests.request('GET', url,headers=self.headers)
        response_json = r.json()['data']['result']
        dataframe_all = pd.DataFrame(columns=self.columns_all)
        for m in response_json:
            data_t = pd.json_normalize(m)
            dk_tmp = pd.DataFrame(columns=self.columns_all)
            for i,r in data_t.iterrows():
                df_values = pd.DataFrame(r['values'], columns=['timestamp','value'])
                start_time = df_values['timestamp'][0]
                df_values['timestamp']=df_values.apply(lambda x:self.reset_time(x.timestamp,start_time),axis=1)
                dk_tmp = pd.concat([dk_tmp,df_values],axis=0)
            dk_tmp['node_ip']  = dk_tmp.apply(lambda x:node_ip,axis=1)
            dk_tmp['metrics'] = dk_tmp.apply(lambda x:name,axis=1)
            dk_tmp['requests'] =dk_tmp.apply(lambda x:req,axis=1)
            dk_tmp['type'] =dk_tmp.apply(lambda x:type,axis=1)
            dk_tmp['interface'] =dk_tmp.apply(lambda x:interface,axis=1)
            dataframe_all = pd.concat([dataframe_all,dk_tmp],ignore_index=True)
            dataframe_all['function'] = dataframe_all.apply(lambda x:function,axis=1)
        return dataframe_all

# os.chdir(os.getcwd())
# prom = Prometheus()
# prom.run_prometheus_perf(start= 1658499788,end=1658500011,platform="openfaas",namespace='openfaas-fn')

# prom.run_prometheus_perf(start= 1636101435.5926323-30,end=1636103235.0917916,platform="Kubeless",namespace='kl')
# prom.run_prometheus_perf(start=1636101435.5926323-30,
#                          end=1636103235.0917916, platform="Kubeless", namespace='kl')

# count(kube_pod_container_info{origin_prometheus=~"$origin_prometheus", container=~"$Container", container != "", container != "POD", namespace=~"$NameSpace"}) by(container) - 0
# 
# import pandas as pd
# os.chdir(os.getcwd())
# col = ["name","start","end","requests","type"]
# col_metrics = ["name", "url"]
# function_run = pd.read_csv('/home/tinker/workspace/Euler-Serverless/Platform-Testing/metric/function_run.csv',names=col,header=None)

# metric = pd.read_csv('/home/tinker/workspace/Euler-Serverless/Platform-Testing/metric/metric.csv',names=col_metrics,header=None)
# prom = TKPrometheus()
# for index, f in function_run.iterrows():
#     for i, m in metric.iterrows():
#         dk = prom.fetch_grafana(start=f['start'],end = f['end'], query=m['url'],step=0.5, name=m['name'], function=f['name'],req =f['requests'],type=f['type'])
#         dk.shape[0]
#         # dk.to_csv('/home/tinker/workspace/Euler-Serverless/Platform-Testing/cloud/' + m + '.csv', mode='a', header=False, index=False)