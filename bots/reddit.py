import praw
import os
from os import environ, stat, path
from glob import glob
import sys
import time
from gntplib import Publisher


class cSubredditMonitor(object):
    def __init__(self, subreddit):
        self.subreddit_name = subreddit
        self.process_name = 'python_{}'.format(self.subreddit_name)
        self.user_agent = ('{} monitor by /u/uhkhu'.format(subreddit))
        self.r = praw.Reddit(self.user_agent)
        self.r_submission = praw.Reddit('Submission variables testing by /u/uhkhu')
        self.subreddit = self.r.get_subreddit(subreddit)
        self.username = environ.get('REDDIT_USERNAME')
        self.password = environ.get('REDDIT_PASSWORD')
        self.submission_log_file = '{}.txt'.format(self._get_submission_log_file_format())
        self.publisher = Publisher('reddit', ['New Post'])
        self.submission_log = []
        self._read_submission_log_file()

    def login(self, r):
        r.login(self.username, self.password)

    def _get_submission_log_file_format(self):
        return path.join(path.dirname(__file__), 'submission_logs/{0}_checked'.format(self.subreddit))

    def _read_submission_log_file(self):
        # check if log file exists. create new if not
        submission_log_file_format = '{}*'.format(self._get_submission_log_file_format())
        submission_log_file_matches = glob(submission_log_file_format)
        if len(submission_log_file_matches) == 0:
            open(self.submission_log_file, 'a').close()
        # read log file and populate self.submission log    
        log = [line.strip() for line in open(self.submission_log_file)]
        self.submission_log = log

    def log_submission(self, submission_id):
        # if empty file, write
        if stat(self.submission_log_file).st_size == 0:
            with open(self.submission_log_file, 'w') as f:
                f.write('{}\n'.format(submission_id))
        # if not empty, append
        else:
            with open(self.submission_log_file, 'a') as f:
                f.write('{}\n'.format(submission_id))

    def new_gen(self, n=1):
        # read log file each time
        self._read_submission_log_file()
        for submission in self.subreddit.get_new(limit=n):
            seen = False
            if submission.id not in self.submission_log:
                self.log_submission(submission.id)
                print 'New Submission logged: {}'.format(submission.id)
            else:
                seen = True
            yield seen, submission
            
    def monitor(self, submission_limit=1):
        while True:
            try:
                e_occur = 0
                print '{0} New Loop at {1} {0}'.format('*' * 10, time.ctime())
                not_seen = []
                for seen, submission in self.new_gen(submission_limit):
                    if not seen: # and len(submission.comments) < 3:  # new submission potentially unanswered
                        not_seen.append((submission.title, submission.url))
                if len(not_seen) > 0:
                    self._growl_alert(self.subreddit_name, not_seen)
                time.sleep(5)

            except Exception as e:
                e_occur += 1
                print 'error in self.monitor: '
                print e
                if e_occur > 10:
                    sys.exit('Unresolvable Error')
                else:
                    print 'Trying again'

    def _growl_alert(self, subreddit, submissions):
        for text, url in submissions:
            self.publisher.publish('New Post', title='New /r/{} Post'.format(self.subreddit_name), text=text, gntp_callback=url)


def test():
    bot = cSubredditMonitor(subreddit='learnpython')
    os.remove(bot.submission_log_file)
    bot.monitor(2)


if __name__ == '__main__':
    test()
