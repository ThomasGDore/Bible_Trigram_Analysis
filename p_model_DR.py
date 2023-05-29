#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from urllib import request
from collections import Counter
# nltk.download('punkt')

stopwords = nltk.corpus.stopwords.words('english')


# In[2]:


url = 'https://www.gutenberg.org/files/8300/8300-h/8300-h.htm'
# This is the html of the entire Douay-Rheims Bible
html = request.urlopen(url).read().decode('utf8')
# Here we are turning it into a string that Beautiful Soup will be able to work with


# In[3]:


soup = BeautifulSoup(html, 'html.parser')
# Beautiful Soup will parse the html and make it where we can pull out just the bits we need


# In[4]:


p_list = [text for text in soup.stripped_strings]
# Using a list comprehension to make a list of each unique <p>
# After several other methods, this seems to be the easiest way to single out the actual verses from the commentary, titles, etc..


# for elm in p_list[228:250]:
#     print(elm)
#     print('\n')
# print(p_list[-57:])

# This whole section above was a guess-and-check to find where the Bible begins and ends.
# I'm not sure why I didn't use rfind but here we are


# In[5]:


dr_p_cln = []
# I will need a list to store items from the p_list above "paragraph"_list or <p>_list, I'm only storing the ones that have a numerical value as their first item

num_list = []
for i in range(0,100):
    num_list.append(str(i))

# Here I am constructing a list of more than all possible numbers we might see in a chapter:verse
# Note that we are transforming the int objects into str objects, this is so they'll recognize two numbers as the same objects

for verse in p_list[228:-57]:
    if verse[0] in num_list:
        dr_p_cln.append(verse)

# I am iterating through the the portion of p_list that contains actual scripture
# I am selecting only <p>s that have a number as their initial value
# I am adding them to the list created above, thusly we have a list of all and only the verses of the Douay-Rheims. The hard part is now done.
        
# print(dr_p_cln[:15])
# Checking work


# In[6]:


dr_2 = []

# Here is a list where we will put the verses as objects after removing numbers, new line markers, and punctuation marks

repl_me = ['\n','\r',',','.',';',':','"','-','--','!','?','”','“','—',"'",'(',')','[',']']

# A list of punctuation marks and new line markers that we will be removing

for i in range(0,100):
    repl_me.append(str(i))

# We are adding strings of the integers in the same method as before to the list 'repl_me'

for verse in dr_p_cln:
    str_ver = verse
    for k in range(0, len(repl_me)):
        str_ver = str_ver.replace(repl_me[k],'')
    dr_2.append(str_ver)

# We are iterating over every object in dr_p_cln
# First we set each verse as a unique new object called 'str_ver'
# Then we iterate over the entire list of repl_me (which is 1-1 with repl_me_dict, ie, it has the same number of objects)
# We update str_ver after replcing every object in the string that is in repl_me [note the .replace(repl_me[k] selects for each object eventually] replacing it with nothing: ''
# Then we append this updated str_ver to our created list dr_2

    
print(dr_2[:5])
# Checking our work!


# In[7]:


dr_t = []

# Here is a list for after we tokenize each word in dr_2 and turn it into a list thtat is still ordered but can be treated as a 'bag of words' (see for more info on this term: https://en.wikipedia.org/wiki/Bag-of-words_model)

for verse in dr_2:
    tokens_temp = word_tokenize(verse)
    for i in tokens_temp:
        dr_t.append(i)
        
# We iterate through every object in dr_2, which has each verse cleaned of punctuation and numbers
# Using word_tokenize we tokenize each string in the list into individual word objects and store them in the list 'tokens_temp'
# We then iterate over tokens_temp, appending each object to dr_t, the list we created above. W
# We do this to avoid creating a list of lists which would be harder to process

print(dr_t[0:50])
# Checking our work!


# In[8]:


dr_t2 = [w.lower() for w in dr_t]
# We make every word lowercase to make it easier for python to count instances

print(dr_t2[:5])
# Checking our work!


# In[9]:


fdist_0 = FreqDist(dr_t2)

# Here we are using FreqDist from nltk.probability to find the most common words in our list

fdist_0.most_common(5)
# Checking our work!
# Notice the top 5 are all stopwords! Let's see what happens when we remove them:


# In[10]:


dr_t3 = [w for w in dr_t2 if w not in stopwords]

# We create a new list based on dr_t2 without the stopwords

fdist_1 = FreqDist(dr_t3)

# Using FreqDist from nltk.probability to find the most common words in our list

fdist_1.most_common(5)
# Checking our work!
# Notice these words are much more informative about the contents of the Bible


# In[11]:


my_trigrams = nltk.trigrams(dr_t2)
# print(type(my_trigrams))

# This experiment is interested in trigrams in the Bible. We will look at both trigrams with and without stop words
# Here we are using nltk.trigrams to analyze our list (still in order, remember) for groups of 3 words in a row
# this object is a generator though, and to use it we'd like to turn it into a list:

trigram_list = []
for i in my_trigrams:
    trigram_list.append(i)
    
# Here we create a list for the trigrams to be stored in 
# Then we iterate over the generator and append each output into the new list

print(trigram_list[:5])
# Checking our work!


# In[12]:


a = dict(Counter(trigram_list))

# Here we are using Counter from collections in the creation of a dictionary
# For the keys we will have each unique trigram, and for the values we will have a count on how many times that unique trigram occurred in 'trigram_list'


# In[13]:


b = {v:k for k,v in a.items()}

# Here we are flipping the keys and values to where we have the count of instances of each unique trigram as our key, and the trigram as the value
# This will make sorting the dictionary and getting the top counts easier


# In[14]:


items_sorted = sorted(b.items(), reverse=True)

# Sorting the reversed dictionary, b.
# Reversing the order of values such as it will be descending in value for an easier evaluation

print(items_sorted[0:50])

# The top 50 trigrams in the Douay-Rheims accompanied with their counts of how many times they occurred


# In[15]:


a['be','not','afraid']

# I was personally curious how often this one occurred.


# In[ ]:


# Below we have the same exact style of analysis, but utilizing the list with the stop words removed, ie, dr_t3. This analysis proved less fruitful (as you can see from the final output).


# In[16]:


my_trigrams_2 = nltk.trigrams(dr_t3)

# This experiment is interested in trigrams in the Bible. We will look at both trigrams with and without stop words
# Here we are using nltk.trigrams to analyze our list (still in order, remember) for groups of 3 words in a row
# this object is a generator though, and to use it we'd like to turn it into a list:

trigram_list_2 = []
for i in my_trigrams_2:
    trigram_list_2.append(i)
    
# Here we create a list for the trigrams to be stored in 
# Then we iterate over the generator and append each output into the new list

print(trigram_list_2[:5])
# Checking our work!


# In[17]:


a_2 = dict(Counter(trigram_list_2))

# Here we are using Counter from collections in the creation of a dictionary
# For the keys we will have each unique trigram, and for the values we will have a count on how many times that unique trigram occurred in 'trigram_list_2'


# In[18]:


b_2 = {v:k for k,v in a_2.items()}

# Here we are flipping the keys and values to where we have the count of instances of each unique trigram as our key, and the trigram as the value
# This will make sorting the dictionary and getting the top counts easier


# In[19]:


val_sorted_2 = sorted(b_2.items(), reverse=True)

# Sorting the reversed dictionary, b_2.
# Reversing the order of values such as it will be descending in value for an easier evaluation

print(val_sorted_2[0:50])

# The top 50 trigrams in the Douay-Rheims accompanied with their counts of how many times they occurred, with the stop words removed
# Personally I find this less useful than when the stop words were not removed. I'm glad we did both!

