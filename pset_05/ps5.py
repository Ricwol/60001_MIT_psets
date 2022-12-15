# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory:

    def __init__(self, guid, title, description, link, pubdate):
        """
        Create a NewsStory object.

        Parameters
        ----------
        guid : str
            A globally unique identifier for this news story.
        title : str
            The news story's headline.
        description : str
            A paragraph or so summarizing the news story.
        link : str
            A link to a website with the entire story
        pubdate : datetime
            Date the news was published
        """
        self._guid = guid
        self._title = title
        self._description = description
        self._link = link
        self._pubdate = pubdate

    def get_guid(self):
        """Returns globally unique identifier (guid) of a news story"""
        return self._guid

    def get_title(self):
        """Returns title of a news story"""
        return self._title

    def get_description(self):
        """Returns description of a news story"""
        return self._description

    def get_link(self):
        """Returns link to a news story"""
        return self._link

    def get_pubdate(self):
        """Returns publishing date (pubdate) of a news story"""
        return self._pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        """
        Create a PhraseTrigger object.

        Parameters
        ----------
        phrase : str
            A simple phrase to set a trigger.
        """
        self._phrase = phrase.lower()

    def is_phrase_in(self, text):
        """
        Returns True if the whole phrase is present in text, False otherwise.

        Trigger fires only when each word in the phrase is present in its
        entirety and appears consecutively in the text, separated only by
        spaces or punctuation.

        Parameters
        ----------
        text : str
            A text of a news story.

        Returns
        -------
        is_in : bool
            True if the whole phrase is consecutively present in text, False
            otherwise

        """
        text = text.lower()
        # Remove any punctuation in text
        for p in string.punctuation:
            # Replace leaves text as is if p not in text
            text = text.replace(p, " ")
        # Remove all whitespace and separate each word
        text = text.split()
        # Split all words in phrase at whitespace
        phrase = self._phrase.split()

        # Use naive text search
        is_in = False
        while len(phrase) <= len(text) and not is_in:
            is_in = True
            # Loop through all words in phrase
            for i, word in enumerate(phrase):
                # IF the ith word in phrase is not equal to the ith word in
                # text THEN set is_in to False as no match is found yet.
                if word != text[i]:
                    is_in = False
            # Remove first word in text to repeat search on substring
            text.pop(0)
        return is_in


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):

    def evaluate(self, story):
        """
        Returns True if self.phrase is in news story's title, False otherwise.

        Parameters
        ----------
        story : NewsStory
            A NewsStory object.

        Returns
        -------
        bool
            Checks if self.phase is in news story's title.

        """
        title = story.get_title()
        return self.is_phrase_in(title)


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):

    def evaluate(self, story):
        """
        Returns True if self.phrase is in news story's description, False
        otherwise.

        Parameters
        ----------
        story : NewsStory
            A NewsStory object.

        Returns
        -------
        bool
            Checks if self.phase is in news story's description.

        """
        description = story.get_description()
        return self.is_phrase_in(description)


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
class TimeTrigger(Trigger):

# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, date_string):
        """
        Create a TimeTrigger object.

        Parameters
        ----------
        date_string : str
            Assumes that `date_string` is in EST and in the format
            "%d %b %Y %H:%M:%S".
        """
        self.date_string = datetime.strptime(date_string, "%d %b %Y %H:%M:%S")


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):

    def evaluate(self, story):
        """
        Returns True if publishing date of news story comes before date set for
        BeforeTrigger.

        Parameters
        ----------
        story : NewsStory
            A NewsStory object.

        Returns
        -------
        bool
            Compares publishing date of news story with date set for
            BeforeTrigger.

        """
        pubdate = story.get_pubdate()
        date_string = self.date_string
        try:
            # Try comparing offset-naive datetimes
            return date_string > pubdate
        except TypeError:
            # Add timezone to date_string to make it an offset-aware datetime
            # Timezone EST
            date_string = date_string.replace(tzinfo=pytz.timezone("EST"))
        # Compare offset-aware datetimes
        return date_string > pubdate


class AfterTrigger(TimeTrigger):

    def evaluate(self, story):
        """
        Returns True if publishing date of news story comes after date set for
        AfterTrigger.

        Parameters
        ----------
        story : NewsStory
            A NewsStory object.

        Returns
        -------
        bool
            Compares publishing date of news story with date set for
            AfterTrigger.

        """
        pubdate = story.get_pubdate()
        date_string = self.date_string
        try:
            # Try comparing offset-naive datetimes
            return date_string < pubdate
        except TypeError:
            # Add timezone to date_string to make it an offset-aware datetime
            # Timezone EST
            date_string = date_string.replace(tzinfo=pytz.timezone("EST"))
        # Compare offset-aware datetimes
        return date_string < pubdate


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):

    def __init__(self, trigger):
        """
        Create a NotTrigger object.

        Parameters
        ----------
        trigger : Trigger
            A Trigger object.

        """
        self.trigger = trigger

    def evaluate(self, story):
        """
        Returns True if trigger is not fired

        Parameters
        ----------
        story : NewsStory
            A NewsStory object.

        Returns
        -------
        bool
            Inverts result of trigger evaluate.

        """
        return not self.trigger.evaluate(story)


# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        """
        Create an AndTrigger object

        Parameters
        ----------
        trigger1 : Trigger
            A Trigger object.
        trigger2 : Trigger
            Another Trigger object.
        """
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        """
        Returns True if both Triggers trigger1 and trigger2 fire.

        Parameters
        ----------
        story : NewsStory
            A NewsStory object.

        Returns
        -------
        bool
            True if story triggers both trigger1 and trigger2, False otherwise.

        """
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)


# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        """
        Create an OrTrigger object

        Parameters
        ----------
        trigger1 : Trigger
            A Trigger object.
        trigger2 : Trigger
            Another Trigger object.
        """
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        """
        Returns True if at least one Trigger fires.

        Parameters
        ----------
        story : NewsStory
            A NewsStory object.

        Returns
        -------
        bool
            True if story triggers at least one Trigger, False otherwise

        """
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

