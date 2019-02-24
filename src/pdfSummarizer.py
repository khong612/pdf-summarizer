#!/usr/bin/env python3

"""pdfSummarizer.py: This script summarizes text provided in a PDF file."""

import slate3k as slate
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer

# Scan user input for PDF file name
print("What is the name of the PDF?")
fileName = input("(Without .pdf file extension)\n")
pdfFileName = fileName + ".pdf"
pdfFileObj = open(pdfFileName, "rb")
pdfPages = slate.PDF(pdfFileObj)

# Extract text from PDF file
text = ""
for page in pdfPages:
    text += page

# Process text by removing numbers and unrecognized punctuation
processedText = re.sub("’", "'", text)
processedText = re.sub("[^a-zA-Z' ]+", " ", processedText)
stopWords = set(stopwords.words("english"))
words = word_tokenize(processedText)

# Normalize words with Porter stemming and build word frequency table
stemmer = SnowballStemmer("english", ignore_stopwords=True)
freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue
    elif stemmer.stem(word) in freqTable:
        freqTable[stemmer.stem(word)] += 1
    else:
        freqTable[stemmer.stem(word)] = 1

# Normalize every sentence in the text
sentences = sent_tokenize(text)
stemmedSentences = []
sentenceValue = dict()
for sentence in sentences:
    stemmedSentence = []
    for word in sentence.lower().split():
        stemmedSentence.append(stemmer.stem(word))
    stemmedSentences.append(stemmedSentence)

# Calculate value of every normalized sentence based on word frequency table
# [:12] helps to save space
for num in range(len(stemmedSentences)):
    for wordValue in freqTable:
        if wordValue in stemmedSentences[num]:
            if sentences[num][:12] in sentenceValue:
                sentenceValue[sentences[num][:12]] += freqTable.get(wordValue)
            else:
                sentenceValue[sentences[num][:12]] = freqTable.get(wordValue)

# Determine average value of a sentence in the text
sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue.get(sentence)

average = int(sumValues / len(sentenceValue))

# Create summary of text using sentences that exceed the average value by some factor
# This factor can be adjusted to reduce/expand the length of the summary
summary = ""
for sentence in sentences:
        if sentence[:12] in sentenceValue and sentenceValue[sentence[:12]] > (3.0 * average):
            summary += " " + " ".join(sentence.split())

# Process the text in summary and write it to a new file
summary = re.sub("’", "'", summary)
summary = re.sub("[^a-zA-Z0-9'\"():;,.!?— ]+", " ", summary)
summaryText = open(fileName + "Summary.txt", "w")
summaryText.write(summary)
summaryText.close()
