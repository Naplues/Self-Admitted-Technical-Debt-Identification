
# coding: utf-8

# In[4]:


import glob
import csv
import math
import re
import numpy as np
import autosklearn.classification
import sklearn.model_selection
from multiprocessing import Pool
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import CountVectorizer
import time
import logging
import operator
from scipy.sparse import csr_matrix


N_GRAM_LENGTH = 10
TOTAL_TYPE = 2
summary = dict()
total_n_gram = 0
total_document = 0
score = dict()
id_n_gram_mapping = dict()
comment_summary = dict()
top_vector = list()
n_grams = dict()

# weight = log(|D|/sdf) * gtf

def read_raw_data():
    with open("design-post-process.txt", 'r') as rawfile:
        global total_document
        reader = csv.reader(rawfile, delimiter='\t')
        for row in reader:
            comment_summary[total_document] = dict()
            temp = row[0]
            temp = temp.strip()
            if(temp == '1'):
                comment_summary[total_document]['project'] = 1
            if(temp == '2'):
                comment_summary[total_document]['project'] = 2
            if(temp == '3'):
                comment_summary[total_document]['project'] = 3
            if(temp == '4'):
                comment_summary[total_document]['project'] = 4
            if(temp == '5'):
                comment_summary[total_document]['project'] = 5
            if(temp == '6'):
                comment_summary[total_document]['project'] = 6
            if(temp == '7'):
                comment_summary[total_document]['project'] = 7
            if(temp == '8'):
                comment_summary[total_document]['project'] = 8
            if(temp == '9'):
                comment_summary[total_document]['project'] = 9
            if(temp == '10'):
                comment_summary[total_document]['project'] = 10

            if(row[1] == '0'):
                comment_summary[total_document]['type'] = 0
            elif(row[1] == '1'):
                comment_summary[total_document]['type'] = 1
            else:
                break
            temp1 = row[2].strip()
            comment_summary[total_document]['comment'] = temp1
            total_document += 1
        #print(comment_summary)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1   
    
#read data from n_gram
def read_n_gram():
    n_gram_id = 0
    total_n_gram = file_len("design-date-spec-filter-ngram.txt")
    print("total_n_gram",total_n_gram)
    with open("design-date-spec-filter-ngram.txt") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in reader:
            words = row[5].strip()
            term = tuple(row[5].strip().split(' '))
            if term not in summary:
                summary[term] = dict()
            summary[term] = {'id':n_gram_id,'len':row[1],'gtf':row[2],'df':row[3],'sdf':row[4], 'term':row[5]}
            weight1 = total_document / int(row[4])
            summary[term]['score'] = math.log10(weight1) * int(row[2])
            score[n_gram_id] =  math.log10(weight1) * int(row[2])
            n_grams[n_gram_id] = term
            n_gram_id += 1

def top_score_vector():
    percent = int(len(score) * 10 / 100)
    top_vector.extend(sorted(score,key=score.get,reverse=True)[:percent])
    print("top_vector",len(top_vector))

def n_gram_split():
    for comment_index in comment_summary:
        comment = comment_summary[comment_index]['comment']
        comment_summary[comment_index]['vector'] = dict()
        comment_post_process = re.sub("\s+"," ",re.sub(r"[^A-Za-z0-9]+"," ",comment.replace("\t"," ").replace("\r\n"," ").lower())).split(" ")
        for i in range(len(comment_post_process)):
            for j in range(i,min(i+N_GRAM_LENGTH+1,len(comment_post_process))):
                if(tuple(comment_post_process[i:j+1]) in summary):
                    if(summary[tuple(comment_post_process[i:j+1])]['id'] in top_vector):
                        if summary[tuple(comment_post_process[i:j+1])]['id'] in comment_summary[comment_index]['vector']:
                            comment_summary[comment_index]['vector'][summary[tuple(comment_post_process[i:j+1])]['id']] += 1
                        else: 
                            comment_summary[comment_index]['vector'][summary[tuple(comment_post_process[i:j+1])]['id']] = 1
    

def vector_idf():
    for i in comment_summary:
         for v in comment_summary[i]['vector']:
            comment_summary[i]['vector'][v] *= score[v]

def cal_coverage():
    empty_vector = 0
    total_vector = len(comment_summary)
    for i in comment_summary:
        if not comment_summary[i]['vector']:
            empty_vector += 1
            print(comment_summary[i],comment_summary[i]['vector'])
    print("coverage ratio:",(total_vector - empty_vector)/total_vector * 100)
    

read_raw_data()
read_n_gram()
top_score_vector()
n_gram_split()
print("finish")
#vector_idf()
cal_coverage()

# In[5]:


from collections import defaultdict
from collections import OrderedDict

n_gram_per_comment = defaultdict(lambda:0)
def cal_coverage1():
    empty_vector = 0
    total_vector = len(comment_summary)
    for i in comment_summary:
        sum = 0
        for j in comment_summary[i]['vector']:
            sum += 1
        n_gram_per_comment[sum] += 1
    print(OrderedDict(sorted(n_gram_per_comment.items(), key=lambda t: t[0])))
#     print("coverage ratio:",(total_vector - empty_vector)/total_vector * 100)
cal_coverage1()


# In[6]:


import autosklearn.classification
import sklearn.model_selection
import numpy as np
import json
from sklearn import cross_validation
from sklearn.metrics import f1_score,precision_score,recall_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import VarianceThreshold
# currently we have top_score_vector and comment&vector
# create x and y -> x contains vector and y contains result
X = []
y = []
z = []

print("test")
for comment_index in comment_summary:
    vector = [0] * len(top_vector)
    for vector_index in comment_summary[comment_index]['vector']:
        vector[top_vector.index(vector_index)] = comment_summary[comment_index]['vector'][vector_index]
        
    X.append(vector)
    y.append(comment_summary[comment_index]['type'])
    z.append(comment_summary[comment_index]['project'])
#print(z)
print("finish")




# In[4]:


# import numpy as np

# print("start")
# np_X = np.asarray(X)
# np_y = np.asarray(y)
# np.savez_compressed('../dataset/Xy', vector=np_X, label=np_y)
# print("finish X,y")


# # # with open('../dataset/X.json', 'w') as fp:
# # #     json.dump(X, fp, sort_keys=True, indent=4)
# # # print("finish X")
# # # with open('../dataset/y.json', 'w') as fp:
# # #     json.dump(y, fp, sort_keys=True, indent=4)
# # # with open('../dataset/comment_summary.json', 'w') as fp:
# # #     json.dump(comment_summary, fp, sort_keys=True, indent=4)
# # # with open('../dataset/top_vector.json', 'w') as fp:
# # #     json.dump(top_vector, fp, sort_keys=True, indent=4)
# # # with open('../dataset/n_grams.json', 'w') as fp:
# # #     json.dump(n_grams, fp, sort_keys=True, indent=4)


# In[5]:


# import glob
# import csv
# import math
# import re
# import numpy as np
# import autosklearn.classification
# import sklearn.model_selection
# from multiprocessing import Pool
# from sklearn.model_selection import KFold
# from sklearn.feature_extraction.text import CountVectorizer
# import time
# import logging
# import operator
# import autosklearn.classification
# import sklearn.model_selection
# import numpy as np
# import json
# from sklearn import cross_validation
# from sklearn.metrics import f1_score,precision_score,recall_score
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.feature_selection import VarianceThreshold

# loaded = np.load('../dataset/Xy.npz')
# np_X = loaded['vector']
# np_y = loaded['label']



from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings("ignore")

measure_scores = dict()
measure_scores['precision'] = list()
measure_scores['recall'] = list()
measure_scores['f1'] = list()



def automl(Xtrain, ytrain, Xtest, ytest, count):
    
    #X_train = np.asarray(Xtrain)
    #X_test = np.asarray(Xtest)
    y_train = np.asarray(ytrain)
    y_test = np.asarray(ytest)
    sparse_datasetX = csr_matrix(Xtrain)
    sparse_Xtest = csr_matrix(Xtest)

    print("checkpoint")
    
    #print("checklist")
    #for i in X_train:
        #f.write(str(i))
    #for j in X_test:
        #f1.write(str(j))
        
    #f.close()
    #f1.close()
    automl = autosklearn.classification.AutoSklearnClassifier(ml_memory_limit=1024*8)
    automl.fit(sparse_datasetX.copy(), y_train.copy(),dataset_name='SATD')
    automl.refit(sparse_datasetX.copy(), y_train.copy())
    y_hat = automl.predict(sparse_Xtest)
    measure_scores['precision'].append(sklearn.metrics.precision_score(y_test, y_hat))
    measure_scores['recall'].append(sklearn.metrics.recall_score(y_test, y_hat))
    measure_scores['f1'].append(sklearn.metrics.f1_score(y_test, y_hat))
    print("round:",count,"Classification report", sklearn.metrics.classification_report(y_test, y_hat))
    print("round:",count,"Confusion matrix", sklearn.metrics.confusion_matrix(y_test, y_hat))

    

#sss = StratifiedKFold(n_splits=10)
#np_X,np_y = np.asarray(X),np.asarray(y)
#sss.get_n_splits(np_X, np_y)
i = 1


for i in range(1,11):
    Xtrain = []
    Xtest = []
    ytrain = []
    ytest = []
    index = 0
    if(i == 1):
        while index < len(z):
            if(z[index] == 1):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    elif(i == 2):
        while index < len(z):
            if(z[index] == 2):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    elif(i == 3):
        while index < len(z):
            if(z[index] == 3):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    elif(i == 4):
        while index < len(z):
            if(z[index] == 4):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    elif(i == 5):
        while index < len(z):
            if(z[index] == 5):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    elif(i == 6):
        while index < len(z):
            if(z[index] == 6):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
       
    elif(i == 7):
        while index < len(z):
            if(z[index] == 7):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    elif(i == 8):
        while index < len(z):
            if(z[index] == 8):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    elif(i == 9):
        while index < len(z):
            if(z[index] == 9):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    elif(i == 10):
        while index < len(z):
            if(z[index] == 10):
                Xtest.append(X[index])
                ytest.append(y[index])
            else:
                Xtrain.append(X[index])
                ytrain.append(y[index])
            index += 1
        
    else:
        break
    print(i)
    automl(Xtrain, ytrain, Xtest, ytest, i)
#print(ytest)
print('precision_score',measure_scores['precision'],np.mean(measure_scores['precision']))
print('recall_score',measure_scores['recall'],np.mean(measure_scores['recall']))
print('f1_score',measure_scores['f1'],np.mean(measure_scores['f1']))

                


                




