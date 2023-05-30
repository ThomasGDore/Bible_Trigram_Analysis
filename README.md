# Trigram analysis of the Douay-Rheims Bible
## Introduction
This is a trigram analysis of the Douay-Rheims Bible. In this analysis we utilized Python, NLTK, and Beautiful Soup in Jupyter Labs to scrape [he Douay-Rheims from Gutenberg](https://www.gutenberg.org/files/8300/8300-h/8300-h.htm) and count the trigrams present in the verses. This analysis was sparked by one question, primarily, but has other potential utilizations. There was a simple curiosity on my own end to know how often the phrase 'be not afraid'occurs in the Bible. I was able to satiate this curiosity with a simple ctrl-f search of the html:

<p align="center">
  <img src="be_not_afraid_17.png", width="65%">
  <div class="caption" align="center">Problem solved!</div>
</p>

I was inspired by this question to further probe the work. What other trigrams might we find? What might they inform us about the contents of the work? And beyond this--we're still living in a predominantly Christian world, and the Bible is still the best-selling book of all time, so there is a strong use-case for businesses to model their messaging and core tenets around common themes in the Bible.

One major problem the researchers had was cleaning the data such that one only has content from the actual verses themselves. It's easy to segment the work such that one gets the entire contents of the Bible, i.e., the verses *and* the book titles *and* the notes about the books' contents *and* the footnotes. This was a unique and interesting problem that after a few iterations the researchers can proudly say they resolved! Though there is still room for improvement.

## Data Acquisition and Analysis

Click [here](https://github.com/ThomasGDore/Bible_Trigram_Analysis/blob/main/p_model_DR.pdf) to see the full commented code, with outputs, as a pdf.

All the core building blocks of this work took place within the python framework on Jupyter Labs. We scraped the webpage using 'request' from the urllib library and then parsed the output utilizing BeautifulSoup. This allowed us to have each <p></p> be a unique object in out list. Whereas previous iterations received the Bible with each new line being a 'unique object' in the list, this allowed for each verse to be captured in a single object. Thusly we had the good fortune of taking advantage of the Bible's own demarcation system, i.e., chapter:verse (both numerical values) to select only the objects that are verses from the list.

To be exact made a list of every number from 0 to 100, and converted each object 'type' from 'int' to 'str', or from integer to string. Then we created a new list using a list comprehension, where it took objects from the previous list built off the <p>'s in the html if and only if they began with a number.
  
'''
  for verse in p_list[228:-57]:
    if verse[0] in num_list:
        dr_p_cln.append(verse)
'''

After this, the hard-part of the evaluation is mostly done. We do some more 'cleaning' of the verses by removing punctuation, and new-line markers '\n' that carried over from the html. We also remove all of the chapter and verse demarcations we earlier utilized. 

We now have a list composed exclusively of verses that have been 'cleaned' of all punctuation. Each 'object' in the list is still an entire verse, and it is not yet a list of 'word-objects'. So we tokenize the sentences using the nltk toolkit, which means we split each 'verse' object into a series of 'word' object and put them into a new list. This list is still ordered as the Bible is, and therefore is still useful for trigram analysis. We then make every word into its lowercase version, thus allowing python to understand, for example, that 'Arbitrary', and 'arbitrary' are not distinct objects after the former is converted into 'arbitrary', thus allowing for a more complete count.

We performed a Frequency Distribution on the list, treating it as a '[bag of words](https://en.wikipedia.org/wiki/Bag-of-words_model)' and found that removing the stop words lead to a more useful output. As the most common words without removing stop words are ('the', 'and', 'of') and after removing stop words they are ('shall', 'Lord', 'thou'). A future analysis might make nltk's list of stopwords larger by adding older english possessive pronomials like 'thou' and 'thy'.

We then generated a list of trigrams using nltk.trigrams, and counted instances of each unique trigram. We put the outputs into a dictionary that associated a trigram as the key, and the count of how many times it occurred as the value to said key. We then organized said dictionary in a descending fashion of greatest counts to least, and had the following output as the top 50 most common trigrams in the Douay-Rheims Bible:


  <p align="center">
  <img src="top_50_wsw.png", width="65%">
  <div class="caption" align="center">The 50 most commmon trigrams in the Douay-Rheims</div>
</p>

Returning to our goal concerning messaging for businesses and marketing teams, we see a focus on duties and responsibilities, e.g., ('and', 'i', 'will'), ('and', 'thou', 'shalt'), and more primarily upon family relations, e.g., ('the', 'son', 'of'), ('the', 'children', 'of'), ('children', 'of', 'Israel'). We would therefore recommend businesses that want to stick around for the long term to center their messaging and business model on serving the families of their customers, and of helping their customers to perform their duties and responsibilities toward the world with dignity.

I was also able to confirm that my ctrl-f search before was correct

'''
a\['be','not','afraid']
##17
'''

We performed the same analysis with the stop words removed but found the trigrams it produced less compelling. If the reader would like to see them I'd point them towards the [.pdf](https://github.com/ThomasGDore/Bible_Trigram_Analysis/blob/main/p_model_DR.pdf) for the full list.


## Potential future directions 

We noticed that there is direct potential for a small fix. As we are only looking here at the most common trigrams across a relatively large dataset we were not perturbed by the appearance of 7 bracketed (\[])comments in the text. Each occurrence was located in the Psalms, and inside the brackets was only a reference to another verse in the Bible, e.g., \[1 Kings 24]. As a) the content would largely have been removed when the brackets and numbers were deleted and b) they only occurred at the end of sentences (thus not interfering with a trigramic interpretation) it is entirely irrelevant to our conclusion and our final counts. However the researchers would like to return to the project to move the bracketed items entirely for the sake of completion. We hypothesize that RegEx would be the tool for the job.


The researchers would also like to pursue a sentiment analysis on the Bible. Namely we are curious about the differences in emotional sentiments between the two 'halves' of the Bible: The Old Testament, and The New Testament. 

This project was deeply enjoyable and the researchers thank you for your time in reading through the analysis.
