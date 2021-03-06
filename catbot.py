import tweepy
import time
import random
import os
import epsilon_source

TWEET_COUNT = 10
SLEEP_TIME = 0.75


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

        # Choose a random trending topic
        index = random.randint(0, len(trend_list) - 1)

        # Extract trend name
        trend_name = trend_list[index].get("name")

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Get XX top popular tweets for this trend, with tweet mode extended to show full tweet

        search_results = api.search(trend_name, result_type="popular", count=TWEET_COUNT, include_entities=False,
                                    tweet_mode="extended")

        # Print resulting tweets for this trend
        for tweet in search_results:

            # Like
            try:
                api.create_favorite(tweet.id)
                print("Liking tweet:", tweet.full_text)
            except tweepy.TweepError as message:
                print("Could not like tweet:", tweet.full_text, message)

            # Prevent Rate Limit
            time.sleep(SLEEP_TIME)

            # Retweet
            try:
                api.retweet(tweet.id)
                print("Retweeting:", tweet.full_text)
            except tweepy.TweepError as message:
                print("Could not retweet tweet:", tweet.full_text, message)

            # Prevent Rate Limit
            time.sleep(SLEEP_TIME)

            # Follow
            try:
                api.create_friendship(tweet.user.id)
                print("Followed @", tweet.user.screen_name)
            except tweepy.TweepError as message:
                print("Could not follow user:", tweet.user.screen_name, message)


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
    selected_user_following = api.friends(selected_user.id, count=TWEET_COUNT)

    # Print list of users the selected user is following
    # Follow some people who that user is following
    for user in selected_user_following:

        # Check if already following user
        if user.screen_name in following_array_from_file:
            print("Already followed @", user.screen_name, sep="")

        # If not following yet, follow
        else:

            # Prevent Rate Limit
            time.sleep(SLEEP_TIME)

            # Follow
            try:
                api.create_friendship(user.id)
                print("Followed @", user.screen_name)
            except tweepy.TweepError as message:
                print("Could not follow user:", user.screen_name, message)

    # Prevent Rate Limit
    time.sleep(SLEEP_TIME)

    # Get that user's latest tweets
    selected_user_timeline = api.user_timeline(selected_user.id, count=TWEET_COUNT)

    # Like and retweet the that user's 10 latest tweets
    for tweet in selected_user_timeline:

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Like
        try:
            api.create_favorite(tweet.id)
            print("Liking tweet:", tweet.text)
        except tweepy.TweepError as message:
            print("Could not like tweet:", tweet.text, message)

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Retweet
        try:
            api.retweet(tweet.id)
            print("Retweeting:", tweet.text)
        except tweepy.TweepError as message:
            print("Could not retweet tweet:", tweet.text, message)

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

    time.sleep(SLEEP_TIME)

    # Search top 10 tweets with query
    search = api.search(query, count=10)

    for tweet in search:

        # Check if already following user
        if tweet.user.screen_name in following_array_from_file:
            print("Already followed @", tweet.user.screen_name, sep="")

        # If not following yet, follow
        else:

            # Prevent Rate Limit
            time.sleep(SLEEP_TIME)

            # Follow
            try:
                api.create_friendship(tweet.user.id)
                print("Followed @", tweet.user.screen_name, sep="")
            except tweepy.TweepError as message:
                print("Could not follow user:", tweet.user.screen_name, message)

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Like
        try:
            api.create_favorite(tweet.id)
            print("Liking tweet:", tweet.text)
        except tweepy.TweepError as message:
            print("Could not like tweet:", tweet.text, message)

        # Prevent Rate Limit
        time.sleep(SLEEP_TIME)

        # Retweet
        try:
            api.retweet(tweet.id)
            print("Retweeting:", tweet.text)
        except tweepy.TweepError as message:
            print("Could not retweet tweet:", tweet.text, message)

    # Close file
    following_archive.close()
    words_file.close()


def purge_tweets_and_following(api):

    # Get following
    following = api.friends(count=50)

    #end


def get_rewards(api):
    '''
        Get rewards based off last action
        reward = diff. in followers since last action
    '''

    followers_file = open("followers_catbot.txt", "r")
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
        followers_file = open("followers_catbot.txt", "w")

        for follower in followers:
            followers_file.write(follower.screen_name + "\n")

        return reward

    # otherwise, close file and return 0
    else:
        followers_file.close()
        print("Reward =", reward)

        return 0


def calculate_reward_avg(filename, reward):

    print("---------------------------\nWriting to file:", filename)

    # If reward file already exists, read in data
    if os.path.isfile(filename):

        # Read the last line in the file
        with open(filename, 'r') as reward_history:
            action_rewards = reward_history.readlines()[-1]

        # Extract all values but just use the action_count/action_avg
        action_count, action_reward_avg, old_date, old_time, null = action_rewards.split(",")
        action_count, action_reward_avg = float(action_count), float(action_reward_avg)

        print("Previous count and avg:", action_count, action_reward_avg)

        # Add last reward for action to avg
        action_reward_avg = ((action_reward_avg * action_count) + reward) / (action_count + 1)
        action_count += 1

        print("New count and avg:", action_count, action_reward_avg)

        # Append File
        reward_history.close()
        reward_history = open(filename, "a")

        # Get time and date
        current_date, current_time = get_current_datetime()
        out_string = str(action_count) + "," + str(action_reward_avg) + "," \
                     + current_date + "," + current_time + ",\n"
        print("Writing to file:", out_string, end="")
        reward_history.write(out_string)
        reward_history.close()

    # End border
    print("---------------------------\n")

    return


def read_or_init_reward_file(filename):
    '''
    return "read file" var if file exists
    init file if it does not yet exist
    '''

    print("---------------------------\nReading file:", filename)

    # If file exists, open it
    if os.path.isfile(filename):

        # Return the last line in the file
        with open(filename, 'r') as file:
            last_line = file.readlines()[-1]

        print("Last Line =", last_line, end="")
        return last_line

    # Else, init a new one and return that
    else:
        print("Creating new file:", filename)
        file = open(filename, "w")
        current_date, current_time = get_current_datetime()
        out_string = "0,1.0," + current_date + "," + current_time + ",\n"
        file.write(out_string)
        file.close()
        return "0,0,0,0,"


def init_followers_list(api):

    filename = "followers_catbot.txt"
    with open(filename, "w") as file:

        follower_list = api.followers()
        # print(follower_list)

        # If no followers, close it
        if len(follower_list) < 1:
            file.close()
            return True

        # If at least one follower, add followers to follower list, one per line
        for follower in follower_list:
            file.write(follower.screen_name + "\n")

    return True


def log_rate_limit():
    minutes_to_sleep = 20
    print("You are being rate limited. Sleeping for,", minutes_to_sleep, "minutes.")

    # Write rate limit to file
    rate_limit_log = open("rate_limit_log.txt", "a")
    time_of_rate_limit = get_current_datetime()
    out_string = "Rate limited at: " + time_of_rate_limit[0] + " " + time_of_rate_limit[1]
    print(out_string)
    rate_limit_log.write(out_string)
    rate_limit_log.close()

    # Sleep for 5 minutes
    time.sleep(minutes_to_sleep * 60)


def main():

    # TODO: Remove "following.txt" aspect. It is useless and less reliable than a straight query of followers.
    # IMPORTANT: Keep secret user keys in separate file
    credentials = open("credentials_catbot.txt", "r")
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

    CONSUMER = creds_array[0]
    CONSUMER_SECRET = creds_array[1]
    ACCESS = creds_array[2]
    ACCESS_SECRET = creds_array[3]

    # Set up API
    auth = tweepy.OAuthHandler(CONSUMER, CONSUMER_SECRET)
    auth.set_access_token(ACCESS, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Initialize files
    path = os.path.dirname(__file__)
    sub_dir = "reward_value_logs\\"
    log_file_path = os.path.join(path, sub_dir)

    '''
    Create filename for file based on date/time of script init
    w/ relative path to sub-directory "reward_value_logs"
    '''

    action1_filename = log_file_path + "catbot_action1_reward_history.csv"
    action2_filename = log_file_path + "catbot_action2_reward_history.csv"
    action3_filename = log_file_path + "catbot_action3_reward_history.csv"

    # Init other vars, begin actions:
    running = True
    action_type = 0
    action_filename = ""
    trial = float(0)

    # TODO: Modify wait time
    # Currently: Every 20 minutes, i.e. 3 actions per hour.
    time_between_actions = 20 * 60

    # Init followers list
    initialized_follower_list = False
    while not initialized_follower_list:
        try:
            initialized_follower_list = init_followers_list(api)

        # Sleeps the agent for when rate limited
        except tweepy.RateLimitError:
            log_rate_limit()

    while running:
        try:

            # Epsilon
            epsilon_threshold = epsilon_source.get_threshold()

            # Decimal btwn 0 and 1
            epsilon = random.random()

            # Print epsilon
            print("\n------------------------------\nTrial:", int(trial))
            print("Epsilon:", epsilon, "Threshold", epsilon_threshold)

            # if epsilon below threshold, do random
            if epsilon > epsilon_threshold:

                print("Random (Exploration) Action")

                action_type = random.randint(1, 3)

                print("Action Type:", action_type)

            # if epsilon above threshold, do greedy
            elif epsilon <= epsilon_threshold:

                print("Greedy (Exploitation) Action")

                # Read files

                # If reward file already exists, read in data
                action1_reward_history = read_or_init_reward_file(action1_filename)
                action2_reward_history = read_or_init_reward_file(action2_filename)
                action3_reward_history = read_or_init_reward_file(action3_filename)

                # Extract avg reward values from each action
                action1_reward_avg = float(action1_reward_history.split(",")[1])
                action2_reward_avg = float(action2_reward_history.split(",")[1])
                action3_reward_avg = float(action3_reward_history.split(",")[1])

                # List these items for ease of code readability
                action_reward_avg_list = 0,action1_reward_avg,action2_reward_avg,action3_reward_avg

                # Account for matches
                # If all actions 1 thru 3 have the same avg:
                if action1_reward_avg == action2_reward_avg and action2_reward_avg == action3_reward_avg:

                    # Choose random between them
                    print("Actions 1, 2, and 3 are equal maxes")

                    action_type = random.randint(1, 3)

                    print("Action Type:", action_type, "Reward:", action_reward_avg_list[action_type])

                # If actions 1 and 2 have equal averages greater than action 3's
                if action1_reward_avg == action2_reward_avg and action1_reward_avg > action3_reward_avg:

                    # Choose random between them
                    print("Actions 1 and 2 are equal maxes")

                    action_type = random.randint(1, 2)

                    print("Action Type:", action_type, "Reward:", action_reward_avg_list[action_type])

                # If actions 2 and 3 have equal averages greater than action 1's
                if action2_reward_avg == action3_reward_avg and action2_reward_avg > action1_reward_avg:

                    # Choose random between them
                    print("Actions 2 and 3 are equal maxes")

                    action_type = random.randint(2, 3)

                    print("Action Type:", action_type, "Reward:", action_reward_avg_list[action_type])

                # If actions 1 and 3 have equal averages greater than action 2's
                if action1_reward_avg == action3_reward_avg and action3_reward_avg > action2_reward_avg:

                    # Choose random between them
                    print("Actions 1 and 3 are equal maxes")

                    action_type = random.randint(1, 2)

                    # randint chooses 1 or 2, but we want action 3 so we turn that "2" into a "3"
                    if action_type == 2:
                        action_type = 3

                    print("Action Type:", action_type, "Reward:", action_reward_avg_list[action_type])

                # If no matching maxes, choose maximum from list:
                else:
                    # Get best action reward via max of rewards, print header
                    best_action_reward = max(action1_reward_avg, action2_reward_avg, action3_reward_avg)
                    print("---------------------------")

                    if best_action_reward == action1_reward_avg:
                        print("Best action: 1, avg reward:", best_action_reward)
                        action_type = 1

                    elif best_action_reward == action2_reward_avg:
                        print("Best action: 2, avg reward:", best_action_reward)
                        action_type = 2

                    elif best_action_reward == action3_reward_avg:
                        print("Best action: 3, avg reward:", best_action_reward)
                        action_type = 3

            '''
            Perform action 1 - 3
            Set action_filename respective to that action
            '''
            if action_type == 1:
                # Action Type 1: Action is based on tweets on trending topics
                action1_trending(api)
                action_filename = action1_filename

            elif action_type == 2:
                # Action Type 2: Action is based on someone the bot is following
                action2_following(api)
                action_filename = action2_filename

            elif action_type == 3:
                # Action Type 3: Action is based on random search query
                action3_random_query(api)
                action_filename = action3_filename

            # Calc rewards AFTER pause between actions
            print("\nAction completed. Sleeping for", time_between_actions, "seconds.")
            time.sleep(time_between_actions)

            # Get reward based on change in num of twitter followers
            reward = get_rewards(api)

            # Calculate reward avg
            calculate_reward_avg(action_filename, reward)

            # Increment trial count
            trial += 1

        # Sleeps the agent for when rate limited
        except tweepy.RateLimitError:
            log_rate_limit()

        # Catch all for all other errors
        except:

            minutes_to_sleep = 20
            print("Unknown error. Sleeping for", minutes_to_sleep, "minutes.")

            # Write error to log file
            rate_limit_log = open("rate_limit_log.txt", "a")
            time_of_rate_limit = get_current_datetime()
            out_string = "Unknown error at: " + time_of_rate_limit[0] + " " + time_of_rate_limit[1]
            print(out_string)
            rate_limit_log.write(out_string)
            rate_limit_log.close()

            # Sleep for 5 minutes
            time.sleep(minutes_to_sleep * 60)


main()
