from MarkovChainBot import RedditBot
import time
from termcolor import colored

rb = RedditBot()
rb.LoadDictionary()

while 1:
	rb.LoadDictionary()
	print colored('Random message:','red')
	print rb.GenerateRandomMessage()

	time.sleep( 30 )