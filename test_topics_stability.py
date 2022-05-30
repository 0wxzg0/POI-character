import gensim
import numpy as np
import pickle
import pandas as pd
from gensim import matutils, models, corpora
import scipy
import pyLDAvis.gensim_models
from sklearn_extra.cluster import KMedoids
import rbo

#data = pd.read_csv('dataset/user_context_matrix_above200_dis250.csv')
#data.to_pickle('dataset/user_context_matrix_above200_dis250.pkl')

id2word = {0:'food',1:'hotel',2:'shopping',3:'service',4:'beauty',5:'travel',6:'entertainment',7:'sports',8:'education',9:'media',10:'medicine',11:'car',12:'traffic',13:'finace',14:'estate',15:'company',16:'government'}

#print(id2word)
tagn = '_above100_150m'
data = pd.read_pickle('dataset/user_context_matrix_above200_dis500.pkl')
pathn = 'lda_result/'
rpt_num = 20

def lda_classify(topic_d, data_d, id2word_d, num_topics): # 特征属性名称，原始词频表，词典，总分类数

    # 将原始词频表和词典转换成lda规定格式的corpus，id2word
    tdm = data_d.transpose()
    # print(tdm)
    #print(data_d.index)
    sparse_counts = scipy.sparse.csr_matrix(tdm)
    # print(sparse_counts)
    corpus = matutils.Sparse2Corpus(sparse_counts)

    diccc = corpora.Dictionary.from_corpus(corpus, id2word_d)
    # print(diccc)

    topics_all = []
    words_all = []

    for n_rpt in range(rpt_num):

        #生成lda分类结果
        lda = models.ldamodel.LdaModel(corpus=corpus, id2word=diccc, num_topics=num_topics, passes=50)
        print("-----print topics "+topic_d+"-----")
        # lda.save(pathn+topic_d+tagn) # 存储lda结果
        # 存储分类结果

        for topic in lda.print_topics(num_words=10):
            tmp_top = topic[1].strip().split("\"")
            #print(tmp_top)
            tmp_topic = [0 for i in range(len(id2word_d))]
            k_top = 0
            words_tmp = []
            while k_top < len(tmp_top):
                if k_top % 2:
                    words_tmp.append(tmp_top[k_top])
                    for iii in range(len(id2word_d)):
                        if id2word_d[iii] == tmp_top[k_top]:
                            tmp_perr = tmp_top[k_top-1]
                            search_num = 0
                            mark_num_str = ''
                            while search_num < len(tmp_perr):
                                if '9' >= tmp_perr[search_num] >= '0' or tmp_perr[search_num] == '.':
                                    mark_num_str = mark_num_str + tmp_perr[search_num]
                                search_num = search_num + 1
                            mark_num = float(mark_num_str)
                            #print(id2word_d[iii] + ' ' + str(mark_num))
                            tmp_topic[iii] = mark_num
                k_top = k_top + 1

            #print(tmp_topic)
            topics_all.append(tmp_topic)
            words_all.append(words_tmp)

    #print(topics_all)
    kmedoids = KMedoids(n_clusters=num_topics).fit(topics_all)
    print("-----cluster result-----")
    print(kmedoids.labels_)

    irbo = 0
    jrbo = 0
    result_rbo = [0 for i in range(num_topics)]
    cnt_label = [0 for i in range(num_topics)]
    for irbo in range(rpt_num * num_topics):
        for jrbo in range(irbo+1, rpt_num * num_topics):
            if kmedoids.labels_[irbo] == kmedoids.labels_[jrbo]:
                #print(words_all[irbo])
                #print(words_all[jrbo])
                cnt_rbo = rbo.RankingSimilarity(words_all[irbo],words_all[jrbo]).rbo(p=0.8)
                #print(cnt_rbo)
                result_rbo[kmedoids.labels_[irbo]] = result_rbo[kmedoids.labels_[irbo]] + cnt_rbo
                cnt_label[kmedoids.labels_[irbo]] = cnt_label[kmedoids.labels_[irbo]] + 1
    #print(result_rbo)
    for tmp_rbo in range(num_topics):
        if cnt_label[tmp_rbo]:
            result_rbo[tmp_rbo] = result_rbo[tmp_rbo] / cnt_label[tmp_rbo]
        else:
            result_rbo[tmp_rbo] = 0
    print("-----rbo result-----")
    print(result_rbo)



#lda_classify("全部",data,id2word,7)

dic1={0:'company',1:'government',2:'education',3:'medicine',4:'traffic',5:'car'}
lda_classify("年龄",data[['company','government','education','medicine','traffic','car']],dic1,3)

dic2={0:'shopping',1:'beauty',2:'service',3:'traffic',4:'car',5:'entertainment',6:'sports'}
lda_classify("性别",data[['shopping','beauty','service','traffic','car','entertainment','sports']],dic2,2)

dic3={0:'food',1:'shopping',2:'travel',3:'entertainment',4:'media',5:'traffic',6:'car'}
lda_classify("经济状况",data[['food','shopping','travel','entertainment','media','traffic','car']],dic3,5)

dic4={0:'sports',1:'entertainment',2:'travel'}
lda_classify("运动倾向",data[['sports','entertainment','travel']],dic4,4)

dic5={0:'education',1:'media',2:'medicine',3:'service',4:'company',5:'government',6:'finace'}
lda_classify("职业",data[['education','media','medicine','service','company','government','finace']],dic5,5)
# 学生/教师，退休，公司职员，政党机关，个体私营者/管理者

dic6={0:'food',1:'shopping',2:'travel',3:'entertainment',4:'media',5:'traffic',6:'car',7:'education',8:'medicine',9:'service',10:'company',11:'government',12:'finace'}
lda_classify("受教育程度",data[['food','shopping','travel','entertainment','media','traffic','car','education','medicine','service','company','government','finace']],dic6,5)



