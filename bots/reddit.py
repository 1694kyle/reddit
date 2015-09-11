import praw
from os import environ, stat, path
from glob import glob

class cReddit(object):
    def __init__(self, subreddit, user_agent):
        self.subreddit_name = subreddit
        self.r = praw.Reddit(user_agent) # ('{} monitor by /u/uhkhu'.format(subreddit))
        self.r_submission = praw.Reddit('Submission variables testing by /u/uhkhu')
        self.subreddit = self.r.get_subreddit(subreddit)
        self.username = environ.get('REDDIT_USERNAME')
        self.password = environ.get('REDDIT_PASSWORD')
        self.submission_log_file_format = '{}*'.format(self._get_submission_log_file_format())
        self.submission_log_file = '{}.txt'.format(self._get_submission_log_file_format())
        self._check_submissions()
        self.submission_log = []
        self._read_submission_log_file()

    def login(self, r):
        r.login(self.username, self.password)

    def _check_submissions(self):
        """
        checks for existing submission log and creates one if not present
        :return: nothing
        """
        submission_log_file_matches = glob(self.submission_log_file_format)
        if len(submission_log_file_matches) == 0:
            open(self.submission_log_file, 'a').close()

    def _get_submission_log_file_format(self):
        return path.join(path.dirname(__file__), 'submission_logs/{0}_checked'.format(self.subreddit))

    def _read_submission_log_file(self):
        log = [line.strip() for line in open(self.submission_log_file)]
        self.submission_log = log

    def log_submission(self, submission_id):
        if stat(self.submission_log_file).st_size == 0:
            with open(self.submission_log_file, 'w') as f:
                f.write('{}\n'.format(submission_id))
        else:
            with open(self.submission_log_file, 'a') as f:
                f.write('{}\n'.format(submission_id))

    def new_gen(self, n=10):
        # need to refetch subreddit to get updated submissions
        self.subreddit = self.r.get_subreddit(self.subreddit_name)
        seen = False
        for submission in self.subreddit.get_new(limit=n):
            if submission.id not in self.submission_log:
                self.log_submission(submission.id)
                print 'New Submission logged: {}'.format(submission.id)
            else:
                seen = True
                # print 'Seen Submission: {}'.format(submission.id)
            yield seen, submission
#
# user_agent = 'learnpython monitor by /u/uhkhu'
#
# bot = cReddit(subreddit = 'learnpython', user_agent=user_agent)
# x = 10
# new = bot.new_gen(x)
#
# for seen, sub in new:
#     print sub.title