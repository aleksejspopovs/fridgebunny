import twitter

def get_bunny_url(twitter_api_key: str, twitter_api_secret: str) -> str:
	tw = twitter.Api(
		consumer_key=twitter_api_key,
		consumer_secret=twitter_api_secret,
		application_only_auth=True,
	)
	tweets = tw.GetUserTimeline(screen_name='RabbitEveryHour')
	for tweet in tweets:
		if tweet.media:
			return tweet.media[0].media_url_https
	raise Exception('no bunnies??')
