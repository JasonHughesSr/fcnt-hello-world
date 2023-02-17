# spelling_bee
## **spelling_bee** is an interactive spelling bee study tool coded in Python 
## Developed for FCNT Into To Programming class: "Hello World"
## Inspired by but not fully forked from https://github.com/PineWarbler/spelling_bee

## Features:
-   Artificial voice prompt for help with pronunciation
-   Supplies, upon user request, a word's definition, etymology, part of speech, example usage sentence, and phonetic spelling--all sourced from the [Merriam Webster](https://www.merriam-webster.com/) dictionary (official dictionary of the Scripts Howard)
-   Study words from a specified difficulty level using sequential studying starting at input word index, using previously missed words, or using randomly selected words
-   Keeps track of words misspelled by the user; misspelled words can be reviewed later using the missed studying option

### Explaining the accompanying .CSV files
This program requires three .csv files to operate: 
-   [FCNT-2023.csv](/FCNT-2023.csv) contains all spelling words, divided by columns into grade levels
-   [progress_history.csv](/progress_history.csv) contains a list of words missed by the user
-   [word_stats.csv](/word_stats.csv) contains the index of the most recent word which the user studied (for persistent session memory)

### Clearing user spelling history:
Users may clear their spelling history by opening the [word_stats](/word_stats.csv) file and deleting all the non-header rows (not the first row)
Likewise, to edit the place last left off, open [progress_history](progress_history.csv) and change the appropriate cell values to the desired word index