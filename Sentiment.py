#This program is meant to take in a large list of tweets an anlyze the sentiment of each individual tweet.
#We then take the average of the tweets by month

# Imports the Google Cloud client library
from google.cloud import language_v1
import os
import csv
import re


#establishing google api credentials
path = r"C:\Users\m221320\Downloads\twitte-sentiement-517f001bf0f2.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=path




# Instantiates a client
client = language_v1.LanguageServiceClient()

# The text to analyze
#Import csv files by month clean the content of the tweets and add it to list of tweets by month
ids=set()

ptext={"01":[],"02":[],"03":[],"04":[],"05":[],"06":[],"07":[],"08":[],"09":[],"10":[],"11":[],"12":[]}
with open("tweets_data(1).csv" , newline='') as f:
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
            #add text to dictionary
            ptext[i[1][5:7]] += [text]
            #mantain updates on flow
            if(len(ids)%10000==0):
                print(str(len(ids)) + " tweets so far")
                for i in ptext:
                    print(str(len(ptext[i])) + " tweets : month " + str(i))
                print("\n")

        else:
            continue

for i in ptext:
    tweets = ptext[i]
    sent_total=0
    neg=0
    nuet=0
    pos=0
    count=0

    #api call for sentiment analysis we take the sentimenet of each individual tweet and average them by month
    #we then keep a count of positive negative and nuetral tweets
    for txt in tweets:
        try:
            document = language_v1.Document(content=txt, type_=language_v1.Document.Type.PLAIN_TEXT)
            sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

            sent_total+= sentiment.score
            count+=1
            if (sentiment.score> 0):
                pos+=1
            if (sentiment.score< 0):
                neg+=1
            if (sentiment.score== 0):
                nuet+=1
        #some tweets are in a language that the google api does not take. We only use English and Spanish
        except Exception as e:
            print(e)
            continue
        if(count%1000==0):
            print(str(count) + " tweets analyzed")


    sent_avg=sent_total/count
    with open(str(i) + ".txt", "w+") as G:
        print("Sentiment: {}".format(sent_avg))
        print("Positive Tweets: " +str(pos))
        print("Negative Tweets: " +str(neg))
        print("Nuetral Tweets: " +str(nuet))
        G.write("Sentiment: {}".format(sent_avg))
        G.write("\n")
        G.write("Positive Tweets: " +str(pos))
        G.write("\n")
        G.write("Negative Tweets: " +str(neg))
        G.write("\n")
        G.write("Nuetral Tweets: " +str(nuet))

    print("This is month: " + str(i) + "\n")


    #
    # document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    # # Detects the sentiment of the text
    # sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    # #print("Text: {}".format(text))
    # print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))



# The score of a document's sentiment indicates the overall emotion of a document. The magnitude of a document's sentiment indicates
#how much emotional content is present within the document, and this value is often proportional to the length of the document.
# It is important to note that the Natural Language API indicates differences between positive and negative emotion in a document,
# but does not identify specific positive and negative emotions. For example, "angry" and "sad" are both considered negative emotions.
#However, when the Natural Language API analyzes text that is considered "angry", or text that is considered "sad", the response only
#indicates that the sentiment in the text is negative, not "sad" or "angry".
# A document with a neutral score (around 0.0) may indicate a low-emotion document, or may indicate mixed emotions, with both high
# positive and negative values which cancel each out. Generally, you can use magnitude values to disambiguate these cases, as truly
#neutral documents will have a low magnitude value, while mixed documents will have higher magnitude values.
# When comparing documents to each other (especially documents of different length), make sure to use the magnitude values to calibrate
#your scores, as they can help you gauge the relevant amount of emotional content.
