import os
import nltk
# nltk.download()
from nltk.corpus import treebank
from nltk.probability import LaplaceProbDist
from nltk.tag.hmm import HiddenMarkovModelTrainer

from sklearn.metrics import accuracy_score

global words_count
global tags_count
global transition
global tags
global prob
global wt_prob
global word_tag
global START_STATE
global words

global TRAIN 
global INPUT
global OUTPUT

TRAIN  = './data_tagged.txt'
INPUT = './input.txt'
OUTPUT = './result.txt'

word_tag = {}
words_count = {}
words = set()
tags_count = {}
tags = set()
transition = {}
prob = {}
wt_prob = {}
START_STATE = 'uwuowo'

import pandas as pd
from tabulate import tabulate

def pretty_print_probs(distribs):
    
    rows = set()
    cols = set()
    for val in distribs.keys():
        # temp = val.split("|")
        rows.add(val[0])
        cols.add(val[1])
        
    rows = list(rows)
    cols = list(cols)

    df = []
    for i in range(len(rows)):
        temp = []
        for j in range(len(cols)):

            temp.append(distribs[(rows[i], cols[j])])
            
        df.append(temp)
        
    I = pd.Index(rows, name="rows")
    C = pd.Index(cols, name="cols")
    df = pd.DataFrame(data=df,index=I, columns=C)
    
    print(tabulate(df, headers='keys', tablefmt='psql'))

def prepareLib(train):
    tagged = []
    with open(train, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.lower()
            words = line.split()
            tmp = []
            for word in words:
                try:
                    word1, word2 = word.split('/')
                except ValueError:
                    print(line)
                tmp.append((word1, word2))
            tagged.append(tmp)
    f.close()
    return tagged

def get_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.isspace() or not line:
                continue
            else:
                line = line.lower() 
                build_model(START_STATE + '/' + START_STATE + ' ' + line)
    f.close()


def build_model(line):
    wordss = line.split()
    # print(words)
    for i in range(len(wordss)-1):
        current = wordss[i]
        nextt = wordss[i+1]
        # print(current, nextt)
        word1, tag1 = current.split('/')
        word2, tag2 = nextt.split('/')
        '''
        count the number of words
        '''
        if word1 != START_STATE:
            if word1 not in words_count:
                words_count[word1] = 1
            else:
                words_count[word1] += 1
            words.add(word1)
        if word2 not in words_count:
            words_count[word2] = 1
        else:
            words_count[word2] += 1
        words.add(word2)
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
        if word1 != START_STATE:
            if (word1, tag1) not in word_tag:
                word_tag[(word1, tag1)] = 1
            else:
                word_tag[(word1, tag1)] += 1
        if (word2, tag2) not in word_tag:
            word_tag[(word2, tag2)] = 1
        else:
            word_tag[(word2, tag2)] += 1

def calculateTransitionProbability():
    for pair in transition:
        tag1 = pair[0]
        count = 0
        for pair2 in transition:
            if pair2[0] == tag1:
                count+= transition[pair2]
        prob[pair] = (transition[pair] + 1)/ (count + len(tags))  #add laplace smoothing
    return prob

def transitionSmoothing():
    prob = calculateTransitionProbability()
    a = {}
    for pair in transition:
        if pair[0] in a:
            a[pair[0]] += transition[pair]
        else:
            a[pair[0]] = transition[pair]
    for tag in tags:
        if tag not in a.keys():
            a[tag] = 0
    for tag in tags:
        if (START_STATE, tag) not in prob:
            prob[(START_STATE, tag)] = 1 / (a[START_STATE] + len(tags))
    for tag1 in tags:
        for tag2 in tags:
            if (tag1, tag2) not in prob:
                prob[(tag1, tag2)] = (1) / (a[tag1] + len(tags))
    # pretty_print_probs(prob)
    return prob

def calculateWordTagProbability():
    for word in words_count:
        for tag in tags:
            count = 0
            if (word, tag) in word_tag:
                count = word_tag[(word, tag)]
            tmp = (count+1)/(tags_count[tag] + len(words))
            wt_prob[(word, tag)] = tmp
    return wt_prob

def viterbi(sentence, tags, prob, wt_prob, tag_count_emis, words):
    # print(prob)
    word_list = sentence.split()
    current_prob = {}
    for tag in tags:
        tp = 0
        em = 0
        if (START_STATE, tag) in prob:
            tp = (prob[START_STATE, tag])
        if word_list[0].lower() in words:
            if (word_list[0].lower(), tag) in wt_prob:
                em = (wt_prob[(word_list[0].lower(), tag)])
                current_prob[tag] = tp * em
        else:
            em = 1 / (tag_count_emis[tag] + len(words))
            current_prob[tag] = tp
    if len(word_list) == 1:
        max_path = max(current_prob, key=current_prob.get)
        return max_path
    else:
        for i in range(1, len(word_list)):
            previous_prob = current_prob
            current_prob = {}
            locals()['dict{}'.format(i)] = {}
            previous_tag = "uwuowo"
            for tag in tags:
                if word_list[i].lower() in words:
                    if (word_list[i].lower(), tag) in wt_prob:
                        em = (wt_prob[(word_list[i].lower(), tag)])
                        max_prob, previous_state = max((previous_prob[previous_tag] * 
                            prob[(previous_tag, tag)] * em, previous_tag) for previous_tag in
                                                       previous_prob)
                        current_prob[tag] = max_prob
                        locals()['dict{}'.format(i)][(previous_state, tag)] = max_prob
                        previous_tag = previous_state
                else:
                    # print(word_list[i])
                    em = (1) / (tag_count_emis[tag] + len(words))
                    try:
                        max_prob, previous_state = max((previous_prob[previous_tag] * prob[(previous_tag, tag)] * em, previous_tag) for previous_tag in previous_prob)
                    except TypeError:
                        print('ERROR')
                        # print(previous_prob[previous_tag])
                        # print((previous_tag, tag))
                        # print(prob)
                    current_prob[tag] = max_prob
                    locals()['dict{}'.format(i)][(previous_state, tag)] = max_prob
                    previous_tag = previous_state
            # print(max_prob)
            if i == len(word_list) - 1:
                max_path = ""
                last_tag = max(current_prob, key=current_prob.get)
                max_path = max_path + last_tag
                for j in range(len(word_list) - 1, 0, -1):
                    for key in locals()['dict{}'.format(j)]:
                        data1, data2 = key
                        if data2 == previous_tag:
                            max_path = max_path + " " + data1
                            previous_tag = data1
                            break
                result = max_path.split()
                result.reverse()
                return " ".join(result)

def writeOutput(init, result, accs, lib_res, lib_acc, file):
    # count = -1
    with open(file, 'a', encoding='utf-8') as f:
        for i in range(len(result)):
            f.write('init: {}'.format(init[i].lower()))
            f.write('mine: {}'.format(result[i]))
            f.write('\n')
            f.write(str(accs[i]))
            f.write('\n')
            f.write('lib: {}'.format(lib_res[i]))
            f.write('\n')
            f.write(str(lib_acc[i]))
            f.write('\n')
            f.write('\n')
    f.close()
    print(str(sum(accs)/len(accs)))
    print(str(sum(lib_acc)/len(lib_acc)))


def runWithLib():
    tagged = prepareLib(TRAIN)
    print(tagged)
    trainer = HiddenMarkovModelTrainer()
    tagger = trainer.train_supervised(tagged, estimator=LaplaceProbDist)
    result = []
    accs = []
    with open('./input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line, gt = splitAndReconstruct(line)
            pos = tagger.tag(line.split())
            string = ""
            pred = []
            for pair in pos:
                string = string+pair[0] + '/' + pair[1] + " "
                pred.append(pair[1])
            result.append(string)
            accs.append(accuracy_score(gt, pred))
            # print('\n')
    f.close()
    # writeOutput(result, accs, OUTPUT)
    return result, accs
            
def splitAndReconstruct(sentence):
    f = ""
    tags = []
    words_and_tags = sentence.split()
    for pair in words_and_tags:
        try:
            word, tag = pair.split('/')
        except ValueError:
            print(sentence)
        if f != "":
            f = f+' '
        f = f+word.lower()
        tags.append(tag.lower())
    return f, tags

def posTagging(line):
    # print(line.get())
    # sentence = line.get()
    get_words('./data_tagged.txt')
    # print(transition.items())
    prob = transitionSmoothing()
    wt_prob = calculateWordTagProbability()
    tag_count_emis = {}
    for probb in wt_prob.items():
        key_tag = probb[0]
        # print(key_tag)
        val = key_tag[-1]
        if val in tag_count_emis:
            tag_count_emis[val] += 1
        else:
            tag_count_emis[val] = 1
    sent = line.get().lower()
    # print(sent)
    path = viterbi(sent, tags, prob, wt_prob, tag_count_emis, words)
    tmp = sent.split()
    ptmp = path.split()
    string = ""
    for i in range(len(tmp)):
        if string != "":
            string = string + ' '
        string += tmp[i] + '/' + ptmp[i]
    print(string)
    return string
    

def main():
    get_words('./data_tagged.txt')
    # print(transition.items())
    prob = transitionSmoothing()
    wt_prob = calculateWordTagProbability()
    tag_count_emis = {}
    for probb in wt_prob.items():
        key_tag = probb[0]
        # print(key_tag)
        val = key_tag[-1]
        if val in tag_count_emis:
            tag_count_emis[val] += 1
        else:
            tag_count_emis[val] = 1
    
    print('1. demo with test data (label available)')
    print('2. demo with a random single sentence')
    k = int(input())
    if k == 1:
        init = []
        result = []
        accs = []
        with open('./input.txt', 'r', encoding='utf-8') as f:
            for line in f:
                init.append(line)
                line, gt = splitAndReconstruct(line)
                path = viterbi(line, tags, prob, wt_prob, tag_count_emis, words)
                tmp = line.split()
                ptmp = path.split()
                string = ""
                for i in range(len(tmp)):
                    string += tmp[i] + '/' + ptmp[i] + ' '
                result.append(string)
                acc = accuracy_score(gt, ptmp)
                # print('gt: {}'.format(gt))
                # print('pred: {}'.format(ptmp))
                accs.append(acc)
        f.close()
        lib_res, lib_acc = runWithLib()
        writeOutput(init, result, accs, lib_res, lib_acc, OUTPUT)
    else:
        sent = input()
        sent = sent.lower()
        path = viterbi(sent, tags, prob, wt_prob, tag_count_emis, words)
        tmp = sent.split()
        ptmp = path.split()
        string = ""
        for i in range(len(tmp)):
            if string != "":
                string = string + ' '
            string += tmp[i] + '/' + ptmp[i]
        print(string)
    # print('\n')
    
        
if __name__ == "__main__":
    main()