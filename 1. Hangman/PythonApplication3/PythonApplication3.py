word_list = []
with open('dictionary.txt') as fin:
    word_list = fin.readline().split()

import random
while True:
    print('Start: 1')
    print('Exit: 2')

    a = int(input())
    print()
    if a == 2:
        exit(0)

    word = word_list[random.randint(0, len(word_list) - 1)]
    len_word = len(word)

    s = ['_'] * len_word
    attempt = 0
    while ''.join(s) != word:
        print('Enter the letter. %s' % ''.join(s))
        letter = input().rstrip()
        exist = False

        for i in range(len_word):
            if word[i] == letter:
                exist = True
                s[i] = letter

        if ''.join(s) == word:
            print()
            print('Done! The answer is %s' % word)
            print('Your total attempt is %d' % attempt)
            print()
            break

        if not exist:
            print('There are no %s' % letter)
        
        attempt += 1
        print('Current attempt is %d' % attempt)
        print()