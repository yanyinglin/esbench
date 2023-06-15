import time
import json
import torch
import socket
import torch.nn as nn
import math

# class VGG(nn.Module):
#     def __init__(self,num_classes=1000):
#         super(VGG,self).__init__()
#         self.features = nn.Sequential(
#             nn.Conv2d(3,64,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.Conv2d(64,64,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.MaxPool2d(kernel_size=2,stride=2),

#             nn.Conv2d(64,128,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.Conv2d(128,128,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.MaxPool2d(kernel_size=2,stride=2),

#             nn.Conv2d(128,256,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.Conv2d(256,256,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.Conv2d(256,256,kernel_size=3,padding=1),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2,stride=2),

#             nn.Conv2d(256,512,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.Conv2d(512,512,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.Conv2d(512,512,kernel_size=3,padding=1),
#             nn.ReLU(True),
#             nn.MaxPool2d(kernel_size=2,stride=2),

#             nn.Conv2d(512, 512, kernel_size=3, padding=1),
#             nn.ReLU(True),
#             nn.Conv2d(512, 512, kernel_size=3, padding=1),
#             nn.ReLU(True),
#             nn.Conv2d(512, 512, kernel_size=3, padding=1),
#             nn.ReLU(True),
#             nn.MaxPool2d(kernel_size=2, stride=2),
#         )
#         self.classifier = nn.Sequential(
#             nn.Linear(512*7*7,4096),
#             nn.ReLU(True),
#             nn.Linear(4096,4096),
#             nn.ReLU(True),
#             nn.Dropout(),
#             nn.Linear(4096,num_classes),
#         )
#     def forward(self,x):
#         x = self.features(x)
#         x = x.view(x.size(0),-1)
#         x = self.classifier(x)
#         return x

def handle(args):
    from handler import VGG
    
    startTime = time.time()
    model= torch.load('/home/app/function/model/vggnet11.pt')
    # model.load_state_dict(torch.load('/home/app/function/model/vggnet16.pkl'))
    # model= torch.load('./model/vggnet16.pt')
    time_model_load = time.time() - startTime

    output = model(torch.randn(3, 3, 224, 224))
    torch.nn.functional.softmax(output[0], dim=0)
    # print(output)
    # return json.dumps({'token':  'vggnet', 'startTime': startTime,'endTime': time.time(),'runtime': time.time()-startTime})
    return json.dumps({"token":  "mobilenet", "time_model_load": time_model_load,  "startTime": startTime,"endTime": end_time,"runtime": end_time-startTime, "ip":socket.gethostbyname(socket.gethostname())})

# handle(None)