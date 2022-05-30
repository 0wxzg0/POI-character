# POI-character
当前版本主要使用程序：
person5.py
get_topics.py

===================
Python3.8


- clusters
	- cl_***.py：各种聚类算法
- dataset
	- POI_gcj02_new.csv：POI数据集
	- user***.txt/user***.csv：用户数据（测试用）
	- user_all.txt：重新编号，读取时使用的用户数据集
	- user_context_matrix_*.csv/pkl：用户特征向量文件
- kda_result：存储lda分类结果
- get_dataset.py：从原始数据集提取用户数据
- get_topics.py：读取用户特征向量文件，输出LDA分类结果
- get_lda_pic.py：可自动生成lda分类结果统计图
- grade_silhouette.py：计算聚类轮廓系数
- person4.py：（旧）调用聚类算法，分析用户特征
- person5.py：调用聚类算法，生成用户基于POI的轨迹特征向量
- poi4.py：调用API生成POI数据集
- test_topics_stability.py：测试结果稳定性
- 其它：已废弃
