import torch
import torch.nn as nn
import torchvision 
import torchvision.transforms as transforms
from torchvision import models
import torch.nn.functional as F


class MyModel(nn.Module):# to naive an approach
  def __init__(self):
    super().__init__()
    c=26
    
    self.conv1=nn.Conv2d(1,8,kernel_size=5,padding=0,stride=1)#24
    self.conv2=nn.Conv2d(8,8,kernel_size=5,padding=0,stride=1)#-> maxpool 12-> 8-> maxpool 4
    self.fc4=nn.Linear(128,64)
    self.fc5=nn.Linear(64,26)

  def forward(self,x):
    x=F.relu(self.conv1(x))
    x=F.max_pool2d(x,2)
    x=F.relu(self.conv2(x))
    x=F.max_pool2d(x,2)
    x=x.view(-1,4*4*8)
    x=F.relu(self.fc4(x))
    x=self.fc5(x)
   
    

    return F.log_softmax(x,dim=1)