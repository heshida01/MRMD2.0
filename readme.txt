 python3  mrmd2.0.py  -i input.csv -s start_index -e end_index -l Step_length  -o accuracy_f1.csv  -c deimensionReduction_dataset.csv
 
 环境: python3.6(参考“requirements.txt”, 执行 "pip install -r requirements.txt",     
       另外下载pymrmr.zip,解压后windows用户执行"python setup.py install "，  
       linux用于执行  "python setup.py build"
                     "python setup.py install"  )
 注：  建议用python3.6 否则安装可能报错
 
 usage:

 python3  mrmd2.0.py  -i input.csv -s start_index -e end_index -l Step_length  -o accuracy_f1.csv  -c deimensionReduction_dataset.csv

 -i 输入的数据集，目前仅支持csv格式
 
 -s 用户指定的区间开始的位置
 
 -e 用户指定的区间结束的位置
 
 -l 区间的步长
 
 -o 降维后数据集的一些指标(精确度和f1),格式为csv
 
 -c 降维后的数据集，csv格式
 
 终端输出的数据可以在Logs文件中查找
                     
