'''
Descripttion: csv:path x1 y1 x2 y2 l1 x1 y1 x2 y2 l2    ->   csv:path x1 y1 x2 y2 l1 
                                                                 path x1 y1 x2 y2 l1 

version: 
Author: Lugy
Date: 2023-09-04 09:52:37
LastEditors: Andy
LastEditTime: 2023-09-23 16:59:04
'''

import os
import numpy as np
import pandas as pd


if __name__ == '__main__':

    csv_file = "dataset/csv_m2s_data/srcImages_label.csv"
    std_csv_file = "dataset/csv_m2s_data/csv_labels.csv"
 

    # 整合csv格式标注文件
    annotations = pd.read_csv(csv_file, header=None).values

    csv_labels = open(std_csv_file, "w")

    csv_labels.write('filename'+ ',' +'xmin'+ ',' +'ymin'+ ',' +'xmax'+ ',' +'ymax'+','+'label'+'\n')

    for annotation in annotations:
        key = annotation[0].split(os.sep)[-1]
        value = np.array(annotation[1].split(' '))
        if len(key) < 9:
            key = '0' + key
        for i in range(int(len(value)/5)):
            csv_labels.write(key+ ',' +value[i*5]+ ',' +value[i*5+1]+ ',' +value[i*5+2]+ ',' +value[i*5+3]+ ',' +value[i*5+4]+ '\n')
    csv_labels.close()   

    print("Change csv finish.") 
            


