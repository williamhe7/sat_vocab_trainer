import csv

sat_word_list = []
with open("sat_vocab1.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        #print(row)  # Each row is a dict with column headers as keys
        del row['Frequency']
        del row['Appears In']
        del row['Root Analysis']
        sat_word_list.append(row)


import re

import PyPDF2

text = ""
with open("sat_vocab.pdf", "rb") as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        text += page.extract_text()
    text = text.replace("\n", " ")
    text = text.replace("(v.)", "@")
    text = text.replace("(adj.)", "#")
    text = text.replace("(n.)", "$")
#print(text[:100000])

def get_last_phrase(text, i):
    lastPhrase = ""
    hasLastPhrase = False
    currentIndex = i-1
    while hasLastPhrase == False:
        if text[currentIndex] == " ":
            currentIndex -=1
            continue
        lastPhrase = text[currentIndex] + lastPhrase
        currentIndex -=1

        if text[currentIndex] == " ":
            hasLastPhrase = True

        if 'Vocabulary' in lastPhrase:
            lastPhrase = lastPhrase.replace('Vocabulary', "")
    return lastPhrase, currentIndex

def get_next_phrase_until(text, i, until):
    nextPhrase = ''
    hasNextPhrase = False
    currentIndex = i+1
    while hasNextPhrase == False:
        if text[currentIndex] != until:
            nextPhrase = nextPhrase + text[currentIndex]
        else:
            hasNextPhrase = True
        currentIndex += 1
    return nextPhrase

current_word = ""
current_def = ""
word_list = []
for i in range(len(text)):

    if text[i] == '@' or text[i] == '#' or text[i] == '$':
        
        lastPhrase, currentIndex = get_last_phrase(text, i)

        if lastPhrase == '1.' or lastPhrase == '2.' or lastPhrase == '3.':
            if lastPhrase == '1.':
                word, index = get_last_phrase(text, currentIndex)
                current_word = word
                temp_def = get_next_phrase_until(text, i, '(')
                current_def = "1. " + temp_def.strip()
            if lastPhrase == '2.':
                temp_def = get_next_phrase_until(text, i, '(')
                current_def = current_def + " 2. " + temp_def.strip()

                word_list.append({'Word' : current_word, 'Definition' : current_def})
            if lastPhrase == '3.':
                
                temp_def = get_next_phrase_until(text, i, '(')
                current_def = current_def + " 3. " + temp_def.strip()

                for j in range(len(word_list)):
                    #for each dictionary in list

                    #gets a dictionary at index j
                    if word_list[j]['Word'] == current_word:
                        word_list[j]['Definition'] = current_def
        else:
            current_word = lastPhrase
            #get def
            current_def = get_next_phrase_until(text, i, '(').strip()
            word_list.append({'Word' : current_word, 'Definition' : current_def})
#print(word_list)
#print(sat_word_list)

final_list = []
for i in sat_word_list:

    keep = True

    for j in word_list:

        if i['Word'] == j['Word']:
            keep = False
            break
        
    if keep:
        final_list.append(i)
#print(final_list)

combined_list = word_list + final_list

#write to a file
with open("total_words.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Word', 'Definition'])
    writer.writeheader()
    writer.writerows(combined_list)

