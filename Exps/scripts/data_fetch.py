from MetricsExp import TKPrometheus

import pandas as pd

col = ["name","start","end","requests","type"]
col_metrics = ["name", "url"]
function_run = pd.read_csv('/home/tinker/workspace/Euler-Serverless/Platform-Testing/metric/function_run.csv',names=col,header=None)

metric = pd.read_csv('/home/tinker/workspace/Euler-Serverless/Platform-Testing/metric/metric.csv',names=col_metrics,encoding='utf-8',engine='python', header=None, sep='\t')

print(metric)
prom = TKPrometheus()
columns_all=['requests','type','timestamp','value','metrics','pod_name',"pod_ip" 'node_name','node_ip','function','interface']
df = pd.DataFrame(columns=columns_all)
for index, f in function_run.iterrows():
    for i,m in metric.iterrows():
        fet = prom.fetch_grafana(start=f['start'],end = f['end'], query=m['url'],step=0.5, name=m['name'], function=f['name'],req =f['requests'],type=f['type'])
        df = df.append(fet,ignore_index=True)
df.to_csv('/home/tinker/workspace/Euler-Serverless/Platform-Testing/version0811/'+ 'metrics.csv', mode='a', header=False, index=False)