# coding=utf-8

"""
## Exercise 2
Lets make a model that generates chord porgressions that can be trained with sequences of observed progressions fo a style. And come up with at least 
one variable to steer the model. The input sequences can be for  examples: cM, a7m, dm, dm, etc... We can decide to make a mood-controlled progression 
generator that favours (or disfavours) major or minor chords. Additionally we could have a "simplicity" value that would favour (or disfavour) chords that 
have only three notes or chords that are more complex. Another addition would be to control the length of the chord progression or the density of the rhythmic 
changes."""


#UTIL FUNCTIONS I:

import os
import numpy as np
import random

#Split chord name in Tonic and Chord: OK!

def split3 (chord):
  if (chord[1]=='b' or chord[1]=='#'):
    a=chord[0]+chord[1]
    b= chord[2:len(chord)]
  else:
    a=chord[0]
    b= chord[1:len(chord)]
  return (a, b)

def cod_nota(st):
    notes = {"A": 0, "A#":1, "Bb": 1, "B": 2, "Cb": 2, "C": 3, 
                     "D": 5,"Eb":6,
        "E": 7,"F": 8,"Gb": 9, "G": 10, 'G#': 11, 'Ab': 11
    }
    return notes.get(st, None)

def cod_interv(st):
    chord_type = {
        "M": 0,
        "m": 1,
        "Maj7": 2,
        "m7": 3,
        "7":4,
        "dim": 5,
        'semidim': 6
    }
    return chord_type.get(st, None)



def cod_tuple(tupla):
    
    cod1 = cod_nota(tupla[0])
    cod2 = cod_interv(tupla[1])

    return (cod1, cod2)


def chord_2_tupla(chord):
  c_split= split3(chord)
  #c_split= split_name (chord)
  chord_cod=cod_tuple(c_split)
  return chord_cod

#Build chord from tupla
def full_chord(tupla):
    chord=[]
    chords_dict = {0: [0, 4, 7], 1: [0,3,7], 2:[0, 4, 7, 11], 3:[0, 3, 7, 10],
                     4:[0, 4, 7, 10], 5: [0, 3, 6 ,9], 6:[0, 3, 6, 10]}
    midi_offset=69
    nota=tupla[0]+midi_offset
    #print(nota)
    progresion=chords_dict.get(tupla[1], None)
    #print(progresion)
    for num in progresion:
     chord.append(num+nota)
    return chord

#UTIL FUNCTIONS II:

def event_list_2_pdf(event_list):

  events, counts = np.unique(event_list, return_counts=True, axis=0)
  
  events=[tuple(x) for x in events]
  #pdf=counts/sum(counts) #ERROR: AQUI ESTA EL FALLO!!!!! #Bien pa py3, MAL pa py2.7
  pdf = counts.astype(float) / sum(counts) #PYTHON 2.7

  return events, pdf
#-------------------------------------------------------------------------------

def select_event_from_pdf (events, pdf):
  event_indexes=range(len(events))
  
  u= np.random.choice(event_indexes, 1, p=pdf)[0]
 
  return events[u]

#-------------------------------------------------------------------------------

def train(input_sequence):
  observed_transitions={}
  for i in range(len(input_sequence)-1):
    if input_sequence[i] in observed_transitions:
      observed_transitions[input_sequence[i]].append(input_sequence[i+1])
    else:
      observed_transitions[input_sequence[i]]=[input_sequence[i+1]]
  
  # now lets make compact versions of the values
  pdf_dict={}
  for key in observed_transitions:
    pdf_dict[key]=[event_list_2_pdf(observed_transitions[key])]

  return pdf_dict

#-------------------------------------------------------------------------------

def chords_from_pdf(trained_pdf, N, cond1):
  list_Maj=[0, 2]
  list_min=[1, 3, 6]
  list_5=[4,5]
  output_sequence=[]
  now=random.choice(list(trained_pdf.keys()))

  output_sequence.append(now)

  for x, i in enumerate(range(N-1)):

    next_events, next_pdf=trained_pdf[now][0] #******* NEXT!

    #[1]]
    pdf_cond = []

    if (cond1==0): #favour Major chords
      for tupla in next_events:
        if(tupla[1] in list_Maj):
          pdf_cond.append(3)
        elif(tupla[1] in list_min):
          pdf_cond.append(1)
        elif (tupla[1] in list_5):
          pdf_cond.append(2)

    elif (cond1==1): #favour Minor chords
      for tupla in next_events:
        if(tupla[1] in list_min):
          pdf_cond.append(3)
        elif(tupla[1] in list_Maj):
          pdf_cond.append(1)
        elif (tupla[1] in list_5):
          pdf_cond.append(2)

    if (cond1==2): #favour V chords
      for tupla in next_events:
        if(tupla[1] in list_Maj):
          pdf_cond.append(1)
        elif(tupla[1] in list_min):
          pdf_cond.append(1)
        elif (tupla[1] in list_5):
          pdf_cond.append(2)
      
 
    pdf_new=[] #PDF_New= pdf
    pdf_mult = [next_pdf[i] * pdf_cond[i] for i in range(len(next_pdf))] #multiply original pdf with pdf_cond
    pdf_new = [elem/sum(pdf_mult) for elem in pdf_mult]#Normalyzing new PDF

    next= select_event_from_pdf(next_events,pdf_new)
    #FIN[1]
  
    now=next
    
    output_sequence.append(now)
  
  return output_sequence




def chord_prog(N, cond1):

  autum_leaves= ['Cm7', 'F7', 'BbMaj7', 'EbMaj7','Adim', 'D7', 'Gm', 'Gm',
               'Cm7', 'F7', 'BbMaj7', 'EbMaj7','Adim', 'D7', 'Gm', 'Gm',
               'Adim', 'D7', 'Gm', 'Gm', 'Cm7', 'F7', 'BbMaj7', 'EbMaj7',
               'Adim', 'D7', 'Gm7', 'Gb7', 'Fm7', 'E7', 'Adim', 'D7', 'Gm']
  autum_cod=[]
  autum_cod = [chord_2_tupla(chord) for chord in autum_leaves]

  trained_pdf = train(autum_cod)

  chords= chords_from_pdf(trained_pdf, N, cond1)

  prog=[]
  [prog.append(full_chord(x)) for x in chords]
  return prog

