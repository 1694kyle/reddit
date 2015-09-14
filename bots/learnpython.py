import praw
from reddit import cSubredditMonitor


class cLearnPython(cSubredditMonitor):
    def __init__(self):
        self.subreddit_name = 'learnpython'
        cSubredditMonitor.__init__(self, subreddit=self.subreddit_name)






