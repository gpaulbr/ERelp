# -*- coding: utf-8 -*-
#!/usr/bin/python
import re, math,random
#from sklearn import neighbors

def word_vector(janela,lista):
   vector = list()
   for i in range(len(lista)):
      vector.append(0)
   for i in range(5):
      try:
         vector[lista[janela[i]]]= janela.count(janela[i])
      except:
         vector[0]+=1
   return vector

def classe(c):
      if c=="O":
         return 1
      elif c=="REL":
         return 0
      elif c==1:
         return 'O'
      elif c==0:
         return 'REL'
      else:
         print 'Não é BIL -', c

#transforma os csv em vetores de bag_of_words para o scikits
#X == matriz de features, y == classe
def gera_vetores_anotados(labelled,lista,tag='False'):
   X = []
   y = []
   c = 0
   word=prevW=prev2W=nextW=next2W=str()
   #print len(labelled)
   for tweet in labelled:
      #print tweet
      vector = list()
      for i in range(len(lista)):
         vector.append(0)
      n_words = len(tweet)
      for i in range(len(tweet)):
         if tag:
            word = tweet[i][0][0]+'/'+tweet[i][0][1]
         else:
            word = tweet[i][0]
         if i>0:
            if tag:
               prevW = tweet[i-1][0][0]+'/'+tweet[i-1][0][1]
            else:
               prevW = tweet[i-1][0]
         else:
            prevw = 'null'
         if i>1:
            if tag:
               prev2w = tweet[i-2][0][0]+'/'+tweet[i-2][0][1]
            else:
               prev2w = tweet[i-2][0]
         else:
            prev2s = 'null'
         if i < n_words-1:
            if tag:
               nextw = tweet[i+1][0][0]+'/'+tweet[i+1][0][1]
            else:
               nextw = tweet[i+1][0]
         else:
            nextw = 'null'
         if i < n_words-2:
            if tag:
               next2w = tweet[i+2][0][0]+'/'+tweet[i+2][0][1]
            else:
               next2w = tweet[i+2][0]
         else:
            next2w = 'null'
         words = (word,  prevW,prev2W,nextW,next2W)
         for j in range(5):
            try:      
               vector[lista[words[j]]]= words.count(words[j])
            except:
               vector[-1]+=1
         X.append(vector)
         c = classe(tweet[i][1])
         y.append(c)
   n = len([i for i in range(len(X)) if classe(y[i])=='O'])/2
   while n!=0:
      i = y.index(classe('O'))
      del X[i]
      del y[i]
      n-=1
      
#   while len([i for i in range(len(y)) if classe(y[i])=='U'])<len([i for i in range(len(y)) if classe(y[i])=='O']):
#      if  len([i for i in range(len(y)) if classe(y[i])=='U']) == 0:
#         break
#      X.extend([X[i] for i in range(len(y)) if classe(y[i])=='U'])
#      y.extend([y[i] for i in range(len(y)) if classe(y[i])=='U'])
#   while len([i for i in range(len(y)) if classe(y[i])=='B'])<len([i for i in range(len(y)) if classe(y[i])=='O']):
#      if len([i for i in range(len(y)) if classe(y[i])=='B'])==0:
#         break
#      X.extend([X[i] for i in range(len(y)) if classe(y[i])=='B'])
#      y.extend([y[i] for i in range(len(y)) if classe(y[i])=='B'])
#   while len([i for i in range(len(y)) if classe(y[i])=='L'])<len([i for i in range(len(y)) if classe(y[i])=='O']):
##      if len([i for i in range(len(y)) if classe(y[i])=='L'])==0:
#         break
#      X.extend([X[i] for i in range(len(y)) if classe(y[i])=='L'])
#      y.extend([y[i] for i in range(len(y)) if classe(y[i])=='L'])
#   while len([i for i in range(len(y)) if classe(y[i])=='I'])<len([i for i in range(len(y)) if classe(y[i])=='O']):
#      if len([i for i in range(len(y)) if classe(y[i])=='I'])==0:
#         break
#      X.extend([X[i] for i in range(len(y)) if classe(y[i])=='I'])
#      y.extend([y[i] for i in range(len(y)) if classe(y[i])=='I'])
         
   return (X,y)


def mod(v):
   m = 0
   for i in v:
      m+=i*i
   return float(m)**(1/2)


def KNN_prediction(KNN, X, y, wvector):
#   confidence = 0
#   mean_dist = 0
#   modulo_wvector = mod(wvector)
   c = KNN.predict([wvector])[0]
   cf = 0
   kneighbors_array = KNN.kneighbors([wvector],20,'distance')
   #if len(kneighbors_array[1][0])==0:
   #   raise Exception("merda")
   #try:
   kb = [((X[int(kneighbors_array[1][0][i])],y[int(kneighbors_array[1][0][i])]),kneighbors_array[0][0][i]) for i in range(len(kneighbors_array[0][0]))]
   for neighbor in kb:
#         modulo_neighbor = mod(neighbor[0][0])
      if neighbor[0][1]==c:
#         print cf, neighbor[1]
         try:
            cf+= float(1)*(float(1)/neighbor[1])
         except:
            cf += 1
#   except:
 #     print len(kneighbors_array[1][0]), kneighbors_array[1][0], len(X), len(y)
   
   return classe(c),cf/20

def KNN_train( tweets,lista,tagged=False):
   KNN = neighbors.KNeighborsClassifier(20,weights='distance')
   (X,y) = gera_vetores_anotados(tweets,lista,tagged)
   KNN.fit(X,y)
   return KNN,X,y

