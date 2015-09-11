import praw
from reddit import cSubredditMonitor


class cLearnPython(cSubredditMonitor):
    def __init__(self):
        cSubredditMonitor.__init__(self)
        self.r = praw.Reddit('learnpython monitor by /u/uhkhu')
        self.login(self.r)
        self.subreddit = self.r.get_subreddit('learnpython')






