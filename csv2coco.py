# -*- coding: utf-8 -*-
'''
@time: 2019/01/11 11:28
spytensor
'''

import os
import json
import numpy as np
import pandas as pd
import cv2
import os
import shutil
from sklearn.model_selection import train_test_split
np.random.seed(41)

#0为背景
# classname_to_id = {"person": 1}

classname_to_id = {"none": 0, "white":1, "red":2, "yellow":3, "blue":4}


class Csv2CoCo:

    def __init__(self,image_dir,total_annos):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
        self.image_dir = image_dir
        self.total_annos = total_annos

    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w'), ensure_ascii=False, indent=2)  # indent=2 更加美观显示

    # 由txt文件构建COCO
    def to_coco(self, keys):
        self._init_categories()
        for key in keys:
            self.images.append(self._image(key))
            shapes = self.total_annos[key]
            for shape in shapes:
                bboxi = []
                for cor in shape[:-1]:
                    bboxi.append(int(cor))
                label = shape[-1]
                annotation = self._annotation(bboxi,label)
                self.annotations.append(annotation)
                self.ann_id += 1
            self.img_id += 1
        instance = {}
        instance['info'] = 'spytensor created'
        instance['license'] = ['license']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance

    # 构建类别
    def _init_categories(self):
        for k, v in classname_to_id.items():
            category = {}
            category['id'] = v
            category['name'] = k
            self.categories.append(category)

    # 构建COCO的image字段
    def _image(self, path):
        image = {}
        print(path)
        img = cv2.imread(self.image_dir + path)
        image['height'] = img.shape[0]
        image['width'] = img.shape[1]
        image['id'] = self.img_id
        image['file_name'] = path
        return image

    # 构建COCO的annotation字段
    def _annotation(self, shape,label):
        # label = shape[-1]
        points = shape[:4]
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = int(classname_to_id[label])
        annotation['segmentation'] = self._get_seg(points)
        annotation['bbox'] = self._get_box(points)
        annotation['iscrowd'] = 0
        annotation['area'] = self._get_area(points)
        return annotation

    # COCO的格式： [x1,y1,w,h] 对应COCO的bbox格式
    def _get_box(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        return [min_x, min_y, max_x - min_x, max_y - min_y] # x y w h
    # 计算面积
    def _get_area(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        return (max_x - min_x+1) * (max_y - min_y+1)
    # segmentation
    def _get_seg(self, points):
        min_x = points[0]
        min_y = points[1]
        max_x = points[2]
        max_y = points[3]
        h = max_y - min_y
        w = max_x - min_x
        a = []
        a.append([min_x,min_y, min_x,min_y+0.5*h, min_x,max_y, min_x+0.5*w,max_y, max_x,max_y, max_x,max_y-0.5*h, max_x,min_y, max_x-0.5*w,min_y])
        return a
   

if __name__ == '__main__':

    ''' 注意添加类别信息 '''
    
    p_val_set = 0.3

    csv_file = "dataset/csv_m2s_data/csv_labels.csv"
    image_dir = "dataset/csv_m2s_data/images/"
    saved_coco_path = "dataset/csv_m2s_data/expdata"

    # 整合csv格式标注文件
    total_csv_annotations = {}
    annotations = pd.read_csv(csv_file, header=None).values

    annotations = annotations[1:] # 去掉表头

    for annotation in annotations:
        key = annotation[0].split(os.sep)[-1]
        value = np.array([annotation[1:]])
        if key in total_csv_annotations.keys():
            total_csv_annotations[key] = np.concatenate((total_csv_annotations[key],value),axis=0)
        else:
            total_csv_annotations[key] = value

    # 按照键值划分数据
    total_keys = list(total_csv_annotations.keys())
    train_keys, val_keys = train_test_split(total_keys, test_size=p_val_set)
    print("train_n:", len(train_keys), 'val_n:', len(val_keys))

    # 创建必须的文件夹
    if not os.path.exists('%s_coco/annotations/'%saved_coco_path):
        os.makedirs('%s_coco/annotations/'%saved_coco_path)
    if not os.path.exists('%s_coco/train2017/'%saved_coco_path):
        os.makedirs('%s_coco/train2017/'%saved_coco_path)
    if not os.path.exists('%s_coco/val2017/'%saved_coco_path):
        os.makedirs('%s_coco/val2017/'%saved_coco_path)

    # 把训练集转化为COCO的json格式
    l2c_train = Csv2CoCo(image_dir=image_dir,total_annos=total_csv_annotations)
    train_instance = l2c_train.to_coco(train_keys)
    l2c_train.save_coco_json(train_instance, '%s_coco/annotations/instances_train2017.json'%saved_coco_path)
    for file in train_keys:
        shutil.copy(image_dir+file,"%s_coco/train2017/"%saved_coco_path)
    for file in val_keys:
        shutil.copy(image_dir+file,"%s_coco/val2017/"%saved_coco_path)

    # 把验证集转化为COCO的json格式
    l2c_val = Csv2CoCo(image_dir=image_dir,total_annos=total_csv_annotations)
    val_instance = l2c_val.to_coco(val_keys)
    l2c_val.save_coco_json(val_instance, '%s_coco/annotations/instances_val2017.json'%saved_coco_path)

    print("csv to coco finished.")
