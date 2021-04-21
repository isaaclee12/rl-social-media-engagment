import tweepy
import time
import random
from datetime import datetime, timedelta
import pytz


def get_current_datetime():

    # For some reason this only runs if I import this here too
    from datetime import datetime, timedelta

    # Set timezone to GMT - which twitter is set to
    datetime = datetime.now()
    # timezone = pytz.timezone("GMT")
    # d_aware = timezone.localize(d)
    # print(d_aware.tzinfo)

    # Move ahead four to get from EST -> GMT
    datetime_gmt = datetime + timedelta(hours=4)

    # Turn datetime object into string tuple & return it
    datetime = datetime_gmt.strftime("%Y-%m-%d %H:%M:%S")

    current_date, current_time = datetime.split()
    # print("\nCurrent Date and Time:", current_date, current_time)

    return current_date, current_time


def check_for_new_tweets(tweets, TWEET_AGE_MAX):

    # Constants for date/time index in datetime tuple
    DATE = 0
    TIME = 1

    for i in range(0, len(tweets)):

        # Get tweet
        tweet = tweets[i]

        # get datetime string of when tweet was sent
        tweet_datetime = tweet.created_at

        # Split datetime string into date and time.
        tweet_datetime_tuple = str(tweet_datetime).split()
        tweet_date = tweet_datetime_tuple[0]
        tweet_time = tweet_datetime_tuple[1]

        #Print tweet contents
        # print("\n")
        print(tweet.text)

        #Get current datetime. Current datetime will print to console here.
        current_datetime = get_current_datetime()

        # print("Tweet datetime: ", tweet_datetime_tuple)
        # print("DATES: ", current_datetime[DATE], tweet_date)

        # Check if the dates match.
        if current_datetime[DATE] == tweet_date:

            # If the dates match, compare times.
            # Split current time into array by H/M/S
            current_time = str(current_datetime[TIME]).split(":")

            # Split tweet time into array by H/M/S.
            tweet_time = str(tweet_time).split(":")

            # Extract hour/minute/seconds form each
            current_hour = int(current_time[0])
            current_minute = int(current_time[1])
            current_seconds = int(current_time[2])

            tweet_hour = int(tweet_time[0])
            tweet_minute = int(tweet_time[1])
            tweet_seconds = int(tweet_time[2])

            # Convert all to minutes and sum up
            current_timesum = (current_hour * 60) + current_minute + (current_seconds/60)
            tweet_timesum = (tweet_hour * 60) + tweet_minute + (tweet_seconds/60)

            current_timesum = float(current_timesum)
            tweet_timesum = float(tweet_timesum)

            time_diff = current_timesum - tweet_timesum

            # Convert time diff in minutes to seconds (this circumvents use of large numbers)
            time_diff = time_diff * 60

            # print("TIMEDIFF: ", time_diff)

            # Check if time difference between when the tweet was
            # and right now is less than tweet age max.
            if (time_diff  <= TWEET_AGE_MAX):

                # If so, then FOR NOW (TODO:), print them out. Later,
                # LATER: Interact with the tweets.

                print("(Time check passed)")

                # Print tweet, datetime, and then newline.
                # print(tweets[i].text,
                # " //", tweet_datetime_tuple[0], " ", tweet_datetime_tuple[1],
                # "\n", sep="")

            else:
                print("(Dates Match, but time check failed.()")
        else:
            print("(Dates do not match.)")
    return


def get_feed_data(api):
    '''
    Gets tweets, mentions, and retweets for bot.
    '''
    # Set up eternal loop
    running = True

    # Set time delay between each iteration.
    SLEEP_TIME = 0.75# Make how old a tweet can be to still be interacted with this much.
    TWEET_AGE_MAX = SLEEP_TIME

    while (running):
        # IMPORTANT: Delay X seconds between each step to prevent getting rate limited (DELAY is at end of loop btw).

        # For some reason datetime only runs if I import this here too
        from datetime import datetime, timedelta

        # Print timestamp for each data pull
        now = str(datetime.now())
        print("\n\nLoop Timestamp:", now)

        # NOTE: ONLY THE FIRST TWO TWEETS, FOR NOW.
        # TODO: CHANGE TO 20 OR SOMETHING

        ################# TWEETS #################
        # This gets all of the last 2 tweets from yourself
        print("\nTWEETS:")
        tweets = api.user_timeline(count=2, screen_name="@egg69017129", include_rts=False)

        # Check every 5 seconds for new tweets sent in the last 5 seconds.
        check_for_new_tweets(tweets, TWEET_AGE_MAX)

        ################ MENTIONS #################
        # This gets all of the last 20 tweets sent to you directly to you.
        print("\nMENTIONS:")
        mentions = api.mentions_timeline()

        # Check every 5 seconds for new mentions sent in the last 5 seconds.
        check_for_new_tweets(mentions, TWEET_AGE_MAX)

        ################# RETWEETS #################
        # This gets the last 20 tweets that have been retweeted by another user.
        print("\nRETWEETS:")
        retweets = api.retweets_of_me()

        # Check every 5 seconds for new retweets sent in the last 5 seconds.
        check_for_new_tweets(retweets, TWEET_AGE_MAX)

        #### VERY IMPORTANT TIME DELAY VAR - DO NOT TOUCH!!! ####
        time.sleep(SLEEP_TIME)

        # PSEUDO:

        # For all tweets sent with a specific hashtag
        # in the last SLEEP_TIME seconds:
        # Reply to them.

        # If a person replies to a tweet from DOGBOT that they have liked and/or retweeted,
        # Like that person's reply-tweet back.

        # For all tweets sent with a specific hashtag
        # in the last SLEEP_TIME seconds:
        # Retweet those tweets.

        # If a person has followed you,
        # and you have yet to follow them back,
        # Follow them back

        # For all new DM's sent in the last SLEEP_TIME seconds,
        # Reply with a message.
        # .list_direct_messages <- get DM's sent/recieved in last 30 days
        # .send_direct_message <- send a DM

    # PRACTICE CODE:

    # ################ TIMELINE #################
    # This gets all of the last 20 tweets on your timeline
    # print("\n", "TIMELINE:", "\n")
    # timeline = api.home_timeline()
    # for i in range(0, len(timeline)):
    #     time.sleep(SLEEP_TIME)
    #     print(timeline[i].text, "\n")
    #
    # ################ MENTIONS #################
    # This gets all of the last 20 tweets sent to you directly to you.
    # mentions = api.mentions_timeline()
    # print("\n", "MENTIONS:", "\n")
    # for i in range(0, len(mentions)):
    #     time.sleep(SLEEP_TIME)
    #     print(mentions[i].text, " //", tweets[i].created_at,"\n", sep="") # created_at
    #
    # ################# RETWEETS #################
    # # This gets the last 20 tweets that have been retweeted by another user.
    # retweets = api.retweets_of_me()
    # print("\n", "RETWEETS:", "\n")
    # for i in range(0, len(retweets)):
    #     time.sleep(SLEEP_TIME)
    #     print(retweets[i].text, " //", tweets[i].created_at,"\n", sep="") # created_at

    # Experimenting with dict key. The best key is
    # created_at, which gives the date and time of tweet creation.
    # mention = mentions[2].text #__dict__..keys()
    # print(mention)
    # Keys:
    """
    '_api', '_json', 'created_at', 'id', 'id_str', 'text', 'truncated',
    'entities', 'source', 'source_url',
    'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id',
    'in_reply_to_user_id_str', 'in_reply_to_screen_name',
    'author', 'user', 'geo', 'coordinates', 'place', 'contributors',
    'is_quote_status', 'retweet_count', 'favorite_count',
    'favorited', 'retweeted', 'lang']
    """


def extract_tweets_from_trending(api):
    '''
    Search trending tweets in the US and write to file
    '''

    # Get trending topic in US, woeid of US: 23424977
    trends = api.trends_place(23424977)

    #### VERY IMPORTANT TIME DELAY VAR - DO NOT TOUCH!!! ####
    SLEEP_TIME = 0.75
    time.sleep(SLEEP_TIME)

    # Extract trends list from dict
    for trend_list in trends:

        # get list of trends from item
        trend_list = trend_list.get("trends")

        # print name for first 5 trends
        for i in range(5):

            # Extract trend name
            trend_name = trend_list[i].get("name")
            print("\n------------------------------------------------------------------------")
            print(trend_name)
            print("------------------------------------------------------------------------")

            # Prevent Rate Limit
            time.sleep(SLEEP_TIME)

            # Get 10 top popular tweets for this trend
            search_results = api.search(trend_name, result_type="popular", count=10, include_entities=False, tweet_mode="extended") # Hopefully this stops cutting them

            # Print resulting tweets for this trend
            for tweet in search_results:
                # print(">>", tweet.text)  # .text gets just the text of the tweet + URL

                # print(search_results)

                try:
                    # Write tweet to file. TODO: Remove the URL during extraction

                    # Remove unicode
                    tweet = tweet.full_text.encode('ascii', 'ignore').decode()

                    # Remove symbols (except @,#,&,-,_,+,=) and make lowercase
                    tweet = tweet.replace("\n", "").replace(",", "").replace(".", "").replace("?", "")\
                        .replace("<", "").replace(">", "").replace("/", "").replace("!", "").replace("%", "")\
                        .replace("^", "").replace("*", "").replace("(", "").replace(")", "").replace("{", "")\
                        .replace("}", "").replace("[", "").replace("]", "").replace("|", "").replace(":", "")\
                        .replace(";", "").replace("\"", "").replace("\\", "").lower()

                    # Split at https to remove url
                    tweet = tweet.split("https")
                    tweet = tweet[0]

                    # Print tweets for debug
                    print(">>", tweet)

                except UnicodeEncodeError:
                    print("ERROR: Unable to write unknown unicode symbol")

                # Prevent Rate Limit
                time.sleep(SLEEP_TIME)


def action1_trending(api):
    '''
    Search top tweets on the top trending topics in the United States at
    the time this function is called. Like and retweet those tweets, and
    follow the people who made those tweets.
    '''

    # Get trending topic in US, woeid of US: 23424977
    trends = api.trends_place(23424977)

    #### VERY IMPORTANT TIME DELAY VAR - DO NOT TOUCH!!! ####
    SLEEP_TIME = 0.75
    time.sleep(SLEEP_TIME)

    # Extract trends list from dict
    for trend_list in trends:

        # get list of trends from item
        trend_list = trend_list.get("trends")

        # print name for first 5 trends
        for i in range(5):

            # Extract trend name
            trend_name = trend_list[i].get("name")
            # print("\n------------------------------------------------------------------------")
            # print(trend_name)
            # print("------------------------------------------------------------------------")

            # Prevent Rate Limit
            time.sleep(SLEEP_TIME)

            # Get XX top popular tweets for this trend, with tweet mode extended to show full tweet
            TWEET_COUNT = 1
            search_results = api.search(trend_name, result_type="popular", count=TWEET_COUNT, include_entities=False,
                                        tweet_mode="extended")

            # Print resulting tweets for this trend
            for tweet in search_results:

                # Get tweet id, and user's id
                id = tweet.id
                user_id = tweet.user.id

                # FAVORITE/LIKE
                api.create_favorite(id)

                # RETWEET
                api.retweet(id)

                # FOLLOW USER
                api.create_friendship(user_id)

                # Print the text of the tweet + URL
                # print(">>", tweet.full_text)

                # Prevent Rate Limit
                time.sleep(SLEEP_TIME)


def action2_following(api):
    '''
    Choose someone the bot is following.
    Like and retweet that user's most recent tweets.
    Follow some of that user's current followers.
    '''

    # Open list of followers
    following_archive = open("following.txt", "r")

    # Get array
    following_array_from_file = []
    line = following_archive.readline()
    while line != "":
        following_array_from_file.append(line)
        line = following_archive.readline()

    #### VERY IMPORTANT TIME DELAY VAR - DO NOT TOUCH!!! ####
    SLEEP_TIME = 0.75
    time.sleep(SLEEP_TIME)

    # Get list of users the agent is following
    following_list = api.friends()

    # Print list of users the agent is following
    # for user in following_list:
    #     print(user.screen_name)

    # Randomly choose which user to engage with
    # TODO: Add greedy version
    selected_user_index = random.randint(0, len(following_list) - 1)
    selected_user = following_list[selected_user_index]

    print("SELECTED USER: ", selected_user.screen_name)


    # Prevent Rate Limit
    time.sleep(SLEEP_TIME)

    # Get list of users the selected user is following
    selected_user_following = api.friends(selected_user.id, count=10)

    # Print list of users the selected user is following
    # Follow some people who that user is following
    for user in selected_user_following:

        # Check if already following user
        if user.screen_name in following_array_from_file:
            print("Already following @", user.screen_name, sep="")

        # If not following yet, follow
        else:
            print("Following @", user.screen_name, sep="")

            # Prevent Rate Limit
            time.sleep(SLEEP_TIME)

            # Follow request
            api.create_friendship(user.id)

    # Prevent Rate Limit
    time.sleep(SLEEP_TIME)

    # Get that user's latest tweets
    selected_user_timeline = api.user_timeline(selected_user.id, count=10)

    # Like and retweet the that user's 10 latest tweets
    for tweet in selected_user_timeline:

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Like
        try:
            print("Liking tweet:", tweet.text)
            api.create_favorite(tweet.id)
        except tweepy.TweepyException:
            print("Could not like tweet")

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Retweet
        try:
            print("Retweeting:", tweet.text)
            api.retweet(tweet.id)
        except tweepy.TweepyException:
            print("Could not retweet tweet")

    # Close file
    following_archive.close()


def action3_random_query(api):
    '''
    Make a random word search based on a dictionary of top 500 words used on Twitter
    Like and retweet with top tweets on those topics
    Follow people who made those tweets
    '''

    # Set up dictionary
    # Have to do this in-function to make sure file gets closed at the end b/c infinite loop
    words_file = open("most_used_words.txt", "r")
    line = words_file.readline()

    words = []

    while line != "":

        words.append(line)

        line = words_file.readline()

    index = random.randint(0, len(words) - 1)
    query = words[index]

    print("QUERY:", query)


    # Open list of followers
    following_archive = open("following.txt", "r")

    # Get array
    following_array_from_file = []
    line = following_archive.readline()
    while line != "":
        following_array_from_file.append(line)
        line = following_archive.readline()

    #### VERY IMPORTANT TIME DELAY VAR - DO NOT TOUCH!!! ####
    SLEEP_TIME = 0.75
    time.sleep(SLEEP_TIME)

    # Search top 10 tweets with query
    search = api.search(query, count=10)

    for tweet in search:

        # Check if already following user
        if tweet.user.screen_name in following_array_from_file:
            print("Already following @", tweet.user.screen_name, sep="")

        # If not following yet, follow
        else:
            print("Following @", tweet.user.screen_name, sep="")

            # Prevent Rate Limit
            time.sleep(SLEEP_TIME)

            # Follow request
            api.create_friendship(tweet.user.id)

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Like
        try:
            print("Liking tweet:", tweet.text)
            api.create_favorite(tweet.id)
        except:
            print("Could not like tweet")

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Retweet
        try:
            print("Retweeting:", tweet.text)
            api.retweet(tweet.id)
        except:
            print("Could not retweet tweet")

    # Close file
    following_archive.close()
    words_file.close()


def purge_tweets_and_following(api):

    # Get following
    following = api.friends(count=50)



    #end


def get_rewards(api):

    followers_file = open("followers.txt", "r")
    followers_array = []

    line = followers_file.readline()
    while line != "":
        followers_array.append(line)
        line = followers_file.readline()

    # Get number of followers since last
    followers = api.followers()

    reward = 0

    # Diff. in followers = reward
    # Compare num followers since last action
    old_follower_count = len(followers_array)
    new_follower_count = len(followers)
    if old_follower_count != new_follower_count:

        reward = new_follower_count - old_follower_count
        print("Reward =", reward)

        # Reset follower txt
        # Overwrite file
        followers_file.close()
        followers_file = open("followers.txt", "w")

        for follower in followers:
            followers_file.write(follower.screen_name)

        return reward

    # otherwise, close file and return 0
    else:
        followers_file.close()
        print("Reward =", reward)

        return 0



    # for follower in followers:
    #     follower.id
    # end


def main():

    # TODO: Remove "following.txt" aspect. It is useless and less reliable than a straight query of followers.
    # IMPORTANT: Keep secret user keys in separate file
    credentials = open("credentials.txt", "r")
    creds_array = []

    line = credentials.readline()
    while line != "":

        # Get line from reading file
        key = line.split(", ")[1]

        # Remove newline char
        key = key.replace("\n", "")

        # Add key to array
        creds_array.append(key)

        line = credentials.readline()

    # print(creds_array)

    CONSUMER = creds_array[0]
    CONSUMER_SECRET = creds_array[1]
    ACCESS = creds_array[2]
    ACCESS_SECRET = creds_array[3]

    # Set up API
    auth = tweepy.OAuthHandler(CONSUMER, CONSUMER_SECRET)
    auth.set_access_token(ACCESS, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Get current datetime tuple
    current_datetime = get_current_datetime

    MINUTES_BETWEEN_ACTIONS = 1
    TIME_BETWEEN_ACTIONS = MINUTES_BETWEEN_ACTIONS * 60

    # Begin Actions:
    running = True

    for x in range(9):
        try:

            get_rewards(api)

            # Get tweets, mentions, and retweets TODO: rename this function
            # TODO: Uncomment if using
            # get_feed_data(api)

            # Get trends and popular tweets for those trends
            # TODO: Uncomment if using
            # extract_tweets_from_trending(api)

            # Action Type 1: Action is based on tweets on trending topics
            # TODO: Uncomment if using
            # action1_trending(api)

            # Action Type 2: Action is based on someone the bot is following
            # TODO: Uncomment if using
            # action2_following(api)

            # Action Type 3: Action is based on random search query
            # TODO: Uncomment if using
            # action3_random_query(api)

            # TODO: Decide if this function is even necessary
            # Extra Action: Purge all tweets and following.
            # Uncomment if using
            # purge_tweets_and_following(api)

            # Sleep agent for x minutes
            time.sleep(TIME_BETWEEN_ACTIONS)

        # Sleeps the agent for 5 minutes when rate limited
        except tweepy.RateLimitError:

            MINUTES_TO_SLEEP = 5
            print("You are being rate limited. Sleeping for,", MINUTES_TO_SLEEP ,"minutes.")

            # Write rate limit to file

            rate_limit_log = open("rate_limit_log.txt", "a")
            time_of_rate_limit = get_current_datetime()
            out_string = "Rate limited at: " + time_of_rate_limit[0] + " " + time_of_rate_limit[1]
            print(out_string)
            rate_limit_log.write(out_string)
            rate_limit_log.close()

            # Sleep for 5 minutes

            time.sleep(MINUTES_TO_SLEEP * 60)


main()
