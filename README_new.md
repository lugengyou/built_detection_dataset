<!--
 * @Descripttion: 
 * @version: 
 * @Author: Lugy
 * @Date: 2023-09-23 16:10:30
 * @LastEditors: Andy
 * @LastEditTime: 2023-09-23 17:09:51
-->

代码说明：

    部分代码参考自： https://github.com/spytensor/prepare_detection_dataset
    !!!感谢 spytensor 作者提供转换代码样例

修改说明：

    修改 csv2labelme.py 代码，使用 "5.3.1" 版本，
        包括 .json 字段顺序、删除 ImageData 数据
    
    添加应用案例转换数据集
        xml2csv_data：（执行 .xml -> csv 转换）
            annotations
            images
            xml2csv.py
        csv_m2s_data：（执行 csv 标签转换，csv -> coco） 
            scrImages
            srcImages_label.csv
            csvlabel_mult2single.py # 将 srcImages_label.csv 转换为 csv_labels.csv 格式

使用说明：

    获得符合条件的 csv 格式数据，可以根据 README.md 使用方式调用接口函数进行格式转换

样例使用说明：
```bash
xml 获取 csv 标注文件
    python xml2csv.py
[已有 csv 不符合格式，进行 csv 转换
    python dataset/csv_m2s_data/csvlabel_mult2single.py]
由 csv 转换为 coco 格式
    python csv2coco.py
由 csv 转 labelme
    cp -r dataset/csv_m2s_data/srcImages dataset/csv_m2s_data/iamges
    python csv2labelme.py
```
    