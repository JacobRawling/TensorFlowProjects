import random 
import cPickle as pickle
import praw
import re
from tqdm import tqdm

class MarkovChainBot:
	chainLength = 2
	maxWords 	= 30
	stopPhrase  = '<Stop>'
	wordList	= {}
	#[ 'Hi', 'there'] = stopPhrase

	def Train(self, message):
		#loop over the message in chunks of 3 words
		for words in self.SplitMessage(message):
			#first two words are the key
			#last is the value  
			key = tuple(words[:-1])

			if key in self.wordList:
				##add to the set of allowed words
				self.wordList[ key ].append( words[self.chainLength] )
			else:
				self.wordList[ key ] = []
				self.wordList[ key ].append( words[self.chainLength] )
	def CleanString(self, message):
		message = re.sub('[:;@/?.>,<\|\[\]\"/\*\'^\\+=*\(\)\{\}0-9]','',message )
		message = message.encode('ascii', 'ignore').decode('ascii')
		return message 

	def SplitMessage(self, message):
		#split the message into an array of strings
		words = message.split()

		if len(words) > self.chainLength:			
			#add a stop condition
			words.append(self.stopPhrase)

			#cyclicly permuate the words 
			for i in range(len(words) - self.chainLength):
				yield words[i:i + self.chainLength + 1]

	def GenerateMessage(self,seed):
		generatedWords = [] 
		key = seed

		if tuple(key) in self.wordList: 
			for i in range(0,len(seed)):
				generatedWords.append(seed[i])

			for i in xrange(self.maxWords):
				##
				avaliableWords = self.wordList[ tuple(key) ]
				nextWord = avaliableWords[random.randint(0,len(avaliableWords)-1)]
				if nextWord == self.stopPhrase:
					#return generatedWords
					break
				else:
					generatedWords.append(nextWord)
					key = key[1:self.chainLength]
					key.append( nextWord )

		returnPhrase = ''
		for i in range(0,len(generatedWords)):
			returnPhrase += generatedWords[i] + ' '
		
		return returnPhrase

	def SaveDictionary(self):
		with open('data.p', 'wb') as fp:
    			pickle.dump(self.wordList, fp)
#    	print self.wordList
	
	def LoadDictionary(self):
		with open('data.p', 'rb') as fp:
  			self.wordList = pickle.load(fp)

  	def PrintDictionary(self):
		for keys,values in self.wordList.items():
		    print(keys)
		    print(values)


class RedditBot(MarkovChainBot):

	def LearnFromSubbredit(self,subreddit,nSubmission):
		print 'Getting all comments in first ' + `nSubmission` + ' posts from: ' + subreddit
		r = praw.Reddit(user_agent='my_cool_application')
		submissions = r.get_subreddit(subreddit).get_top(limit=nSubmission)
		pbar = tqdm(total=nSubmission,ncols=100)
		for submission in tqdm(submissions):
			pbar.update(1)
			self.Train(self.CleanString(submission.title))
			for comment in submission.comments:
				try:
					self.Train(self.CleanString(comment.body))
				except AttributeError:
					print "ERROR: comment did not have body."
		pbar.close()
		self.SaveDictionary()

