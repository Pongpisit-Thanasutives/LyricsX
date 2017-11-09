import re
import nltk
import random
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize,sent_tokenize
from textblob import TextBlob
from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from statistics import mode
### This is still under development ###
### For the simplicity sake, I use just only Naive Bayes algorithm while developing ###
### Negation handling with 1 not or n't : 1 sentence ###
### Negation adverb handling ###
def posTag(wordsTokenized):
	betterTag=[]
	nltkTag = nltk.pos_tag(wordsTokenized)
	for w,tag in nltkTag:
		betterTag.append((w.lower(),tag))
	return betterTag
def isNoun(tag):
	noun = "N[\w]*"
	if re.search(noun,tag) and tag[0]=='N':
		return True
	else:return False
def isAdjective(tag):
	adjective = "J[\w]*"
	if re.search(adjective,tag) and tag[0]=='J':
		return True
	else:return False
def isAdverb(tag):
	adverb = "R[\w]*"
	if re.search(adverb,tag) and tag[0]=='R':
		return True
	else:return False
def isVerb(tag):
	verb = "V[\w]*"
	if re.search(verb,tag) and tag[0]=='V':
		return True
	else:return False 
def isPunctuation(word,tag):
	if word==tag:return True
	else:return False
def isPrep(tag):
	if tag=='IN':return True
	else:return False
class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self._classifiers = classifiers
	def classify(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		return mode(votes)
def find_features(ref_words,doc):
	words=set(doc)
	features={}
	for w in ref_words:
		features[w]=(w in words)
	return features
def confidence(self, features):
	votes = []
	for c in self._classifiers:
		v = c.classify(features)
		votes.append(v)
	choice_votes = votes.count(mode(votes))
	conf = choice_votes / len(votes)
	return conf
dataset=open("dataset.txt",encoding='utf8')
data=[];all_words=[]
for line in dataset:
	### Constructing data ###
	line=line.strip().replace('\ufeff','')
	wordAndTag=posTag(word_tokenize(line.split('#')[0]))
	if ('not','RB') in wordAndTag or ("n't",'RB') in wordAndTag or ('never', 'RB') in wordAndTag:
		lst=[]
		indexOfNegation=-1
		try:
			indexOfNegation=wordAndTag.index(('not','RB'))
		except ValueError:
			try:
				indexOfNegation=wordAndTag.index(("n't",'RB'))	
			except ValueError:
				indexOfNegation=wordAndTag.index(('never', 'RB'))
		s_left=wordAndTag[0:indexOfNegation+1]
		for eachWord,tag in s_left:
			lst.append(eachWord)
		s_right=wordAndTag[indexOfNegation+1:]
		punctuationFound=False
		for eachWord,tag in s_right:
			if isPunctuation(eachWord, tag):
				punctuationFound=True
			if punctuationFound==False:
				lst.append('not_'+eachWord)
			else:
				lst.append(eachWord)
		# print(lst)
		data.append((lst,line.split('#')[1]))	
	else:
		data.append((word_tokenize(line.split('#')[0]),line.split('#')[1]))
	### Constructing all_words ###
	if ('not','RB') in wordAndTag or ("n't",'RB') in wordAndTag or ('never', 'RB') in wordAndTag:
		idx=-1
		try:
			idx=wordAndTag.index(('not','RB'))
		except ValueError:
			try:
				idx=wordAndTag.index(("n't",'RB'))
			except ValueError:
			 	idx=wordAndTag.index(('never', 'RB'))
		withoutNegation_left=wordAndTag[0:idx]
		withoutNegation_right=wordAndTag[idx+1:]
		# print(withoutNegation_left,"left")
		# print(withoutNegation_right,"right")
		for w,tag in withoutNegation_left:
			if isVerb(tag) or isAdjective(tag) or isAdverb(tag) or isPrep(tag):
				all_words.append(w)
		isPunctuationFound=False
		for w,tag in withoutNegation_right:
			if isPunctuation(w, tag):
				isPunctuationFound=True
			if isPunctuationFound==False:
				if isVerb(tag) or isAdjective(tag) or isAdverb(tag) or isPrep(tag):
					all_words.append('not_'+w)
			else:
				if isVerb(tag) or isAdjective(tag) or isAdverb(tag) or isPrep(tag):
					all_words.append(w)
		isPunctuationFound=True
	else:
		withoutNegation=wordAndTag
		# print(withoutNegation)
		for w,tag in withoutNegation:
			if isVerb(tag) or isAdjective(tag) or isAdverb(tag) or isPrep(tag):
				all_words.append(w)
# print(data)
all_words=nltk.FreqDist(all_words)
# print(all_words.most_common(30))
word_feature=list(all_words.keys())
feature=[(find_features(word_feature,review),category) for (review,category) in data]
train_set=feature
classifier=nltk.NaiveBayesClassifier.train(train_set)
###Testing session###
while 1:
	sample_text=input("Sample text : ").lower()
	# Wtf is considered to be misspelled in general english dictionary
	sample_text=sample_text.replace("dont","don't").replace("didnt","didn't").replace("doesnt","doesn't").replace("havent","haven't").replace("hasnt","hasn't").replace("cant","can't")
	sample_text_tags=nltk.pos_tag(word_tokenize(sample_text))
	if ('not','RB') in sample_text_tags or ("n't",'RB') in sample_text_tags or ("never",'RB') in sample_text_tags:
		negationPosition=-1
		properWordsTokenized=[]
		try:
			negationPosition=sample_text_tags.index(('not','RB'))
		except ValueError:
			try:
				negationPosition=sample_text_tags.index(("n't",'RB'))
			except ValueError:
				negationPosition=sample_text_tags.index(('never','RB'))
		sample_text_left=sample_text_tags[0:negationPosition+1]	 	
		for eachWord,tag in sample_text_left:
			properWordsTokenized.append(eachWord)
		sample_text_right=sample_text_tags[negationPosition+1:]
		puncFound=False
		for eachWord,tag in sample_text_right:
			if isPunctuation(eachWord, tag):
				puncFound=True
			if puncFound==False:
				properWordsTokenized.append('not_'+eachWord)
			else:
				properWordsTokenized.append(eachWord)
		# print(properWordsTokenized)
		# print(find_features(word_feature,word_tokenize(sample_text)))
		print(classifier.classify(find_features(word_feature,properWordsTokenized)))
	else:
		# print(nltk.pos_tag(word_tokenize(sample_text)))
		# print(find_features(word_feature,word_tokenize(sample_text)))
		print(classifier.classify(find_features(word_feature,word_tokenize(sample_text))))