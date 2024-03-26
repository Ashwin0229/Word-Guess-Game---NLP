'''
Name   : Ashwin Sai C
Course : NLP - CS6320-001
Title  : Homework 1: Word Guess Game
Term   : Spring 2024

'''

from   collections import OrderedDict
import nltk
from   nltk.corpus import stopwords
from   nltk.stem   import WordNetLemmatizer
import random
import sys

def Read_File(filename):
	'''
		Parameters:
			filename : it is the name of the file to be read and parsed

		Description:
			This function gets the filename as input, reads the file and 
			returns the file data.

		return:
			data: it contains the lines read from the file given
	'''

	file_handle = open(filename,"r")
	data        = file_handle.readlines()
	file_handle.close()

	return data

def Calculate_Lexical_Diversity(data):
	'''
		Parameters:
			data : it contains the lines read from the file given.

		Description:
			This function is used to calculate the Lexical Diversity
			of the words/tokens present in the given filename.

		return:
			No return data
	'''
	
	tokens_list = []	

	for sent in data:
		for word in nltk.word_tokenize(sent):
			tokens_list.append(word)

	unique_list = set(tokens_list)
	# print(len(tokens_list))
	# print(len(unique_list))

	#lexical diversity = number of unique tokens / total number of tokens
	lexical_diversity_value = len(unique_list) / len(tokens_list)

	print("\nLexical Diversity : ",round(lexical_diversity_value,2),'\n')

def Preprocess_RawText(data):
	'''
		Parameters:
			data : it contains the lines read from the file given.

		Description:
			This function preprocess the data from the file by filtering,
				-only alphabet tokens
				-lower case
				-token length >= 5
				-tokens not in stopwords list
				-lemmatizing tokens and create a list of unique lemmatized tokens
				-pos tagging the unique tokens (print 20 tokens)
				-list lemmas that are nouns

		return:
			preprocessed_list : preprocessed set of tokens
			NN_list           : list of unique nouns
	'''

	stop_words = set(stopwords.words('english'))

	preprocessed_list      = []
	lemmatized_text        = []
	unique_lemmatized_list = []	
	NN_list                = []

	#preprocessing the tokens for isalpha(), not in stopwords and length > 5
	for sent in data:
		for word in nltk.word_tokenize(sent):
			if word.lower().isalpha() and word.lower() not in stop_words and len(word) > 5:
				preprocessed_list.append(word.lower())

	#lemmatizing the preprocessed tokens
	lemmatized_text        = [WordNetLemmatizer().lemmatize(word.lower()) for word in preprocessed_list]
	#unique list of lemmatized tokens
	unique_lemmatized_list = list(set(lemmatized_text))
	#po tagging
	pos_tagged_lemma       = nltk.pos_tag(unique_lemmatized_list)

	print("The first 20 words with tags..")
	for index in range(0,20):
		print(index,'. ',pos_tagged_lemma[index])

	#filtering out only the nouns
	NN_list = [word for word, tag in pos_tagged_lemma if tag == "NN" or tag == "NNS" or tag == "NNP" or tag == "NNPS"]

	print("\nNumber of Tokens : ",len(preprocessed_list), " Number of Nouns : ",len(NN_list))


	return [preprocessed_list, NN_list]

def NounCount_Mapping(tokens_list, NN_list):
	'''
		Parameters:
			tokens_list : preprocessed list of tokens from file
			NN_list     : unique nouns list

		Description:
			This function is used to map the occurence of each noun from the NN_list
			to the tokens list. (Ex. {noun: number of times the noun occured in token list}})

		return:
			top_common_nouns: returns the top 50 nouns sorted in decreasing order based on occurrence.
	'''

	noun_count       = {}
	sorted_noun      = {} 
	top_common_nouns = []

	#map noun in dict with its occurrence in the token list
	for noun in NN_list:
		noun_count[noun] = tokens_list.count(noun)

	# print(len(noun_count))

	#sorting the nouns based on occurrence
	sorted_noun      = dict(sorted(noun_count.items(), key=lambda x: x[1], reverse=True))
	sorted_noun_keys = list(sorted_noun.keys())

	print("\nThe first 50 most common words and counts..")
	top_common_nouns = sorted_noun_keys[:50]
	for index,key in enumerate(top_common_nouns):
		print(index,'. ',key," : ",sorted_noun[key])

	return top_common_nouns

def Guess_Game(nouns):
	'''
		Parameters:
			nouns : the top 50 nouns present in the token list

		Description:
			This function creates a guess game to guess what noun is displayed.
			The game goes on until
				-score is greater than or equal to 0
				-user does not enter '!'
				-successfully guessed a word and wants to continue more.
			The game ends if
				-score is less than 0
				-user enters '!'
				-wants to terminate and play no more.

			The user enters a letter and if the letter is present in the word,
			the letter will be displayed in the place of occurrence and 1 point will
			be given to the user for every correct guess. If the letter is not present
			1 point will be reducted from the score and the wrong choices wont be 
			displayed in the word.

		return:
			No return data
	'''

	print("\n*********************Guess Game*********************\n")
	
	#flag whether to continue or terminate the game
	to_continue = "Y"
	points      = 5
	
	while to_continue == "Y":
		
		print("Let's play a word guessing game!\n")		
		choice         = ""
		choice_list    = []                               #list of correct user choices
		game_word      = ""                               #temporary word in game, changes based on user guess
		random_integer = random.randint(0, 49)
		guess_word     = nouns[random_integer]            #the word to be guessed
		
		#the word to be used for the guess game
		# print(guess_word)		

		while True:
			print("--------------------------")

			#empty the word, and repopulate based on choice list
			game_word = ""

			for ch in guess_word:
				if ch in choice_list:
					game_word += ch
				else:
					game_word += "_ "

			#prints the current word with guessed characters
			print(game_word)

			if game_word == guess_word:
				#Exits if correctly guessed.

				print("Congrats! You solved it!!")
				print("Current Score : ",points)
				print("--------------------------")
				break

			#user enters a letter
			choice = input("\nGuess a Letter : ").lower()			

			if choice == "!":
				print("Exiting the game.! Thank you for playing.")
				# break
				exit(0)

			while True:
				#input has to be only alphabets and non-repetitive characters

				if not choice.isalpha():
					print("Alphabets only!")
					choice = input("\nGuess a Letter : ")
				
				elif choice in choice_list:
					print("Already present!")
					choice = input("\nGuess a Letter : ")
				
				else:
					break			
			
			if choice in guess_word:			
				points += 1
				print("Right!. Score is : ",points,"\n")
				choice_list.append(choice)
			
			else:
				points -= 1
				print("Sorry, guess again!. Score is : ",points,"\n")				
				if points < 0:
					print("Game Over! Please try again!!")
					print("The word was '"+guess_word+"'")
					print("--------------------------")
					# break
					exit(0)

		to_continue = input("\n\nGuess another word Y/N : ")
		to_continue = to_continue.upper()

	print("\nThank you for playing.!!")

def Initiate_Program():
	'''
		Parameters:
			None

		Description:
			This function 
			 	-collects data from the file
			 	-calculates the lexical diversity
			 	-preprocesses the tokens and noun list
			 	-retreives the common noun list
			 	-starts the guess game

		return:
			No return data
	'''

	print("hi")

	try:
		print("Filename : ",sys.argv[1])		
	except Exception as e:
		print(e)
		print("File name is not given!")
		print("Try 'python algorithm1.py filename.txt'")
		exit()

	try:
		data                       = Read_File(sys.argv[1])
		Calculate_Lexical_Diversity(data)
		preprocessed_list, NN_list = Preprocess_RawText(data)
		top_common_nouns           = NounCount_Mapping(preprocessed_list,NN_list)
		Guess_Game(top_common_nouns)
	except Exception as e:
		print(e)

if __name__ == "__main__":
	'''
		Parameters:
			None

		Description:
			Start point of the program execution

		return:
			No return data
	'''

	Initiate_Program()