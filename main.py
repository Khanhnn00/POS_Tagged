
import os

global words_count
global tags_count
global transition
global tags
global prob
global wt_prob
global word_tag

word_tag = {}
words_count = {}
tags_count = {}
tags = set()
transition = {}
prob = {}
wt_prob = {}


def get_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.isspace() or not line:
                continue
            else:
                line = line.lower() 
                build_model(line)
    f.close()


def build_model(line):
    words = line.split()
    # print(words)
    for i in range(len(words)-1):
        current = words[i]
        nextt = words[i+1]
        print(current, nextt)
        word1, tag1 = current.split('/')
        word2, tag2 = nextt.split('/')
        '''
        count the number of words
        '''
        if word1 not in words_count:
            words_count[word1] = 1
        else:
            words_count[word1] += 1
        if word2 not in words_count:
            words_count[word2] = 1
        else:
            words_count[word2] += 1
        '''
        count the number of tags
        '''
        if tag1 not in tags_count:
            tags_count[tag1] = 1
        else:
            tags_count[tag1] += 1
        if tag2 not in tags_count:
            tags_count[tag2] = 1
        else:
            tags_count[tag2] += 1
        '''
        count the number of transitions
        '''
        tag_pair = (tag1, tag2)
        if tag_pair not in transition:
            transition[tag_pair] = 1
        else:
            transition[tag_pair] += 1
        tags.add(tag1)
        tags.add(tag2)
        '''
        count the number of word having tag
        '''
        if (word1, tag1) not in word_tag:
            word_tag[(word1, tag1)] = 1
        else:
            word_tag[(word1, tag1)] += 1
        if (word2, tag2) not in word_tag:
            word_tag[(word2, tag2)] = 1
        else:
            word_tag[(word2, tag2)] += 1

def calculateTransitionProbability():
    for tag in tags:
        for tag2 in tags:
            count = 0
            if (tag, tag2) in transition:
                count = transition[(tag, tag2)]
            prob[(tag, tag2)] = count/ tags_count[tag]
    return prob

def calculateWordTagProbability():
    for word in words_count:
        for tag in tags:
            count = 0
            if (word, tag) in word_tag:
                count = word_tag[(word, tag)]
            tmp = count/tags_count[tag]
            wt_prob[(word, tag)] = tmp
    return wt_prob
            

def main():
    get_words('./data_tagged.txt')
    prob = calculateTransitionProbability()
    print(prob)
    # print(transition[('pdt', 'cd')])
    # print('===============================')
    # print(tags_count)
    # print('===============================')
    # print(tags)
    # print('===============================')
    # print(prob)
        
if __name__ == "__main__":
    main()