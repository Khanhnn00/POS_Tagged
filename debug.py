import os
import nltk
# nltk.download()
from nltk.corpus import treebank
from nltk.probability import LaplaceProbDist
from nltk.tag.hmm import HiddenMarkovModelTrainer

taggedsents = treebank.tagged_sents()
print(taggedsents)

trainer = HiddenMarkovModelTrainer()
tagger = trainer.train_supervised(taggedsents, estimator=LaplaceProbDist)
sent = 'When I graduated from a less than desirable college , no employers in New York would take me seriously'
pos = tagger.tag(sent.split())
print(pos)
# words = []
# with open('data.txt', 'r') as f:
#     for x in f:
#         x = x.replace(',', '')
#         tmp = x.split()
#         for each in tmp:
#             words.append(each)
#         words.append('//')
# f.close()
# # words = set(words)
# with open('analys.csv', 'wt', encoding='utf-8' ) as f:
#     for word in words:
#         f.write(word.lower())
#         f.write('\n')
# f.close()