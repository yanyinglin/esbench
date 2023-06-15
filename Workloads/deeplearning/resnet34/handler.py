import time
import json
import torch
import socket
from torch import nn
  

def handle(args):
    startTime = time.time()
    model= torch.load('/home/app/function/model/resnet34.pt')
    time_model_load = time.time() - startTime
    # model.load_state_dict(torch.load('/home/app/function/model/resnet50.pkl'))
    # model= torch.load('./model/resnet34.pt')

    x=torch.randn(16,3,224,224)
    output = model(x)
    torch.nn.functional.softmax(output[0], dim=0)
    # print(output)
    # return json.dumps({'token':  'resnet34', 'startTime': startTime,'endTime': time.time(),'runtime': time.time()-startTime})
    return json.dumps({"token":  "resnet34",  "time_model_load": time_model_load, "startTime": startTime,"endTime": time.time(),"runtime": time.time()-startTime,"ip":socket.gethostbyname(socket.gethostname())})


# handle(None)