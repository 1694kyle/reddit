import Tkinter as tk
import webbrowser

class cAlert:
    def __init__(self, root, subreddit, submissions):
        self.root = root
        for text, url in submissions:
            link = tk.Label(text=text, foreground="#0000ff")
            link.bind("<1>", lambda event, url=url: self.click_link(event, url))
            link.pack()


    def click_link(self, event, url):
        webbrowser.open(url)

