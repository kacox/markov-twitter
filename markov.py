"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import twitter
import re


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)


        body = body + text_file.read()

        # use regex to find all tags (@username)
        username_pattern = re.compile(r'@+[a-zA-Z]*')
        all_tags = username_pattern.findall(body)
        #print(all_tags[:5])

        # turn body (BIG string) into a list
        listified_body = list(body.split(" "))
        print(listified_body[:10])

        # remove all tags from body
        for twitter_tag in all_tags:
            listified_body.remove(twitter_tag)

        # rejoin listified_body back into string
        cleaned_body = " ".join(listified_body)

        text_file.close()

    print(cleaned_body[:200])


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()

    # remove @usernames
    # cleaned_words = list(words)
    # for word in words:
    #     #body = body.replace("@", "")
    #     if word[0] == "@":
    #         cleaned_words.remove(word)
    #         #cleaned_words.pop(cleaned_words.index(word))


    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    key = choice(list(chains.keys()))
    words = [key[0], key[1]]
    while (key in chains) and (len(" ".join(words)) < 135):
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    tweet_text = " ".join(words)

    # Make sure starts with a capital letter and ends with punctuation.
    if not tweet_text[0].isupper():
        tweet_text = tweet_text[0].upper() + tweet_text[1:]

    if not tweet_text[-1] in [".","!","?"]:
        tweet_text = tweet_text[:] + choice([".","!","?"])

    return tweet_text


def tweet(chains):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    # make api object
    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                      consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                      access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
                      access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

    # authenticate
    api.VerifyCredentials()

    # post tweets repetitively
    user_input = ""

    while user_input != "q":
        status = api.PostUpdate(make_text(chains))
        print(status.text)

        user_input = input("Enter to tweet again [q to quit] > ")


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)
# print(text[:500])

# Get a Markov chain
#chains = make_chains(text)
#print(chains)


# Your task is to write a new function tweet, that will take chains as input
#tweet(chains)
