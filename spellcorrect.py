from __future__ import division
import ast
from ngram import nGram
import math as calc

class SpellCorrect():
    """A program to correct non-word spelling error in sentences using ngram MAP Language Models, Noisy Channel Model, Error Confusion Matrix and Damerau-Levenshtein Edit Distance.
Usage:
Input: 'she is a briliant acress'
Response: she is a brilliant actress"""
    def __init__(self):
        """Constructor method to load external nGram class, load words, confusion matrix and dictionary."""
        self.ng = nGram(True, True, False, False, False)
        self.words = sorted(set(self.ng.words))[3246:]
        self.loadConfusionMatrix()
        self.dict = self.loadDict()
        return

    def loadDict(self):
        """Method to load dictionary from external data file."""
        print "Loading dictionary from data file"
        f=open('dictionary.data', 'r')
        return f.read().split("\n")
    
    def dlEditDistance(self, s1, s2):
        """Method to calculate Damerau-Levenshtein Edit Distance for two strings."""
        s1 = '#' + s1
        s2 = '#' + s2
        m = len(s1)
        n = len(s2)
        D = [[0]*n for i in range(m)]
        for i in range(m):
             for j in range(n):
                 D[i][0] = i
                 D[0][j] = j
        for i in range(m):
            for j in range(n):
                dis=[0]*4
                if i == 0 or j == 0:
                    continue
                dis[0] = D[i-1][j] + 1
                dis[1] = D[i][j-1] + 1
                if s1[i] != s2[j]:
                    dis[2] = D[i-1][j-1] +2
                else:
                    dis[2] = D[i-1][j-1]
                if s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                    dis[3] = D[i-1][j-1] - 1
                if dis[3] != 0:
                    D[i][j] = min(dis[0:4])
                else:
                    D[i][j] = min(dis[0:3])
        return D[m-1][n-1]

    def genCandidates(self, word):
        """Method to generate set of candidates for a given word using Damerau-Levenshtein Edit Distance."""
        candidates = dict()
        for item in self.words:
            #print item, ", ",
            distance = self.dlEditDistance(word, item)
            if distance <= 1:
                candidates[item]=distance
        return sorted(candidates, key=candidates.get, reverse=False)

    def editType(self, candidate, word):
        "Method to calculate edit type for single edit errors."
        edit=[False]*4
        correct=""
        error=""
        x=''
        w=''
        for i in range(min([len(word),len(candidate)])-1):
            if candidate[0:i+1] != word[0:i+1]:
                if candidate[i:] == word[i-1:]:
                    edit[1]=True
                    correct = candidate[i-1]
                    error = ''
                    x = candidate[i-2]
                    w = candidate[i-2]+candidate[i-1]
                    break
                elif candidate[i:] == word[i+1:]:
                    
                    correct = ''
                    error = word[i]
                    if i == 0:
                        w = '#'
                        x = '#'+error
                    else:
                        w=word[i-1]
                        x=word[i-1]+error
                    edit[0]=True
                    break
                if candidate[i+1:] == word[i+1:]:
                    edit[2]=True
                    correct = candidate[i]
                    error = word[i]
                    x = error
                    w = correct
                    break
                if candidate[i] == word[i+1] and candidate[i+2:]==word[i+2:]:
                    edit[3]=True
                    correct = candidate[i]+candidate[i+1]
                    error = word[i]+word[i+1]
                    x=error
                    w=correct
                    break
        candidate=candidate[::-1]
        word=word[::-1]
        for i in range(min([len(word),len(candidate)])-1):
            if candidate[0:i+1] != word[0:i+1]:
                if candidate[i:] == word[i-1:]:
                    edit[1]=True
                    correct = candidate[i-1]
                    error = ''
                    x = candidate[i-2]
                    w = candidate[i-2]+candidate[i-1]
                    break
                elif candidate[i:] == word[i+1:]:
                    
                    correct = ''
                    error = word[i]
                    if i == 0:
                        w = '#'
                        x = '#'+error
                    else:
                        w=word[i-1]
                        x=word[i-1]+error
                    edit[0]=True
                    break
                if candidate[i+1:] == word[i+1:]:
                    edit[2]=True
                    correct = candidate[i]
                    error = word[i]
                    x = error
                    w = correct
                    break
                if candidate[i] == word[i+1] and candidate[i+2:]==word[i+2:]:
                    edit[3]=True
                    correct = candidate[i]+candidate[i+1]
                    error = word[i]+word[i+1]
                    x=error
                    w=correct
                    break
        if word == candidate:
            return "None", '', '', '', ''
        if edit[1]:
            return "Deletion", correct, error, x, w
        elif edit[0]:
            return "Insertion", correct, error, x, w
        elif edit[2]:
            return "Substitution", correct, error, x, w
        elif edit[3]:
            return "Reversal", correct, error, x, w
        

    def loadConfusionMatrix(self):
        """Method to load Confusion Matrix from external data file."""
        f=open('addconfusion.data', 'r')
        data=f.read()
        f.close
        self.addmatrix=ast.literal_eval(data)
        f=open('subconfusion.data', 'r')
        data=f.read()
        f.close
        self.submatrix=ast.literal_eval(data)
        f=open('revconfusion.data', 'r')
        data=f.read()
        f.close
        self.revmatrix=ast.literal_eval(data)
        f=open('delconfusion.data', 'r')
        data=f.read()
        f.close
        self.delmatrix=ast.literal_eval(data)

    def channelModel(self, x,y, edit):
        """Method to calculate channel model probability for errors."""
        corpus = ' '.join(self.ng.words)
        if edit == 'add':
            if x == '#':
                return self.addmatrix[x+y]/corpus.count(' '+y)
            else:
                return self.addmatrix[x+y]/corpus.count(x)
        if edit == 'sub':
            return self.submatrix[(x+y)[0:2]]/corpus.count(y)
        if edit == 'rev':
            return self.revmatrix[x+y]/corpus.count(x+y)
        if edit == 'del':
            return self.delmatrix[x+y]/corpus.count(x+y)
help(SpellCorrect)
sc = SpellCorrect()
#print sc.editType('acres', 'acress')
#print sc.genCandidates('acress')
#exit
while True:
    sentence = str(input('Input: ').lower()).split()
    correct=""    
    for index, word in enumerate(sentence):
        candidates = sc.genCandidates(word)
        if word in candidates:
            correct=correct+word+' '
            continue
        #print word, ': ', candidates
        NP=dict()
        P=dict()
        for item in candidates:
            
            #print item, ": ", sc.ng.unigram[item], ": ", sc.ng.unigramprobability(item)
            edit = sc.editType(item, word)
            #print item, ': ' , edit
            if edit == None: continue
            if edit[0] == "Insertion":
                NP[item] = sc.channelModel(edit[3][0],edit[3][1], 'add')
            if edit[0] == 'Deletion':
                NP[item] = sc.channelModel(edit[4][0], edit[4][1], 'del')
            if edit[0] == 'Reversal':
                NP[item] = sc.channelModel(edit[4][0], edit[4][1], 'rev')
            if edit[0] == 'Substitution':
                NP[item] = sc.channelModel(edit[3], edit[4], 'sub')
        for item in NP:
            channel = NP[item]
            if len(sentence)-1 != index:
                bigram = calc.pow(calc.e, sc.ng.sentenceprobability(sentence[index-1]+item+sentence[index+1], 'bi', 'antilog'))
            else:
                bigram = calc.pow(calc.e, sc.ng.sentenceprobability(sentence[index-1]+item, 'bi', 'antilog'))
            #print channel, ": ", unigram
            P[item] = channel*bigram*calc.pow(10,9)
        P = sorted(P, key=P.get, reverse=True)
        if P == []:
            P.append('')
        correct = correct +P[0] +' '
        
    print 'Response: '+correct
