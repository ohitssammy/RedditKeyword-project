import praw #This module is used to create Reddit instances
import json
from urllib import request
from string import punctuation

'''The reddit_instance object will contain the reddit instance we will create to handle all API calls. 
   Read the Python Reddit API Wrapper(PRAW) documentation for further details'''

#TODO: (1) Create a Reddit app at https://reddit.com/prefs/apps
#TODO: (2) Update your credentials in the credentials_template.json file
#TODO: (3) Rename credentials_template.json to credentials.json
#Tip: bash command for above step: cp credentials_template.json credentials.json

def create_reddit_instance(read_only = False):
    '''This function reads the crendentials from credentials.json and creates a Reddit instance.
        You will use this instance to retrieve further information. Before you complete this 
        function, be sure to create your credentials on the Reddit website, update 
        credentials_template.json and rename it to credentials.json
    '''
    credentials = None
    #TODO: (4) Open 'credential.json' and read the information into the credentials object initialized above. 
    with open('credentials.json', 'r') as creds:
        credentials = json.load(creds) 
    '''The read only parameter determines whether a read-only object,i.e, no login required, 
    or an OAuth2 authenticated object should be created
    '''
    #TODO: (5) Pass all parameters relevant to read-only and user-authenticated objects. One of the parameters is already completed for you.
    if(not read_only):
        reddit_instance = praw.Reddit(
                                    client_id = credentials['client_id'],
                                    client_secret = credentials['client_secret'],
                                    username= credentials['username'], 
                                    password=credentials['password'],
                                    user_agent = credentials['user_agent']
                                     )

    else:
        reddit_instance = praw.Reddit(                                    
                                    client_id = credentials['client_id'],
                                    client_secret = credentials['client_secret'],
                                    user_agent = credentials['user_agent']
                                    )
    #TODO: (6) Return the reddit instance you created below.
    return reddit_instance
    
    
def ten_top_posts(reddit_instance, subreddit_name):
    '''This function takes a subreddit name as a string and prints out ten posts
    under the top category'''
    #TODO: (7) Create a subreddit instance with subreddit_name and reddit_instance.
    subreddit = reddit_instance.subreddit(subreddit_name)


    #TODO: (8) Return the top posts in the subreddit by calling the .top() function on it.
    #TODO: (9) Set the limit parameter for the top function to 10, so that the top 10 posts are returned.
    return subreddit.top(limit = 2)

def returnTitle_Description_Comments(post):
    '''returns a list that extracts all the information from the post: title, description, comments'''
    listComment = returnCommentArray(post)
    contentArray = [post.title, post.selftext, listComment]
    return contentArray

def returnCommentArray(post):
    '''returns a list of the posts' comments'''
    listComment = []
    for comment in post.comments:
        listComment.append(comment.body)
    return listComment

def count_words_in_sentence(wordfreq, sentence):
    '''
        Takes a sentence and counts the individual words after removing punctuations.
    '''
    sentence_str = ''.join(c.lower() for c in sentence if c not in punctuation)
    sentence_arr = sentence_str.split()
    for word in sentence_arr:
        if word not in wordfreq:
            wordfreq[word] = 0
        wordfreq[word] += 1
    return wordfreq

def createDictionary(posts):
    wordfreq = {}
    
    for raw_post in posts:
        post_information = returnTitle_Description_Comments(raw_post)
        wordfreq.update(count_words_in_sentence(wordfreq, post_information[0]))
        wordfreq.update(count_words_in_sentence(wordfreq, post_information[1]))
        for comment in post_information[2]:
            wordfreq.update(count_words_in_sentence(wordfreq, comment))
    return wordfreq

def returnTop10Keywords(dictWords):
    ''' returns the top 10 keywords from a dictionary'''
    keywords = []
    counter = 0
    for key,value in sorted(dictWords.items(), key = lambda x: x[1], reverse = True):
        if(counter < 10):
            if(len(key) > 4):
                keywords.append(key)
                counter += 1
    return keywords

if __name__ == '__main__':
    '''Experiment with your reddit function here. Examine the output on the console.'''
    #TODO: (10) Set the value of subreddit_name to your favorite subreddit.
    subreddit_name = 'grandorder' 
    #TODO: (11) Create a new instance of the praw Reddit object.
    reddit_instance = create_reddit_instance(read_only=True) #so it will not print all the file calling which is good for debugging.
    #TODO: (12) Generate a list of top ten posts for your subreddit, using the praw Reddit object you created.
    posts = ten_top_posts(reddit_instance,subreddit_name)
    #TODO: (13) Iterate through the posts list returned by the function call above, and print its title attribute

    dictionary = createDictionary(posts)
    top10 = returnTop10Keywords(dictionary)
    counter = 1
    for key in top10:
        print("%d." % counter, key, dictionary[key])
        counter += 1
