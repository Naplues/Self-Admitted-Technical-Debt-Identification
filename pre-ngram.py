import csv
import re
import io

file = open("design-pre-ngram.txt","w+")
with open("Date_SATD.csv", mode='r') as infile:
    reader = csv.reader(infile, delimiter=',')
    next(reader)
    count = 0
    countnon=0
    countnull=0
    for rows in reader:

        tempSentence = ""
        if (rows[1] == "DEFECT"):
            #tempSentence = tempSentence + "1"
            #countdef += 1
            countnon = countnon + 1
            continue
        if (rows[1] == "TEST"):
            #tempSentence = tempSentence + "1"
            countnon = countnon + 1
            continue
            #countdef += 1  
        if (rows[1] == "DOCUMENTATION"):
            #tempSentence = tempSentence + "1"
            #countdef += 1 
            countnon = countnon + 1
            continue  
        #if (rows[1] == "WITHOUT_CLASSIFICATION"):
            #countnon = countnon + 1
            #continue 
            #tempSentence = tempSentence + "0"
            #print("yeah")
        #if (rows[1] == "DESIGN"):
            #tempSentence = tempSentence + "1"
            #countnon = countnon + 1
            #continue
        if (rows[1] == "IMPLEMENTATION"):
            tempSentence = tempSentence + "1"
            countnon = countnon + 1
            continue

        p = re.sub(r'\\n',' ',rows[2])
        p = re.sub(r'[?]', ' questionMark ', p)
        p = re.sub(r'["]', ' quote0 ', p)
        p = re.sub(r'[`]', ' quote1 ', p)
        p = re.sub(r'[{]', ' quote2 ', p)
        p = re.sub(r'[}]', ' quote3 ', p)
        p = re.sub(r'[(]', ' quote4 ', p)
        p = re.sub(r'[)]', ' quote5 ', p)
        p = re.sub(r'[\']', ' quote6 ', p)
        p = re.sub(r'[,]', ' quote7 ', p)
        p = re.sub(r'[@]', ' quote8 ', p)
        p = re.sub(r'[:]', ' quote9 ', p)
        p = re.sub(r'[;]', ' quote10 ', p)
        p = re.sub(r'[<]', ' quote11 ', p)
        p = re.sub(r'[>]', ' quote12 ', p)
        p = re.sub(r'[!]', ' quote13 ', p)
        p = re.sub(r'[.]', ' quote14 ', p)
        p = re.sub(r'[-]', ' quote15 ', p)
        p = re.sub(r'[=]', ' quote16 ', p)
        p = re.sub(r'[_]', ' quote17 ', p)
        p = re.sub(r'[+]', ' quote18 ', p)
        p = re.sub(r'[/]', ' quote19 ', p)
        p = re.sub(r'[\[]', ' quote20 ', p)
        p = re.sub(r'[\]]', ' quote21 ', p)
        p = re.sub(r'[*]', ' quote22 ', p)
        p = re.sub(r'[|]', ' quote23 ', p)
        p = re.sub(r'[~]', ' quote24 ', p)
        p = re.sub(r'[\^]', ' quote25 ', p)
        p = re.sub(r'[\\]', ' quote26 ', p)
        p = re.sub(r'[$]', ' quote27 ', p)
        p = re.sub(r'[%]', ' quote28 ', p)
        p = re.sub(r'[#]', ' quote29 ', p)
        p = re.sub(r'[&]', ' quote30 ', p)
        p = re.sub(r'[^A-Za-z0-9]+',' ',p)
        p = re.sub(r'\s+', ' ', p)

        '''p = re.sub(r'\\n', ' ', rows[2])
        p = re.sub(r'[^A-Za-z0-9]+', ' ', p)
        p = re.sub(r'\s+', ' ', p)'''

        tempSentence = tempSentence + p
        tempSentence = tempSentence.lower()
        tempSentence = tempSentence.strip()
        if(len(tempSentence)==0):
            countnull = countnull + 1
            continue
        tempSentence = chr(0x02) + chr(0x03) + '\n' + tempSentence + '\n' 
        file.write(str(tempSentence))
        count = count + 1
    print("normal = ",count)
    print("not use = ",countnon)
    print("null = ",countnull)
    
file.close()