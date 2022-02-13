quotes = []
with open('quotes.txt', encoding = 'UTF-8') as fin:
    for line in fin.readlines():
        line = line.rstrip()
        quotes.append((line, len(line)))

import time, random

print('Typing practice starts in 3 seconds.')
time.sleep(1)
print('Typing practice starts in 2 seconds.')
time.sleep(1)
print('Typing practice starts in 1 seconds.')
time.sleep(1)

accuracy = 0
count = 1
highest_speed = 0
while True:
    typing = quotes[random.randint(0, len(quotes) - 1)]
    print('%d: %s' % (count, typing[0]))
    print('%d: ' % count, end = '')
    time1 = time.time()
    s = input().rstrip()
    time2 = time.time()

    while len(s) < typing[1]:
        s += ' '

    identical = 0
    for i in range(typing[1]):
        if s[i] == typing[0][i]:
            identical += 1

    current_accuracy = identical / typing[1] * 100
    speed = current_accuracy / 100 * typing[1] * 60 / (time2 - time1)
    print('Speed: %.2f typings per minute' % speed)
    highest_speed = max(speed, highest_speed)
    print('Highest Speed: %.2f typings per minute' % highest_speed)
    print('Current Accuracy: %.2f%%' % current_accuracy)

    accuracy *= count - 1
    accuracy += current_accuracy
    accuracy /= count
    print('Total Accurancy: %.2f%%' % accuracy)
    print()

    count += 1
