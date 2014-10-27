# -*- coding: utf-8 -*-
import csv
import math
#from operator import itemgetter
import operator
#read the documents from state-of-the-union.csv, row[0] is the year and row[1] is the speeach
csv.field_size_limit(1000000000)
documentList = []
yearList = []

with open('state-of-the-union.csv','rb') as f:
	reader = csv.reader(f)
	for row in reader:
		yearList.append(row[0])
		documentList.append(row[1])
		#print yearList[i]
		#i += 1

#Tokenize the text of each speech

def tokenize(document):
	#transfer to lower case
	document = document.lower()
    #remove all punction characters
	chars = ['.', '/', "'", '"', '?', '!', '#', '$', '%', '^', '&','*', '(', ')', ' - ', '_', '+' ,'=', '@', ':', '\\', ',',';', '~', '`', '<', '>', '|', '[', ']', '{', '}', '–', '“','»', '«', '°', '’', '--']
    
	for c in chars:
		document = document.replace(c,' ')
    #split the strings by space
	document = document.split()
    
	stopwords = ['the', 'that', 'to', 'as', 'there', 'has', 'and', 'or', 'is', 'not', 'a', 'of', 'but', 'in', 'by', 'on', 'are', 'it', 'if']
	document = [w for w in document if w.lower().strip() not in stopwords]
	return list(document)

#count the number of words in a document
def wordCount(document):
	tokens = tokenize(document)
	return len(tokens)


tflist = []
words_in_doc = {}
words_in_files = {}
num_docs = len(documentList)

tfidfdocumenList = []	

for document in documentList:
	word_in_doc = {}
	docment_words = tokenize(document)


	for word in docment_words:
		if word in word_in_doc:
			word_in_doc[word] += 1
		else:
			word_in_doc[word] = 1

	for (word,freq) in word_in_doc.items():
		if word in words_in_files:
			words_in_files[word] += 1
		else:
			words_in_files[word] = 1

	words_in_doc[document] = word_in_doc						

for document in documentList:
	tfidfresult = []
	max_freq = 0;
	doclen = float (wordCount(document))
	for (word,freq) in words_in_doc[document].items():
		idf = math.log(float(num_docs) / float(words_in_files[word]))
		tfidf = float(freq) / float(doclen) * float(idf)
		tfidfresult.append([word, tfidf])
		
	tfidfdocumenList.append(tfidfresult)

sumdecade = []
for x in range(212, 223):
	sumdecade += tfidfdocumenList[x]

sumlist = {}
for [word,tfidf] in sumdecade:
	if word in sumlist:
		sumlist[word] += tfidf
	else:
		sumlist[word] = tfidf
		
print("The top 20 words in 1980")

for item in sorted(tfidfdocumenList[192],key=operator.itemgetter(1),reverse=True)[:20]:
	print "%f <= %s" % (item[1],item[0])

print("The top 20 words through decades")

for item in sorted(sumlist.items(),key=operator.itemgetter(1),reverse=True)[:20]:
	print "%f <= %s" % (item[1],item[0])	



