twitter-spammer-detector
========================

Detecting Spammers in Twitter

Using J48 Classifier to build a classifier and then train it to detect spammers in twitter

58 different attributes are extracted for each users.

Detection of Spammers in Twitter
Priya Narayana Subramanian

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