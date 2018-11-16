import csv
import sys
sys.path.insert(0, '../')

n_gram_filter = list()
def read_n_gram():
    with open("design-date-spec-ngram.txt", mode='r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in reader:
            words = row[5].strip()
            term = tuple(row[5].strip().split(' '))
            # global term frequency greater than 1
            if int(row[2]) <= 1:
                #print(row[5])
                continue
            n_gram_filter.append(row)
                    
def write_n_gram():
    with open("design-date-spec-filter-ngram.txt",mode='w+') as csvfile:
        writer = csv.writer(csvfile,delimiter='\t', quotechar='|')
#                for row in n_gram_filter[project+classified]:
#                    text = row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+"\t"+row[4]+"\t"+row[5]
        writer.writerows(n_gram_filter)
                
read_n_gram()
print(len(n_gram_filter))
write_n_gram()
#for i in n_gram_filter:
#    print(n_gram_filter[i][0])