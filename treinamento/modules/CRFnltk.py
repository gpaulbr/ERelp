# -*- coding: utf-8 -*-
#!/usr/bin/python

import re, math, sys
#from stringcrf2 import Instance, build_domain,StringCRF
from nltk.tag.crf import MalletCRF
import nltk.classify.mallet

def extractFeatures(tweet, indexWord):
    return tweet[indexWord]

#chamada do Mallet passando a fcao de extracao de features
def CRFTrain(labelled, it):    
   crf = MalletCRF.train(extractFeatures,labelled,filename="mallet_" + str(it) + "it")#,max_iterations=10)
   
   return crf

#DEVE SER A PRIMEIRA FUNÇÃO CHAMADA
#dir -  diretorio do mallet
def configMallet(dir):
    nltk.classify.mallet.config_mallet(dir)

def CRF_prediction(crf,tweet):
   l = crf.tag(tweet)
   labels = [d[1] for d in l]
   return labels#,p
   
   
