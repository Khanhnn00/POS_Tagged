import os

words = []
with open('data.txt', 'r') as f:
    for x in f:
        x = x.replace(',', '')
        tmp = x.split()
        for each in tmp:
            words.append(each)
        words.append('//')
f.close()
# words = set(words)
with open('analys.csv', 'wt', encoding='utf-8' ) as f:
    for word in words:
        f.write(word.lower())
        f.write('\n')
f.close()