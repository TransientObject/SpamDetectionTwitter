SpamDetectionTwitter
========================

Detecting Spammers in Twitter

Using J48 Classifier to build a classifier and then train it to detect spammers in twitter

58 different attributes are extracted for each users.

Detection of Spammers in Twitter


Author - Priya Narayana Subramanian

December 5, 2013
Abstract

With the advent of social networking, online media has gained a lot of popularity. To the
extent that mainstream media has taken a backseat. Users like to have instant updates on things
and people that interest them. In this regard, social media are, in a way a tailor made electronic
newspaper that people have access to round the clock. Twitter with its microblogging feature, is even more efficient in delivering news in a crisp and concise fashion. But, as with any technology,
twitter too can be used in negative ways. One of the most common ways to exploit twitter is spam.

Spammers propagate falsified information hidden behind an shortened URL, luring the users to
open the web pages. These web pages might either have some irrelevant advertisements or might
be a security threat which affects the user's system without his notice. One of the most common
ways to get the users to click the URLs are by using trending topics. This research work identifies characteristics that can be used to identify such spammers in twitter. Ground truth is used to
train a classifier which is then validated in two different ways. 

Also, the importance of attributes
with regards to the decision making process are discussed.
1 Introduction and Prior Works
With the size of twitter and its user base, its almost inevitable to have a spam free environment.
And spam is not just a false marketing or a virus attack. Things like profanity, insults, hate speech,
fraudulent reviews, fake profiles constitutes a little part of an exhaustive list, if there exists one. Why
twitter ? Twitter is more easy to spam because of its microblogging facility. If you can get people
interested in 140 characters, then you can get them to click a link or buy a product even. As they
say, curiosity kills. Any other social media has a larger content disposition which tends to give the
user more than what is necessary and hence sometime reveals the trick. 


Effects of spam in twitter is
not only realized by the end users. Imagine the amount of useless data twitter has to store, process
and maintain. Its a waste of resource and time from twitter's perspective as well. But, Detection
of spammers is not so easy after all. Although twitter has become better at eliminating spammers
recently, still there are a lot of spammers that are hiding perfectly. This is because spammers evolve
along with the spam detection strategies.
Trending tags are a major way in which spam propagates through the network. An instance of this
would be using tags like "blackfriday" and "cybermonday" during thanksgiving time. More people
are likely to be searching for deals and this gives an edge to spammers who can use this tag and lure
an user into doing something that they wouldn't normally do. If an ad says "iPad for 100$, hurry up!
goo.gl/sX7gIV", people would normally open the link. More than 99% of the internet users will not
know the implications of hitting a bad URL. This can be detected and eliminated only to an extent,
partly due to the high volume of tweets that 
ows through the network during this time.

There has been a lot of works going on recently to detect spammers. 

Our work can be split as,

1. Collection of Data. Ground Truth has been obtained from http://homepages.dcc.ufmg.br/
~fabricio/spammerscollection.html, the author of the first paper. Similarly Ground truth
for Non Spammers are collected. Lastly, users who tweeted about trending topics are identified
as a test set.
2. Constructing the Classifier. Using weka, an opensource tool for machine learning, a classifier is
generated from the groundtruth.
3. Analysis of the features. Out of the 58 features (we use only 58 of the 62), we analyze what
features are more important in the decision making process.

3 Twitter users' features and Main Result

We evaluate 58 features of the pre-classified dataset of spammers and non-spammer users. The 58
features would be divided into two category: content attributes and user behavior attributes. Content
attributes are properties of the text of tweets posted by users, which capture specific properties related
to the way users write tweets. User behavior attributes capture specific properties of the user behavior
in terms of the posting frequency, social interactions, and in
uence on the Twitter network.

3.1 Content Attributes
In total, we have 37 attributes related to content of the tweets. That is, number of URLs in each
tweet, number of hashtags, number of words on each tweet, number of users mentioned in each tweet,
number of character, count of numbers and so on. The list of attributes can be found in the appendix

3.2 User behavior Attributes
In total, we have 21 attributes about the user behavior. As assumed and according to the measurement
of our dataset, spammers are more likely to have less followers, more followees, lower number of times
the user was mentioned, lower number of times the user was replied to, lower number of times the
user replied someone, lower number of followees of the users followers (since they are more likely to
be spammers as well), more fixed time between tweets, and more fixed tweets posted per day and per
week.


