spellcorrect
============

A program to correct non-word spelling error in sentences using ngram MAP Language Models, Noisy Channel Model, Error Confusion Matrix and Damerau-Levenshtein Edit Distance.

    class SpellCorrect
     |  A program to correct non-word spelling error in sentences using ngram MAP Language Models, Noisy Channel Model, Error Confusion Matrix and Damerau-Levenshtein Edit Distance.
     |  Usage:
     |  Input: 'she is a briliant acress'
     |  Response: she is a brilliant actress
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Constructor method to load external nGram class, load words, confusion matrix and dictionary.
     |  
     |  channelModel(self, x, y, edit)
     |      Method to calculate channel model probability for errors.
     |  
     |  dlEditDistance(self, s1, s2)
     |      Method to calculate Damerau-Levenshtein Edit Distance for two strings.
     |  
     |  editType(self, candidate, word)
     |      Method to calculate edit type for single edit errors.
     |  
     |  genCandidates(self, word)
     |      Method to generate set of candidates for a given word using Damerau-Levenshtein Edit Distance.
     |  
     |  loadConfusionMatrix(self)
     |      Method to load Confusion Matrix from external data file.
     |  
     |  loadDict(self)
     |      Method to load dictionary from external data file.
