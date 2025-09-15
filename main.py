import json
import csv
import random


total_words = []
with open ('total_words.csv', "r") as f:
 reader = csv.DictReader(f)
 total_words = list(reader)
#print(loaded_data)


words_learned = []
with open ('words_learned.csv', 'r') as f:
 reader = csv.DictReader(f)
 words_learned = list(reader)
#print(words_learned)


#words not learned
words_not_learned = []
for i in total_words:
 keep = True


 for j in words_learned:
   if i['Word'] == j['Word']:
     keep = False
     break
 if keep:
   words_not_learned.append(i)
#print(words_not_learned)


learning = input('Learn Words (Y/n)? ')


if learning.lower() == "y":
 #generate random 5 words that are not learned
 words_to_learn = []
 while len(words_to_learn) < 5:
   rand = random.randint(0, len(words_not_learned))
   if words_not_learned[rand] not in words_to_learn:
     words_to_learn.append(words_not_learned[rand])
  for i in range(5):
   print(f"Word: {words_to_learn[i]['Word']}")
   print(f"Definition of Word: {words_to_learn[i]['Definition']}")
  
   input("Proceed? (Y) ")
 words_learned = words_learned + words_to_learn


deleteWordsLearned = input('Reset Words Learned (Y/n) ')
if deleteWordsLearned.lower() == "y":
 words_learned = []


testWordsLearned = input('Test Words Learned (50%)? (Y/n) ')
if testWordsLearned.lower() == "y":
 words_to_test = []
 length = int(len(words_learned) / 2)
 while len(words_to_test) < length:
   rand = random.randint(0, len(words_learned))
   if words_learned[rand] not in words_to_test:
     words_to_test.append(words_learned[rand])


 for i in range(len(words_to_test)):
   ans= input(f'What is the definition of {words_to_test[i]['Word']}? ')
   print(f'Ans: {words_to_test[i]['Definition']}')


with open('words_learned.csv', 'w', encoding='utf-8') as f:
 writer = csv.DictWriter(f, fieldnames=['Word', 'Definition'])
 writer.writeheader()
 writer.writerows(words_learned)





