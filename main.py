# words_alpha.txt file from: https://github.com/dwyl/english-words/blob/master/words_alpha.txt
# words_alpha contains many words not in the spellingbee dictionary

# popular.txt from https://github.com/dolph/dictionary/blob/master/popular.txt
# too restrictive

# word.list.txt from https://norvig.com/ngrams/word.list
# In between the 2 lists above, still contains many words not used in SpellingBee

import re

with open('word.list.txt') as f:
    words = f.read().splitlines()
# center = input('Enter Center Character: ')
# surrounding = input('Enter the Surrounding Characters')
center = 'h'
surrounding = 'crutao'

four_or_more = '{4,}'
p = re.compile(f'^[{center + surrounding}]{four_or_more}$')
words = [word for word in words if center in word and p.match(word)]
print(words)
print(f'There are {len(words)} words in the list')



