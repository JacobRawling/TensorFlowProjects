from MarkovChainBot import RedditBot

rb = RedditBot()
rb.LoadDictionary()
#rb.Train('Choose an encoding standard. Click the File tab, or in Word 2007 click the Microsoft Office Button . Click Save As. In the File name box, type a new name for the file. In the Save as type box, select Plain Text. Click Save. If the Microsoft Office Word Compatibility Checker dialog box appears, click Continue.')
#rb.SaveDictionary()
#rb.LearnFromSubbredit('askreddit',100)
rb.LearnFromSubbredit('askscience',25)
#rb.PrintDictionary()

#rb.LoadDictionary()
#print rb.GenerateMessage(['I','think'])

while 1:
	input = raw_input('')
	words = input.split()
	key = []
	if len(words) < 2:
		continue
	for i in range(0,2):
		key.append(words[i])
	print rb.GenerateMessage(key)



#tb.SaveDictionary()
#tb2 = TwitterBot()
#tb2.LoadDictionary()