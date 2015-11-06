from reddit import cSubredditMonitor


class cFlyFishing(cSubredditMonitor):
    def __init__(self):
        self.subreddit_name = 'flyfishing'
        cSubredditMonitor.__init__(self, subreddit=self.subreddit_name)


if __name__ == '__main__':
    bot = cFlyFishing()
    bot.monitor()
