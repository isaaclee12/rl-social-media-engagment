import random

def main():
    # Analyze each line of csv
    infile = open("trending.csv")

    # matrix for text
    tweets = []

    # string for text
    string = ""

    # Establish dict
    tweet_dict = {}

    line = infile.readline()

    # For each topic:
    while line != "":

        array = line.split(",")

        # Title is first item:
        title = array[0]

        # For each tweet:
        for x in range(len(array)):

            # Get current tweet and split it into words
            tweet = array[x]

            # Word counts
            words = tweet.split(" ")

            for word in words:

                # Filter out blank words
                if word != "":
                    # print(word)

                    # See if word not already in dict
                    if word not in tweet_dict:

                        # Add it to dict with value 1
                        tweet_dict.update({word: 1})

                    # If word already in dict
                    else:

                        # Add to value + 1
                        tweet_dict.update({word: tweet_dict.get(word) + 1})

        # Sort dict
        sorted_dict = {}
        sorted_keys = sorted(tweet_dict, key=tweet_dict.get)

        for key in sorted_keys:
            sorted_dict[key] = tweet_dict[key]

        # Header for each topic
        print("\n------------------------------------------------------------------------")
        print(title)
        print("------------------------------------------------------------------------")


        # Print in reverse, for practice of getting best words.
        # for x in range(len(sorted_dict) - 1, 0, -1):
        #     last_item = list(sorted_dict)[x]
        #     print(last_item, sorted_dict.get(last_item))


        # Choose random words to output as tweet
        # TODO: Weight words by count
        # TODO: Make this somehow form coherent sentences...
        tweet_word_length = random.randint(5, 15)
        for x in range(tweet_word_length):
            random_index = random.randint(0, len(sorted_dict) - 1)
            print(list(sorted_dict)[random_index], end = " ")

        # Next line
        line = infile.readline()

    # Notice patterns in the way things are stated



    # Try to imitate the tweets

main()
