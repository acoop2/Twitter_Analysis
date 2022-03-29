#This is a program used to create a worcloud of a months worth od tweets. This will be used to distinguish the chatter of each month and what
#Users were discussing at the time to see if we can find any correlation with our sentiment

#!/usr/local/bin/python3
#Import of relevant packages
import csv
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from google.cloud import language_v1
import os
import re




# Load a List of Stopwords for filtering
Ignore = open("Stopwords.txt").read().split()
#Set and update Stopwords
STOPWORDS.update(Ignore)
stopwords = set(STOPWORDS)

ids=set()

ptext={"01":"","02":"","03":"","04":"","05":"","06":"","07":"","08":"","09":"","10":"","11":"","12":""}
with open("tweet_data.csv" , newline='') as f:
    file = csv.reader(f)
    for i in file:
        if ((str(i[0]) in ids)==False and len(i[0])==19):
            ids.add(str(i[0]))
            #Clean the text
            text = i[2]
            text= text.strip("b'RT")
            text= text.strip('"RT')
            text = re.sub("@[A-Za-z0-9_]+","", text)
            text = re.sub("#[A-Za-z0-9_]+","", text)
            text = re.sub(r"http\S+", "", text)
            text = re.sub(r'\\x\S+', "", text)
            text= text.strip(" :")
            #add text to dixtuinary
            ptext[i[1][5:7]] += " "
            ptext[i[1][5:7]] += text
            if(len(ids)%10000==0):
                print(str(len(ids)) + " tweets so far")
                for i in ptext:
                    print(str(len(ptext[i])) + " bytes : month " + str(i))
                print("\n")

        else:
            continue

for i in ptext:
    text = ptext[i]
    # Generation of a WordCloud image with a set of customization
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=5000,
        width=1920,
        height=1080,
        max_font_size=1000
                          ).generate(str(text)).to_file("month_" + str(i) + "_cloud.png")
    #Plotter

    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
