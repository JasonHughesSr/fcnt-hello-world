def get_MW_definition(word):
    """
    webscrapes a word's definition from the Merriam-Webster online dictionary (https://www.merriam-webster.com/) 
    

      Input: word = search term for which to retrieve definition
      
      Output: definition = list of all definitions of requested word

    """
    from urllib.request import urlopen
    import re
    
    
    baseurl = "https://www.merriam-webster.com/dictionary/"
    url = baseurl+word
    
    try:
        page = urlopen(url)
    except:
        print("Unable to load webpage. Check internet connection and that requested word is spelled correctly.")
        return None
        
    html = page.read().decode("utf-8")
    
    beginFlag =  r'<span class="dtText">' # ??
    # beginFlag = r'<span class="dtText"><strong class="mw_t_bc">: </strong>' # this flag only works for non-names
    closureFlag = "</span>"
    foundStarts = [m.start() for m in re.finditer(beginFlag, html)]
    
    if len(foundStarts) == 0:
        return None # because couldn't find a definition
    
    definition=[]

    for i in range(0, len(foundStarts)):
        
        particle = html[foundStarts[i]+len(beginFlag) : html.find(closureFlag, foundStarts[i])]  
        particle = re.sub('<[^<]+?>', '', particle)
        
        # remove colons...
        particle = particle.replace(':', '')
        definition.append(particle)
    return definition



def get_MW_etymology(word):
    """
    webscrapes a word's etymology from the Merriam-Webster online dictionary (https://www.merriam-webster.com/) 
    

      Input: word = search term for which to retrieve etymology
      
      Output: etymology = list of all etymologies of requested word

    """
    from urllib.request import urlopen
    import re
    
    
    baseurl = "https://www.merriam-webster.com/dictionary/"
    url = baseurl+word
    
    try:
        page = urlopen(url)
    except:
        print("Unable to load webpage. Check internet connection and that requested word is spelled correctly.")
        return None
        
    html = page.read().decode("utf-8")
    
    beginFlag = r'<p class="et">'
    closureFlag = "</p>"
    foundStarts = [m.start() for m in re.finditer(beginFlag, html)]
    
    if foundStarts == []:
        return None
    
    etymology=[]

    for i in range(0, len(foundStarts)):
        
        particle = html[foundStarts[i]+len(beginFlag) : html.find(closureFlag, foundStarts[i])]  

        if "entry" not in particle:
            particle = re.sub('<[^<]+?>', '', particle) # remove nested <..> tags
            particle = particle.replace('\n', ' ') # remove newline breaks
            particle = re.sub(' +', ' ', particle) # remove double spaces
        
            etymology.append(particle)
        else:
            pass
    return etymology

def get_MW_example_sentences(word):
    """
    webscrapes example sentences from the Merriam-Webster online dictionary (https://www.merriam-webster.com/) 
    

      Input: word = search term for which to retrieve example sentences
      
      Output: exampleSentences = list of all example sentences of requested word
                                  will return None (null) if no example sentences could be found

    """
    from urllib.request import urlopen
    import re
    
    
    baseurl = "https://www.merriam-webster.com/dictionary/"
    url = baseurl+word
    
    try:
        page = urlopen(url)
    except:
        print("Unable to load webpage. Check internet connection and that requested word is spelled correctly.")
        return None
        
    html = page.read().decode("utf-8")
    
    beginFlag = r'<div class="in-sentences">'
    closureFlag = r"</div>"
    foundStarts = [m.start() for m in re.finditer(beginFlag, html)]
    
    if foundStarts == []:
        return None
    try:
        exampleSentences = html[foundStarts[0]+len(beginFlag) : html.find(closureFlag, foundStarts[0])]  
    except IndexError: # some word pages do not have the regular example sentences, only some scraped from news sites
        beginFlagFallback = r'<span class="t has-aq">'
        closureFlagFallback = r'<span class="aq has-aq">'
        foundStarts = [m.start() for m in re.finditer(beginFlagFallback, html)]
        if foundStarts == []:
            return None
        exampleSentences = ''
        for k in range(len(foundStarts)):
            exampleSentences += (html[foundStarts[k]+len(beginFlagFallback) : html.find(closureFlagFallback, foundStarts[k])]) 
    
    exampleSentences = re.sub('<[^<]+?>', '', exampleSentences) # remove nested <..> tags
    
    if "Quotes-->" in exampleSentences or "Extra Examples-->" in exampleSentences:
        exampleSentences = exampleSentences.replace("Quotes-->", '')
        exampleSentences = exampleSentences.replace('Extra Examples-->', '')
        
    partsofSpeech = ['Noun', "Verb", 'Adjective', "Adverb", 'Preposition', "Pronoun", "Conjunction", "Interjection"]
    for string in partsofSpeech:
        if string in exampleSentences:
            exampleSentences = exampleSentences.replace(string, '') # remove part of speech from before ex. sentences
    
    exampleSentences = exampleSentences.replace('\n', '') # remove newline breaks
    
    exampleSentences = re.sub(' +', ' ', exampleSentences) # remove double spaces

    exampleSentences = exampleSentences.split('.') # separate sentences

    return exampleSentences

def get_MW_parts_of_speech(word):
    """
    webscrapes a word's parts of speech from the Merriam-Webster online dictionary (https://www.merriam-webster.com/) 
    

      Input: word = search term for which to retrieve etymology
      
      Output: foundPartsofSpeech = list of all parts of speech forms of requested word

    """
    from urllib.request import urlopen
    import re
    
    
    baseurl = "https://www.merriam-webster.com/dictionary/"
    url = baseurl+word
    
    try:
        page = urlopen(url)
    except:
        print("Unable to load webpage. Check internet connection and that requested word is spelled correctly.")
        return None
        
    html = page.read().decode("utf-8")
    
    beginFlag = r'class="important-blue-link"'
    closureFlag = r"</span>"
    foundStarts = [m.start() for m in re.finditer(beginFlag, html)]
    
    partsofSpeech = ['Noun', "Verb", 'Adjective', "Adverb", 'Preposition', "Pronoun", "Conjunction", "Interjection"]
    foundPartsofSpeech = []

    for i in range(0, len(foundStarts)):
        
        particle = html[foundStarts[i]+len(beginFlag) : html.find(closureFlag, foundStarts[i])]  
        particle = re.sub('<[^<]+?>', '', particle) # remove nested <..> tags
        particle = particle.replace('\n', '') # remove newline breaks
        particle = re.sub(' +', ' ', particle) # remove double spaces

        for string in partsofSpeech:
            if string.lower() in particle and string not in foundPartsofSpeech:
                foundPartsofSpeech.append(string)

    return foundPartsofSpeech

def get_MW_phonetic_spelling(word):
    """
    webscrapes a word's parts of phonetic spelling(s) from the Merriam-Webster online dictionary (https://www.merriam-webster.com/) 
    

      Input: word = search term for which to retrieve phonetic spelling(s)
      
      Output: foundPartsofSpeech = list of all phonetic spelling(s) of requested word

    """
    from urllib.request import urlopen
    import re

    baseurl = "https://www.merriam-webster.com/dictionary/"
    url = baseurl+word
    
    try:
        page = urlopen(url)
    except:
        print("Unable to load webpage. Check internet connection and that requested word is spelled correctly.")
        return None
        
    html = page.read().decode("utf-8")
    
    beginFlag = r'<span class="pr"> '
    closureFlag = "</span>"
    foundStarts = [m.start() for m in re.finditer(beginFlag, html)]
    
    definition=[]
    
    for i in range(0, len(foundStarts)):
        
        particle = html[foundStarts[i]+len(beginFlag) : html.find(closureFlag, foundStarts[i])]  
        particle = re.sub('<[^<]+?>', '', particle)
        
        definition.append(particle)
    
    # remove duplicates...
    no_duplicates = list(set(definition))
    return no_duplicates


'''

from miscFunctions import pprintTime
import time
start = time.time()

definition = get_MW_definition('pearl')

end = time.time()
pprintTime(start, end)


start = time.time()
import threading
# import time

def trigger():
   time.sleep(5000)
# do somethi else here.

thread = threading.Thread(target = trigger)
thread.daemon = True
thread.start()
import math

while True:
    if math.floor((time.time() - start)%29) == 0: # because 30 seconds is maximum duration for Google Speech API
        # end previous recognizer instance and start new one...
        # have google process speech in background
        print("New beginning")
        def ask_google():
            # do some long download here
    print('.', end='')
        
''' 

