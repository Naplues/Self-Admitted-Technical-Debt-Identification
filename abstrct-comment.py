# coding: utf-8

# ## Abstract comment

# In[1]:


# import csv
import re
import pandas as pd
#from myconfig import *
file_name = ['Date_SATD.csv',"technical_debt_dataset.csv","SATD_sim.csv"]

comment = list()

def regex(comment):   
    p = re.sub(r'\\n',' ',comment)
    #Jun 9 2004 12:40 PM
    p = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) (([0-9])|([0-2][0-9])|([3][0-1])) \d{4} \d+:\d+ (PM|AM|pm|am)',' abstractdate',p)
    #January 1, 1970 00:00:00
    p = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) (([0-9])|([0-2][0-9])|([3][0-1])), \d{4} \d+:\d+:\d+ (PM|AM|pm|am)*',' abstractdate',p)
    #Dec 31 23:59:59 EST
    p = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) (([0-9])|([0-2][0-9])|([3][0-1])) \d+:\d+:\d+ [A-Z]{3}',' abstractdate',p)
    #12/4/04 9:10 AM
    p = re.sub(r'(0[1-9]|[12]\d|3[01])\/([1-9]|0[1-9]|1[0-2])\/(\d{2}) \d+:\d+ (PM|AM|pm|am)',' abstractdate',p)
    # 2006-03-06 23:16:24 +0100 (lun., 06 mars 2006)
    p = re.sub(r'\d+-\d+-\d+ \d+:\d+:\d+ [-|+]\d+ \([\S+ ]+\)',' abstractdate',p)
    #20070820
    p = re.sub(r'([12]\d{3})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])',' abstractdate',p)
    #2003-08-05
    p = re.sub(r'([12]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])',' abstractdate',p)
    #04-April-2001
    p = re.sub(r'(([0-9])|([0-2][0-9])|([3][0-1]))-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)-\d{4}',' abstractdate',p)
    # 21.02.2011
    p = re.sub(r'(0[1-9]|[12]\d|3[01])\.(0[1-9]|1[0-2])\.([12]\d{3})',' abstractdate',p)
    #03/14/2001
    p = re.sub(r'(0[1-9]|1[0-2])\/(0[1-9]|[12]\d|3[01])\/([12]\d{3}|\d{2})',' abstractdate',p)
    # 25/05 22/05/2012
    p = re.sub(r'(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/([12]\d{3}|\d{2})',' abstractdate',p)
    # 23 June 2013
    p = re.sub(r'(([0-9])|([0-2][0-9])|([3][0-1])) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) \d{4}',' abstractdate',p)
    #September 1998
    p = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) \d{4}',' abstractdate',p)
    #Sep 23, 2007
    p = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) (([0-9])|([0-2][0-9])|([3][0-1])), \d{4}',' abstractdate',p)
    #August 1st, 2006
    p = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) (([0-9])|([0-2][0-9])|([3][0-1]))(st|rd|nd|th), \d{4}',' abstractdate',p)
    #Nov. 2008
    p = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\. \d{4}',' abstractdate',p)

    p = re.sub(r'https?:\/\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',' abstracturl',p)
    p = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',' abstracturl',p)
    p = re.sub(r'(www\.)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',' abstracturl',p)
    

    #email
    #p = re.sub(r'[\w.-]+@[\w.-]+\.\w+',' abstractemail',p)
#     p = re.sub(r'(tomcat|jdk|hdfs|hadoop|servlet|yarn|cxf|camel|atmosphere|lmapreduce|hazelcast|catalina|hibernate)',' @abstractproduct ', p, flags=re.IGNORECASE)
#     p = re.sub(r'[^A-Za-z0-9]+',' ',p)
    p = re.sub(r'\s+',' ',p)
    return p

a = pd.read_csv(file_name[1],encoding = "ISO-8859-1")

#remove empty row
a=a.dropna()

print(len(a))
for ind_a,col_a in a.iterrows():
    a.loc[ind_a, 'commenttext'] = regex(col_a['commenttext'])
    
a.to_csv('Date_SATD.csv', index=False, quoting=2)



#from myconfig import *
'''from collections import OrderedDict
from operator import itemgetter    
import spacy
import csv
import operator
from collections import OrderedDict
import re
comments = list()
token = set()


with open(file_name[1], 'r',encoding='latin1') as csvfile:
    global token
    reader = csv.DictReader(csvfile)
    for row in reader:
        for word in row['commenttext'].strip().split(" "):
            token.add(word.strip().lower())
            
print(len(token))
nlp = spacy.load('en_core_web_md')  # make sure to use larger model!

string = ""
lenone = list()
lenmorethanone = list()
for i in token:
    string += i + " "
tokens = nlp(string)

print(len(tokens))
tokencamel =nlp(u'ant argouml columba emf hibernate jedit jfreechart jmeter jruby squirrel')
comments_sim = dict()
token_sets = set()
#file = open("FPositive-req.txt","w")
#score = dict()
#i = 0
for token1 in tokencamel:
    if(len(token1) < 2):
        continue
    for token2 in tokens:
        if(len(token2) < 2):
            continue
        #score[i] = dict()
        #score[i]['simscore'] = token1.similarity(token2)
        #score[i]['simword'] = str(token1) + " " + str(token2)
        #i += 1
        #score[token1.similarity(token2)] = token1.txt+" "+token2.txt
        if token1.similarity(token2) >= 0.9:
            comments_sim[token2.text] = token1.similarity(token2)
            token_sets.add(token2.text)
    token_sets.add(token1.text)
#sim_vector = list()
#sim_vector.extend(sorted(score.items(),key=lambda x: x[1]['simscore'],reverse=True))
#file.write(str(sim_vector))   
#file.close()
token_lists = sorted(list(token_sets))
print(token_lists)
r = re.compile(r'[a-z]+')
token_lists = filter(r.match, token_lists)
print(token_lists)
product_names = "|".join(token_lists)
print(product_names)



# In[3]:


# import csv
import re
import pandas as pd
comment = list()

def regex(comment):   
    p = re.sub(r'('+product_names+')',' abstractproduct ', comment, flags=re.IGNORECASE)
    p = re.sub(r'\s+',' ',p)
    return p

a = pd.read_csv(file_name[1],encoding = "ISO-8859-1")

#remove empty row
a=a.dropna()

print(len(a))
for ind_a,col_a in a.iterrows():
    a.loc[ind_a, 'commenttext'] = regex(col_a['commenttext'])
    
a.to_csv(file_name[2], index=False, quoting=2)

import spacy
import csv
import pandas as pd
nlp = spacy.load('en')
count = 0

a = pd.read_csv(file_name[2],encoding = "ISO-8859-1")

#remove empty row
a=a.dropna()

print(len(a))
for ind_a,col_a in a.iterrows():
    string = ""
    doc = nlp(col_a['commenttext'])
    for i in doc:
        temp = i.lemma_
        if(temp == "-PRON-"):
            temp = "pron"
        string = string + temp + " "
    string = string.lower()
    a.loc[ind_a, 'commenttext'] = string
    count += 1
print(count)
    
a.to_csv("technical_debt_dataset_ab_lem.csv", index=False, quoting=2)'''

