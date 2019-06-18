import twitter
import pymsteams
import time

class Tweet:
	def __init__ (self,profilePic,userName,screenName,createdAt,twitterLink,tweetText):
		self.profilePic = profilePic
		self.userName = userName
		self.screenName = screenName
		self.createdAt = createdAt
		self.twitterLink = twitterLink
		self.tweetText = tweetText
		self.teamsUrl = 'WEBHOOK_URL_GOES_HERE'

	#This posts the given tweet to the teams channel provided by the teamsUrl variable	
	def share_on_teams(tweet):
		#Creates a connector card object using the Microsoft Webhook URL
		teamsMessage = pymsteams.connectorcard(tweet.teamsUrl)

		# Add text to the message.
		teamsMessage.text(tweet.userName + " posted a new tweet!")

		#Create the section
		messageSection = pymsteams.cardsection()

		#Activity Elements
		messageSection.activityTitle(tweet.userName + " @" + tweet.screenName)
		messageSection.activitySubtitle("Posted on " + tweet.createdAt)
		messageSection.activityImage(tweet.profilePic)
		messageSection.activityText(tweet.tweetText)

		#Section Text
		messageSection.text('<a href="{}">Direct link to tweet</a>'.format(tweet.twitterLink))

		#Add section text to the teams message
		teamsMessage.addSection(messageSection)

		#Send the message to the channel
		teamsMessage.send()


#Get an API object from the twitter api that we can use to make API calls to get tweets
api = twitter.Api(consumer_key='CONSUMER_KEY_GOES_HERE',
                  consumer_secret='CONSUMER_SECRET_GOES_HERE',
                  access_token_key='ACCESS_TOKEN_KEY_GOES_HERE',
                  access_token_secret='ACCESS_TOKEN_SECRET')

#This opens a text file to get the list of posted tweets
def get_list_of_posted_tweets():
	with open('elon_tweets.txt') as file:
		lines = file.read().splitlines()
	file.close()
	return lines

#Adds a tweet id to the list of posted tweets. 
def add_to_list_of_tweets(tweet_id):
	f = open("elon_tweets.txt", "a")
	f.write(tweet_id + '\n')
	f.close()

#Gets the most recent tweets from a list of  twitter handles
def get_tweets_from_twitter(screen_names):
	for name in screen_names:
		#Get the most recent tweets from twitter API
		tweets_list = api.GetUserTimeline(screen_name=name, count=5)

		#Assume no new tweets have been posted
		newTweets = False

		#Loop through tweets from API, checking to see if they have already been posted
		for tweet in tweets_list:
			posted_tweets = get_list_of_posted_tweets()
			
			#If the tweet has not been posted, create a new tweet instance and share it on teams
			if str(tweet.id) not in posted_tweets:
				newTweets = True
				twitter_status_link = "https://twitter.com/{}/status/{}".format(str(tweet.user.screen_name),str(tweet.id))
				newTweet = Tweet(tweet.user.profile_image_url_https, tweet.user.name, tweet.user.screen_name, tweet.created_at.rsplit(' ', 2)[0], twitter_status_link, tweet.text)
				newTweet.share_on_teams()

				print("Posting tweet ID: " + str(tweet.id))
				add_to_list_of_tweets(str(tweet.id))
		
		if not newTweets:
			print("No new tweets from " + str(tweet.user.screen_name) + " to post!")

#Run continuously, checking for new tweets every sixty seconds
while True:
    get_tweets_from_twitter(['elonmusk','tesla'])
    time.sleep(60)
