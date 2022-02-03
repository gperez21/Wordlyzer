import string
import random
from typing import OrderedDict
from english_words import english_words_lower_alpha_set
import matplotlib.pyplot as plt

def five_letter_words():
	"""Return set of 5 letter words"""
	flw = []
	for w in english_words_lower_alpha_set:
		if len(w) == 5:
			flw.append(w)
	return flw

def pick_word(flws):
	"""Pick the wordle"""
	return random.choice(flws)

def score_word(answer, guess):
	"""Return Score of word in tuple form

	if letter is correct and in correct place return 2
	if letter is correct but not in correct place return 1
	if letter is in word but already guessed correctly -1
	if letter is not in word or in word but already in correct place return 0
	"""
	score = [0, 0, 0, 0, 0]
	for i, l in enumerate(guess):
		# correct
		if l == answer[i]:
			score[i] = 2
		# correct not in spot
		elif l in answer:
			score[i] = 1
		# not in word 
		else:
			score[i] = 0
	for i, l in enumerate(guess):
		if score[i] == 1:
			already_found = True
			for j, a in enumerate(answer):
				if j != i and a == l:
					if score[j] != 2:
						already_found = False
			if already_found:
				score[i] = -1
	return score

def valid_words(guess, score, last_round_valid):
	"""Return list of valid words"""
	new_valid = []
	required_letters = []
	for i, l in enumerate(guess):
		if score[i] != 0:
			required_letters.append(l)
	for w in last_round_valid:
		word_l = list(w)
		valid = True
		for i, l in enumerate(guess):
			# contains invalid letter
			if score[i] == 0:
				if l in word_l:
					valid = False
			# correct letter but can't be at index
			elif score[i] in [-1, 1]:
				if word_l[i] == l:
					valid = False
			elif score[i] == 2:
				if word_l[i] != l:
					valid = False
		for req in required_letters:
			if req not in w:
				valid = False
		if valid:
			new_valid.append(w)
	return new_valid

flws = five_letter_words()

def play_wordle(answer, starter_word):
	"""Iterate game based starter word and wordle word"""
	score = score_word(answer, starter_word)
	new_valid = five_letter_words()
	rounds = 1
	guesses = [starter_word]
	# print(answer)
	# print(starter_word, score)
	new_valid = valid_words(starter_word, score, new_valid)
	while score != [2, 2, 2, 2, 2]:
		new_guess = random.choice(new_valid)
		guesses.append(new_guess)
		score = score_word(answer, new_guess)
		# print(new_guess, score)
		new_valid = valid_words(new_guess, score, new_valid)
		rounds += 1
		if rounds > 500:
			break
	# print(answer, ": ", guesses)
	return rounds


w_list = ['reais', 'slate', 'aegis', 'lares', 'rales', 'tares', 'siren', 'raise',
		  'rents', 'snare', 'earns', 'store', 'learn', 'stead']
lowest_word = ''
low_score = 99
limit_list = []
for w in flws:
	if 'e' in w and 'a' in w:
		if 'z' not in w and 'x' not in w:
			if 's' in w or 't' in w or 'n' in w or 'r' in w or 'd' in w:
				limit_list.append(w)

words = {'salet': [], 'least':[]}
for x in words.keys(): #, 'quaky', 'zappy']: #['notes', 'resin', 'tares', 'senor', 'least']:
	value = 0
	# starter_word = input('Word...')
	starter_word = x
	if len(starter_word) < 3:
		print('Too short...')
		continue
	if starter_word == 'end':
		break
	trials, all_guesses = 0, 0
	# hist = OrderedDict({i+1: 0 for i in range(12)})
	scores = []
	for i in range(10000):
		answer = pick_word(flws)
		# answer = x
		starter_word = x #pick_word(flws)
		# if 'e' in starter_word or 'a' in starter_word:
		# 	continue
		tries = play_wordle(answer, starter_word)
		trials += 1
		all_guesses += tries
		# hist[tries] += 1
		scores.append(tries)
	avg_tries = all_guesses/trials
	if avg_tries < low_score:
		low_score = avg_tries
		lowest_word = starter_word
	print(f'Starting with -{starter_word}- results in average of {avg_tries} tries on 10,000 trials')
	# words[x] = [hist[i]/100000 for i in hist.keys()]
	words[x] = scores
	# plt.bar(hist.keys(), hist.values(), color='g')
	# plt.show()
	# print(f'Lowest word is {lowest_word}... best score is {low_score}')
for w in words.keys():
	plt.hist(words[w], [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12], alpha=0.5, label=f'Guessing for {w}')
plt.legend(loc='upper right')
plt.show()