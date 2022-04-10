from sklearn.cluster import k_means
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt
import pandas as pd

data = pd.read_csv(r"dataset/user1796.csv", header=0)
# print(data)
x = data[["x", "y"]]

score = []

# 对k=2-12
for i in range(14):
    model = k_means(x, n_clusters=i + 8) # 用sklearn里的kmeans函数得到聚类结果
    score.append(silhouette_score(x, model[1])) # 用sklearn里的silhouette_score函数得到轮廓系数

plt.figure(figsize=(15, 6), dpi=80)
plt.subplot(1, 2, 1)
plt.scatter(data['x'], data['y'], s=5)

plt.subplot(1, 2, 2) # 绘制折线图，找到最佳的k值
plt.plot(range(8, 22, 1), score)
plt.show()