from bots.reddit import cReddit
import Tkinter as tk
from alert import cAlert
import sys
import time

user_agent = 'learnpython/new monitor by /u/uhku'
sub = 'learnpython'
bot = cReddit(sub, user_agent)


def get_submissions():
    new = bot.new_gen(5)
    print '{0} New Loop at {1} {0}'.format('*' * 10, time.ctime())
    not_seen = []
    for seen, submission in new:
        if not seen and len(submission.comments) < 3:
            not_seen.append((submission.title, submission.url))
    if len(not_seen) > 0:
        alert_user(sub, not_seen)


def alert_user(subreddit, submissions):
    root = tk.Tk()
    app = cAlert(root, subreddit, submissions)
    root.mainloop()

while True:

    try:
        get_submissions()
    except Exception as e:
            print e
            continue
    time.sleep(5)

