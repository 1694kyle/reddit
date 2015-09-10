import praw
from reddit import cReddit


class cLearnPython(cReddit):
    def __init__(self):
        cReddit.__init__(self)
        self.r = praw.Reddit('learnpython monitor by /u/uhkhu')
        self.login(self.r)
        self.subreddit = self.r.get_subreddit('learnpython')






