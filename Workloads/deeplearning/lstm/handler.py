import time
import json
import torch
from torch import nn
import socket

class LstmRNN(nn.Module):
    """
        Parameters：
        - input_size: feature size
        - hidden_size: number of hidden units
        - output_size: number of output
        - num_layers: layers of LSTM to stack
    """
    def __init__(self, input_size, hidden_size=1, output_size=1, num_layers=1):
        super().__init__()
 
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers) # utilize the LSTM model in torch.nn 
        self.forwardCalculation = nn.Linear(hidden_size, output_size)
 
    def forward(self, _x):
        x, _ = self.lstm(_x)  # _x is input, size (seq_len, batch, input_size)
        s, b, h = x.shape  # x is output, size (seq_len, batch, hidden_size)
        x = x.view(s*b, h)
        x = self.forwardCalculation(x)
        x = x.view(s, b, -1)
        return x

def handle(args):
    startTime = time.time()
    model = LstmRNN(1, 16, output_size=1, num_layers=1)
    model.load_state_dict(torch.load('/home/app/function/model/lstm.pkl'))
    time_model_load = time.time() - startTime


    output = model(torch.randn(5, 3, 1))
    # m = torch.nn.functional.softmax(output[0], dim=0).detach().numpy().tolist()
    # print(output)
    return json.dumps({"token":  "lstm", "time_model_load": time_model_load, "startTime": startTime,"endTime": time.time(),"runtime": time.time()-startTime,"ip":socket.gethostbyname(socket.gethostname())})

# handle(None)
