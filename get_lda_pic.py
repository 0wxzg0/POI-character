import gensim
import numpy as np
import pickle
import pandas as pd
from gensim import matutils, models, corpora
import scipy
import pyLDAvis.gensim_models


id2word = {0:'food',1:'hotel',2:'shopping',3:'service',4:'beauty',5:'travel',6:'entertainment',7:'sports',8:'education',9:'media',10:'medicine',11:'car',12:'traffic',13:'finace',14:'estate',15:'company',16:'government'}
pathn = 'lda_result/'

tagn = '_above200_150m'
data = pd.read_pickle('dataset/user_context_matrix_above200.pkl')



dic1={0:'company',1:'government',2:'education',3:'medicine',4:'traffic',5:'car'}
#lda_classify("年龄",data[['company','government','education','medicine','traffic','car']],dic1,3)

dic2={0:'shopping',1:'beauty',2:'service',3:'traffic',4:'car',5:'entertainment',6:'sports'}
#lda_classify("性别",data[['shopping','beauty','service','traffic','car','entertainment','sports']],dic2,2)

dic3={0:'food',1:'shopping',2:'travel',3:'entertainment',4:'media',5:'traffic',6:'car'}
#lda_classify("经济状况",data[['food','shopping','travel','entertainment','media','traffic','car']],dic3,5)

dic4={0:'sports',1:'entertainment',2:'travel'}
#lda_classify("运动倾向",data[['sports','entertainment','travel']],dic4,4)

dic5={0:'education',1:'media',2:'medicine',3:'service',4:'company',5:'government',6:'finace'}
#lda_classify("职业",data[['education','media','medicine','service','company','government','finace']],dic5,5)
# 学生/教师，退休，公司职员，政党机关，个体私营者/管理者

dic6={0:'food',1:'shopping',2:'travel',3:'entertainment',4:'media',5:'traffic',6:'car',7:'education',8:'medicine',9:'service',10:'company',11:'government',12:'finace'}
#lda_classify("受教育程度",data[['food','shopping','travel','entertainment','media','traffic','car','education','medicine','service','company','government','finace']],dic6,5)

topics = ["0","年龄","性别","经济状况","运动倾向","职业","受教育程度"]

topic_d = topics[1]
data_d=data[['company','government','education','medicine','traffic','car']]

tdm = data_d.transpose()
# print(tdm)
#print(data_d.index)
sparse_counts = scipy.sparse.csr_matrix(tdm)
# print(sparse_counts)
corpus = matutils.Sparse2Corpus(sparse_counts)


lda=models.ldamodel.LdaModel.load(pathn+topic_d+tagn)
for topic in lda.print_topics(num_words=5):
    print(topic)

#corpus_transformed = lda[corpus]
#for kk in range(10):
#    print(corpus_transformed[kk])
#list(zip([a for [(a, b)] in corpus_transformed], data_d.index))

vis = pyLDAvis.gensim_models.prepare(lda, corpus, corpora.Dictionary.from_corpus(corpus, dic1))
pyLDAvis.show(vis,local=False)


