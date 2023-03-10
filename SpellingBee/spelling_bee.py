import unidecode
import pandas as pd
import numpy as np
import random
from gtts import gTTS
import os
import playsound
import datetime
import csv
import time


from get_word_info_functions import *


def scrub_word_list(word_list):
    # clean up each word spelling...
    newList = [None]*len(word_list) # create empty list
    newList = word_list
    for i in range(len(word_list)):
        newList[i] = newList[i].lower()                      # put in lowercase
        newList[i] = newList[i].replace(' ', '')             # remove spaces
        newList[i] = newList[i].replace('-', '')             # remove hyphens
        newList[i] = newList[i].replace('.', '')             # remove periods
        newList[i] = newList[i].replace("'", '')             # remove apostrophes
    return word_list

def speak(text, 
          folder="",
          filename="auto-discard_spelling_bee_audio.mp3"):

    splitted = text.split(" ") # create list containing each word
    if len(splitted) > 20: # 20 words seems to be a good threshold...
        splitted = splitted[0:20]
        text = ' '.join(splitted)
        text += '.............et cetera' # the repeated ellipsis is for a pause
        
    tts = gTTS(text=text, lang='en', tld='us', slow=True)


    path = folder+filename
    
    if os.path.isfile(path): # if the file already exists, erase it to avoid raising a Permission Error
        os.remove(path)
        
    tts.save(path)
    playsound.playsound(path, block=True)
    os.remove(path)

def prepare_list_for_speech(myList):
       # include commas and 'or' between possibilities...
       if len(myList)>1:
           t=''
           for i in range(len(myList)-1):
               t+=myList[i]+', '
           t+='or ' + myList[len(myList)-1]
       else:
           t=myList[0]
       return t

def record_mistake(filename, difficulty_level, word_index, correct_spelling, wrong_spelling, timestamp_formatted, timestamp_raw):
    # writing to csv file 
    try:
        with open(filename, 'a', newline='') as csvfile: # a for append (don't overwrite previous entries) 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
        
            # writing the current data row
            csvwriter.writerow([difficulty_level, word_index, correct_spelling, wrong_spelling, timestamp_formatted, timestamp_raw])
    except PermissionError:
        errorString = "Unable to load '" + filename + "'\nCheck that the above file is closed and that it exists on this machine."
        print(errorString)
    
def read_left_off_place(filename, difficulty_level):
    data = pd.read_csv(filename, header=None)
    return data[1][int(difficulty_level)-1] # [column][row]

def record_left_off_place(filename, difficulty_level, index):
    data = pd.read_csv(filename, header=None)
    array = data.to_numpy()
    array[difficulty_level-1][1]=int(index) # set current index
    
    try:
        with open(filename, 'w', newline='') as csvfile: # `w` because we'll overwrite the original data
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
        
            # writing the modified array rows
            # csvwriter.writerow(header_row)
            csvwriter.writerows(array)
    except PermissionError:
        errorString = "Unable to load '" + filename + "'\nCheck that the above file is closed and that it exists on this machine."
        print(errorString)
        
def get_missed_indices(filename):
    '''Returns a numpy array of indices of words misspelled (recent to past) '''
    data = pd.read_csv(filename, encoding="ISO-8859-1") # fancy encoding for the exotic markings sometimes encountered in the official word lists
    d = data.word_index.to_numpy()
    reversed_order = d[::-1]
    return reversed_order

def censor_sentence(word, sentence):
    '''
    censors a word from a given sentence using a dynamic matching threshold
    Parameters
    ----------
    word : str
        word to censor (it and its variants)
    sentence : str
        example sentence
    
    Returns
        censored sentence (not containing word or its variants) as a str

    '''
    from difflib import get_close_matches
    splitted = sentence.split(" ") # create list containing each word
    
    # determine threshold
    if len(word) > 7:
            thresh = (len(word)-3) / len(word) # because three is usually the maximum # letter deviations in a word '-ing'
    else:
        thresh = 0.65 # this is a good median threshold

    closest_matches = get_close_matches(word=word, possibilities=splitted, n=len(splitted), cutoff=thresh)
    
    for offender in closest_matches:
        index = [i for i in range(len(splitted)) if splitted[i] == offender][0]
        splitted[index] = '**similar word**'
        
    back2string = ' '.join(splitted)

    return back2string
    



mistakeHistory = 'word_stats.csv'

progressHistory = 'progress_history.csv'

data = pd.read_csv('FCNT-2023.csv', skiprows=0)

repeat_hotkeys = ['a', 'again']
definition_hotkeys = ['d', 'def']
usage_hotkeys = ['u', 'use']
PoS_hotkeys = ['p', 'part']
etymology_hotkeys = ['e', 'etym']
phonetic_symbol_hotkeys = ['s', 'sym']

menu_return_hotkeys = ['m', 'menu']
valid_difficulty_choices = [1, 2, 3]

sleepTime = 5 # for returning to main menu on error
mistake_delay = 1.5

def print_spelling_menu():
        print("\nOptions:\n", 
          repeat_hotkeys, " for repeat pronunciation\n",
          definition_hotkeys, "   for definitions\n",
          usage_hotkeys, "   for example sentences\n",
          PoS_hotkeys, "  for parts of speech\n",
          etymology_hotkeys, "  for etymologies\n",
          phonetic_symbol_hotkeys, "   for phonetic spellings\n\n",
          
          [str(i) for i in valid_difficulty_choices], "to change word difficulty level\n",
          menu_return_hotkeys, "  to see this menu again\n"
          )



one = np.array(data.Fourth_Bee[~pd.isnull(data.Fourth_Bee)]) #First Column in CSV is 4th - 6th Grade Words

two = np.array(data.Seventh_Bee[~pd.isnull(data.Seventh_Bee)]) #Second Column in CSV is 7th - 8th Grade Words

three = np.array(data.Ninth_Bee[~pd.isnull(data.Ninth_Bee)]) #Third Column in CSV is 9th - 12th Grade Words

together = [one, two, three]

valid_difficulty_choices = [1, 2, 3]


reset_loop = True # flag for catching if user reaches end of spelling list and must return to main menu

while True:
    if reset_loop == True:
        reset_loop = False # reset to not continue looping
        
        print_spelling_menu()
        
        
        # get word difficulty
        valid_input = False
        while not valid_input:
            difficulty = input('Please enter a word difficulty level [1] [2] [3] : \n [1]: For 4th - 6th Grade \n [2]: For 7th - 8th Grade \n [3]: For 9th - 12th Grade> ')
            
            try:
               int(difficulty)
               if int(difficulty) in valid_difficulty_choices:
                   valid_input = True
               else:
                   print("That is not an option. Please input a valid difficulty level.")
            except:
                 print("That is not an option. Please input a valid integer difficulty level.")
        
        # get starting point
        valid_input = False
        while not valid_input:
            print("\n----- Study Options -----\n")
            print(" Start sequential studying at word index                                 (enter an integer)\n", 
                  "Start sequentially where you previously left off                        (enter `p` or `prev`)\n",
                  "Start random-order studying at random starting index                    (enter `r` or `random`)\n",
                  "Start studying missed words (all difficulties; from recent to older)    (enter `m` or `miss`)"
                  )
            style_input = input('>  ')
            
            if style_input in ['r', 'random']:
                valid_input = True
                style = 'random'
            elif style_input in ['p', 'prev']:
                valid_input = True
                style = 'previous'
                # get the current progress state now before looping commences to minimize unnecessary .csv readings
                previous_index = read_left_off_place(filename = progressHistory, difficulty_level = difficulty)
            elif style_input in ['m', 'miss']:
                valid_input = True
                style = 'miss'
                review_array = get_missed_indices(mistakeHistory)
            else: # then input should be an integer as index
                try:
                   int(style_input)
                   valid_input = True
                   style = 'index'
                except:
                     print(str(style_input)+" is not an option. Please input a valid integer or string.")
        
            
        index_counter = 0
        while True:
            
            if style == 'random':
                current_word_index = random.randint(0, len(together[int(difficulty)-1])-1)
                rawWord = together[int(difficulty)-1][current_word_index]
                begin_index = 0
                
            elif style == 'index':
                current_word_index = int(style_input) + index_counter
                try:
                    rawWord = together[int(difficulty)-1][current_word_index]
                except IndexError:
                    # congratulate user on level completion and return to main menu
                    exitString = '\nCongratulations! You have reached the end of level ' + str(difficulty) + ' words.  Program returning to menu in ' + str(sleepTime) + ' seconds...\n'
                    print(exitString)
                    time.sleep(sleepTime)
                    reset_loop = True
                    break
            
                    
                begin_index = int(style_input)
          
            elif style == 'previous':
                current_word_index = previous_index + index_counter
                try:
                    rawWord = together[int(difficulty)-1][current_word_index]
                except:
                    # congratulate user on level completion and return to main menu
                    exitString = '\nCongratulations! You have reached the end of level ' + str(difficulty) + ' words.  Program returning to menu in ' + str(sleepTime) + ' seconds...\n'
                    print(exitString)
                    time.sleep(sleepTime)
                    reset_loop = True
                    break
                    
                begin_index = previous_index
                
                    
            elif style == 'miss':
                try:
                    rawWord = together[int(difficulty)-1][review_array[index_counter]]
                except:
                    # congratulate user on level completion and return to main menu
                    exitString = '\nCongratulations! You have finished reviewing missed words. Program returning to menu in ' + str(sleepTime) + ' seconds...\n'
                    print(exitString)
                    time.sleep(sleepTime)
                    reset_loop = True
                    break
    
                current_word_index = review_array[index_counter]
                
            index_counter += 1
        
            
            # alternate spellings separated by `; `
            withoutAccents = unidecode.unidecode(rawWord)
            word = withoutAccents.split('; ')
            
            word = scrub_word_list(word)
            
            
            
            word_spelled = False
            while not word_spelled:
                
                speak("Please spell " + withoutAccents.split('; ')[0])
                spellInput = input("Type spelling: ")
                spellInput = scrub_word_list([spellInput])[0]
                
                # check whether the user spelled the word correctly...
                if spellInput in word:
                    print("Correctly Spelled!", rawWord)
                    print('--------')
                    word_spelled = True
                    
                elif spellInput in definition_hotkeys:
                    definition = get_MW_definition(str(word[0]))
                    if definition == None:
                        print("Definition: No definition found on the Merriam Webster website.  Sorry!")
                    else:
                        censored = censor_sentence(word = str(word[0]), sentence = definition[0])
                        print("Definition: "+ censored)
                        speak("Definition: "+ definition[0])
                    
                elif spellInput in usage_hotkeys:
                    usage_example = get_MW_example_sentences(str(word[0]))
                    if usage_example == None:
                        print("No example sentences found on the Merriam Webster website.  Sorry!")
                    else:
                        # censor out the word for printing...
                        censored = censor_sentence(word = str(word[0]), sentence = usage_example[0])
                        print("Example Sentence: "+ censored + '.') 
                        speak("Example Sentence: "+ usage_example[0])
                    
                elif spellInput in PoS_hotkeys:
                    parts = get_MW_parts_of_speech(str(word[0]))
                    
                    t = prepare_list_for_speech(parts)
           
                    print("Part(s) of Speech: " + t) # only show first sentence
                    speak("Parts of Speech: " + t)
                
                elif spellInput in phonetic_symbol_hotkeys:
                    phonetic = get_MW_phonetic_spelling(str(word[0]))
                    t = prepare_list_for_speech(phonetic)
                    print("Phonetic Spelling: " + t)
                    
                elif spellInput in etymology_hotkeys:
                    etymology = get_MW_etymology(str(word[0]))
                    
                    if etymology == None:
                        print("No etymology found on the Merriam Webster website.  Sorry!")
                    else:
                        censored = censor_sentence(word = str(word[0]), sentence = etymology[0])
                        print('Etymology: ' + censored)
                        
                elif spellInput in repeat_hotkeys:
                    # say the word again
                    speak(withoutAccents.split('; ')[0])
                    
                elif spellInput in [str(i) for i in valid_difficulty_choices]:
                    if int(spellInput) != difficulty:
                        print('\nDifficulty now changed to level ' + spellInput + ' words. Study style is still set to ' + style + ' studying.\n')
                        difficulty = int(spellInput)
                        break
                    else:
                        print('\nDifficulty level is already set to ' + spellInput + ' words.\n')
                
                elif spellInput in menu_return_hotkeys:
                    print_spelling_menu()
                    
                else:
                    print("Oops! Not quite.")
                    time.sleep(mistake_delay)
                    print("Correct:", rawWord)
                    print('--------')
                    
                    time.sleep(mistake_delay)
                    
                    word_spelled = True
                    
                    # record mistake in mistake csv file
                    thisTime = datetime.datetime.fromtimestamp(time.time()).strftime('%c')
                    wordIndex = current_word_index
                    
                    record_mistake(filename = mistakeHistory, 
                                   difficulty_level = difficulty, 
                                   word_index = current_word_index,
                                   correct_spelling = rawWord, 
                                   wrong_spelling = spellInput, 
                                   timestamp_formatted = thisTime, 
                                   timestamp_raw = time.time())
                    
            
                # record progress to progress.csv
                if style not in ['random', 'miss']:
                    record_left_off_place(progressHistory, int(difficulty), (begin_index + index_counter))
                
            word_spelled = False
            
        else:
            pass