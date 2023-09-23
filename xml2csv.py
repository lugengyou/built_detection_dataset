'''
Descripttion: 
version: 
Author: Lugy
Date: 2023-09-04 22:02:59
LastEditors: Andy
LastEditTime: 2023-09-23 16:53:03
'''

import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):#改为自己xml文件命名格式
        # print(xml_file)
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for obj in root.iter('object'):
            xmlbox = obj.find('bndbox')
            value = (root.find('filename').text,                    
                     int(float(xmlbox.find('xmin').text)),
                     int(float(xmlbox.find('ymin').text)),
                     int(float(xmlbox.find('xmax').text)),
                     int(float(xmlbox.find('ymax').text)),
                     obj.find('name').text
                     )
            xml_list.append(value)

    column_name = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class']  # 改为自己的列名
    xml_df = pd.DataFrame(xml_list, columns=column_name)

    return xml_df


if __name__ == "__main__":
    
    xml_path = "dataset/xml2csv_data/annotations"
    save_csv = "dataset/xml2csv_data/labels.csv"

    print('xml to csv ...\n')

    xml_df = xml_to_csv(xml_path)
    xml_df.to_csv(save_csv, index=None)  # 改为自己csv存储路径

    print(f'Successfully converted xml to {save_csv}.\n')

