import csv
import re
import io


file = open("design-post-process.txt","w+")
with open("Date_SATD.csv", mode='r') as infile:
    reader = csv.reader(infile, delimiter=',')
    next(reader)
    count = 0
    countnon=0
    countnull=0



    for rows in reader:

        tempSentence = ""
        temp = rows[0]
        temp = temp.strip()

        if(temp == "apache-ant-1.7.0"):
            tempSentence = "1" + "\t"
        if(temp == "apache-jmeter-2.10"):
            tempSentence = "2" + "\t"
        if(temp == "argouml"):
            tempSentence = "3" + "\t"
        if(temp == "columba-1.4-src"):
            tempSentence = "4" + "\t"
        if(temp == "emf-2.4.1"):
            tempSentence = "5" + "\t"
        if(temp == "hibernate-distribution-3.3.2.GA"):
            tempSentence = "6" + "\t"
        if(temp == "jEdit-4.2"):
            tempSentence = "7" + "\t"
        if(temp == "jfreechart-1.0.19"):
            tempSentence = "8" + "\t"
        if(temp == "jruby-1.4.0"):
            tempSentence = "9" + "\t"
        if(temp == "sql12"):
            tempSentence = "10" + "\t"

            
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
        if (rows[1] == "WITHOUT_CLASSIFICATION"):
            tempSentence = tempSentence + "0" 
            #countnon = countnon + 1
            #continue 
        if (rows[1] == "DESIGN"):
            tempSentence = tempSentence + "1"
            #countnon = countnon + 1
            #continue
        if (rows[1] == "IMPLEMENTATION"):
            #tempSentence = tempSentence + "1"
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

        p = p.strip()
        if(len(p) == 0):
            countnull = countnull + 1
            continue
        tempSentence = tempSentence + "\t" + p
        tempSentence = tempSentence.lower()
        tempSentence = tempSentence.lstrip()
        tempSentence = tempSentence.rstrip()
        #if(len(tempSentence)==3):
            #countnull = countnull + 1
            #continue
        file.write(str(tempSentence)+ "\n")
        count = count + 1

    print("normal = ",count)
    print("not use = ",countnon)
    print("null = ",countnull)
    
file.close()