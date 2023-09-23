'''
Author: Lugy
Date: 2023-09-09 15:10:49
LastEditTime: 2023-09-23 17:07:57
LastEditors: Andy
Description: 对应 labelme.exe 的 5.3.1 版本
版权声明
'''

import os
import cv2
import json
import pandas as pd
import numpy as np
import base64


image_path = "dataset/csv_m2s_data/images/"
csv_file = "dataset/csv_m2s_data/csv_labels.csv"

annotations = pd.read_csv(csv_file, header=None).values
total_csv_annotations = {}

read_imageData = False

for annotation in annotations[1:]:
    key = annotation[0].split(os.sep)[-1]
    value = np.array([annotation[1:]])
    if key in total_csv_annotations.keys():
        total_csv_annotations[key] = np.concatenate((total_csv_annotations[key],value),axis=0)
    else:
        total_csv_annotations[key] = value

for key,value in total_csv_annotations.items():
    height,width = cv2.imread(image_path+key).shape[:2]
    labelme_format = {
    "version":"5.3.1",
    "flags":{},
    }
    
    shapes = []
    for shape in value:
        label = shape[-1]
        points = [
            [float(shape[0]),
             float(shape[1])
            ],
            [float(shape[2]),
             float(shape[3])
            ]
        ]

        s = {"label":label} 
        s["points"] = points
        s["group_id"] = None
        s["description"] = ""
        s["shape_type"] = "rectangle"
        s["flags"] = {}
        
        shapes.append(s)
        
    labelme_format["shapes"] = shapes
    labelme_format["imagePath"] = key

    imageData = None
    if read_imageData:
        with open(image_path+key,"rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode('utf-8')

    labelme_format["imageData"] = imageData
    labelme_format["imageHeight"] = height
    labelme_format["imageWidth"] = width

    json.dump(labelme_format, open("%s%s"%(image_path,key.replace(".jpg", ".json")),"w"), ensure_ascii=False, indent=2)

print("csv to labelme finished.")
