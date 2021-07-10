# -*- coding: utf-8 -*-
"""Yolo-V5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tHs5blPGhdvxWs_PlqVxjmbivnXFYvtE

##Setting Up The YOLOv5 Environment
"""

!git clone https://github.com/ultralytics/yolov5  
!pip install -U -r yolov5/requirements.txt

!pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolov5

!ls

import torch
from IPython.display import Image  
from utils.google_utils import gdrive_download  

print('Using torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

"""## Downloading the data"""

!curl -L "https://app.roboflow.com/ds/UQvf0P2emC?key=ArobqLSGfA" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip

"""## Define Model Configuration and Architecture"""

# Commented out IPython magic to ensure Python compatibility.
# %cat data.yaml

import yaml
with open("data.yaml", 'r') as stream:
    num_classes = str(yaml.safe_load(stream)['nc'])

from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))

# Commented out IPython magic to ensure Python compatibility.
# 
# %%writetemplate /content/yolov5/data.yaml
# 
# train: ./train/images
# val: ./valid/images
# 
# nc: 1
# names: ['pistol']

# Commented out IPython magic to ensure Python compatibility.
# %cat data.yaml

with open(r'data.yaml') as file:
    labels_list = yaml.load(file, Loader=yaml.FullLoader)

    label_names = labels_list['names']

print("Number of Classes are {}, whose labels are {} for this Object Detection project".format(num_classes,label_names))

# Commented out IPython magic to ensure Python compatibility.
#this is the model configuration we will use for our tutorial 
# yolov5s.yaml contains the configuration of neural network required for training.
# %cat /content/yolov5/models/yolov5s.yaml

# Commented out IPython magic to ensure Python compatibility.
# # Below we are changing the configuration so that it becomes compatible to number of classes required in this project
# %%writetemplate /content/yolov5/models/custom_yolov5s.yaml
# 
# # parameters
# nc: 1  # number of classes  # CHANGED HERE
# depth_multiple: 0.33  # model depth multiple
# width_multiple: 0.50  # layer channel multiple
# 
# # anchors
# anchors:
#   - [10,13, 16,30, 33,23]  # P3/8
#   - [30,61, 62,45, 59,119]  # P4/16
#   - [116,90, 156,198, 373,326]  # P5/32
# 
# # YOLOv5 backbone
# backbone:
#   # [from, number, module, args]
#   [[-1, 1, Focus, [64, 3]],  # 0-P1/2
#    [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
#    [-1, 3, BottleneckCSP, [128]],
#    [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
#    [-1, 9, BottleneckCSP, [256]],
#    [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
#    [-1, 9, BottleneckCSP, [512]],
#    [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
#    [-1, 1, SPP, [1024, [5, 9, 13]]],
#    [-1, 3, BottleneckCSP, [1024, False]],  # 9
#   ]
# 
# # YOLOv5 head
# head:
#   [[-1, 1, Conv, [512, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 6], 1, Concat, [1]],  # cat backbone P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 13
# 
#    [-1, 1, Conv, [256, 1, 1]],
#    [-1, 1, nn.Upsample, [None, 2, 'nearest']],
#    [[-1, 4], 1, Concat, [1]],  # cat backbone P3
#    [-1, 3, BottleneckCSP, [256, False]],  # 17 (P3/8-small)
# 
#    [-1, 1, Conv, [256, 3, 2]],
#    [[-1, 14], 1, Concat, [1]],  # cat head P4
#    [-1, 3, BottleneckCSP, [512, False]],  # 20 (P4/16-medium)
# 
#    [-1, 1, Conv, [512, 3, 2]],
#    [[-1, 10], 1, Concat, [1]],  # cat head P5
#    [-1, 3, BottleneckCSP, [1024, False]],  # 23 (P5/32-large)
# 
#    [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
#   ]

import os
os.chdir('/content/yolov5')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# %cd /content/yolov5/
# !python train.py --img 416 --batch 80 --epochs 1000 --data './data.yaml' --cfg ./models/custom_yolov5s.yaml --weights ''

"""## Evaluate Custom YOLOv5 Detector Performance
Training losses and performance metrics are saved to Tensorboard and also to a logfile defined above with the **--name** flag when we train. In our case, we named this `yolov5s_results`. (If given no name, it defaults to `results.txt`.) The results file is plotted as a png after training completes.

Partially completed `results.txt` files can be plotted with `from utils.utils import plot_results; plot_results()`
"""

# Commented out IPython magic to ensure Python compatibility.
# Start tensorboard
# Launch after you have started training to all the graphs needed for inspection
# logs save in the folder "runs"
# %load_ext tensorboard
# %tensorboard --logdir /content/yolov5/runs

print("GROUND TRUTH TRAINING DATA:")
Image(filename='/content/yolov5/runs/train/exp2/test_batch0_labels.jpg', width=900)

# print out an augmented training example
# Below is the augmented training data.
# NOTE: The dataset already contains the augmented data with annotations, so that you dont have to do it.
print("GROUND TRUTH AUGMENTED TRAINING DATA:")
Image(filename='/content/yolov5/runs/train/exp2/train_batch0.jpg', width=900)

# Commented out IPython magic to ensure Python compatibility.

# %cd /content/yolov5/
!python detect.py --weights /content/yolov5/runs/train/exp2/weights/best.pt --img 416 --conf 0.4 --source ./test/images

"""### Let's check the output"""

import glob
from IPython.display import Image, display

for imageName in glob.glob('/content/yolov5/runs/detect/exp/*.jpg'): #assuming JPG
    display(Image(filename=imageName))
    print("\n")

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/gdrive')

# %cp /content/yolov5/runs/train/exp2/weights/yolov5.weights /content/gdrive/My\ Drive