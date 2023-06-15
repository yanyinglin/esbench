import time
import json
import torch
import socket

def handle(args):
    startTime = time.time()
    model= torch.load('/home/app/function/model/mobilenet_v11_3.pt')
    time_model_load = time.time() - startTime
    # model.load_state_dict(torch.load('/home/app/function/model/mobilenet.pkl'))
    # model= torch.load('./model/mobilenet_v11_3.pt')
    
    x = torch.randn(32,3,32,32)
    y = model(x)
    
    m = torch.nn.functional.softmax(y[0], dim=0)
    end_time = time.time()
    # print(m)
    # return json.dumps({'token':  'mobilenet', 'startTime': startTime,'endTime': time.time(),'runtime': time.time()-startTime})
    return json.dumps({"token":  "mobilenet", "time_model_load": time_model_load, 
    "startTime": startTime,"endTime": end_time,"runtime": end_time-startTime, "ip":socket.gethostbyname(socket.gethostname())})


# handle(None)